from animation import Animation
import json
from universe import SolarSystem


class Loader:
    """
    Class responsible for the loading of json files with data. Accepts parameter path (path to the data). Actual loading
    is done using the load_data function.
    """
    def __init__(self, path: str):
        self.path = path

    def load_data(self) -> dict:
        """
        Loads json alike data and returns it as a dict.
        :return:
        """
        with open(self.path) as file:
            data = json.loads(file.read())
        return data


class Manager:
    """
    Manager class responsible for calling the loading, calculation and animation. Accepts parameter path (path to data)
    """
    def __init__(self, path: str):
        self.loader = Loader(path)
        self.system = SolarSystem()
        self.animation = Animation(self.system)

    def run(self):
        """
        Executing function. Loads data, adds planets and then start animation.
        :return:
        """
        planets = self.loader.load_data()
        self.system.add_planets(planets)
        self.animation.start_animation()
