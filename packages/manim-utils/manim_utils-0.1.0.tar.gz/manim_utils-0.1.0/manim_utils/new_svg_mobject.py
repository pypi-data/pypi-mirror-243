from manim import SVGMobject, config
from pathlib import Path
import requests
from uuid import uuid4


class NewSVGMobject(SVGMobject):
    def __init__(
        self,
        filename: str = None,
        string: str = None,
        url: str = None,
        should_center: bool = True,
        height: float | None = 2,
        width: float | None = None, color: str | None = None,
        opacity: float | None = None,
        fill_color: str | None = None,
        fill_opacity: float | None = None,
        stroke_color: str | None = None,
        stroke_opacity: float | None = None,
        stroke_width: float | None = None,
        svg_default: dict | None = None,
        path_string_config: dict | None = None,
        use_svg_cache: bool = True,
        **kwargs
    ):
        assert any([filename, string, url]
                   ), "Must specify exactly one of filename, string, or url"
        if filename is not None:
            file_name = filename
        elif string is not None:
            media_dir = Path(config.media_dir)
            if not media_dir.exists():
                media_dir.mkdir()
            if not (media_dir / "svg_cache").exists():
                (media_dir / "svg_cache").mkdir()
            file_name = media_dir / "svg_cache" / f"{uuid4()}.svg"
            with open(file_name, "w") as f:
                f.write(string)
        else:
            content = requests.get(url).text
            media_dir = Path(config.media_dir)
            if not media_dir.exists():
                media_dir.mkdir()
            if not (media_dir / "svg_cache").exists():
                (media_dir / "svg_cache").mkdir()
            file_name = media_dir / "svg_cache" / f"{uuid4()}.svg"
            with open(file_name, "w") as f:
                f.write(content)
        super().__init__(
            file_name,
            should_center,
            height,
            width,
            color,
            opacity,
            fill_color,
            fill_opacity,
            stroke_color,
            stroke_opacity,
            stroke_width,
            svg_default,
            path_string_config,
            use_svg_cache,
            **kwargs
        )


SVGMobject = NewSVGMobject
