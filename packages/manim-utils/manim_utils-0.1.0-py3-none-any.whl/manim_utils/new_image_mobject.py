from manim import ImageMobject
from manim.constants import DEFAULT_QUALITY, QUALITIES
from PIL import Image
import numpy as np
import requests


class NewImageMobject(ImageMobject):
    def __init__(
        self,
        filename: str = None,
        array: np.ndarray = None,
        url: str = None,
        scale_to_resolution: int = QUALITIES[DEFAULT_QUALITY]["pixel_height"],
        invert=False,
        image_mode="RGBA",
        **kwargs
    ):
        assert any([filename, array, url]
                   ), "Must specify exactly one of filename, array, or url"
        if filename is not None:
            filename_or_array = filename
        elif array is not None:
            filename_or_array = array
        else:
            filename_or_array = np.array(Image.open(
                requests.get(url, stream=True).raw))
        super().__init__(filename_or_array, scale_to_resolution, invert, image_mode, **kwargs)


ImageMobject = NewImageMobject
