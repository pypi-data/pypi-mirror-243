"""
A library to draw simple figures such as points, segments, polygons, arrows, and
boxes in the 3D space using Matplotlib as the backend.
The library exposes classes for the figures, enumerations for the common
colors and line styles, and a function draw3d() to render the figures.
"""
import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

logging.basicConfig(
    format="%(asctime)s [%(levelname)8s] (%(name)s) | %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.info("Using vec3d.graph v0.2.0")


class Colors3D(Enum):
    """A few Matplotlib colors using several techniques such as the CN scheme in
    which 'C' precedes a number acting as an index into the default property
    cycle (see https://matplotlib.org/stable/users/explain/colors/colors.html).
    """

    BLUE = "C0"
    BLACK = "k"
    RED = "C3"
    GREEN = "C2"
    PURPLE = "C4"
    BROWN = "C5"
    PINK = "C6"
    ORANGE = "C11"
    GRAY = "gray"
    CYAN = "c"


class LineStyles3D(Enum):
    """A few Matplotlib linestyles defined for convenience."""

    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"
    DASH_DOT = "dashdot"
    LOOSELY_DOTTED = (0, (1, 10))
    DENSELY_DOTTED = (0, (1, 1))
    LOOSELY_DASHED = (0, (5, 10))
    DENSELY_DASHED = (0, (5, 1))


# See https://github.com/matplotlib/matplotlib/issues/21688
class FancyArrow3D(FancyArrowPatch):
    """Utility class that is used to create Arrows in 3D using FancyArrowPatch
    as the basis.
    """

    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(
        self, renderer=None  # pylint: disable=unused-argument
    ):
        xs3d, ys3d, zs3d = self._verts3d

        # self.axes.M is used to convert 3D data into something that can be
        # plotted using Matplotlib's 2D plotting functions.
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)


IntOrFloat = int | float


class Figure3D(ABC):
    """Abstract base class for all the figures that can be represented in the 3D
    space.
    """

    @staticmethod
    def draw_segment(
        *,
        axes,
        start_point: tuple[IntOrFloat, IntOrFloat, IntOrFloat],
        end_point: tuple[IntOrFloat, IntOrFloat, IntOrFloat],
        color=Colors3D.BLACK,
        linestyle=LineStyles3D.SOLID,
    ) -> None:
        """Static utility method used to draw a segment between the start and
        end points with the given color and linestyle. This function is called
        by its side-effect.

        Args:
            axes: Matplotlib axes
            start_point (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): the
                starting point of the segment
            end_point (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): the
                ending point of the segment
            color (Colors3D): the color of the segment
            linestyle (Linestyle3D): the linestyle of the segment

        Returns:
            None
        """
        xs, ys, zs = [[start_point[i], end_point[i]] for i in range(0, 3)]
        axes.plot(xs, ys, zs, color=color.value, linestyle=linestyle.value)

    @abstractmethod
    def extract_vectors(self) -> tuple[IntOrFloat, IntOrFloat, IntOrFloat]:
        """Generator function that returns the vectors (points) that define the
        figure.

        Returns:
            tuple[IntOrFloat, IntOrFloat, IntOrFloat]: a tuple with the
                corresponding Cartesian coordinates of the vector (point) in the
                3D space.
        """

    @abstractmethod
    def render(self, *, axes, **kwargs) -> None:
        """Performs the necessary side-effects on Matplotlib library to be able
        to render the corresponding 3D figure on a plot.
        """


class Arrow3D(Figure3D):
    """Represents an arrow on the 3D space, defined by its tip and tail
    Cartesian coordinates (x, y, z). If tail is not provided, the arrow is
    assumed to have its tail in the origin (0, 0, 0). The color argument sets
    the color of the segment and head of the arrow. By default, arrows are drawn
    in red. The arrow can also be drawn in different line styles providing the
    linestyle argument. By default, the arrow uses a solid linestyle.
    """

    def __init__(
        self,
        tip: tuple[IntOrFloat, IntOrFloat, IntOrFloat],
        tail=(0, 0, 0),
        color=Colors3D.RED,
        linestyle=LineStyles3D.SOLID,
    ):
        self.tip = tip
        self.tail = tail
        self.color = color
        self.linestyle = linestyle

    def extract_vectors(self) -> tuple[IntOrFloat, IntOrFloat, IntOrFloat]:
        yield self.tip
        yield self.tail

    def render(self, *, axes, **kwargs) -> None:
        xs, ys, zs = zip(self.tail, self.tip)
        a = FancyArrow3D(
            xs,
            ys,
            zs,
            mutation_scale=20,
            arrowstyle="-|>",
            color=self.color.value,
            shrinkA=0,
            shrinkB=0,
            linestyle=self.linestyle.value,
        )
        axes.add_artist(a)


