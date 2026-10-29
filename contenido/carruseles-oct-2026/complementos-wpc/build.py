# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow==13.0.0"]
# ///

"""Compone seis slides con Pillow a partir de las bases de image_gen.

Ejecutar: uv run build.py
"""

import math
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont, ImageOps

from src.brand import (
    CREAM,
    DARK_GREEN,
    GREEN,
    HEIGHT,
    INK,
    MONTSERRAT,
    ROOT,
    SAGE,
    SCRIPT,
    WIDTH,
    WOOD,
)
from src.logo import paste_logo

OUT = ROOT / "slides"
OUT.mkdir(exist_ok=True)


@lru_cache(maxsize=128)
def font(size, weight=700, script=False):
    f = ImageFont.truetype(str(SCRIPT if script else MONTSERRAT), size)
    f.set_variation_by_axes([weight])
    return f


def new():
    return Image.new("RGB", (WIDTH, HEIGHT), CREAM)


def text(im, xy, value, size, color=INK, weight=500, max_width=None, script=False):
    x, y = xy
    f = font(size, weight, script)
    if max_width is not None:
        while f.getlength(value) > max_width:
            size -= 1
            f = font(size, weight, script)
    box = ImageDraw.Draw(im).textbbox(xy, value, font=f, anchor="lt")
    if box[0] < 70:
        x += 70 - box[0]
        xy = (x, y)
        box = ImageDraw.Draw(im).textbbox(xy, value, font=f, anchor="lt")
    assert box[0] >= 70 and box[2] <= WIDTH - 70, (value, box)
    assert box[1] >= 70 and box[3] <= HEIGHT - 70, (value, box)
    ImageDraw.Draw(im).text(xy, value, font=f, fill=color, anchor="lt")
    return box


def centered(im, y, value, size, color=WOOD, weight=900, max_width=940):
    while font(size, weight).getlength(value) > max_width:
        size -= 1
    x = (WIDTH - font(size, weight).getlength(value)) / 2
    return text(im, (x, y), value, size, color, weight)


def photo(im, filename, box, centering=(0.5, 0.5)):
    x, y, w, h = box
    source = Image.open(ROOT / "bases" / filename).convert("RGB")
    source = ImageOps.fit(source, (w, h), Image.Resampling.LANCZOS, centering=centering)
    im.paste(source, (x, y))


def pill(im, box, value, size):
    x, y, w, h = box
    ImageDraw.Draw(im).rounded_rectangle((x, y, x + w, y + h), radius=25, fill=GREEN)
    f = font(size, 750)
    while f.getlength(value) > w - 36:
        size -= 1
        f = font(size, 750)
    bbox = f.getbbox(value)
    text(
        im,
        (x + (w - f.getlength(value)) / 2, y + (h - bbox[3] + bbox[1]) / 2),
        value,
        size,
        CREAM,
        750,
    )


def label(im, xy, value, size=30):
    x, y = xy
    w = math.ceil(font(size, 750).getlength(value)) + 36
    h = size + 30
    ImageDraw.Draw(im).rectangle((x, y, x + w, y + h), fill=GREEN)
    text(im, (x + 18, y + 15), value, size, CREAM, 750)
    return x, y, w, h


def guide(im, points):
    d = ImageDraw.Draw(im)
    d.line(points, fill=CREAM, width=5, joint="curve")
    x, y = points[-1]
    d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=CREAM)


def arrow(im, start, end, color=GREEN):
    x, y = end
    d = ImageDraw.Draw(im)
    d.line([start, end], fill=color, width=4)
    d.line([(x - 18, y - 11), (x, y), (x - 18, y + 11)], fill=color, width=4)


