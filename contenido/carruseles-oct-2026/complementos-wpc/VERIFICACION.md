# Verificación del carrusel

Entrega ajustada a `CONTENIDO.md` y `../_comun/BRIEF.md`.

- Seis archivos JPEG: `slides/01.jpg` a `slides/06.jpg`, todos de 1080 × 1350 px.
- `hoja.jpg`: los seis slides en una sola fila, 3240 × 675 px.
- `CAPTION.md`: español de México, seis hashtags y CTA «escríbenos y cotiza».
- Texto compuesto con Pillow, Montserrat variable y Dancing Script. Flecha dibujada con línea.
- Logo oficial pegado desde `../_comun/logo-circular.png`.
- Bases de image_gen sin texto; prompts en `bases/PROMPTS.json` y `bases/08-wpc-stud.prompt.txt`.
- Revisión visual individual realizada abriendo cada JPG: márgenes, contraste, ortografía, productos visibles y logo sin deformación. Portada y cierre se reabrieron tras ajustar la franja inferior; también se abrió la hoja conjunta.
- Medidas de WPC Stud verificadas contra el contenido: 6 × 4.2 cm y 10 × 5 cm; largo 2.9 m.
- Ruff format y Ruff check aprobados. El build comprueba que cada caja de texto respete los márgenes.

## Reproducir

Desde esta carpeta:

```sh
uv run build.py
```

Incluye dependencias inline PEP 723. No vuelve a generar imágenes: recompone los archivos guardados en `bases/` y lee fuentes/logo de `../_comun/`.

El entorno restringido impidió escribir en la caché global de uv y descargar de PyPI. Se reutilizó Pillow ya disponible para llenar una caché dentro de esta carpeta. El build completo pasó con:

```sh
UV_CACHE_DIR="$PWD/.uv-cache" uv run --offline build.py
```

Se conservaron copias PNG y `preview.png` además de los JPG solicitados.
