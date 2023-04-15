from planet_project.animation import Animation
import json
from planet_project.universe import SolarSystem
import random
import string

import numpy as np
from planet_project.constants import G


class Loader:
    """
    Class responsible for the loading of json files with data. Accepts parameter path (path to the data). Actual loading
    is done using the load_data function.
    """

    def __init__(self, **kwargs):
        self.path = kwargs.get('path')
        self.planets_number = kwargs.get('planets_number')

        if self.path is None and self.planets_number is None:
            raise ValueError('You must provide path parameter or planets_number parameter to load data.')
        if self.path is not None and self.planets_number is not None:
            raise ValueError(
                'You must provide either path parameter or planets_number parameter to load data, not both.')

    def load_data(self) -> dict:
        """
        Loads json alike data and returns it as a dict.
        :return:
        """
        if self.path is None:
            return self.generate_random_data()
        else:
            return self.load_data_from_json()

    def generate_random_data(self) -> dict:
        # dict with our planets
        data = {}
        sun_position = np.array([random.uniform(-10e8, 10e8), random.uniform(-10e8, 1e8)])
        sun_velocity = np.array([random.uniform(-10000, 10000), random.uniform(-10000, 10000)])
        sun_mass = random.uniform(1e30, 2e30)
        # sun_mass = 1.989e+30
        self.generate_planet(data, sun_position, sun_velocity, sun_mass)

        for planet in range(self.planets_number - 1):
            # generate the position of the planet
            position = np.array([random.uniform(-10e10, 10e10), random.uniform(-10e10, 1e10)])

            # generate the velocity of the planet
            velocity = np.array([random.uniform(-30000, 30000), random.uniform(-30000, 30000)])

            # kinda random guess of the mass. I wanted the generated solarsystem to be compact
            # and not all the planets escaping out of the gravitational field of the sun
            r = np.linalg.norm(sun_position - position)
            mass = (3e20 * np.linalg.norm(r)**2)/(sun_mass * G)
            # generate the planet, we update the data
            self.generate_planet(data, position, velocity, mass)
        return data

    def generate_planet(self, data: dict, position: np.ndarray, velocity: np.ndarray, mass: float):
        # create a random name with random length for a planet
        name_length = random.randint(1, 10)
        planet_name = ''.join(random.choices(string.ascii_letters, k=name_length))
        planets_attributes = {'position': position, 'velocity': velocity, 'mass': mass}

        # fill the data dict with the values
        data[planet_name] = {}
        for attribute in planets_attributes.keys():
            data[planet_name][attribute] = planets_attributes[attribute]

    def load_data_from_json(self):
        with open(self.path) as file:
            data = json.loads(file.read())
        return data


class Simulation:
    """
    Manager class responsible for calling the loading, calculation and animation.
    Provide the path parameter (and load data from json file) or planets_num parameter (and generate random planets).
    """

    def __init__(self, dt: int = 60*60*24, **kwargs):
        self.dt = dt
        if self.dt is None:
            raise ValueError('You must provide dt (time step) parameter.')
        self.loader = Loader(**kwargs)
        self.system = SolarSystem(self.dt)
        self.animation = Animation(self.system)

    def run(self):
        """
        Executing function. Loads data, adds planets and then start animation.
        :return:
        """
        planets = self.loader.load_data()
        self.system.add_planets(planets)
        self.animation.start_animation()