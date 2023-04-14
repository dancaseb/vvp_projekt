import matplotlib.pyplot as plt
import numpy as np
# you must install ffmpeg to run this code
plt.rcParams['animation.ffmpeg_path'] = 'C:\\Users\\Dano\\Downloads\\ffmpeg-master-latest-win64-gpl\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe'

import matplotlib.animation as animation

import universe


class Animation:
    """
    Animation class used for animating the object movement. Takes SolarSystem object as parameter. The __init__ function
    creates the base figure with xlim and ylim. The animation will be a sequence of these figures.
    """
    def __init__(self, solar_system: universe.SolarSystem):
        self.system = solar_system
        self.trajectories_plots = []
        self.planets_plot = []
        self.plots = []
        self.background = plt.imread('background_space.png')
        # Create the figure object and axes
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-5e12, 5e12)
        self.ax.set_ylim(-5e12, 5e12)
        # self.ax.set_facecolor('black')
        self.paused = False
        self.planets_animation = None


    def init_animation(self) -> list[plt.Axes.plot]:
        """
        Initialize animation. This function is a parameter to the FuncAnimation. init_function is called every time
        the animation is repeated.
        :return:
        """
        # remove the plots before the start of animation and clear all list. We must start with empty lists to prevent
        # unexpected behaviour
        for plot in self.planets_plot:
            plot.remove()
        self.trajectories_plots.clear()
        self.planets_plot.clear()
        self.plots.clear()

        planets_num = len(self.system.planets)
        # for each planet we create own plot and store it in trajectories_plots
        # trajectory plots, ls='-' specifies the line style
        for _ in range(planets_num):
            one_planet_trajectory, = self.ax.plot([], [], 'gray', ls='-')
            self.trajectories_plots.append(one_planet_trajectory)

            # Single point plot representing the actual planet. I didn't parametrize the one_planet_trajectory to plot
            # a point in the end of trajectory, because when the animation was reset, the point stayed in the plot.
            # Having a different plot for the actual planet, we can easily remove it when resetting the animation.
            plot_planet, = self.ax.plot([], [], 'o', color='blue')
            self.planets_plot.append(plot_planet)
        # list of all plots. trajectories and planets
        self.plots = self.trajectories_plots + self.planets_plot

        # return an iterable with plots to the animation function
        return self.plots

    def update(self, _):
        """
        update function is a required parameter for FuncAnimation. We must update the frames. This finds the updates
        position of planets.

        Inspiration for the animation of multiple plot lines was taken from here: https://stackoverflow.com/a/23065440
        Documentation for FuncAnimation: https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html
        Examples of FuncAnimation usage: https://matplotlib.org/stable/api/animation_api.html
        :return:
        """
        # Calculate the new positions of the planets and get the plotting ojects
        planet_plots = self.system.update_position()

        # lists of x and y coordinates to plot the trajectories
        xlist = [[position[0] for position in planet_plot.positions] for planet_plot in planet_plots]
        ylist = [[position[1] for position in planet_plot.positions] for planet_plot in planet_plots]

        # set data for each trajectory plot separately.
        for index, trajectory_plot in enumerate(self.trajectories_plots):
            trajectory_plot.set_data(xlist[index], ylist[index])

        # x,y coordinates for the planets actual position.
        # At this position a circle representing the planet will be plotted
        x = np.array([planet.position[0] for planet in planet_plots])
        y = np.array([planet.position[1] for planet in planet_plots])
        colors = [planet.color for planet in planet_plots]
        masses = np.array([planet.mass for planet in planet_plots])
        masses_scaled = np.interp(masses, (min(masses), max(masses)), (4, 15))
        masses[0] = 20
        # set data for each planet plot separately.
        for index, planet_plot in enumerate(self.planets_plot):
            planet_plot.set_data(x[index], y[index])
            planet_plot.set_color(colors[index])
            planet_plot.set_markersize(masses_scaled[index])

        # list of all plots. trajectories and planets
        self.plots = self.trajectories_plots + self.planets_plot

        # return an iterable with plots to the animation function
        return self.plots

    def start_animation(self):
        """
        Function to start the animation. This is done by the FuncAnimation from matplotlib.Animation module.
        After exiting the animation is saved.
        :return:
        """

        self.planets_animation = animation.FuncAnimation(self.fig, self.update, init_func=self.init_animation,
                                                         frames=100, interval=20, repeat=True)

        # when clicking on figure the animation stops
        self.fig.canvas.mpl_connect('button_press_event', self._toggle_pause)
        plt.imshow(self.background, extent=[-5e12, 5e12, -5e12, 5e12])
        # Show the plot
        plt.show()

        # # save video using FFMpeg
        # writer = animation.FFMpegWriter(fps=10)
        # # Save the animation as a video file
        # self.planets_animation.save("video.mp4", writer=writer)

        # If you don't have FFMpeg installed uncomment this line and comment the lines above
        # self.planets_animation.save("video.gif", fps=10)

    def _toggle_pause(self, *args, **kwargs):
        # internal function, pauses and resumes animation when clicked on figure
        if self.paused:
            self.planets_animation.resume()
        else:
            self.planets_animation.pause()
        self.paused = not self.paused
