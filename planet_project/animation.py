import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import planet_project.universe as universe
from planet_project.constants import star_mass, planet_scale, star_size, edges


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
        self.xlim_min, self.xlim_max = self._find_limits(0)
        self.ylim_min, self.ylim_max = self._find_limits(1)
        if self.background_on:
            self.stars_x = np.random.uniform(low=self.xlim_min, high=self.xlim_max, size=500)
            self.stars_y = np.random.uniform(low=self.ylim_min, high=self.ylim_max, size=500)
        self.ax.set_xlim(self.xlim_min, self.xlim_max)
        self.ax.set_ylim(self.ylim_min, self.ylim_max)
        self.ax.set_facecolor('black')
        self.paused = False
        self.planets_animation = None
        self.planets_num = 0

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

        self.planets_num = len(self.system.planets)
        # for each planet we create own plot and store it in trajectories_plots
        # trajectory plots, ls='-' specifies the line style
        for _ in range(self.planets_num):
            one_planet_trajectory, = self.ax.plot([], [], 'gray', ls='-', zorder=2)
            self.trajectories_plots.append(one_planet_trajectory)

        if self.background_on:
            background_stars = self.ax.plot(self.stars_x, self.stars_y, '.', markersize=1, color='white', alpha=0.5,
                                            zorder=1)
            self.background.append(background_stars)

        # list of all plots. background, trajectories and planets
        self.plots = self.trajectories_plots + self.background

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

        self._prepare_plots(xlist, ylist, planet_plots)

        # list of all plots. background, trajectories
        self.plots = self.trajectories_plots + self.background

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

        # Show the plot
        plt.show()

        # save video using FFMpeg
        # writer = animation.FFMpegWriter(fps=10)
        # # Save the animation as a video file
        # self.planets_animation.save("planets_simulation.mp4", writer=writer)

    def save_animation(self):
        # ziskat xlist a ylist a pak pomoci slicu davat jako parametr _prepare_plots. Podivat se, jak poresit x a y (mozna udelat jako posledni prvek z xlist a ylist?)
        pass
        # plt.xlim(self.xlim_min * self.gif_zoom, self.xlim_max * self.gif_zoom)
        # plt.ylim(self.ylim_min * self.gif_zoom, self.ylim_max * self.gif_zoom)
        # print('Saving animation...')
        # writergif = animation.PillowWriter(fps=self.gif_fps)
        # self.planets_animation.save(self.gif_path, writergif)
        # print('Saving done.')
        # plt.xlim(self.xlim_min, self.xlim_max)
        # plt.ylim(self.ylim_min, self.ylim_max)




    def _toggle_pause(self, *args, **kwargs):
        # internal function, pauses and resumes animation when clicked on figure
        if self.paused:
            self.planets_animation.resume()
        else:
            self.planets_animation.pause()
        self.paused = not self.paused

    def _find_limits(self, axis: int):
        # find lim_max and lim_min for given axis (0 is axis x and 1 is axis y)
        if axis != 0 and axis != 1:
            raise ValueError('axis must be set to zero or one in _find_limits function.')
        positions = [planet.position[axis] for planet in self.system.planets]
        return min(positions) - edges, max(positions) + edges

    def _delete_planet_circles(self):
        # delete all patches from self.ax. We only add circles (representing the planet plot) as patches
        [p.remove() for p in self.ax.patches]

    def _prepare_plots(self, xlist, ylist, planet_plots):
        """
        Add the necessary info into our plots. Working with positions (xlist, ylist) and a list with all planet plotting
        objects.
        :param xlist:
        :param ylist:
        :param planet_plots:
        :return:
        """
        # x,y coordinates represent the planets last position.
        # At this position a circle representing the planet will be plotted
        x = np.array([planet_x_positions[-1] for planet_x_positions in xlist])
        y = np.array([planet_y_positions[-1] for planet_y_positions in ylist])

        colors = [planet.color for planet in planet_plots]
        masses = np.array([planet.mass for planet in planet_plots])
        mass_mask = masses <= star_mass
        masses_scaled = np.zeros(len(planet_plots, ))
        # only take into consideration smaller planets (without the sun)
        masses_scaled[mass_mask] = np.interp(masses[mass_mask], (min(masses[mass_mask]), max(masses[mass_mask])),
                                             planet_scale)
        # set the marker size of the sun
        masses_scaled[~mass_mask] = star_size
        # set data, color and marker size for each planet plot separately.

        # delete previous circles in ax. Plotting will be faster
        self._delete_planet_circles()
        # set data for each trajectory plot separately. Each trajectory has a planet, add planet as patch (circle)
        for index, trajectory_plot in enumerate(self.trajectories_plots):
            trajectory_plot.set_data(xlist[index], ylist[index])
            circle = plt.Circle((x[index], y[index]), radius=masses_scaled[index], color=colors[index], fill=True,
                                zorder=3)
            self.ax.add_patch(circle)
