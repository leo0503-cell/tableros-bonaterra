"""Identidad compartida; los archivos originales sólo se leen."""

from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).resolve().parents[1]
COMMON = ROOT.parent / "_comun"
CREAM = "#F8F0DE"
GREEN = "#3E602D"
DARK_GREEN = "#637356"
BROWN = "#6A3521"
INK = "#231F20"
SAGE = "#949E79"
SIZE = (1080, 1350)

# Paleta del BRIEF_MARCA.md para la exportación PNG.
PNG_COLORS = {
    "cream": "#F8F0DE",
    "ink": "#231F20",
    "brown": "#6A3521",
    "green": "#3E602D",
    "sage": "#85966F",
}


@lru_cache(maxsize=80)
def font(size: int, weight: int = 500, script: bool = False):
    filename = "DancingScript.ttf" if script else "Montserrat.ttf"
    face = ImageFont.truetype(str(COMMON / "fonts" / filename), size)
    face.set_variation_by_axes([700 if script else weight])
    return face
