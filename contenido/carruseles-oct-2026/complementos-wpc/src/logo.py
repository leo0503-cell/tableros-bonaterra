"""Pega el logo oficial, sin redibujarlo ni alterar sus proporciones."""

from PIL import Image

from src.brand import COMMON


def paste_logo(canvas, xy, size):
    logo = Image.open(COMMON / "logo-circular.png").convert("RGBA")
    logo.thumbnail((size, size), Image.Resampling.LANCZOS)
    canvas.paste(logo, xy, logo)
