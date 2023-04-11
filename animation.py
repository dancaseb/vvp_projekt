import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation


class Animation:
    """
    Animation class used for animating the object movement. Takes SolarSystem object as parameter. The __init__ function
    creates the base figure with xlim and ylim. The animation will be a sequence of these figures.
    """
    def __init__(self, solar_system):
        self.system = solar_system
        self.trajectories_plots = []

        # Create the figure object and axes
        power = 13
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-10**power, 10**power)
        self.ax.set_ylim(-10**power, 10**power)
        self.x = np.array([])
        self.y = np.array([])
        # I guess this is not needed
        # self.graph, = self.ax.plot([], [])
        self.paused = False
        self.planets_animation = None

    def init_animation(self):
        """
        Initialize animation. This function is a parameter to the FuncAnimation. init_function is called every time
        the animation is repeated.
        :return:
        """
        #
        try:
            self.trajectories_plots[-1].remove()
        except IndexError:
            pass
        self.trajectories_plots.clear()

        planets_num = len(self.system.planets)
        # for each planet we create own plot and store it in trajectories_plots
        # trajectory plots, ls='-' specifies the line style
        for _ in range(planets_num):
            one_planet_trajectory, = self.ax.plot([], [], 'g', ls='-')
            self.trajectories_plots.append(one_planet_trajectory)

        # Single point plot representing the actual planet. I didn't parametrize the one_planet_trajectory to plot
        # a point in the end of trajectory, because when the animation was reset, the point stayed in the plot. Having a
        # different plot for the actual planet, we can easily remove it when resetting the animation.
        plot_planet_point, = self.ax.plot([], [], 'o', color='blue')
        self.trajectories_plots.append(plot_planet_point)

        # return a list of plots
        return self.trajectories_plots


    def update(self, frame):
        """
        update function is a required parameter for FuncAnimation. We must update the frames. This finds the updates
        position of planets.

        Inspiration for the animation of multiple plot lines was taken from here: https://stackoverflow.com/a/23065440
        Documentation for FuncAnimation: https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html
        Examples of FuncAnimation usage: https://matplotlib.org/stable/api/animation_api.html
        :param frame:
        :return:
        """
        # Calculate the new positions of the planets
        x, y = self.system.update_position()

        # Fetch the trajectories of all planets saved in a list
        trajectories = self.system.get_planets_trajectories()
        # lists of x and y coordinates to plot the trajectories
        xlist = [[position[0] for position in trajectory] for trajectory in trajectories]
        ylist = [[position[1] for position in trajectory] for trajectory in trajectories]

        # Add x,y coordinates for the planets actual position.
        # At this position a circle representing the planet will be plotted
        xlist.append(x)
        ylist.append(y)

        # set data for each plot separately.
        for index, trajectory_plot in enumerate(self.trajectories_plots):
            trajectory_plot.set_data(xlist[index], ylist[index])

        # return the list of plots
        return self.trajectories_plots

    def start_animation(self):
        """
        Function to start the animation. This is done by the FuncAnimation from matplotlib.animation module.
        After exiting the animation is saved.
        :return:
        """

        self.planets_animation = animation.FuncAnimation(self.fig, self.update, init_func=self.init_animation,
                                                         frames=60, interval=20, repeat=True)

        # when clicking on figure the animation stops
        self.fig.canvas.mpl_connect('button_press_event', self._toggle_pause)

        # Show the plot
        plt.show()
        # FFwriter = animation.FFMpegWriter(codec='avi')
        # self.animation.save("video.gif")
        # writervideo = animation.FFMpegWriter(fps=60)
        # self.animation.save('increasingStraightLine.mp4', writer=writervideo)

    def _toggle_pause(self, *args, **kwargs):
        # internal function, pauses and resumes animation when clicked on figure
        if self.paused:
            self.planets_animation.resume()
        else:
            self.planets_animation.pause()
        self.paused = not self.paused
