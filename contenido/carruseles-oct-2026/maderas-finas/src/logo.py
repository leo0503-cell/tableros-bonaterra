"""Colocación del PNG oficial, sin redibujarlo ni modificar su color."""

from PIL import Image

from .brand import COMMON


def paste_logo(canvas: Image.Image, xy: tuple[int, int], size: int):
    with Image.open(COMMON / "logo-circular.png") as original:
        logo = original.convert("RGBA")
    logo.thumbnail((size, size), Image.Resampling.LANCZOS)
    canvas.paste(logo, xy, logo)
