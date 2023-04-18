import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import planet_project.universe as universe
from planet_project.constants import star_mass, planet_scale, star_size


# you must install ffmpeg to run this code and redirect to .exe file. Don't know how it works on Linux. This is only for
# saving the image. If you don't have ffmpeg, the video will be saved as a .gif file
# plt.rcParams[
#     'animation.ffmpeg_path'] = 'C:\\Users\\Dano\\Downloads\\ffmpeg-master-latest-win64-gpl\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe'


class Animation:
    """
    Animation class used for animating the object movement. Takes SolarSystem object as parameter. The __init__ function
    creates the base figure with xlim and ylim. The animation will be a sequence of these figures.
    """

    def __init__(self, solar_system: universe.SolarSystem, background_on: bool = True,
                 gif_path: str = 'planets_simulation.gif', gif_fps: int = 10, gif_length: int = 30,
                 gif_zoom: float = 0.5):
        self.system = solar_system
        self.gif_path = gif_path
        self.gif_fps = gif_fps
        self.gif_length = gif_length
        self.gif_zoom = gif_zoom
        self.background_on = background_on
        self.trajectories_plots = []
        self.planets_plot = []
        self.plots = []
        self.background = []
        # Create the figure object and axes
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.xlim_min, self.xlim_max = -5e12, 5e12
        self.ylim_min, self.ylim_max = -5e12, 5e12
        if self.background_on:
            self.stars_x = np.random.uniform(low=self.xlim_min, high=self.xlim_max, size=500)
            self.stars_y = np.random.uniform(low=self.ylim_min, high=self.ylim_max, size=500)
        self.ax.set_xlim(self.xlim_min, self.xlim_max)
        self.ax.set_ylim(self.ylim_min, self.ylim_max)
        self.ax.set_facecolor('black')
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
        self.background.clear()

        planets_num = len(self.system.planets)
        # for each planet we create own plot and store it in trajectories_plots
        # trajectory plots, ls='-' specifies the line style
        for _ in range(planets_num):
            one_planet_trajectory, = self.ax.plot([], [], 'gray', ls='-', zorder=2)
            self.trajectories_plots.append(one_planet_trajectory)

            # Single point plot representing the actual planet. I didn't parametrize the one_planet_trajectory to plot
            # a point in the end of trajectory, because when the animation was reset, the point stayed in the plot.
            # Having a different plot for the actual planet, we can easily remove it when resetting the animation.
            plot_planet, = self.ax.plot([], [], 'o', color='blue', alpha=1, zorder=3)
            self.planets_plot.append(plot_planet)
        if self.background_on:
            background_stars = self.ax.plot(self.stars_x, self.stars_y, '.', markersize=1, color='white', alpha=0.5,
                                            zorder=1)
            self.background.append(background_stars)

        # list of all plots. background, trajectories and planets
        self.plots = self.trajectories_plots + self.planets_plot + self.background

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
        # set different markersizes according to planets mass (higher mass, bigger markersize in the plot
        masses = np.array([planet.mass for planet in planet_plots])
        # mass_mask = np.array([False if mass > star_mass else True for mass in masses])
        mass_mask = masses <= star_mass
        masses_scaled = np.zeros(len(planet_plots,))
        # only take into consideration smaller planets (without the sun)
        masses_scaled[mass_mask] = np.interp(masses[mass_mask], (min(masses[mass_mask]), max(masses[mass_mask])),
                                             planet_scale)
        # set the marker size of the sun
        masses_scaled[~mass_mask] = star_size
        # set data, color and marker size for each planet plot separately.
        for index, planet_plot in enumerate(self.planets_plot):
            planet_plot.set_data(x[index], y[index])
            planet_plot.set_color(colors[index])
            planet_plot.set_markersize(masses_scaled[index])

        # list of all plots. background, trajectories and planets
        self.plots = self.trajectories_plots + self.planets_plot + self.background

        # return an iterable with plots to the animation function
        return self.plots

    def start_animation(self):
        """
        Function to start the animation. This is done by the FuncAnimation from matplotlib.Animation module.
        After exiting the animation is saved.
        :return:
        """

        self.planets_animation = animation.FuncAnimation(self.fig, self.update, init_func=self.init_animation,
                                                         interval=20, repeat=True,
                                                         save_count=self.gif_length * self.gif_fps)

        # when clicking on figure the animation stops
        self.fig.canvas.mpl_connect('button_press_event', self._toggle_pause)
        # plt.imshow(self.background, extent=[-5e12, 5e12, -5e12, 5e12])

        self.save_animation()

        # Show the plot
        plt.show()

        # save video using FFMpeg
        # writer = animation.FFMpegWriter(fps=10)
        # # Save the animation as a video file
        # self.planets_animation.save("planets_simulation.mp4", writer=writer)

    def save_animation(self):
        plt.xlim(self.xlim_min * self.gif_zoom, self.xlim_max * self.gif_zoom)
        plt.ylim(self.ylim_min * self.gif_zoom, self.ylim_max * self.gif_zoom)
        # If you don't have FFMpeg installed uncomment this line and comment the lines below
        print('Saving animation...')
        writergif = animation.PillowWriter(fps=self.gif_fps)
        self.planets_animation.save(self.gif_path, writergif)
        print('Saving done.')
        plt.xlim(self.xlim_min, self.xlim_max)
        plt.ylim(self.ylim_min, self.ylim_max)


    def _toggle_pause(self, *args, **kwargs):
        # internal function, pauses and resumes animation when clicked on figure
        if self.paused:
            self.planets_animation.resume()
        else:
            self.planets_animation.pause()
        self.paused = not self.paused
