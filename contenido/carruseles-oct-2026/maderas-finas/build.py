# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["pillow==13.0.0"]
# ///
"""Recompone el carrusel desde las bases locales: uv run build.py.

Prioridad editorial: ../_comun/BRIEF.md y CONTENIDO.md.
Las fotos base no llevan letras ni logos. Todo el texto, los indicadores,
los iconos y el logo original se componen aquí con Pillow.
"""

from PIL import Image, ImageDraw, ImageOps

from src.brand import BROWN, CREAM, DARK_GREEN, GREEN, INK, ROOT, SIZE, font
from src.logo import paste_logo

OUT = ROOT / "slides"
BOUNDS = []


def text(canvas, value, x, y, size, color=INK, weight=500, script=False):
    """Coordenada y = parte visible superior, no ascendente de la fuente."""
    draw = ImageDraw.Draw(canvas)
    face = font(size, weight, script)
    box = draw.textbbox((0, 0), value, font=face)
    width, height = box[2] - box[0], box[3] - box[1]
    assert 0 <= x and x + width <= SIZE[0], (value, x, width)
    assert 0 <= y and y + height <= SIZE[1], (value, y, height)
    BOUNDS.append((value, x, y, width, height))
    draw.text((x - box[0], y - box[1]), value, font=face, fill=color)
    return width, height


def centered(canvas, value, y, size, color=INK, weight=500, script=False):
    box = font(size, weight, script).getbbox(value)
    return text(
        canvas,
        value,
        (SIZE[0] - box[2] + box[0]) // 2,
        y,
        size,
        color,
        weight,
        script,
    )


def lines(canvas, values, x, y, size, leading, color=INK, weight=500):
    for index, value in enumerate(values):
        text(canvas, value, x, y + index * leading, size, color, weight)


def photo(path: str, size: tuple[int, int], centering=(0.5, 0.5)):
    with Image.open(ROOT / path) as original:
        return ImageOps.fit(
            ImageOps.exif_transpose(original).convert("RGB"),
            size,
            Image.Resampling.LANCZOS,
            centering=centering,
        )


def pill(canvas, value, xy, width, height, size=34):
    x, y = xy
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((x, y, x + width, y + height), radius=22, fill=GREEN)
    box = font(size, 750).getbbox(value)
    tw, th = box[2] - box[0], box[3] - box[1]
    text(canvas, value, x + (width - tw) // 2, y + (height - th) // 2, size, CREAM, 750)


def arrow(canvas, start, end, color=GREEN, width=4):
    draw = ImageDraw.Draw(canvas)
    x, y = end
    draw.line((start, end), fill=color, width=width)
    draw.line(((x - 16, y - 10), (x, y), (x - 16, y + 10)), fill=color, width=width)


def icon(draw, kind, x, y):
    """Iconos de servicios dibujados con líneas; no son parte del logo."""
    c = CREAM
    if kind == "cut":
        draw.rectangle((x, y + 35, x + 48, y + 41), outline=c, width=3)
        draw.arc((x + 5, y, x + 43, y + 38), 180, 360, fill=c, width=4)
        draw.line((x + 24, y + 4, x + 24, y + 11), fill=c, width=3)
        draw.line((x + 10, y + 9, x + 15, y + 15), fill=c, width=3)
        draw.line((x + 33, y + 15, x + 38, y + 9), fill=c, width=3)
        draw.ellipse((x + 20, y + 23, x + 28, y + 31), fill=c)
    elif kind == "edge":
        draw.polygon(
            ((x, y + 15), (x + 26, y + 5), (x + 51, y + 16), (x + 25, y + 29)),
            outline=c,
            width=3,
        )
        draw.line(
            (x, y + 15, x, y + 29, x + 25, y + 42, x + 51, y + 29, x + 51, y + 16),
            fill=c,
            width=3,
        )
        draw.line((x + 25, y + 29, x + 25, y + 42), fill=c, width=3)
    else:
        draw.rectangle((x, y + 6, x + 32, y + 31), outline=c, width=3)
        draw.line(
            (
                x + 32,
                y + 15,
                x + 43,
                y + 15,
                x + 52,
                y + 25,
                x + 52,
                y + 32,
                x + 32,
                y + 32,
            ),
            fill=c,
            width=3,
        )
        for cx in (12, 42):
            draw.ellipse((x + cx - 5, y + 29, x + cx + 5, y + 39), fill=c)


def service_band(canvas):
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 1200, 1080, 1350), fill=DARK_GREEN)
    draw.rectangle((0, 1200, 258, 1350), fill=CREAM)
    text(canvas, "SERVICIOS", 70, 1252, 25, GREEN, 800)
    text(canvas, "COMPLEMENTO", 70, 1286, 17, GREEN, 650)
    for x, kind, label in (
        (290, "cut", ["CORTE A", "MEDIDA"]),
        (548, "edge", ["ENCHAPADO"]),
        (810, "delivery", ["ENVÍO A", "DOMICILIO"]),
    ):
        icon(draw, kind, x, 1252)
        lines(
            canvas, label, x + 65, 1254 if len(label) == 2 else 1267, 21, 28, CREAM, 700
        )
    for x in (528, 790):
        draw.line((x, 1243, x, 1310), fill=CREAM, width=2)


def label(canvas, value, endpoint, width):
    draw = ImageDraw.Draw(canvas)
    x, y = 70, 84
    draw.rectangle((x, y, x + width, y + 82), fill=GREEN)
    text(canvas, value, x + 24, y + 20, 49, CREAM, 800)
    endx, endy = endpoint
    draw.line(((110, y + 82), (110, endy), (endx, endy)), fill=CREAM, width=4)
    draw.ellipse((endx - 7, endy - 7, endx + 7, endy + 7), fill=CREAM)


