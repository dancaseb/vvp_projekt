from constants import G
import numpy as np

class Planet:
    def __init__(self, mass, position, velocity, name):
        self.name = name
        self._mass = mass
        self._position = position
        self._acceleration = np.array([0.0, 0.0])
        self._force = np.array([0.0, 0.0])
        self._velocity = velocity
        self.forces = []
        self.dt = 60*60*24
        self.positions = [tuple(self._position)]

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        if not isinstance(new_position, np.ndarray):
            raise AssertionError('Position must be a element tuple.')
        if len(new_position) != 2:
            raise AssertionError('Position must contain 2 elements for x and y axis.')
        self._position = new_position

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, new_acceleration):
        self._acceleration = new_acceleration

    @property
    def force(self):
        return self._force

    @force.setter
    def force(self, new_force):
        self._force = new_force

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, new_mass):
        self._mass = new_mass

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, new_velocity):
        self._velocity = new_velocity

    def calculate_position(self):
        self.force = np.add.reduce(self.forces)
        a = self.calculate_acceleration(self.force)
        v = self.calculate_velocity(a)
        self.velocity = v
        ds = self.calculate_distance(self.velocity, a)
        self.position += ds
        # append the new position, used for plotting trajectory
        self.positions.append(tuple(self.position))
        self.forces.clear()

    def calculate_acceleration(self, force):
        a = force / self.mass
        return a

    def calculate_velocity(self, acceleration):
        # konst. rychlost na intervalu dt
        dv = acceleration * self.dt  # zmena rychlosti behem dt
        v = self.velocity + dv
        return v

    def calculate_distance(self, velocity, acceleration):
        ds = velocity * self.dt
        return ds

class SolarSystem:
    def __init__(self):
        self.planets = []


    def distance(self, pos1, pos2):
        return pos2 - pos1

    def unit_vector(self, vector):
        return vector / np.linalg.norm(vector)

    def add_planets(self, planets):
        for planet_name in planets:
            self.planets.append(
                Planet(position=np.array(planets[planet_name]['position']),
                       velocity=np.array(planets[planet_name]['velocity']),
                       mass=planets[planet_name]['mass'], name=planet_name))

    def calculate_force(self, planet1, planet2):
        F = (self.unit_vector(self.distance(planet1.position, planet2.position)) * (G * (planet1.mass * planet2.mass))) / (
                    np.linalg.norm(self.distance(planet1.position, planet2.position)) ** 2)
        return F


    def update_position(self):
        # do for each of two planets
        # mozna pomoci itertools?
        for index1, planet1 in enumerate(self.planets):
            for index2, planet2 in enumerate(self.planets):
                if index2 == index1:
                    continue
                else:
                    # print(planet1, planet2)
                    F = self.calculate_force(planet1, planet2)
                    planet1.forces.append(F)

        for planet in self.planets:
            planet.calculate_position()

        #data for scatter plot
        x = np.array([p.position[0] for p in self.planets])
        y = np.array([p.position[1] for p in self.planets])
        # print(self.planets[1].positions)
        # positions = np.array([planet.positions for planet in self.planets])
        # print(f"positions: {[x for x in positions]}")
        # x = np.array([position[0] for position in positions])
        # y = np.array([position[1] for position in positions])

        return x, y

    def get_planets_trajectories(self):
        # prostor pro optimalizaci, nemusi se prekopirovat cele pole, ale pouze nejak appendovat.
        trajectories = np.array([p.positions for p in self.planets])
        return trajectories
