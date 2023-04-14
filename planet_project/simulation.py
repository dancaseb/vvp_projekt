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
        sun_position = np.array([0.0, 0.0])
        sun_velocity = np.array([-0.0, 0.0])
        # sun_mass = random.uniform(1e30, 1e40)
        sun_mass = 1.989e+29
        self.generate_planet(data, sun_position, sun_velocity, sun_mass)

        for planet in range(self.planets_number - 1):
            # generate the mass of the planet
            # position = [random.uniform(-1e4, 1e4), random.uniform(-1e4, 1e4)]
            position = np.array([
                random.uniform(-10e10, 1e10),
                random.uniform(-10e10, 1e10)])

            # position = np.array([
            #     46715511567.428986,
            #     34221828241.256115])
            # position = [2*p for p in position]
            # velocity = [random.uniform(-1e0, 1e1), random.uniform(-1e0, 1e1)]
            velocity = np.array([-28011.358452879696,
                                 38237.72741186753])
            # mass = random.uniform(1e1, 1e2)
            r = np.linalg.norm(sun_position - position)
            mass = (1e20 * np.linalg.norm(r)**2)/(sun_mass * G)
            print(f"{mass:e}")
            self.generate_planet(data, position, velocity, mass)
            # create a random name with random length for a planet
        return data

    def generate_planet(self, data: dict, position: list, velocity: list, mass: float):
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

    def __init__(self, **kwargs):
        dt = kwargs.get('dt')
        self.loader = Loader(**kwargs)
        self.system = SolarSystem(dt)
        self.animation = Animation(self.system)

    def run(self):
        """
        Executing function. Loads data, adds planets and then start animation.
        :return:
        """
        planets = self.loader.load_data()
        self.system.add_planets(planets)
        self.animation.start_animation()
