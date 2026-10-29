"""Carrusel PNG conforme a BRIEF.md y ../_comun/BRIEF_MARCA.md."""

from functools import lru_cache

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from .brand import COMMON, PNG_COLORS, ROOT
from .logo import paste_logo

CREAM, INK, BROWN, GREEN, SAGE = (
    PNG_COLORS[key] for key in ("cream", "ink", "brown", "green", "sage")
)
W, H = 1080, 1350
BASES, SLIDES = ROOT / "bases", ROOT / "slides"
TEXT_BOXES = []


@lru_cache(maxsize=100)
def font(size, weight=500, script=False):
    path = COMMON / "fonts" / ("DancingScript.ttf" if script else "Montserrat.ttf")
    f = ImageFont.truetype(str(path), size)
    f.set_variation_by_axes([weight])
    return f


def label(im, value, xy, size, color=INK, weight=500, anchor="lt", script=False):
    draw = ImageDraw.Draw(im)
    f = font(size, weight, script)
    box = draw.textbbox(xy, value, font=f, anchor=anchor)
    assert box[0] >= 70 and box[2] <= W - 70, (value, box)
    assert box[1] >= 70 and box[3] <= H - 70, (value, box)
    TEXT_BOXES.append((value, box))
    draw.text(xy, value, fill=color, font=f, anchor=anchor)


