# Carrusel PNG — BRIEF.md

Exportación del brief solicitado: seis PNG 1080 × 1350 en `slides/01.png` a `06.png`, `preview.png` y `CAPTION.md`.

Se generaron las cinco bases sin texto con la herramienta integrada `image_gen` y se copiaron a `bases/`. Los textos, las etiquetas, las líneas, los iconos y el PNG oficial del logo se componen con Pillow.

## Reconstruir

```sh
uv run --with pillow build.py --png
```

En esta Mac se puede ejecutar sin red con el Python y Pillow ya disponibles:

```sh
uv run --offline --no-cache --no-project --python /usr/bin/python3 python build.py --png
```

Se conservó la exportación JPG que apareció durante el trabajo en `build.py`; el modo `--png` usa `src/carousel_png.py`, conforme a `BRIEF.md` y `../_comun/BRIEF_MARCA.md`. Los colores PNG se declaran en `src/brand.py`. El logo se coloca mediante `src/logo.py`, sin deformarlo ni cambiarle el color.

## Bases y prompts

Herramienta integrada `image_gen`, no API ni CLI. Todos los prompts pidieron una sola imagen fotorrealista, sin texto, letras, logos ni marcas de agua. Se pidió luz natural cálida, materiales táctiles y tonos crema/madera sin tinte verde.

- `bases/01-parota-portada.png`: tablón grueso de parota con cantos vivos, de pie en estudio crema #F8F0DE, vista casi frontal, veta amplia dorada y oscura y sombra suave a la derecha. Referencia de textura: `Madera aserrada parota.jpeg`.
- `bases/02-parota-comedor.png`: comedor de casa mexicana contemporánea, mesa de parota protagonista con borde vivo, veta marcada y acabado mate, sillas de lino y muros crema. Referencia de textura: `Madera aserrada parota.jpeg`.
- `bases/03-tzalam-recamara.png`: cabecera y muro de paneles anchos lisos de tzalam en recámara cálida, cama de lino marfil, luz natural y veta fina café con matiz rojizo. Referencia: `madera tzalam.jpeg`.
- `bases/04-rosa-morada-puerta.png`: puerta alta cerrada de rosa morada, panel plano de veta vertical café rojiza, acabado satinado mate, muros crema, jaladera bronce y piso travertino. No se suministró referencia real de esta especie.
- `bases/05-nogal-cocina.png`: cocina mexicana contemporánea con gabinetes planos y alacena alta de nogal oscuro, veta café, cubierta y salpicadero de piedra clara. Referencia: `madera aserrada nogal.jpeg`.

Las muestras del cierre provienen de las fotos reales de parota, tzalam y nogal. La de rosa morada es un recorte ilustrativo de la puerta generada. El archivo adicional `01-parota-portada-v2.png` se conservó para la versión JPG.

## Control visual

Revisión individual de las seis slides y la tira. Correcciones: márgenes inferiores, separación entre iconos y textos de servicios, tablón vertical y muestras de veta cuadradas con etiquetas debajo. Se comprueban tamaño y margen mínimo de 70 px de todos los textos. Sin precios ni teléfono en PNG; sólo datos del brief. Logo oficial con proporción y transparencia originales.
