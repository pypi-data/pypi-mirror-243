from typing import Callable, Iterable
from manim import Table, config
from manim.mobject.text.text_mobject import Paragraph
from manim.mobject.types.vectorized_mobject import VMobject
from manim.utils.color import BLACK, ParsableManimColor

try:
    import pandas as pd
except ImportError:
    pd = None


class NewTable(Table):
    def __init__(
        self,
        table: Iterable[Iterable[float | str | VMobject]],
        row_labels: Iterable[VMobject] | None = None,
        col_labels: Iterable[VMobject] | None = None,
        top_left_entry: VMobject | None = None,
        v_buff: float = 0.8, h_buff: float = 1.3,
        include_outer_lines: bool = False,
        add_background_rectangles_to_entries: bool = False,
        entries_background_color: ParsableManimColor = BLACK,
        include_background_rectangle: bool = False,
        background_rectangle_color: ParsableManimColor = BLACK,
        element_to_mobject: Callable[[
            float | str | VMobject], VMobject] = Paragraph,
        element_to_mobject_config: dict = {},
        arrange_in_grid_config: dict = {},
        line_config: dict = {},
        **kwargs
    ):
        super().__init__(table, row_labels, col_labels, top_left_entry, v_buff, h_buff, include_outer_lines, add_background_rectangles_to_entries, entries_background_color,
                         include_background_rectangle, background_rectangle_color, element_to_mobject, element_to_mobject_config, arrange_in_grid_config, line_config, **kwargs)
        self.table = table

    def get_column(self, index: int):
        return [row[index] for row in self.table]

    if pd is not None:
        @classmethod
        def from_dataframe(
            cls,
            dataframe: pd.DataFrame,
            scale_to_fit_screen: bool = True,
            include_index: bool = False,
            include_column_labels: bool = True,
            nan_string: str = "NaN",
            **kwargs
        ):
            result = cls(
                [[nan_string if pd.isna(x) else str(x) for x in row]
                 for row in dataframe.values],
                row_labels=list(map(Paragraph, [str(el) for el in dataframe.index.tolist()]
                                    )) if include_index else None,
                col_labels=list(map(Paragraph, dataframe.columns.tolist()
                                    )) if include_column_labels else None,
                **kwargs
            )
            if scale_to_fit_screen:
                if result.width > config.frame_width - 2:
                    result.scale_to_fit_width(config.frame_width - 2)
                if result.height > config.frame_height - 1:
                    result.scale_to_fit_height(config.frame_height - 1)
            return result


Table = NewTable
