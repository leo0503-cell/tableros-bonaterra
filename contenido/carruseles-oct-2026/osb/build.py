# /// script
# requires-python = ">=3.12"
# dependencies = ["Pillow==13.0.0"]
# ///
"""Reconstruye las seis láminas usando las fotos base guardadas en assets/."""

import json
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from src.brand import (
    BROWN,
    CREAM,
    DARK_GREEN,
    FONT,
    GREEN,
    INK,
    ROOT,
    SAGE,
    SCRIPT,
)
from src.logo import paste_logo

W, H = 1080, 1350
SLIDES = ROOT / "slides"
RECORD = []


@lru_cache(maxsize=128)
def font(size, weight=500, script=False):
    f = ImageFont.truetype(str(SCRIPT if script else FONT), size)
    f.set_variation_by_axes([weight])
    return f


def text(im, xy, value, size, color=INK, weight=500, script=False):
    f = font(size, weight, script)
    d = ImageDraw.Draw(im)
    box = d.textbbox(xy, value, font=f, anchor="lt")
    assert box[0] >= 0 and box[1] >= 0 and box[2] <= W and box[3] <= H, (
        value,
        box,
    )
    d.text(xy, value, font=f, fill=color, anchor="lt")
    RECORD.append({"text": value, "bounds": box})
    return box


def lines(im, xy, values, size, color=INK, weight=500, gap=12):
    x, y = xy
    for value in values:
        text(im, (x, y), value, size, color, weight)
        y += size + gap
    return y


