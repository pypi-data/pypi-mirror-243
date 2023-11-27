from manim import (
    CoordinateSystem,
    VGroup,
    Dot,
    ParsableManimColor,
    Restore,
    RIGHT,
    UP,
    WHITE,
    DL,
    config
)
from manim_utils.new_table import Table
from typing import Sequence, Callable

try:
    import pandas as pd
except ImportError:
    pd = None


class ScatterPlot(VGroup):
    def __init__(
        self,
        x_values: Sequence[float],
        y_values: Sequence[float],
        axes: CoordinateSystem | None = None,
        color_palette: Callable[[float, float],
                                ParsableManimColor] | None = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.axes = axes
        self.x_values = x_values
        self.y_values = y_values
        self.color_palette = color_palette or (lambda x, y: WHITE)
        self._setup()

    def _setup(self):
        if self.axes is None:
            self.add(*[Dot(x*RIGHT + y*UP).set_color(self.color_palette(x, y))
                       for x, y in zip(self.x_values, self.y_values)])
            self.center()
            if self.width > config.frame_width - 2:
                self.scale_to_fit_width(config.frame_width - 2)
            if self.height > config.frame_height - 1:
                self.scale_to_fit_height(config.frame_height - 1)
            for dot in self:
                dot.scale_to_fit_height(0.16)
            return
        self.add(*[Dot(self.axes.c2p(x, y)).set_color(self.color_palette(x, y))
                   for x, y in zip(self.x_values, self.y_values)])

    if pd is not None:
        @classmethod
        def from_dataframe(
            cls,
            dataframe: pd.DataFrame,
            x_column: str | int,
            y_column: str | int,
            axes: CoordinateSystem | None = None,
            color_palette: Callable[[float, float],
                                    ParsableManimColor] | None = None,
            **kwargs
        ):
            new_df = dataframe[[x_column, y_column]].dropna()
            x_values = new_df[x_column].values
            y_values = new_df[y_column].values
            return cls(
                x_values,
                y_values,
                axes=axes,
                color_palette=color_palette,
                **kwargs
            )

    @classmethod
    def from_manim_table(
        cls,
        table: Table,
        x_column: int,
        y_column: int,
        axes: CoordinateSystem | None = None,
        color_palette: Callable[[float, float],
                                ParsableManimColor] | None = None,
        **kwargs
    ):
        return cls(
            [float(el) for el in table.get_column(x_column)],
            [float(el) for el in table.get_column(y_column)],
            axes=axes,
            color_palette=color_palette,
            **kwargs
        )

    def create(self, **kwargs):
        self.save_state()
        if self.axes:
            for dot in self:
                dot.move_to(self.axes.get_origin())
            return Restore(self, **kwargs)
        dl_corner = self.get_corner(DL)
        for dot in self:
            dot.move_to(dl_corner)
        return Restore(self, **kwargs)