def icon(im, name, cx, cy):
    """Iconos de línea propios; no son parte del logotipo."""
    d = ImageDraw.Draw(im)
    c = CREAM
    if name == "saw":
        pts = []
        for i in range(48):
            a = i * math.tau / 48
            r = 21 if i % 2 else 25
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
        d.polygon(pts, outline=c, width=2)
        d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), outline=c, width=3)
        d.line((cx - 31, cy + 26, cx + 31, cy + 26), fill=c, width=3)
    elif name == "board":
        d.polygon(
            [(cx - 32, cy - 9), (cx + 8, cy - 23), (cx + 33, cy - 9), (cx - 8, cy + 7)],
            outline=c,
            width=3,
        )
        d.line(
            [
                (cx - 32, cy - 9),
                (cx - 32, cy + 7),
                (cx - 8, cy + 22),
                (cx + 33, cy + 6),
                (cx + 33, cy - 9),
            ],
            fill=c,
            width=3,
        )
        d.line((cx - 8, cy + 7, cx - 8, cy + 22), fill=c, width=3)
    elif name == "truck":
        d.rectangle((cx - 32, cy - 19, cx + 6, cy + 15), outline=c, width=3)
        d.line(
            [
                (cx + 6, cy - 11),
                (cx + 22, cy - 11),
                (cx + 33, cy + 1),
                (cx + 33, cy + 15),
                (cx + 6, cy + 15),
            ],
            fill=c,
            width=3,
        )
        for dx in (-19, 21):
            d.ellipse(
                (cx + dx - 7, cy + 9, cx + dx + 7, cy + 23),
                fill=DARK_GREEN,
                outline=c,
                width=3,
            )


def services(im):
    d = ImageDraw.Draw(im)
    d.rectangle((0, 1185, 1079, 1349), fill=CREAM)
    d.rectangle((310, 1185, 1079, 1349), fill=DARK_GREEN)
    text(im, (70, 1230), "SERVICIOS", 26, GREEN, 800)
    text(im, (70, 1266), "COMPLEMENTO", 17, GREEN, 700)
    cols = [
        (430, "saw", "CORTE A", "MEDIDA"),
        (665, "board", "ENCHAPADO", ""),
        (900, "truck", "ENVÍO A", "DOMICILIO"),
    ]
    for cx, name, first, second in cols:
        icon(im, name, cx, 1210)
        if second:
            for yy, line in [(1240, first), (1263, second)]:
                f = font(20, 750)
                text(im, (cx - f.getlength(line) / 2, yy), line, 20, CREAM, 750)
        else:
            f = font(20, 750)
            text(im, (cx - f.getlength(first) / 2, 1263), first, 20, CREAM, 750)
    for x in (548, 782):
        d.line((x, 1210, x, 1277), fill=CREAM, width=1)


def footer(im, page):
    d = ImageDraw.Draw(im)
    d.line((70, 1210, 1010, 1210), fill=SAGE, width=2)
    text(im, (70, 1245), "TABLEROS BONATERRA", 23, GREEN, 750)
    value = f"{page:02d} / 06"
    text(im, (1010 - font(23, 600).getlength(value), 1245), value, 23, GREEN, 600)


def save(im, number):
    im.save(OUT / f"{number:02d}.png", optimize=True)
    im.save(OUT / f"{number:02d}.jpg", quality=96, subsampling=0, optimize=True)


def cover():
    im = new()
    centered(im, 76, "¿YA TIENES TU", 83)
    centered(im, 174, "WPC?", 188)
    pill(im, (90, 367, 900, 73), "NO OLVIDES LOS COMPLEMENTOS", 35)
    text(im, (690, 465), "Desliza", 48, GREEN, 650, script=True)
    arrow(im, (865, 493), (980, 493))
    photo(im, "01-muro-terminado.png", (0, 535, 1080, 650))
    paste_logo(im, (831, 951), 179)
    services(im)
    save(im, 1)


def structure():
    im = new()
    text(im, (70, 105), "BASTIDOR WPC", 88, WOOD, 900, max_width=940)
    text(im, (70, 232), "La estructura donde se fija tu panel", 41, max_width=940)
    photo(im, "02-bastidor.png", (0, 388, 1080, 790))
    label(im, (661, 453), "BASTIDOR", 31)
    guide(im, [(705, 513), (705, 662), (840, 662)])
    footer(im, 2)
    save(im, 2)


