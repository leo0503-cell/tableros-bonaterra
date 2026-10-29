"""Marca Tableros Bonaterra — colores, tipografía y bloques de diseño.

Paleta muestreada por pixel de los posts reales de @tablerosbonaterra
(no del catálogo impreso, que usa un verde más oscuro y acento café).
Ver ~/.claude/skills/marca-tableros-bonaterra.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- colores
CREMA = "#F8F2E6"
CREMA_2 = "#EAE5D2"
SALVIA = "#85966F"        # banner de titulo
VERDE_OSCURO = "#637356"  # franja de servicios
VERDE_MARCA = "#3E602D"   # verde del logo y del catalogo
SALVIA_CLARO = "#AFBE9B"  # script sobre fondo verde (contraste)
TINTA = "#231F20"

# ------------------------------------------------------------ tipografia
# El catalogo usa Montserrat + Futura BT. En esta Mac no hay Montserrat:
# Futura (sistema) para titulares, Avenir Next para texto, Snell para script.
FUTURA = "/System/Library/Fonts/Supplemental/Futura.ttc"
AVENIR = "/System/Library/Fonts/Avenir Next.ttc"
SNELL = "/System/Library/Fonts/Supplemental/SnellRoundhand.ttc"


def f_titulo(size):
    return ImageFont.truetype(FUTURA, size, index=2)  # Futura Bold


def f_kicker(size):
    return ImageFont.truetype(FUTURA, size, index=4)  # Condensed ExtraBold


def f_texto(size, peso="regular"):
    idx = {"regular": 7, "medium": 5, "demi": 2, "bold": 0, "heavy": 8}[peso]
    return ImageFont.truetype(AVENIR, size, index=idx)


def f_script(size):
    return ImageFont.truetype(SNELL, size, index=2)  # Snell Black


# --------------------------------------------------------------- lienzo
W, H = 1080, 1350
MARGEN = 72
SERVICIOS = "ASESORÍA PERSONALIZADA · CORTE A MEDIDA · ENVÍO A DOMICILIO"


def lienzo(color=CREMA):
    return Image.new("RGB", (W, H), color)


def foto_fondo(ruta, zoom=1.0, foco=0.5):
    """Recorta una foto a 1080x1350 cubriendo todo el lienzo."""
    im = Image.open(ruta).convert("RGB")
    escala = max(W / im.width, H / im.height) * zoom
    im = im.resize((int(im.width * escala), int(im.height * escala)), Image.LANCZOS)
    x = int((im.width - W) * foco)
    y = int((im.height - H) * foco)
    return im.crop((x, y, x + W, y + H))


def velo(img, color=VERDE_MARCA, desde=0.42, alpha_max=232, curva=0.75):
    """Degradado vertical del color de marca: deja ver la foto arriba.

    `curva` > 1 retrasa el velo y luego lo cierra rápido: sobre maderas cálidas
    evita la franja verdosa a medio camino entre la foto y el color sólido.
    """
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    rgb = Image.new("RGB", (1, 1), color).getpixel((0, 0))
    y0 = int(H * desde)
    for y in range(y0, H):
        t = (y - y0) / max(1, H - y0)
        d.line([(0, y), (W, y)], fill=rgb + (int(alpha_max * (t ** curva)),))
    base = img.convert("RGBA")
    base.alpha_composite(capa)
    return base.convert("RGB")


def logo(img, x=MARGEN, y=54, tam=132):
    lg = Image.open("fotos/logo.png").convert("RGBA")
    lg = lg.resize((tam, tam), Image.LANCZOS)
    img.paste(lg, (x, y), lg)


def pastilla(d, xy, texto, fuente, fondo=SALVIA, color=CREMA, pad=(34, 18), r=None):
    """Banner redondeado con el texto dentro. Devuelve (x1, y1)."""
    x, y = xy
    ancho = d.textlength(texto, font=fuente)
    alto = fuente.size
    x1 = x + ancho + pad[0] * 2
    y1 = y + alto + pad[1] * 2
    radio = r if r is not None else (y1 - y) // 2
    d.rounded_rectangle([x, y, x1, y1], radius=radio, fill=fondo)
    d.text((x + pad[0], y + pad[1] - fuente.size * 0.08), texto, font=fuente, fill=color)
    return x1, y1


def parrafo(d, xy, texto, fuente, color=TINTA, ancho=W - MARGEN * 2, interlinea=1.34):
    """Texto con salto de linea automatico. Devuelve la y final."""
    x, y = xy
    for bloque in texto.split("\n"):
        linea = ""
        for palabra in bloque.split(" "):
            prueba = (linea + " " + palabra).strip()
            if d.textlength(prueba, font=fuente) <= ancho:
                linea = prueba
            else:
                d.text((x, y), linea, font=fuente, fill=color)
                y += int(fuente.size * interlinea)
                linea = palabra
        d.text((x, y), linea, font=fuente, fill=color)
        y += int(fuente.size * interlinea)
    return y


def franja(img, texto=SERVICIOS, alto=104, fondo=VERDE_OSCURO):
    d = ImageDraw.Draw(img)
    d.rectangle([0, H - alto, W, H], fill=fondo)
    fu = f_texto(23, "demi")
    ancho = d.textlength(texto, font=fu)
    d.text(((W - ancho) / 2, H - alto / 2 - fu.size * 0.62), texto, font=fu, fill=CREMA)


def paginador(d, n, total, color=CREMA, y=None):
    """Puntos de avance del carrusel, discretos, arriba a la derecha."""
    y = y if y is not None else 118
    r, gap = 7, 26
    x = W - MARGEN - (total - 1) * gap
    for i in range(total):
        cx = x + i * gap
        if i == n - 1:
            d.ellipse([cx - r, y - r, cx + r, y + r], fill=color)
        else:
            d.ellipse([cx - r, y - r, cx + r, y + r], outline=color, width=2)


def guardar(img, ruta):
    img.save(ruta, quality=95, subsampling=0)
    print("  ✓", ruta)
