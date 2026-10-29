"""Genera los carruseles de Instagram de Cimbra y Parota para Tableros Bonaterra.

    cd ~/Documents/Tableros_Bonaterra/contenido/posts-cimbra-parota
    uv run --with pillow python3 build.py

Todas las medidas salen del catálogo oficial (catalogo BONATERRA_compressed.pdf,
p.11, p.12 y p.13). Nada aquí es inventado: lo que no está en el catálogo va
entre <corchetes> o simplemente no se afirma.
"""

from PIL import Image, ImageDraw

from brand import (
    CREMA, CREMA_2, SALVIA, SALVIA_CLARO, VERDE_OSCURO, VERDE_MARCA, TINTA,
    W, H, MARGEN,
    f_titulo, f_kicker, f_texto, f_script,
    lienzo, foto_fondo, velo, logo, pastilla, parrafo, franja, paginador, guardar,
)

WA = "449 205 0503"
DIR = "Harold R. Pape 209, Desarrollo Especial Galerías"
PIE = H - 104          # donde empieza la franja de servicios


# ---------------------------------------------------------------- piezas base
def portada(foto, kicker, titulo, script, n, total, zoom=1.0, foco=0.5):
    """Foto arriba, bloque verde sólido abajo: sin velos que ensucien la madera."""
    lineas = titulo.split("\n")
    ft, fk, fs = f_titulo(92), f_kicker(38), f_script(66)
    alto_bloque = 104 + 64 + len(lineas) * int(ft.size * 1.06) + 34 + fs.size + 96
    corte = H - alto_bloque

    img = lienzo(VERDE_MARCA)
    img.paste(foto_fondo(foto, zoom=zoom, foco=foco).crop((0, 0, W, corte)), (0, 0))
    d = ImageDraw.Draw(img)
    logo(img)
    paginador(d, n, total)

    y = corte + 60
    pastilla(d, (MARGEN, y - 44), kicker, fk, fondo=SALVIA)
    y += 64
    for linea in lineas:
        d.text((MARGEN, y), linea, font=ft, fill=CREMA)
        y += int(ft.size * 1.06)
    d.text((MARGEN, y + 24), script, font=fs, fill=SALVIA_CLARO)

    franja(img)
    return img


def hoja(titulo, n, total, foto=None, alto_foto=470, zoom=1.0, foco=0.5):
    """Slide crema con banner de título y, opcionalmente, una banda de foto."""
    img = lienzo(CREMA)
    if foto:
        banda = foto_fondo(foto, zoom=zoom, foco=foco).crop((0, 0, W, alto_foto))
        img.paste(banda, (0, 0))
    d = ImageDraw.Draw(img)
    logo(img, tam=118)
    paginador(d, n, total, color=CREMA if foto else VERDE_MARCA)

    y = (alto_foto - 44) if foto else 232
    _, y1 = pastilla(d, (MARGEN, y), titulo, f_titulo(54), fondo=SALVIA)
    franja(img)
    return img, d, y1 + 54


def tarjeta(d, y, etiqueta, texto, alto=340):
    d.rounded_rectangle([MARGEN, y, W - MARGEN, y + alto], radius=30, fill=CREMA_2)
    pastilla(d, (MARGEN + 36, y + 40), etiqueta, f_kicker(36), fondo=VERDE_MARCA)
    parrafo(d, (MARGEN + 38, y + 158), texto, f_texto(32, "regular"),
            ancho=W - MARGEN * 2 - 76)
    return y + alto + 56


def fila(d, y, nombre, detalles, linea=True):
    d.text((MARGEN, y), nombre, font=f_titulo(44), fill=VERDE_MARCA)
    y += 64
    for det in detalles:
        d.text((MARGEN + 6, y), det, font=f_texto(33, "medium"), fill=TINTA)
        y += 48
    y += 16
    if linea:
        d.line([(MARGEN, y), (W - MARGEN, y)], fill=CREMA_2, width=3)
        y += 38
    return y


def nota(d, y, texto, color=VERDE_MARCA):
    """Cierre de slide: frase de asesoría, alineada al pie del área útil."""
    fu = f_texto(31, "medium")
    parrafo(d, (MARGEN, y), texto, fu, color=color)


