# import itertools
# import matplotlib.pyplot as plt
# import time
# from constants import G
# import numpy as np
# import matplotlib.animation as animation
# import json
# class Planet:
#     def __init__(self, mass, position, velocity, name):
#         self.name = name
#         self._mass = mass
#         self._position = position
#         self._acceleration = np.array([0.0, 0.0])
#         # self._direction = np.array([0, 0])
#         self._force = np.array([0.0, 0.0])
#         self._velocity = velocity
#         self.forces = []
#         self.dt = 60*60*24*7
#         self.positions = [tuple(self._position)]
#
#     @property
#     def position(self):
#         return self._position
#
#     @position.setter
#     def position(self, new_position):
#         if not isinstance(new_position, np.ndarray):
#             raise AssertionError('Position must be a element tuple.')
#         if len(new_position) != 2:
#             raise AssertionError('Position must contain 2 elements for x and y axis.')
#         self._position = new_position
#
#     @property
#     def acceleration(self):
#         return self._acceleration
#
#     @acceleration.setter
#     def acceleration(self, new_acceleration):
#         self._acceleration = new_acceleration
#
#     # @property
#     # def direction(self):
#     #     return self._direction
#     #
#     # @direction.setter
#     # def direction(self, new_direction):
#     #     self._direction = new_direction
#
#     @property
#     def force(self):
#         return self._force
#
#     @force.setter
#     def force(self, new_force):
#         self._force = new_force
#
#     @property
#     def mass(self):
#         return self._mass
#
#     @mass.setter
#     def mass(self, new_mass):
#         self._mass = new_mass
#
#     @property
#     def velocity(self):
#         return self._velocity
#
#     @velocity.setter
#     def velocity(self, new_velocity):
#         self._velocity = new_velocity
#
#     def calculate_position(self):
#         self.force = np.add.reduce(self.forces)
#         # print(f"force {self.force}")
#         # print(self.position,self.forces)
#         a = self.calculate_acceleration(self.force)
#         v = self.calculate_velocity(a)
#         self.velocity = v
#         s = self.calculate_distance(self.velocity, a)
#         self.position += s
#         # if self.name == 'Mercury':
#         #     print(f"force of merkury {np.linalg.norm(self.force) /1000}")
#         #     print(f"velocity of merkury {np.linalg.norm(self.velocity) /1000}")
#         #     print(f"acceleration of merkury {np.linalg.norm(a) /1000}")
#         #     print(f"position of merkury {self.position}")
#         #     print("**************")
#         # print(f"position {self.position}")
#         # append the new position, used for plotting trajectory
#         self.positions.append(tuple(self.position))
#         # print(f"velocity {self.velocity}")
#         self.forces.clear()
#         # print(f"position {self.position}")
#
#     def calculate_acceleration(self, force):
#         a = force / self.mass
#         return a
#
#     def calculate_velocity(self, acceleration):
#         # mozna blbe? to znamena, ze se porad zrychluje, idk
#         # v = acceleration * self.dt + self.velocity
#         # konst. rychlost na intervalu dt
#         dv = acceleration * self.dt  # zmena rychlosti behem dt
#         v = self.velocity + dv
#         return v
#
#     def calculate_distance(self, velocity, acceleration):
#         ds = velocity * self.dt
#         # s = 0.5 * acceleration * self.dt**2 + velocity * self.dt
#         return ds
#
#
#
# class SolarSystem:
#     def __init__(self):
#         self.planets = []
#         # self.draw = Draw()
#
#     def distance(self, pos1, pos2):
#         # return np.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)
#         # return np.linalg.norm(pos1 - pos2)
#         return pos2 - pos1
#
#     def unit_vector(self, vector):
#         return vector / np.linalg.norm(vector)
#
#     def add_planets(self, planets):
#         for planet_name in planets:
#             # print(planet_name)
#             # # print(planets[planet_name])
#             # print(planets[planet_name]['position'], planets[planet_name]['velocity'], planets[planet_name]['mass'])
#             self.planets.append(
#                 Planet(position=np.array(planets[planet_name]['position']),
#                        velocity=np.array(planets[planet_name]['velocity']),
#                        mass=planets[planet_name]['mass'], name=planet_name))
#         # sun = Planet(1.989e+30, np.array([0.0, 0.0]), np.array([0.0, 0.0]), name="sun")
#         # # p = Planet(10**10, np.array([0, 342218282.256115]), np.array([-28011.358452879696,
#         # # -38237.72741186753]), name="planet")
#         # mercury = Planet(3.301e+23, np.array([46715511567.428986, 34221828241.256115]),
#         #                  np.array([-28011.358452879696, 38237.72741186753]), name="mercury")
#         # venus = Planet(4.867e+24, np.array([-86869168232.3607, -64520695457.83519]),
#         #                np.array([20869.112567920518, -28097.689239997333]), name="venus")
#         #
#         # # g = Planet(1.989e+30, np.array([10000000.0, 10000000.0]), np.array([0, 0]))
#         # # q = Planet(30000000, np.array([100.0, 100.0]))
#         # self.planets.extend([sun, mercury, venus])
#
#     def calculate_force(self, planet1, planet2):
#         F = (self.unit_vector(self.distance(planet1.position, planet2.position)) * (G * (planet1.mass * planet2.mass))) / (
#                     np.linalg.norm(self.distance(planet1.position, planet2.position)) ** 2)
#         # print(f"distance {np.linalg.norm(self.distance(planet1.position, planet2.position))}")
#         # print(np.linalg.norm(self.distance(planet1.position, planet2.position)))
#         return F
#
#
#     # def update_position(self):
#     #     F = self.calculate_force(self.planets[0], self.planets[1])
#     #     a = self.calculate_acceleration(F, self.planets[0])
#     #     v = self.calculate_velocity(a)
#     #     s = self.calculate_distance(v)
#     #     # print(self.planets[0].position)
#     #     self.planets[0].position += s
#     #     # print(self.planets[0].position)
#
#     def update_position(self):
#         # do for each of two planets
#         # for planet1, planet2 in itertools.permutations(self.planets, 2):
#         #     # print(planet1, planet2)
#         #     F = self.calculate_force(planet1, planet2)
#         #     print(f"F:{F}")
#         #     a = self.calculate_acceleration(F, planet1)
#         #     print(f"a:{a}")
#         #     v = self.calculate_velocity(a, planet1)
#         #     planet1.velocity = v
#         #     print(planet1.velocity)
#         #     s = self.calculate_distance(v)
#         #     planet1.position += s
#         #     print(planet1.position)
#         for index1, planet1 in enumerate(self.planets):
#             for index2, planet2 in enumerate(self.planets):
#                 if index2 == index1:
#                     continue
#                 else:
#                     # print(planet1, planet2)
#                     F = self.calculate_force(planet1, planet2)
#                     planet1.forces.append(F)
#
#         for planet in self.planets:
#             # print(planet.name)
#             planet.calculate_position()
#             # print("**********************")
#
#         x = np.array([p.position[0] for p in self.planets])
#         y = np.array([p.position[1] for p in self.planets])
#         # print(self.planets[1].positions)
#         # positions = np.array([planet.positions for planet in self.planets])
#         # print(f"positions: {[x for x in positions]}")
#         # x = np.array([position[0] for position in positions])
#         # y = np.array([position[1] for position in positions])
#         return x, y
#         # return positions
#
#
#
#     # def plot(self):
#     # def plot_everything(self):
#     #     x = np.array([p.position[0] for p in self.planets])
#     #     y = np.array([p.position[1] for p in self.planets])
#     #     fig, axes = plt.subplots()
#     #     axes.set_xlim(0, 10000000)
#     #     axes.set_ylim(0, 10000000)
#     #     plt.scatter(x, y)
#     #     # plt.xlabel('X-axis')
#     #     # plt.ylabel('Y-axis')
#     #     plt.show()
#     #     # self.images.append(im)
#     #     # Display the plot
#     #
#     #     # plt.pause(0.5)
#     #     # im = plt.
#
#     #
#     # def run(self):
#     #     self.update_position()
#     #     # print(self.planets[0].position)
#
#
# # class Draw:
# #     def __init__(self):
# #         self.fig, self.axes = plt.subplots()
# #         self.axes.set_xlim(0, 10000000)
# #         self.axes.set_ylim(0, 10000000)
# #         point, = self.axes.plot(0, 0, marker='o', markersize=10, color='red')
# #         plt.xlabel('X-axis')
# #         plt.ylabel('Y-axis')
# #
# #     def update(self, frame, points):
# class Animation:
#     # Define the initial position of the point
#
#
#     # Define the update function for the animation
#     def __init__(self, solar_system):
#         self.system = solar_system#
#
#     def update(self, frame):
#         # Calculate the new position of the point
#         x, y = self.system.update_position()
#         # Update the position of the point on the plot
#         self.plotting_graph.set_offsets(np.column_stack((x, y)))
#         # self.plotting_graph.set_data(x, y)
#         # Return the point object
#         return self.plotting_graph,
#     def plot(self):
#
#         # # Create the point object
#         # point, = ax.plot(x, y, marker='o', markersize=10, color='red')
#
#         # Create the animation object
#         na = 13
#         self.fig, self.ax = plt.subplots()
#         self.ax.set_xlim(-10**na, 10**na)
#         self.ax.set_ylim(-10**na, 10**na)
#         self.x = np.array([])
#         self.y = np.array([])
#         self.plotting_graph = self.ax.scatter([], [])
#         # self.system = SolarSystem()
#         # self.system.add_planets()
#
#         self.animation = animation.FuncAnimation(self.fig, self.update, frames=60, interval=5)
#         self.paused = False
#
#         self.fig.canvas.mpl_connect('button_press_event', self.toggle_pause)
#
#         # Show the plot
#         plt.show()
#         # FFwriter = animation.FFMpegWriter(codec='avi')
#         # self.animation.save("video.gif")
#         # writervideo = animation.FFMpegWriter(fps=60)
#         # self.animation.save('increasingStraightLine.mp4', writer=writervideo)
#
#     def toggle_pause(self, *args, **kwargs):
#         if self.paused:
#             self.animation.resume()
#         else:
#             self.animation.pause()
#         self.paused = not self.paused
#
#
# class Loader:
#     def __init__(self, path):
#         self.path = path
#
#     def load_data(self):
#         with open(self.path) as file:
#             data = json.loads(file.read())
#         return data
#
#
# class Manager:
#     def __init__(self):
#         self.loader = Loader("data/planets.json")
#         self.system = SolarSystem()
#         self.animation = Animation(self.system)
#
#     def run(self):
#         planets = self.loader.load_data()
#         self.system.add_planets(planets)
#         self.animation.plot()
#
#
#
#
# # class Draw:
# #     def __init__(self):
# #         self.fig, self.axes = plt.subplots()
# #         self.axes.set_xlim(0, 500)
# #         self.axes.set_ylim(0, 500)
# #         plt.xlabel('X-axis')
# #         plt.ylabel('Y-axis')
# #     def plot(self, planets):
# #         self.x = np.array([p.position[0] for p in planets])
# #         self.y = np.array([p.position[1] for p in planets])
# #         self.axes
# #
# #     def animate(self):
# #
# #     def animate(self):
# #
# #         # anim.save('sine_wave.gif', writer='imagemagick')
# #         plt.show()
# #         plt.scatter()
# #         plt.show()
#
#
#
# # def distance(pos1, pos2):
# #     # return np.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)
# #     # return np.linalg.norm(pos1 - pos2)
# #     return pos2 - pos1
# #
# # def unit_vector(vector):
# #     return vector / np.linalg.norm(vector)
# #
# # if __name__ == '__main__':
# #     dt = 10
# #     p = Planet(300000000000, np.array([23.0, 13.0]))
# #     g = Planet(40000000, np.array([100.0, 82.0]))
# #     print(np.linalg.norm(distance(g.position, p.position)))
# #     # print(distance(g.position, p.position))
# #     F = (unit_vector(distance(p.position, g.position)) * (G * (p.mass * g.mass))) / (np.linalg.norm(distance(p.position, g.position))**2)
# #     print(np.linalg.norm(F))
# #     print(F)
# #
# #     a = F/p.mass
# #     print(a)
# #     print(np.linalg.norm(a))
# #
# #
# #     # # print(a)
# #     v = a * dt
# #     print(v)
# #     print(np.linalg.norm(v))
# #     s = v * dt
# #     print(type(s))
# #     p.position += s
# #     print(p.position)
#
# # system = SolarSystem()
# # system.add_planets()
# # # system.update_position()
# # # system.plot_everything()
# # system.run()
# # manager = Manager()
# # manager.run()
#
# from planet_project import Manager
# # tk backend opens a new interactive window
# # %matplotlib tk
# # run the calculations
# manager = Manager("data/planets.json")
# manager.run()
#

from planet_project.simulation import Simulation
# tk backend opens a new interactive window

# run the calculations
# manager = Simulation(path='data/planets.json')
# manager.run()
manager = Simulation(planets_number=12, dt=60*60*24*7)
manager.run()

# manager = Simulation(path='data/planets.json', dt=60*60*24)
# manager.run()
# simulation = Simulation(path="data/planets.json", dt=60*60*24*7)
# simulation.run()
# simulation = Simulation(path="data/three_body.json", dt=60*60*24*7)
# simulation.run()
# import numpy as np
# from universe import Planet
#
# p = Planet('23', [3],3,4)
# p.position = np.array([2,2])
# loader = Loader(path='data/test.json')
# data = loader.load_data()
# print('test', data)
# loader = Loader(planets_number=3)
# data = loader.generate_random_data()
# print('random', data)