class Points3D(Figure3D):
    """Represents a collections of points in the 3D space, given their Cartesian
    coordinates (x, y, z). The points will be displayed as dots in the given
    color. The default color is black.
    """

    def __init__(self, *vectors, color=Colors3D.BLACK) -> None:
        self.vectors = list(vectors)
        self.color = color

    def extract_vectors(self) -> tuple[IntOrFloat, IntOrFloat, IntOrFloat]:
        for v in self.vectors:
            yield v

    def render(self, *, axes, **kwargs) -> None:
        xs, ys, zs = zip(*self.vectors)
        axes.scatter(xs, ys, zs, color=self.color.value, **kwargs)


class Segment3D(Figure3D):
    """Represents a segment on the 3D space, defined by its starting and ending
    point using their Cartesian coordinates (x, y, z). The segment will be drawn
    using the given color and the given line style.
    """

    def __init__(
        self,
        start_point: tuple[IntOrFloat, IntOrFloat, IntOrFloat],
        end_point: tuple[IntOrFloat, IntOrFloat, IntOrFloat],
        *,
        color=Colors3D.BLUE,
        linestyle=LineStyles3D.SOLID,
    ) -> None:
        self.start_point = start_point
        self.end_point = end_point
        self.color = color
        self.linestyle = linestyle

    def extract_vectors(self) -> tuple[IntOrFloat, IntOrFloat, IntOrFloat]:
        yield self.start_point
        yield self.end_point

    def render(self, *, axes, **kwargs) -> None:
        Figure3D.draw_segment(
            axes=axes,
            start_point=self.start_point,
            end_point=self.end_point,
            color=self.color,
            linestyle=self.linestyle,
        )


class Box3D(Figure3D):
    """Represents a dashed box in the 3D space delimited by a single point given
    its Cartesian coordinates, and its projection into the x-, y-, and z-axes.
    """

    def __init__(self, x: IntOrFloat, y: IntOrFloat, z: IntOrFloat) -> None:
        self.vector = (x, y, z)

    def extract_vectors(self) -> tuple[IntOrFloat, IntOrFloat, IntOrFloat]:
        yield self.vector

    def render(self, *, axes, **kwargs) -> None:
        x, y, z = self.vector
        kwargs = {"linestyle": LineStyles3D.DASHED, "color": Colors3D.GRAY}
        Figure3D.draw_segment(
            axes=axes, start_point=(0, y, 0), end_point=(x, y, 0), **kwargs
        )
        Figure3D.draw_segment(
            axes=axes, start_point=(0, 0, z), end_point=(0, y, z), **kwargs
        )
        Figure3D.draw_segment(
            axes=axes, start_point=(0, 0, z), end_point=(x, 0, z), **kwargs
        )
        Figure3D.draw_segment(
            axes=axes, start_point=(0, y, 0), end_point=(0, y, z), **kwargs
        )
        Figure3D.draw_segment(
            axes=axes, start_point=(x, 0, 0), end_point=(x, y, 0), **kwargs
        )
        Figure3D.draw_segment(
            axes=axes, start_point=(x, 0, 0), end_point=(x, 0, z), **kwargs
        )
        Figure3D.draw_segment(
            axes=axes, start_point=(0, y, z), end_point=(x, y, z), **kwargs
        )
        Figure3D.draw_segment(
            axes=axes, start_point=(x, 0, z), end_point=(x, y, z), **kwargs
        )
        Figure3D.draw_segment(
            axes=axes, start_point=(x, y, 0), end_point=(x, y, z), **kwargs
        )


class Polygon3D(Figure3D):
    """Represents a polygon in the 3D space, defined by its vertices givern
    their Cartesian coordinates (x, y, z). You can specify the color of the
    lines delimiting the polygon.
    """

    def __init__(
        self, *vertices, color=Colors3D.BLUE, linestyle=LineStyles3D.SOLID
    ) -> None:
        self.vertices = vertices
        self.color = color
        self.linestyle = linestyle

    def extract_vectors(self) -> tuple[IntOrFloat, IntOrFloat, IntOrFloat]:
        for v in self.vertices:
            yield v

    def render(self, *, axes, **kwargs) -> None:
        for i in range(0, len(self.vertices)):
            Figure3D.draw_segment(
                axes=axes,
                start_point=self.vertices[i],
                end_point=self.vertices[(i + 1) % len(self.vertices)],
                color=self.color,
                linestyle=self.linestyle,
            )


