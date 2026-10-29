# /// script
# dependencies = ["pillow", "pillow-heif"]
# ///
"""Carrusel 'Todo lo que necesitas' con fotos reales del almacén. uv run build.py"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from pillow_heif import register_heif_opener

register_heif_opener()
AQUI = Path(__file__).parent
DL = Path.home() / "Downloads"
FONTS = AQUI.parent / "carruseles-oct-2026/_comun/fonts"
LOGO = AQUI.parent / "assets/logo-circular.png"
OUT = AQUI / "slides"
OUT.mkdir(exist_ok=True)

W, H = 1080, 1350
CREMA, VERDE, VERDE_OSC, CAFE = "#F8F0DE", "#3E602D", "#637356", "#6A3521"


def font(size, peso=800, italic=False):
    f = ImageFont.truetype(str(FONTS / ("Montserrat-Italic.ttf" if italic else "Montserrat.ttf")), size)
    f.set_variation_by_axes([peso])
    return f


def script(size):
    f = ImageFont.truetype(str(FONTS / "DancingScript.ttf"), size)
    f.set_variation_by_axes([700])
    return f


def foto(src, foco=0.5):
    p = DL / src if (DL / src).exists() else AQUI / "fotos" / src
    im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    return ImageOps.fit(im, (W, H), Image.LANCZOS, centering=(0.5, foco))


def logo(c, size=170, pos=(48, 48)):
    lg = Image.open(LOGO).convert("RGBA").resize((size, size), Image.LANCZOS)
    c.paste(lg, pos, lg)


def pastilla(d, txt, y, f, bg=VERDE, fg=CREMA, cx=W // 2, pad=(38, 18)):
    w = d.textlength(txt, font=f)
    a = f.getbbox(txt)
    h = a[3] - a[1]
    x0 = cx - w / 2 - pad[0]
    d.rounded_rectangle((x0, y, cx + w / 2 + pad[0], y + h + 2 * pad[1]), 22, fill=bg)
    d.text((cx, y + pad[1] - a[1]), txt, font=f, fill=fg, anchor="mt")
    return y + h + 2 * pad[1]


def sombra_abajo(c, alto=620):
    g = Image.new("L", (1, alto))
    for i in range(alto):
        g.putpixel((0, i), int(235 * (i / alto) ** 1.6))
    negro = Image.new("RGB", (W, alto), "#141a10")
    c.paste(negro, (0, H - alto), g.resize((W, alto)))


def franja_servicios(c):
    d = ImageDraw.Draw(c)
    d.rectangle((0, H - 120, W, H), fill=VERDE_OSC)
    txt = "CORTE A MEDIDA  ·  ENCHAPADO  ·  ENVÍO A DOMICILIO"
    d.text((W // 2, H - 60), txt, font=font(30, 700), fill=CREMA, anchor="mm")


def paginador(d, i, n=6):
    x = W - 48 - (n - 1) * 26
    for k in range(n):
        r = 8 if k == i else 6
        d.ellipse((x + k * 26 - r, 70 - r, x + k * 26 + r, 70 + r), fill=CREMA if k == i else "#cfc6b0")


def slide_foto(src, titulo, sub, i, foco=0.5):
    c = foto(src, foco)
    sombra_abajo(c)
    d = ImageDraw.Draw(c)
    logo(c, 150)
    paginador(d, i)
    y = H - 330
    for linea in titulo:
        d.text((64, y), linea, font=font(80, 850), fill=CREMA)
        y += 88
    pastilla(d, sub, y + 18, font(34, 700), cx=64 + d.textlength(sub, font=font(34, 700)) / 2 + 38)
    return c


# 1 · Portada
c = foto("IMG_5416.jpg", 0.55)
sombra_abajo(c, 800)
d = ImageDraw.Draw(c)
logo(c, 190)
paginador(d, 0)
d.text((W // 2, 880), "TODO LO QUE", font=font(96, 850), fill=CREMA, anchor="mm")
d.text((W // 2, 985), "NECESITAS", font=font(118, 900), fill=CREMA, anchor="mm")
pastilla(d, "EN UN SOLO LUGAR", 1060, font(44, 800))
d.text((W // 2, 1230), "Desliza y conoce nuestro almacén", font=script(46), fill=CREMA, anchor="mm")
c.save(OUT / "01.jpg", quality=93)

slide_foto("IMG_5401.HEIC", ["MDF Y", "TRIPLAY"], "Estibas listas para tu proyecto", 1).save(OUT / "02.jpg", quality=93)
slide_foto("IMG_5392.HEIC", ["MADERA", "DE PINO"], "Para carpintería y construcción", 2).save(OUT / "03.jpg", quality=93)
slide_foto("IMG_5413.HEIC", ["MELAMINAS"], "Diseños maderados y lisos", 3).save(OUT / "04.jpg", quality=93)
slide_foto("IMG_5381.jpg", ["Y MUCHO", "MÁS"], "Lo que tu proyecto pida", 4, 0.4).save(OUT / "05.jpg", quality=93)

# 6 · Cierre en crema
c = Image.new("RGB", (W, H), CREMA)
d = ImageDraw.Draw(c)
paginador(d, 5)
fondo = foto("IMG_5410.jpg", 0.5).resize((W, H))
ventana = ImageOps.fit(fondo, (860, 520), centering=(0.5, 0.45))
m = Image.new("L", ventana.size, 0)
ImageDraw.Draw(m).rounded_rectangle((0, 0, *ventana.size), 36, fill=255)
c.paste(ventana, (110, 330), m)
lg = Image.open(LOGO).convert("RGBA").resize((210, 210), Image.LANCZOS)
c.paste(lg, (W // 2 - 105, 90), lg)
d.text((W // 2, 920), "¡Te esperamos!", font=script(78), fill=VERDE, anchor="mm")
d.text((W // 2, 1010), "Harold R. Pape 209, Galerías · Ags.", font=font(36, 700), fill=CAFE, anchor="mm")
d.text((W // 2, 1065), "Cotiza por mensaje o visítanos", font=font(32, 500), fill="#231F20", anchor="mm")
franja_servicios(c)
c.save(OUT / "06.jpg", quality=93)

# hoja de revisión
hoja = Image.new("RGB", (6 * 360, 450), "white")
for k in range(6):
    hoja.paste(Image.open(OUT / f"{k + 1:02d}.jpg").resize((360, 450)), (k * 360, 0))
hoja.save(AQUI / "hoja.jpg", quality=85)
