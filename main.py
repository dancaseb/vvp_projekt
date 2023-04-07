import itertools
import matplotlib.pyplot as plt
import time
from constants import G
import numpy as np
from matplotlib.animation import FuncAnimation
class Planet:
    def __init__(self, mass, position):
        self._mass = mass
        self._position = position
        self._acceleration = np.array([0.0, 0.0])
        # self._direction = np.array([0, 0])
        self._force = np.array([0.0, 0.0])
        self._velocity = np.array([0.0, 0.0])

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

    # @property
    # def direction(self):
    #     return self._direction
    #
    # @direction.setter
    # def direction(self, new_direction):
    #     self._direction = new_direction

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



class SolarSystem:
    def __init__(self):
        self.planets = []
        self.dt = 10000
        # self.draw = Draw()

    def distance(self, pos1, pos2):
        # return np.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)
        # return np.linalg.norm(pos1 - pos2)
        return pos2 - pos1

    def unit_vector(self, vector):
        return vector / np.linalg.norm(vector)

    def add_planets(self):
        p = Planet(30000000, np.array([400.0, 400.0]))
        g = Planet(40000000, np.array([250.0, 250.0]))
        q = Planet(30000000, np.array([100.0, 100.0]))
        self.planets.extend([p, g, q])

    def calculate_force(self, planet1, planet2):
        F = (self.unit_vector(self.distance(planet1.position, planet2.position)) * (G * (planet1.mass * planet2.mass))) / (
                    np.linalg.norm(self.distance(planet1.position, planet2.position)) ** 2)
        return F

    def calculate_acceleration(self, force, planet):
        a = force / planet.mass
        return a

    def calculate_velocity(self, acceleration):
        v = acceleration * self.dt
        return v

    def calculate_distance(self, velocity):
        s = velocity * self.dt
        return s

    # def update_position(self):
    #     F = self.calculate_force(self.planets[0], self.planets[1])
    #     a = self.calculate_acceleration(F, self.planets[0])
    #     v = self.calculate_velocity(a)
    #     s = self.calculate_distance(v)
    #     # print(self.planets[0].position)
    #     self.planets[0].position += s
    #     # print(self.planets[0].position)

    def update_position(self):
        # do for each of two planets
        for planet1, planet2 in itertools.permutations(self.planets, 2):
            F = self.calculate_force(planet1, planet2)
            a = self.calculate_acceleration(F, planet1)
            v = self.calculate_velocity(a)
            s = self.calculate_distance(v)
            planet1.position += s


    def plot_everything(self):
        self.images = []
        x = np.array([p.position[0] for p in self.planets])
        y = np.array([p.position[1] for p in self.planets])

        fig, axes = plt.subplots()
        axes.set_xlim(0,500)
        axes.set_ylim(0, 500)
        plt.scatter(x, y)
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.show()
        # self.images.append(im)
        # Display the plot

        # plt.pause(0.5)
        # im = plt.


    def run(self):
        for _ in range(100):
            self.update_position()
            # print(self.planets[0].position)
            self.plot_everything()


# class Draw:
#     def __init__(self):
#         self.fig, self.axes = plt.subplots()
#         self.axes.set_xlim(0, 500)
#         self.axes.set_ylim(0, 500)
#         plt.xlabel('X-axis')
#         plt.ylabel('Y-axis')
#     def plot(self, planets):
#         self.x = np.array([p.position[0] for p in planets])
#         self.y = np.array([p.position[1] for p in planets])
#         self.axes
#
#     def animate(self):
#
#     def animate(self):
#
#         # anim.save('sine_wave.gif', writer='imagemagick')
#         plt.show()
#         plt.scatter()
#         plt.show()



# def distance(pos1, pos2):
#     # return np.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)
#     # return np.linalg.norm(pos1 - pos2)
#     return pos2 - pos1
#
# def unit_vector(vector):
#     return vector / np.linalg.norm(vector)
#
# if __name__ == '__main__':
#     dt = 10
#     p = Planet(300000000000, np.array([23.0, 13.0]))
#     g = Planet(40000000, np.array([100.0, 82.0]))
#     print(np.linalg.norm(distance(g.position, p.position)))
#     # print(distance(g.position, p.position))
#     F = (unit_vector(distance(p.position, g.position)) * (G * (p.mass * g.mass))) / (np.linalg.norm(distance(p.position, g.position))**2)
#     print(np.linalg.norm(F))
#     print(F)
#
#     a = F/p.mass
#     print(a)
#     print(np.linalg.norm(a))
#
#
#     # # print(a)
#     v = a * dt
#     print(v)
#     print(np.linalg.norm(v))
#     s = v * dt
#     print(type(s))
#     p.position += s
#     print(p.position)

system = SolarSystem()
system.add_planets()
# system.update_position()
# system.plot_everything()
system.run()

