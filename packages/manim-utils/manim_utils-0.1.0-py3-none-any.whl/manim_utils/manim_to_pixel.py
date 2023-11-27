from manim import config
import numpy as np


def manim_to_pixel(manim_coord: np.ndarray):
    manim_coord += np.array([config.frame_x_radius, -config.frame_y_radius, 0])
    manim_coord *= np.array([1, -1, 1])
    manim_coord *= config.pixel_height / config.frame_height
    manim_coord = manim_coord.astype(int)
    manim_coord = manim_coord[:2]
    return manim_coord
