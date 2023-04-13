from constants import G
import numpy as np


class Planet:
    """
    Class representing a planet. Initializing parameters are mass, position, velocity and name.
    """
    def __init__(self, mass, position, velocity, name):
        """
        # Initialize values. Acceleration and force/forces will be calculated. dt is the time step. positions are the
        past positions the planet was at. Using properties to set and get values.
        :param mass:
        :param position:
        :param velocity:
        :param name:
        """
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
        """
        This function calculates the new position of the planet according to forces acting on the planet.
        :return:
        """
        # vector sum of force vectors
        self.force = np.add.reduce(self.forces)
        a = self.calculate_acceleration(self.force)
        # new velocity
        v = self.calculate_velocity(a)
        self.velocity = v
        # change in position
        ds = self.calculate_distance(self.velocity)
        # add the change to previous position
        self.position += ds
        # append the new position, used for plotting trajectory
        self.positions.append(tuple(self.position))
        self.forces.clear()

    def calculate_acceleration(self, force):
        """
        Calculates the planet's vector of acceleration using the formula a = F/m
        :param force:
        :return:
        """
        a = force / self.mass
        return a

    def calculate_velocity(self, acceleration):
        """
        Calculates the planet's vector of velocity using the formula v = a * t. The velocity is constant during interval
        dt, dv is change of velocity during time dt
        :param acceleration:
        :return:
        """
        dv = acceleration * self.dt
        v = self.velocity + dv
        return v

    def calculate_distance(self, velocity):
        """
        Calculates the planet's vector of change in distance using the formula s = v * t.
        :param velocity:
        :return:
        """

        ds = velocity * self.dt
        return ds


class SolarSystem:
    """
    Class representing the Solar System with multiple planets. Doesn't take any parameters. Instead, the planets are
    added via the add_planets() function.
    """
    def __init__(self):
        self.planets = []

    def distance_vector(self, pos1, pos2):
        """
        Find the vector difference. We use it with position arguments pos1 and pos2
        :param pos1:
        :param pos2:
        :return:
        """
        return pos2 - pos1

    def unit_vector(self, vector):
        """
        Calculate the unit vector for a given vector.
        :param vector:
        :return:
        """
        return vector / np.linalg.norm(vector)

    def add_planets(self, planets: dict):
        """
        Function to add planets. See example json files in data folder to find the format of input data.
        :param planets:
        :return:
        """
        for planet_name in planets:
            self.planets.append(
                Planet(position=np.array(planets[planet_name]['position']),
                       velocity=np.array(planets[planet_name]['velocity']),
                       mass=planets[planet_name]['mass'], name=planet_name))

    def calculate_force(self, planet1, planet2):
        """
        Calculate the force vector between two planets. Formula can be found at https://en.wikipedia.org/wiki/Force
        :param planet1:
        :param planet2:
        :return:
        """
        F = (self.unit_vector(self.distance_vector(planet1.position, planet2.position)) * (
                    G * (planet1.mass * planet2.mass))) / (
                    np.linalg.norm(self.distance_vector(planet1.position, planet2.position)) ** 2)
        return F


    def update_position(self):
        """
        For planet1 calculate the force between another planet. Do this for all possible combinations. Then append
        the calculated force to the forces list for planet1. After the forces list has been updated, calculate new
        positions for all the planets. Returns 2 np.arrays containing x and y coordinates for all planets positions .
        :return:
        """

        for index1, planet1 in enumerate(self.planets):
            for index2, planet2 in enumerate(self.planets):
                if index2 == index1:
                    continue
                else:
                    F = self.calculate_force(planet1, planet2)
                    planet1.forces.append(F)

        for planet in self.planets:
            planet.calculate_position()

        x = np.array([p.position[0] for p in self.planets])
        y = np.array([p.position[1] for p in self.planets])

        return x, y

    def get_planets_trajectories(self):
        # prostor pro optimalizaci, nemusi se prekopirovat cele pole, ale pouze nejak appendovat.
        """
        Get the planets trajectory. Each planet holds a list containing its previous positions. Used for plotting.
        :return:
        """
        trajectories = np.array([p.positions for p in self.planets])
        return trajectories