# Brief común — carrusel Instagram Tableros Bonaterra (@tablerosbonaterra)

Tableros Bonaterra: materiales para carpintería y construcción en Aguascalientes (melamina, MDF, triplay,
WPC, PVC mármol, madera, OSB, enchapados). Mascota: elefante. Tono cálido, terroso, de madera. Nada frío ni "tech".

## Formato
- 6 slides PNG de 1080 × 1350 (4:5), nombrados 01.png … 06.png en `slides/`.
- También `preview.png`: las 6 slides en una tira horizontal reducida (para revisar de un vistazo).

## Identidad (OBLIGATORIO, copia el sistema de `../_comun/refs/`)
Mira las 3 referencias reales del feed antes de diseñar. El sistema es:
- Fondo crema `#F8F0DE` (alterno `#F8F2E6`). Texto corrido negro tinta `#231F20`.
- Titulares en **Montserrat ExtraBold/Black, MAYÚSCULAS**, en café madera `#6A3521` o verde `#3E602D`.
- **Pastilla** verde `#3E602D` con esquinas redondeadas y texto crema en Montserrat Bold mayúsculas, debajo del titular.
- Acento **script** (Dancing Script) verde, chico, tipo "Inspírate →" con flecha de línea.
- **Franja inferior** de ancho completo: izquierda crema con "SERVICIOS / COMPLEMENTO" en verde; derecha bloque verde
  con iconos de línea crema + "CORTE A MEDIDA" | "ENCHAPADO" | "ENVÍO A DOMICILIO". Úsala en portada y cierre (no en todas).
- Logo circular REAL: `../_comun/logo-circular.png` (PNG con alfa). Pégalo con Pillow tal cual; NUNCA lo regeneres ni lo
  redibujes con IA. En renders a sangre puede ir en crema semitransparente abajo a la derecha como en ref-render-interior.
- Etiquetas sobre foto: rectángulo verde `#3E602D` con texto crema bold + línea guía blanca con punto (ver ref-render-interior).
- Verde salvia `#85966F` / `#637356` sólo como apoyo. Sin degradados verdes sobre la madera (ensucian el tono): bloques sólidos.
- Fuentes en `../_comun/fonts/` (Montserrat variable: usa set_variation_by_name o by_axes para el peso; Dancing Script).

## Cómo producir
1. Usa TU herramienta de generación de imágenes para las fotos/renders base (sin texto dentro de la imagen; texto = 0).
   Fotorrealista, luz cálida natural, interiores/obras mexicanas creíbles. Si hay fotos de producto reales en esta carpeta,
   úsalas como referencia de textura/veta para que el material se vea igual.
2. Compón todas las slides con Python + Pillow en `build.py` (corre con `uv run --with pillow build.py`). El texto SIEMPRE
   se escribe con Pillow (ortografía y acentos perfectos), nunca dentro de la imagen generada.
3. Abre cada PNG final y revísalo: que nada se encime, márgenes ≥ 70 px, texto legible en celular, acentos correctos,
   el logo sin deformar. Corrige y vuelve a renderizar hasta que quede bien.
4. Escribe `CAPTION.md`: caption en español de México, voz de la marca (cercana, práctica, emojis 🐘🪵 con moderación),
   3–6 líneas + CTA a mandar mensaje por WhatsApp/DM + 8–12 hashtags locales (#Aguascalientes #CarpinteríaAgs ...).

## Reglas duras
- **Ningún número, precio, medida ni dato inventado.** Sólo usa los datos que te dé el brief del carrusel.
  Si un dato falta, no lo pongas (o déjalo entre `<corchetes>` en el CAPTION, nunca en la imagen).
- No pongas teléfono ni precios en las slides.
- No mezclar con otras marcas (nada de azul/verde eléctrico de TMM).
- Trabaja sólo dentro de esta carpeta.