def pill(im, xy, label, size=27, pad=25, height=64):
    x, y = xy
    width = round(font(size, 700).getlength(label)) + 2 * pad
    ImageDraw.Draw(im).rounded_rectangle(
        (x, y, x + width, y + height), radius=18, fill=GREEN
    )
    text(im, (x + pad, y + (height - size) // 2 - 1), label, size, CREAM, 700)


def photo(im, source, box, centering=(0.5, 0.5)):
    x, y, width, height = box
    with Image.open(ROOT / source) as source_im:
        crop = ImageOps.fit(
            source_im.convert("RGB"),
            (width, height),
            Image.Resampling.LANCZOS,
            centering=centering,
        )
    im.paste(crop, (x, y))


def base(number, category):
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    text(im, (74, 72), "TABLEROS BONATERRA", 22, GREEN, 700)
    d.line((74, 119, 1006, 119), fill=SAGE, width=2)
    if category:
        text(im, (74, 153), category, 23, GREEN, 700)
    return im


def small_footer(im):
    d = ImageDraw.Draw(im)
    d.line((74, 1235, 906, 1235), fill=SAGE, width=2)
    text(im, (74, 1260), "MADERA PARA TUS PROYECTOS", 20, GREEN, 600)
    paste_logo(im, (924, 1220), 82)


def arrow(im, x, y, width=100):
    d = ImageDraw.Draw(im)
    d.line((x, y, x + width, y), fill=GREEN, width=4)
    d.line(
        (x + width - 19, y - 13, x + width, y, x + width - 19, y + 13),
        fill=GREEN,
        width=4,
    )


def check(im, x, y, cross=False):
    d = ImageDraw.Draw(im)
    d.ellipse((x, y, x + 38, y + 38), outline=BROWN if cross else GREEN, width=2)
    if cross:
        d.line((x + 12, y + 12, x + 26, y + 26), fill=BROWN, width=3)
        d.line((x + 26, y + 12, x + 12, y + 26), fill=BROWN, width=3)
    else:
        d.line((x + 9, y + 20, x + 17, y + 27, x + 30, y + 12), fill=GREEN, width=4)


def service_icon(d, x, y, kind):
    c = CREAM
    if kind == "cut":
        d.arc((x + 2, y, x + 40, y + 38), 180, 360, fill=c, width=3)
        d.line((x, y + 24, x + 44, y + 24), fill=c, width=3)
        d.rectangle((x, y + 31, x + 44, y + 38), outline=c, width=2)
        for dx in (7, 16, 25, 34):
            d.line((x + dx, y + 2, x + dx + 3, y - 3), fill=c, width=2)
    elif kind == "edge":
        d.polygon(
            [(x, y + 12), (x + 29, y), (x + 47, y + 10), (x + 18, y + 23)],
            outline=c,
            width=2,
        )
        d.line(
            (x, y + 12, x, y + 27, x + 18, y + 38, x + 47, y + 24, x + 47, y + 10),
            fill=c,
            width=2,
        )
        d.line((x + 18, y + 23, x + 18, y + 38), fill=c, width=2)
    else:
        d.rectangle((x, y + 4, x + 27, y + 31), outline=c, width=2)
        d.line(
            (
                x + 27,
                y + 12,
                x + 39,
                y + 12,
                x + 48,
                y + 24,
                x + 48,
                y + 31,
                x + 27,
                y + 31,
            ),
            fill=c,
            width=2,
        )
        for dx in (10, 39):
            d.ellipse(
                (x + dx - 5, y + 27, x + dx + 5, y + 37),
                fill=DARK_GREEN,
                outline=c,
                width=2,
            )


def services(im):
    d = ImageDraw.Draw(im)
    d.rectangle((0, 1208, W, H), fill=DARK_GREEN)
    d.rectangle((0, 1208, 284, H), fill=CREAM)
    lines(im, (74, 1248), ["SERVICIOS", "COMPLEMENTO"], 22, GREEN, 700, 7)
    for x, kind, label in (
        (310, "cut", ["CORTE A", "MEDIDA"]),
        (558, "edge", ["ENCHAPADO"]),
        (790, "truck", ["ENVÍO A", "DOMICILIO"]),
    ):
        service_icon(d, x, 1255, kind)
        lines(im, (x + 59, 1251 if len(label) == 2 else 1265), label, 21, CREAM, 700, 6)


def save(im, n):
    assert im.size == (W, H)
    im.save(SLIDES / f"{n:02d}.jpg", quality=96, subsampling=0, dpi=(72, 72))
    im.save(SLIDES / f"{n:02d}.png")
    return im


def cover():
    im = base(1, None)
    text(im, (74, 164), "¿YA CONOCES EL", 68, BROWN, 800)
    text(im, (64, 253), "OSB?", 231, BROWN, 900)
    pill(im, (74, 492), "TABLERO DE INGENIERÍA", 30, height=70)
    text(im, (695, 512), "Desliza", 51, GREEN, 600, True)
    arrow(im, 884, 542, 117)
    shadow = Image.new("RGBA", im.size)
    ImageDraw.Draw(shadow).rectangle((91, 616, 1005, 1127), fill=(35, 31, 32, 65))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    im.paste(shadow, (0, 0), shadow)
    photo(im, "osb americana.png", (74, 596, 932, 510))
    d = ImageDraw.Draw(im)
    d.rectangle((74, 1106, 1006, 1118), fill=BROWN)
    paste_logo(im, (846, 998), 142)
    services(im)
    return save(im, 1)


def what():
    im = base(2, "CONOCE EL MATERIAL")
    text(im, (74, 209), "¿QUÉ ES?", 99, BROWN, 900)
    photo(im, "osb asiatica.png", (74, 350, 932, 460))
    pill(im, (102, 738), "OSB", 27, height=57)
    lines(
        im,
        (74, 861),
        [
            "Hojuelas de madera orientadas",
            "en capas cruzadas y prensadas",
            "con resina: resistente y estable.",
        ],
        43,
        INK,
        500,
        18,
    )
    text(im, (74, 1110), "Conoce su textura", 56, GREEN, 600, True)
    small_footer(im)
    return save(im, 2)


def uses():
    im = base(3, None)
    text(im, (74, 169), "PARA QUÉ SÍ", 91, GREEN, 900)
    photo(im, "assets/obra-osb.png", (74, 303, 932, 478), (0.5, 0.48))
    pill(im, (98, 688), "MUROS, ENTREPISOS Y TECHOS", 23, pad=20, height=59)
    rows = [
        (829, ["Muros y", "divisiones"]),
        (918, ["Bases de entrepiso", "y techo"]),
        (1007, ["Tarimas y embalaje"]),
        (1096, ["Muebles de estilo", "industrial"]),
    ]
    for y, words in rows:
        check(im, 74, y + 1)
        lines(im, (130, y), words, 31, INK, 500, 6)
    photo(im, "assets/mueble-osb.png", (620, 829, 386, 335), (0.56, 0.54))
    small_footer(im)
    return save(im, 3)


def care():
    im = base(4, None)
    text(im, (74, 169), "OJO CON…", 102, BROWN, 900)
    photo(im, "assets/humedad-osb.png", (74, 312, 932, 426))
    check(im, 74, 800, True)
    lines(
        im,
        (132, 795),
        ["La humedad directa y el", "exterior sin protección."],
        42,
        INK,
        500,
        12,
    )
    check(im, 74, 948, True)
    text(im, (132, 944), "No es para acabados finos.", 39, INK, 500)
    ImageDraw.Draw(im).rounded_rectangle((74, 1063, 1006, 1164), radius=20, fill=GREEN)
    text(im, (112, 1090), "Sella los cantos", 53, CREAM, 700)
    small_footer(im)
    return save(im, 4)


def stock():
    im = base(5, None)
    lines(im, (74, 169), ["EN", "BONATERRA"], 90, BROWN, 900, 5)
    photo(im, "osb europeo.png", (74, 409, 932, 335))
    pill(im, (98, 658), "OSB", 40, height=67)
    text(im, (74, 787), "LP APA · Kronos · Multiplac", 44, GREEN, 700)
    text(im, (74, 865), "11 mm  ·  18 mm", 61, BROWN, 800)
    d = ImageDraw.Draw(im)
    d.line((74, 984, 1006, 984), fill=SAGE, width=2)
    lines(
        im,
        (74, 1023),
        ["También tableros de ingeniería:", "PERFOCEL Y ASTILLA"],
        38,
        INK,
        500,
        24,
    )
    small_footer(im)
    return save(im, 5)


def close():
    im = base(5, None)
    lines(im, (74, 169), ["TE LO CORTAMOS", "A MEDIDA"], 76, BROWN, 900, 13)
    pill(im, (74, 376), "ESCRÍBENOS Y COTIZA", 29, height=66)
    photo(im, "osb.jpg", (74, 485, 932, 438), (0.5, 0.43))
    paste_logo(im, (788, 774), 190)
    lines(im, (74, 966), ["ENVÍO SIN COSTO", "EN AGUASCALIENTES"], 37, GREEN, 800, 10)
    text(im, (74, 1085), "Asesoría personalizada", 31, INK, 500)
    text(im, (74, 1140), "Harold R. Pape 209, Galerías, Ags.", 27, INK, 500)
    services(im)
    return save(im, 5)


def main():
    SLIDES.mkdir(exist_ok=True)
    imgs = [cover(), what(), uses(), care(), close()]
    review = Image.new("RGB", (1800, 450), CREAM)
    for idx, im in enumerate(imgs):
        review.paste(im.resize((360, 450), Image.Resampling.LANCZOS), (idx * 360, 0))
    review.save(ROOT / "hoja.jpg", quality=95, subsampling=0)
    review.save(ROOT / "preview.png")
    (ROOT / "assets/layout-check.json").write_text(
        json.dumps(RECORD, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("Listos: slides/01.jpg … slides/06.jpg y hoja.jpg (1080 × 1350 por slide).")


if __name__ == "__main__":
    main()
