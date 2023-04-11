import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation


class Animation:

    def __init__(self, solar_system):
        self.system = solar_system
        self.trajectories_plots = []

        # Create the animation object
        na = 13
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-10**na, 10**na)
        self.ax.set_ylim(-10**na, 10**na)
        # self.ax2 = self.ax.twinx()
        self.x = np.array([])
        self.y = np.array([])
        self.graph, = self.ax.plot([], [])
    def init(self):
        self.trajectories_plots.clear()
        # for each planet we create own plot
        planets_num = len(self.system.planets)
        for _ in range(planets_num):
            obj, = self.ax.plot([], [], 'bo', ls='-', ms=8, markevery=[-1])
            self.trajectories_plots.append(obj)

        return self.trajectories_plots
    # Define the update function for the animation
    def update(self, frame):
        # Calculate the new positions of the planets
        x,y = self.system.update_position()
        # Update the positions in the plot graph
        # self.graph.set_offsets(np.column_stack((x, y)))
        # self.graph.set_data()
        # line_segments = LineCollection(self.system.get_planets_trajecotires(), linewidths=(0.5, 1, 1.5, 2), linestyle='solid')
        # self.ax.add_collection(line_segments)
        # The trajectory graphs
        trajectories = self.system.get_planets_trajectories()
        # lists of x and y coordinates to plot
        xlist = [[position[0] for position in trajectory] for trajectory in trajectories]
        ylist = [[position[1] for position in trajectory] for trajectory in trajectories]

        for index, trajectory_plot in enumerate(self.trajectories_plots):
            trajectory_plot.set_data(xlist[index], ylist[index])  # set data for each line separately.

        # return graph
        return self.trajectories_plots
    def plot(self):
        # self.graph = self.ax.plot([], [], 'o',ls='-', ms=8,markevery=[-1])
        # self.trajectory_graph = self.ax2.plot()

        self.animation = animation.FuncAnimation(self.fig, self.update, init_func=self.init, frames=1000000, interval=5, blit=True, repeat=False)
        self.paused = False

        self.fig.canvas.mpl_connect('button_press_event', self.toggle_pause)

        # Show the plot
        plt.show()
        # FFwriter = animation.FFMpegWriter(codec='avi')
        # self.animation.save("video.gif")
        # writervideo = animation.FFMpegWriter(fps=60)
        # self.animation.save('increasingStraightLine.mp4', writer=writervideo)

    def toggle_pause(self, *args, **kwargs):
        if self.paused:
            self.animation.resume()
        else:
            self.animation.pause()
        self.paused = not self.paused
