from animation import Animation
import json
from universe import SolarSystem

class Loader:
    def __init__(self, path):
        self.path = path

    def load_data(self):
        with open(self.path) as file:
            data = json.loads(file.read())
        return data


class Manager:
    def __init__(self, path):
        self.loader = Loader(path)
        self.system = SolarSystem()
        self.animation = Animation(self.system)

    def run(self):
        planets = self.loader.load_data()
        self.system.add_planets(planets)
        self.animation.plot()
