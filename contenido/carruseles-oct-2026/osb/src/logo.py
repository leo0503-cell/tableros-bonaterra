from PIL import Image

from .brand import COMMON


def paste_logo(canvas, xy, size):
    """Pega el archivo oficial completo, sin redibujarlo ni deformarlo."""
    logo = Image.open(COMMON / "logo-circular.png").convert("RGBA")
    logo.thumbnail((size, size), Image.Resampling.LANCZOS)
    canvas.paste(logo, xy, logo)