def draw3d(
    *objects: Sequence[Figure3D],
    origin=True,
    axes=True,
    width=6,
    save_as: str = None,
    azim=None,
    elev=None,
    xlim=None,
    ylim=None,
    zlim=None,
    xticks=None,
    yticks=None,
    zticks=None,
    depthshade=False,
):
    """Draws the given 3D objects in a Matplotlib plot with the given plot
    configuration.

    Args:
        objects (Sequence[Figure3D]): the list of figures to be displayed in the
            plot.
        origin (bool, optional): whether to show or not the origin of
            coordinates in the plot. By default it is displayed.
        axes (bool, optional): whether to show or not the x-, y-, and
            z-coordinates axes. By default axes are shown.
        width (IntOrFloat): the width of the plot in the screen in inches. You
            can think of it as the canvas width: the larger this number, the
            bigger the plot. Default is 6 which is OK for most 3D drawings.
        save_as (str, optional): path of file to be created with the plot, or
            None if no file is to be created.
        azim (float, optional): The azimuthal angle in degrees rotates the
            camera about the vertical axis corresponding to a right-handed
            rotation.
        elev (float, optional): The elevation angle in degrees rotates the
            camera above the plane pierced by the vertical axis, with a positive
            angle corresponding to a location above that plane.
        xlim (tuple[float, float], optional): The x-axis view limits established
            as a tuple (left, right). If not provided, a sensible limit will be
            established for you. Note that for this parameter to have an effect,
            the ylim, and zlim arguments must also be given.
        ylim (tuple[float, float], optional): The y-axis view limits established
            as a tuple (left, right). If not provided, a sensible limit will be
            established for you. Note that for this parameter to have an effect,
            the xlim, and zlim arguments must also be given.
        zlim (tuple[float, float], optional): The z-axis view limits established
            as a tuple (bottom, up). If not provided, a sensible limit will be
            established for you. Note that for this parameter to have an effect,
            the xlim, and ylim arguments must also be given.
        xticks (Sequence[float], optional): Sets the ticks locations in the
            x-axis. For example, to set the ticks in 0, 1, 2 you would set
            xticks=[0, 1, 2]. If not provided, a sensible limit will be
            established for you. Note that for this parameter to have an effect
            you will have to set the yticks, and zticks as well.
        yticks (Sequence[float], optional): Sets the ticks locations in the
            y-axis. For example, to set the ticks in 0, 1, 2 you would set
            yticks=[0, 1, 2]. If not provided, a sensible limit will be
            established for you. Note that for this parameter to have an effect
            you will have to set the xticks, and zticks as well.
        zticks (Sequence[float], optional): Sets the ticks locations in the
            z-axis. For example, to set the ticks in 0, 1, 2 you would set
            zticks=[0, 1, 2]. If not provided, a sensible limit will be
            established for you. Note that for this parameter to have an effect
            you will have to set the xticks, and yticks as well.
        depthshade (bool, optional): whether to dim the points thar are farthest
            from the view. False by default, which means points are not dimmed.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.view_init(elev=elev, azim=azim)

    all_vectors = [v for obj in objects for v in obj.extract_vectors()]
    if origin:
        all_vectors.append((0, 0, 0))
    xs, ys, zs = zip(*all_vectors)

    max_x, min_x = max(0, *xs), min(0, *xs)
    max_y, min_y = max(0, *ys), min(0, *ys)
    max_z, min_z = max(0, *zs), min(0, *zs)

    x_size = max_x - min_x
    y_size = max_y - min_y
    z_size = max_z - min_z

    padding_x = 0.05 * x_size if x_size else 1
    padding_y = 0.05 * y_size if y_size else 1
    padding_z = 0.05 * z_size if z_size else 1

    plot_x_range = (min(min_x - padding_x, -2), max(max_x + padding_x, 2))
    plot_y_range = (min(min_y - padding_y, -2), max(max_y + padding_y, 2))
    plot_z_range = (min(min_z - padding_z, -2), max(max_z + padding_z, 2))

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    if y_size != 0:
        fig.set_size_inches(width, width * x_size / y_size)

    if axes:
        Figure3D.draw_segment(
            axes=ax,
            start_point=(plot_x_range[0], 0, 0),
            end_point=(plot_x_range[1], 0, 0),
        )
        Figure3D.draw_segment(
            axes=ax,
            start_point=(0, plot_y_range[0], 0),
            end_point=(0, plot_y_range[1], 0),
        )
        Figure3D.draw_segment(
            axes=ax,
            start_point=(0, 0, plot_z_range[0]),
            end_point=(0, 0, plot_z_range[1]),
        )

    if origin:
        ax.scatter([0], [0], [0], color=Colors3D.BLACK.value, marker="x")

    for obj in objects:
        obj.render(axes=ax, depthshade=depthshade)

    if xlim is not None and ylim is not None and zlim is not None:
        plt.xlim(*xlim)
        plt.ylim(*ylim)
        ax.set_zlim(*zlim)

    if xticks is not None and yticks is not None and zticks is not None:
        plt.xticks(xticks)
        plt.yticks(yticks)
        ax.set_zticks(zticks)

    if save_as:
        plt.savefig(save_as)

    plt.show()
