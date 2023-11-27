try:
    import matplotlib.pyplot as plt
    from matplotlib.collections import PathCollection
except ImportError:
    plt = None

from manim import ParsableManimColor, Axes, CoordinateSystem, config
from manim_utils.scatter_plot import ScatterPlot
from typing import Callable


if plt is not None:
    def scatter_matplotlib_to_manim(
        scatter: PathCollection,
        axes: plt.Axes | None = None,
        color_palette: Callable[[float, float],
                                ParsableManimColor] | None = None,
        manim_axes_class: type[CoordinateSystem] | None = Axes,
        x_length: float | None = round(config.frame_width) - 2,
        y_length: float | None = round(config.frame_height) - 2,
        add_coordinates: bool = True,
        **kwargs
    ) -> ScatterPlot:
        if axes is None:
            axes: plt.Axes = plt.gca()
        if manim_axes_class is None:
            manim_axes = None
        else:
            manim_axes = manim_axes_class(
                x_range=(axes.get_xlim()[0], axes.get_xlim()[
                         1], axes.get_xticks()[1] - axes.get_xticks()[0]),
                y_range=(axes.get_ylim()[0], axes.get_ylim()[
                         1], axes.get_yticks()[1] - axes.get_yticks()[0]),
                x_length=x_length,
                y_length=y_length,
            )
            if add_coordinates:
                manim_axes.add_coordinates()
        return (
            ScatterPlot(
                x_values=scatter.get_offsets()[:, 0],
                y_values=scatter.get_offsets()[:, 1],
                axes=manim_axes,
                color_palette=color_palette,
                **kwargs
            ),
            manim_axes
        )
else:
    scatter_matplotlib_to_manim = None
