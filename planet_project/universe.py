from planet_project.constants import G, planet_colors
import numpy as np
import itertools


class Planet:
    """
    Class representing a planet. Initializing parameters are mass, position, velocity and name.
    """
    def __init__(self, mass: float, position: np.ndarray, velocity: np.ndarray, dt: int, name: str, color: str):
        """
        # Initialize values. Acceleration and force/forces will be calculated. dt is the time step. positions are the
        past positions the planet was at. Using properties to set and get values.
        :param mass:
        :param position:
        :param velocity:
        :param name:
        """
        self.name = name
        self.color = color
        self._mass = mass
        self._position = position
        self._acceleration = np.array([0.0, 0.0])
        self._force = np.array([0.0, 0.0])
        self._velocity = velocity
        self.forces = []
        self.dt = dt
        self.positions = [tuple(self._position)]
        self.planet_plot = self.PlanetPlot(self)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position: np.ndarray):
        if not isinstance(new_position, np.ndarray):
            raise AssertionError('Position must be ndarray type.')
        if new_position.shape != (2,):
            raise AssertionError('Position must contain 2 elements for x and y axis.')
        self._position = new_position

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, new_acceleration: np.ndarray):
        if not isinstance(new_acceleration, np.ndarray):
            raise AssertionError('Acceleration must be ndarray type.')
        if new_acceleration.shape != (2,):
            raise AssertionError('Acceleration must contain 2 elements for x and y axis.')
        self._acceleration = new_acceleration

    @property
    def force(self):
        return self._force

    @force.setter
    def force(self, new_force: np.ndarray):
        if not isinstance(new_force, np.ndarray):
            raise AssertionError('Force must be ndarray type.')
        if new_force.shape != (2,):
            raise AssertionError('Force must contain 2 elements for x and y axis.')
        self._force = new_force

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, new_mass: float):
        self._mass = new_mass

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, new_velocity: np.ndarray):
        if not isinstance(new_velocity, np.ndarray):
            raise AssertionError('Velocity must be ndarray type.')
        if new_velocity.shape != (2,):
            raise AssertionError('Velocity must contain 2 elements for x and y axis.')
        self._velocity = new_velocity

    def calculate_position(self):
        """
        This function calculates the new position of the planet according to forces acting on the planet.
        :return:
        """
        # vector sum of force vectors
        self.force = np.add.reduce(self.forces)
        self.acceleration = self.calculate_acceleration()
        # new velocity
        self.velocity = self.calculate_velocity()
        # change in position
        ds = self.calculate_distance_traveled()
        # add the change to previous position
        self.position += ds

        # append the new position, used for plotting trajectory
        self.positions.append(tuple(self.position))
        # keep the plotting image up to date
        self.update_plot()
        self.forces.clear()

    def calculate_acceleration(self) -> np.ndarray:
        """
        Calculates the planet's vector of acceleration using the formula a = F/m
        :return:
        """
        a = self.force / self.mass
        return a

    def calculate_velocity(self) -> np.ndarray:
        """
        Calculates the planet's vector of velocity using the formula dv = a * dt. The velocity is constant during interval
        dt, dv is change of velocity during time dt
        :return:
        """
        dv = self.acceleration * self.dt
        v = self.velocity + dv
        return v

    def calculate_distance_traveled(self) -> np.ndarray:
        """
        Calculates the planet's vector of change in distance using the formula s = v * t.
        :return:
        """

        ds = self.velocity * self.dt
        return ds

    def update_plot(self):
        """
        Update the plotting objects attributes.
        :return:
        """
        self.planet_plot.positions = self.positions

    class PlanetPlot:
        """
        Inner class of Planet which will be passed to the plotting animation. Contains only the necessary information
        used for plotting.
        """
        def __init__(self, planet):
            self.name = planet.name
            self.color = planet.color
            self.mass = planet.mass
            self.positions = planet.positions


class SolarSystem:
    """
    Class representing the Solar System with multiple planets. Doesn't take any parameters. Instead, the planets are
    added via the add_planets() function.
    """
    def __init__(self, dt):
        self.planets = []
        self.dt = dt

    def distance_vector(self, pos1: np.ndarray, pos2: np.ndarray) -> np.ndarray:
        """
        Find the vector difference. We use it with position arguments pos1 and pos2
        :param pos1:
        :param pos2:
        :return:
        """
        return pos2 - pos1

    def unit_vector(self, vector: np.ndarray) -> np.ndarray:
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
        colors = itertools.cycle(planet_colors)

        for planet_name in planets:
            self.planets.append(
                Planet(position=np.array(planets[planet_name]['position']),
                       velocity=np.array(planets[planet_name]['velocity']),
                       mass=planets[planet_name]['mass'], dt=self.dt, name=planet_name, color=next(colors)))

    def calculate_force(self, planet1: Planet, planet2: Planet) -> np.ndarray:
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

    def update_position(self) -> list:
        """
        For planet1 calculate the force between another planet. Do this for all possible combinations. Then append
        the calculated force to the forces list for planet1. After the forces list has been updated, calculate new
        positions for all the planets. Returns 2 np.arrays containing x and y coordinates for all planets positions .
        :return:
        """

        for index1, planet1 in enumerate(self.planets):
            for index2, planet2 in enumerate(self.planets[index1+1:]):
                F = self.calculate_force(planet1, planet2)
                planet1.forces.append(F)
                planet2.forces.append(-F)

        for planet in self.planets:
            planet.calculate_position()

        planet_plots = [p.planet_plot for p in self.planets]

        return planet_plots