def clips():
    im = new()
    text(im, (70, 105), "STARTER CLIP", 84, WOOD, 900, max_width=940)
    text(im, (70, 205), "+ PLASTIC CAPS", 77, WOOD, 900, max_width=940)
    photo(im, "03-starter-clip.png", (70, 368, 456, 484), centering=(0.52, 0.55))
    photo(im, "04-plastic-caps-v2.png", (554, 368, 456, 484))
    label(im, (90, 390), "STARTER CLIP", 27)
    label(im, (574, 390), "PLASTIC CAPS", 27)
    for x, lines in [
        (70, ["Arranca la instalación", "derecha"]),
        (554, ["Tapan los extremos", "del stud o viga"]),
    ]:
        for i, line in enumerate(lines):
            text(im, (x, 900 + i * 51), line, 35, max_width=456)
    footer(im, 3)
    save(im, 3)


def corners():
    im = new()
    text(im, (70, 105), "ESQUINEROS", 96, WOOD, 900, max_width=940)
    pill(im, (70, 235, 230, 76), "WPC", 48)
    text(im, (70, 355), "Remates limpios en cada esquina", 41, max_width=940)
    text(im, (70, 412), "Interior y exterior", 36, GREEN, 600)
    photo(im, "05-esquina-exterior.png", (70, 513, 456, 643))
    photo(im, "06-esquina-interior.png", (554, 513, 456, 643))
    label(im, (90, 537), "EXTERIOR", 28)
    label(im, (574, 537), "INTERIOR", 28)
    guide(im, [(166, 595), (166, 737), (306, 737)])
    guide(im, [(650, 595), (650, 737), (781, 737)])
    footer(im, 4)
    save(im, 4)


def edging():
    im = new()
    text(im, (70, 105), "WPC STUD", 84, WOOD, 900)
    photo(im, "08-wpc-stud.png", (70, 235, 500, 365))
    text(im, (620, 256), "MEDIDAS", 27, GREEN, 750)
    text(im, (620, 325), "6 × 4.2 cm", 41, weight=700)
    text(im, (620, 397), "10 × 5 cm", 41, weight=700)
    text(im, (620, 499), "Largo: 2.9 m", 34, GREEN, 600)
    ImageDraw.Draw(im).line((70, 655, 1010, 655), fill=SAGE, width=2)
    text(im, (70, 710), "CUBRECANTOS", 78, WOOD, 900, max_width=940)
    photo(im, "07-cubrecantos.png", (70, 840, 500, 330))
    text(im, (620, 910), "Cantos limpios", 35, max_width=390)
    text(im, (620, 966), "en tus tableros", 35, max_width=390)
    footer(im, 5)
    save(im, 5)


def closing():
    im = new()
    centered(im, 96, "PIDE TODO", 112)
    pill(im, (170, 250, 740, 89), "EN UN SOLO LUGAR", 46)
    photo(im, "01-muro-terminado.png", (70, 386, 940, 342), centering=(0.45, 0.4))
    text(im, (70, 790), "ASESORÍA", 46, WOOD, 850)
    text(im, (70, 850), "PERSONALIZADA", 38, WOOD, 850)
    text(im, (70, 932), "Diseños especiales", 35, weight=500)
    text(im, (70, 983), "bajo pedido.", 35, weight=500)
    paste_logo(im, (793, 790), 217)
    text(im, (70, 1070), "Escríbenos y cotiza", 48, GREEN, 750)
    text(im, (70, 1142), "Harold R. Pape 209, Galerías, Ags.", 27, GREEN, 500)
    services(im)
    save(im, 6)


def preview():
    tile_w, tile_h = 324, 405
    strip = Image.new("RGB", (tile_w * 6, tile_h), CREAM)
    for i in range(6):
        slide = Image.open(OUT / f"{i + 1:02d}.png")
        slide = slide.resize((tile_w, tile_h), Image.Resampling.LANCZOS)
        strip.paste(slide, (i * tile_w, 0))
    strip.save(ROOT / "preview.png", optimize=True)
    sheet = Image.new("RGB", (540 * 6, 675), CREAM)
    for i in range(6):
        with Image.open(OUT / f"{i + 1:02d}.jpg") as slide:
            sheet.paste(
                slide.resize((540, 675), Image.Resampling.LANCZOS), (i * 540, 0)
            )
    sheet.save(ROOT / "hoja.jpg", quality=95, subsampling=0, optimize=True)


if __name__ == "__main__":
    cover()
    structure()
    clips()
    corners()
    edging()
    closing()
    preview()
    print("6 JPG de 1080 × 1350, hoja.jpg y copias PNG generados.")