def pill(im, value, y, size=44):
    width = round(font(size, 750).getlength(value)) + 66
    x = (W - width) // 2
    ImageDraw.Draw(im).rounded_rectangle((x, y, x + width, y + 80), 22, fill=GREEN)
    label(im, value, (W // 2, y + 21), size, CREAM, 750, "mt")


def arrow(im, xy, length=95):
    x, y = xy
    draw = ImageDraw.Draw(im)
    draw.line((x, y, x + length, y), fill=GREEN, width=4)
    draw.line(
        (x + length - 19, y - 10, x + length, y, x + length - 19, y + 10),
        fill=GREEN,
        width=4,
    )


def icon(draw, kind, x, y):
    if kind == "cut":
        draw.arc((x + 4, y, x + 42, y + 38), 180, 360, fill=CREAM, width=3)
        draw.ellipse((x + 19, y + 13, x + 25, y + 19), outline=CREAM, width=3)
        for dx, dy in [(5, 12), (10, 5), (21, 0), (33, 4), (40, 12)]:
            draw.line((x + dx, y + dy, x + dx - 3, y + dy - 6), fill=CREAM, width=3)
        draw.line((x, y + 31, x + 48, y + 31), fill=CREAM, width=3)
        draw.rectangle((x, y + 34, x + 48, y + 42), outline=CREAM, width=3)
    elif kind == "edge":
        draw.line(
            (x, y + 10, x + 28, y, x + 51, y + 10, x + 23, y + 23, x, y + 10),
            fill=CREAM,
            width=3,
        )
        draw.line(
            (x, y + 10, x, y + 24, x + 23, y + 38, x + 51, y + 24, x + 51, y + 10),
            fill=CREAM,
            width=3,
        )
        draw.line((x + 23, y + 23, x + 23, y + 38), fill=CREAM, width=3)
    else:
        draw.rectangle((x, y + 4, x + 31, y + 30), outline=CREAM, width=3)
        draw.line(
            (
                x + 31,
                y + 13,
                x + 42,
                y + 13,
                x + 51,
                y + 24,
                x + 51,
                y + 33,
                x + 31,
                y + 33,
            ),
            fill=CREAM,
            width=3,
        )
        for dx in (10, 40):
            draw.ellipse(
                (x + dx - 5, y + 29, x + dx + 5, y + 39),
                fill=GREEN,
                outline=CREAM,
                width=3,
            )
        draw.line((x - 7, y + 13, x + 11, y + 13), fill=CREAM, width=3)


def services(im):
    y = 1170
    draw = ImageDraw.Draw(im)
    draw.line((0, y, W, y), fill=SAGE, width=2)
    draw.rectangle((298, y, W, H), fill=GREEN)
    label(im, "SERVICIOS", (74, y + 59), 27, GREEN, 800)
    label(im, "COMPLEMENTO", (74, y + 94), 21, GREEN, 650)
    for x, kind, words in [
        (329, "cut", ("CORTE A", "MEDIDA")),
        (558, "edge", ("ENCHAPADO",)),
        (793, "truck", ("ENVÍO A", "DOMICILIO")),
    ]:
        icon(draw, kind, x + 76, y + 13)
        for i, word in enumerate(words):
            label(im, word, (x + 102, y + 66 + 25 * i), 21, CREAM, 700, "mt")
    for x in [544, 778]:
        draw.line((x, y + 32, x, y + 116), fill=CREAM, width=1)


def save(im, number):
    assert im.size == (W, H)
    im.convert("RGB").save(SLIDES / f"{number:02d}.png", optimize=True)


def cover():
    im = Image.new("RGB", (W, H), CREAM)
    photo = Image.open(BASES / "01-parota-portada.png").convert("RGB")
    photo = photo.resize((608, 760), Image.Resampling.LANCZOS)
    mask = Image.new("L", photo.size, 0)
    ImageDraw.Draw(mask).rectangle((28, 28, 580, 732), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(18))
    im.paste(photo, (236, 396), mask)
    label(im, "MADERAS FINAS", (540, 100), 100, BROWN, 900, "mt")
    pill(im, "CON CARÁCTER", 232, 48)
    label(im, "Desliza", (733, 336), 56, GREEN, 600, script=True)
    arrow(im, (902, 368), 94)
    paste_logo(im, (842, 992), 164)
    services(im)
    save(im, 1)


def interior(number, filename, name, copy, formats, point, extra=False):
    im = Image.new("RGB", (W, H), CREAM)
    photo = Image.open(BASES / filename).convert("RGB")
    photo = ImageOps.fit(
        photo, (W, 960), Image.Resampling.LANCZOS, centering=(0.5, 0.42)
    )
    im.paste(photo, (0, 0))
    draw = ImageDraw.Draw(im)
    fw = round(font(56, 800).getlength(name))
    draw.rectangle((74, 94, 74 + fw + 52, 190), fill=GREEN)
    label(im, name, (100, 114), 56, CREAM, 800)
    px, py = point
    draw.line((112, 190, 112, py, px, py), fill=CREAM, width=5)
    draw.ellipse((px - 9, py - 9, px + 9, py + 9), fill=CREAM)
    for i, value in enumerate(copy):
        label(im, value, (74, 1000 + i * 55), 38, INK, 500)
    draw.line((74, 1122, 1006, 1122), fill=SAGE, width=2)
    label(im, formats, (74, 1156), 31, GREEN, 750)
    if extra:
        label(im, "También: Parotilla · Albacia · Encino FAS", (74, 1222), 25, INK, 500)
        label(im, "Poplar · Marupa", (74, 1253), 25, INK, 500)
    paste_logo(im, (868, 1140), 138)
    save(im, number)


def closing():
    im = Image.new("RGB", (W, H), CREAM)
    label(im, "¿CUÁL VA EN", (540, 78), 78, BROWN, 900, "mt")
    label(im, "TU PROYECTO?", (540, 165), 78, BROWN, 900, "mt")
    pill(im, "TE ASESORAMOS", 284, 43)
    samples = [
        ("PAROTA", ROOT / "Madera aserrada parota.jpeg", None),
        ("TZALAM", ROOT / "madera tzalam.jpeg", None),
        ("ROSA MORADA", BASES / "04-rosa-morada-puerta.png", (335, 220, 710, 595)),
        ("NOGAL", ROOT / "madera aserrada nogal.jpeg", None),
    ]
    draw = ImageDraw.Draw(im)
    for i, (name, path, crop) in enumerate(samples):
        x, y = 230 + (i % 2) * 360, 400 + (i // 2) * 330
        sample = Image.open(path).convert("RGB")
        if crop:
            sample = sample.crop(crop)
        sample = ImageOps.fit(sample, (260, 260), Image.Resampling.LANCZOS)
        im.paste(sample, (x, y))
        draw.rectangle((x, y + 260, x + 259, y + 313), fill=GREEN)
        label(im, name, (x + 130, y + 276), 24, CREAM, 750, "mt")
    label(im, "Envío sin costo en Aguascalientes", (240, 1093), 32, GREEN, 750)
    paste_logo(im, (74, 1030), 126)
    services(im)
    save(im, 6)


def main():
    TEXT_BOXES.clear()
    SLIDES.mkdir(exist_ok=True)
    cover()
    interior(
        2,
        "02-parota-comedor.png",
        "PAROTA",
        ["Veta amplia y tonos dorados.", "Ideal para mesas y cubiertas."],
        "Aserrada · Triplay · Enchapado",
        (438, 455),
    )
    interior(
        3,
        "03-tzalam-recamara.png",
        "TZALAM",
        ["Tono café con vetas oscuras.", "Ideal para muebles y lambrines."],
        "Aserrada · Triplay",
        (378, 338),
    )
    interior(
        4,
        "04-rosa-morada-puerta.png",
        "ROSA MORADA",
        ["Rojiza y elegante.", "Ideal para puertas y piezas de lujo."],
        "Aserrada · Triplay",
        (443, 400),
    )
    interior(
        5,
        "05-nogal-cocina.png",
        "NOGAL",
        ["Oscuro y sobrio.", "Ideal para cocinas y closets."],
        "Triplay · Enchapado",
        (753, 374),
        extra=True,
    )
    closing()
    preview = Image.new("RGB", (324 * 6, 405), CREAM)
    for i in range(6):
        image = Image.open(SLIDES / f"{i + 1:02d}.png")
        preview.paste(image.resize((324, 405), Image.Resampling.LANCZOS), (324 * i, 0))
    preview.save(ROOT / "preview.png", optimize=True)
    print(
        f"6 PNG de {W} × {H}; preview de 1944 × 405. {len(TEXT_BOXES)} textos dentro de márgenes ≥ 70 px."
    )