def cierre(titulo, script, n, total):
    img = lienzo(VERDE_MARCA)
    d = ImageDraw.Draw(img)
    paginador(d, n, total)

    lg = Image.open("fotos/logo.png").convert("RGBA").resize((320, 320), Image.LANCZOS)
    img.paste(lg, ((W - 320) // 2, 170), lg)

    ft = f_titulo(74)
    y = 560
    for linea in titulo.split("\n"):
        ancho = d.textlength(linea, font=ft)
        d.text(((W - ancho) / 2, y), linea, font=ft, fill=CREMA)
        y += int(ft.size * 1.12)

    fs = f_script(64)
    ancho = d.textlength(script, font=fs)
    d.text(((W - ancho) / 2, y + 20), script, font=fs, fill=SALVIA_CLARO)

    y += 190
    for texto, fu in [
        (f"WhatsApp {WA}", f_texto(42, "demi")),
        (DIR, f_texto(29, "regular")),
        ("Aguascalientes, Ags.", f_texto(29, "regular")),
        ("@tablerosbonaterra", f_texto(31, "demi")),
    ]:
        ancho = d.textlength(texto, font=fu)
        d.text(((W - ancho) / 2, y), texto, font=fu, fill=CREMA)
        y += int(fu.size * 1.55)

    franja(img, fondo=VERDE_OSCURO)
    return img


# --------------------------------------------------------------------- CIMBRA
def cimbra():
    print("CIMBRA")
    T = 7

    guardar(portada("fotos/cimbra-brasil.jpg", "TABLERO CIMBRA",
                    "No toda la cimbra\nes igual.", "Desliza y encuentra la tuya",
                    1, T, zoom=1.15, foco=0.4), "cimbra/01.png")

    # 02 — con film vs sin film
    img, d, y = hoja("¿Con film o sin film?", 2, T)
    y = tarjeta(d, y, "SIN FILM",
                "Pino natural en la cara. Es la cimbra de siempre para\n"
                "colados donde el acabado se resana o se aplana después.")
    y = tarjeta(d, y, "CON FILM",
                "Lleva una película sobre la cara del tablero: la superficie\n"
                "queda más lisa y el desmolde sale más limpio.")
    fs = f_script(52)
    d.text((MARGEN, PIE - 96), "Las dos te las tenemos", font=fs, fill=SALVIA)
    guardar(img, "cimbra/02.png")

    # 03 — sin film
    img, d, y = hoja("Sin film · pino natural", 3, T,
                     foto="fotos/cimbra-nacional.png", zoom=1.1, foco=0.35)
    y = fila(d, y, "PINO BRASIL", ["C+C · 9, 12, 15 y 18 mm", "BG · 12, 15 y 18 mm"])
    y = fila(d, y, "PINO ASIÁTICO", ["Combi Core · 12, 15 y 18 mm CDX",
                                     "Poplar · 12, 15 y 18 mm CDX"])
    y = fila(d, y, "PINO USA", ["15 mm MC"], linea=False)
    nota(d, PIE - 130, "¿No sabes cuál elegir? Nuestro equipo te ayuda a encontrar\n"
                       "la mejor opción para tu obra.")
    guardar(img, "cimbra/03.png")

    # 04 — con film
    img, d, y = hoja("Con film", 4, T)
    y = fila(d, y, "ASIÁTICA · BRASIL · TULSA", ["15 y 18 mm"])
    y = fila(d, y, "FILM PLÁSTICA ASIÁTICA", ["15 y 18 mm"])
    y = fila(d, y, "RUSA FILM BIRCH", ["12 y 18 mm"], linea=False)
    nota(d, PIE - 178, "El film cuida la cara del tablero colado tras colado.\n"
                       "Si tu obra repite cimbrado, pregunta por esta línea\n"
                       "antes de decidir.")
    guardar(img, "cimbra/04.png")

    # 05 — MDO Plata
    img, d, y = hoja("MDO Plata", 5, T)
    y = parrafo(d, (MARGEN, y), "Tablero con recubrimiento, para cuando la cara\n"
                                "del colado sí se va a ver.", f_texto(38, "regular"))
    y += 70
    d.rounded_rectangle([MARGEN, y, W - MARGEN, y + 230], radius=30, fill=CREMA_2)
    ft = f_titulo(96)
    texto = "15 y 18 mm"
    ancho = d.textlength(texto, font=ft)
    d.text(((W - ancho) / 2, y + 62), texto, font=ft, fill=VERDE_MARCA)
    nota(d, PIE - 178, "Manejamos cimbra en más orígenes y espesores de los que\n"
                       "caben en un carrusel. Dinos qué colado traes y te decimos\n"
                       "qué tenemos.")
    guardar(img, "cimbra/05.png")

    # 06 — cómo pedirla
    img = lienzo(VERDE_MARCA)
    d = ImageDraw.Draw(img)
    logo(img, tam=118)
    paginador(d, 6, T)
    ft = f_titulo(64)
    y = 250
    for linea in ["Antes de pedir tu", "cimbra, ten a la mano:"]:
        d.text((MARGEN, y), linea, font=ft, fill=CREMA)
        y += int(ft.size * 1.14)
    y += 74
    for i, texto in enumerate([
        "El espesor que te pide la obra",
        "Si el colado va aparente o se resana",
        "Cuántas veces la piensas reusar",
    ], 1):
        d.ellipse([MARGEN, y, MARGEN + 72, y + 72], fill=SALVIA)
        num, fn = str(i), f_titulo(40)
        ancho = d.textlength(num, font=fn)
        d.text((MARGEN + 36 - ancho / 2, y + 14), num, font=fn, fill=VERDE_MARCA)
        parrafo(d, (MARGEN + 108, y + 10), texto, f_texto(36, "medium"),
                color=CREMA, ancho=W - MARGEN * 2 - 108)
        y += 168
    fs = f_script(60)
    d.text((MARGEN, y + 26), "Con eso te decimos cuál te conviene",
           font=fs, fill=SALVIA_CLARO)
    franja(img, fondo=VERDE_OSCURO)
    guardar(img, "cimbra/06.png")

    guardar(cierre("Madera, precio\ny servicio.", "Cotiza tu obra", 7, T), "cimbra/07.png")


# --------------------------------------------------------------------- PAROTA
def parota():
    print("PAROTA")
    T = 5

    guardar(portada("fotos/parota.jpg", "MADERA TROPICAL",
                    "Parota.", "La que se roba la mesa",
                    1, T, zoom=1.05, foco=0.45), "parota/01.png")

    # 02 — por qué la piden
    img, d, y = hoja("Por qué la piden", 2, T)
    y = tarjeta(d, y, "LA VETA",
                "Marcada y de tono cálido: cada pieza sale distinta,\n"
                "no hay dos mesas iguales.")
    y = tarjeta(d, y, "EL USO",
                "Es la madera para lo que queda a la vista: mesas,\n"
                "barras, cabeceras y puertas.")
    fs = f_script(52)
    d.text((MARGEN, PIE - 96), "Inspírate y cotiza la tuya", font=fs, fill=SALVIA)
    guardar(img, "parota/02.png")

    # 03 — tablero fino
    img, d, y = hoja("Tablero fino", 3, T, foto="fotos/parota.jpg", zoom=1.4, foco=0.2)
    y = fila(d, y, "TRIPLAY", ["5, 12, 15 y 18 mm"])
    y = fila(d, y, "LISTÓN", ["15 y 18 mm"], linea=False)
    y += 34
    d.rounded_rectangle([MARGEN, y, W - MARGEN, y + 250], radius=30, fill=CREMA_2)
    parrafo(d, (MARGEN + 38, y + 52),
            "La veta de la madera maciza con la estabilidad\n"
            "del tablero, y sin batallar con el habilitado.",
            f_texto(34, "medium"), color=VERDE_MARCA, ancho=W - MARGEN * 2 - 76)
    guardar(img, "parota/03.png")

    # 04 — madera aserrada
    img, d, y = hoja("Madera aserrada", 4, T)
    y = fila(d, y, "PAROTA MR", ["Para muebles y proyectos de carpintería"])
    y = fila(d, y, "PAROTA SELECTA", ["Selección para piezas a la vista"], linea=False)
    y += 20
    d.rounded_rectangle([MARGEN, y, W - MARGEN, y + 220], radius=30, fill=CREMA_2)
    parrafo(d, (MARGEN + 38, y + 50),
            "También manejamos tzalam, rosa morada,\ncumaru para deck y encino.",
            f_texto(34, "medium"), color=VERDE_MARCA, ancho=W - MARGEN * 2 - 76)
    nota(d, y + 270, "Escríbenos por medidas y disponibilidad del día:\n"
                     "la madera tropical se mueve rápido.")
    guardar(img, "parota/04.png")

    guardar(cierre("Madera, precio\ny servicio.", "Cotiza tu proyecto", 5, T),
            "parota/05.png")


if __name__ == "__main__":
    cimbra()
    parota()
    print("\nListo. 7 slides de cimbra + 5 de parota.")