def cover():
    canvas = Image.new("RGB", SIZE, CREAM)
    centered(canvas, "MADERAS", 85, 130, BROWN, 900)
    centered(canvas, "FINAS", 225, 130, BROWN, 900)
    pill(canvas, "con carácter", (272, 347), 536, 84, 47)
    text(canvas, "Desliza", 730, 446, 62, GREEN, script=True)
    arrow(canvas, (924, 483), (1008, 483))
    canvas.paste(photo("bases/01-parota-portada-v2.png", (1080, 720)), (0, 510))
    paste_logo(canvas, (850, 1013), 160)
    service_band(canvas)
    return canvas


def material(
    name, filename, description, availability, endpoint, label_width, also=None
):
    canvas = Image.new("RGB", SIZE, CREAM)
    canvas.paste(photo(filename, (1080, 975), centering=(0.5, 0.43)), (0, 0))
    label(canvas, name, endpoint, label_width)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 975, 1080, 1350), fill=CREAM)
    draw.rectangle((70, 1015, 122, 1020), fill=GREEN)
    lines(canvas, description, 70, 1046, 38, 51, INK, 500)
    lines(canvas, availability, 70, 1181, 28, 39, GREEN, 700)
    if also:
        text(canvas, also, 70, 1250, 27, BROWN, 600)
    paste_logo(canvas, (850, 1120), 160)
    return canvas


def swatch(canvas, source, crop, x, name):
    with Image.open(ROOT / source) as original:
        sample = original.convert("RGB")
        if crop:
            sample = sample.crop(crop)
        sample = ImageOps.fit(sample, (208, 208), Image.Resampling.LANCZOS)
    canvas.paste(sample, (x, 478))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((x, 478, x + 207, 685), outline=BROWN, width=2)
    for index, word in enumerate(name.split("\n")):
        f = font(25, 800)
        box = f.getbbox(word)
        text(
            canvas,
            word,
            x + (208 - box[2] + box[0]) // 2,
            713 + index * 33,
            25,
            BROWN,
            800,
        )


def closing():
    canvas = Image.new("RGB", SIZE, CREAM)
    centered(canvas, "¿CUÁL VA EN", 87, 86, BROWN, 900)
    centered(canvas, "TU PROYECTO?", 192, 86, BROWN, 900)
    pill(canvas, "TE ASESORAMOS", (270, 325), 540, 80, 34)
    swatch(canvas, "Madera aserrada parota.jpeg", None, 70, "PAROTA")
    swatch(canvas, "madera tzalam.jpeg", None, 314, "TZALAM")
    # Muestra ilustrativa extraída del render; no existe una foto real de esta especie.
    swatch(
        canvas,
        "bases/04-rosa-morada-puerta.png",
        (340, 200, 740, 600),
        558,
        "ROSA\nMORADA",
    )
    swatch(canvas, "madera aserrada nogal.jpeg", None, 802, "NOGAL")
    centered(canvas, "Envío sin costo", 826, 42, GREEN, 800)
    centered(canvas, "en Aguascalientes", 883, 34, GREEN, 650)
    text(canvas, "Escríbenos y cotiza", 70, 999, 58, GREEN, script=True)
    arrow(canvas, (594, 1043), (716, 1043))
    paste_logo(canvas, (824, 967), 186)
    text(canvas, "Harold R. Pape 209, Galerías, Ags.", 70, 1136, 27, INK, 500)
    service_band(canvas)
    return canvas


def build():
    OUT.mkdir(exist_ok=True)
    slides = [
        cover(),
        material(
            "PAROTA",
            "bases/02-parota-comedor.png",
            ["Veta amplia y cálida,", "ideal para mesas y cubiertas"],
            ["Madera aserrada (MR y Selecta)", "y triplay"],
            (435, 440),
            293,
        ),
        material(
            "TZALAM",
            "bases/03-tzalam-recamara.png",
            ["Tono café rosado y veta fina,", "para muebles y cocinas"],
            ["Madera aserrada (MR) y triplay"],
            (430, 340),
            302,
        ),
        material(
            "ROSA MORADA",
            "bases/04-rosa-morada-puerta.png",
            ["Color profundo para piezas", "que se notan"],
            ["Madera aserrada (MR) y triplay"],
            (540, 348),
            495,
        ),
        material(
            "NOGAL",
            "bases/05-nogal-cocina.png",
            ["Elegancia oscura", "para interiores"],
            ["Triplay y enchapado"],
            (750, 365),
            267,
            also="También: parotilla, encino y poplar",
        ),
        closing(),
    ]
    for index, slide in enumerate(slides, 1):
        assert slide.size == SIZE
        slide.save(OUT / f"{index:02}.jpg", quality=96, subsampling=0, dpi=(72, 72))
    # Una fila, en orden de publicación. Sin etiquetas ajenas al arte final.
    sheet = Image.new("RGB", (360 * 6, 450), CREAM)
    for index, slide in enumerate(slides):
        sheet.paste(
            slide.resize((360, 450), Image.Resampling.LANCZOS), (360 * index, 0)
        )
    sheet.save(ROOT / "hoja.jpg", quality=95, subsampling=0)
    print(
        f"Listo: {len(slides)} JPG de 1080×1350 y hoja.jpg; {len(BOUNDS)} textos dentro del lienzo."
    )


if __name__ == "__main__":
    import sys

    if "--png" in sys.argv:
        from src.carousel_png import main

        main()
    else:
        build()
