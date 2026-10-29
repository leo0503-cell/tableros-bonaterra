# Carrusel OSB · Tableros Bonaterra

Entrega basada en `../_comun/BRIEF.md` y `CONTENIDO.md`. Frente a diferencias
con briefs anteriores, se priorizaron estos dos archivos solicitados.

- `slides/01.jpg` … `slides/06.jpg`: entrega principal, 1080 × 1350 px, en orden.
- `hoja.jpg`: las seis láminas en una fila.
- `CAPTION.md`: caption en español MX con CTA y seis hashtags.
- `slides/01.png` … `slides/06.png` y `preview.png`: copias adicionales del mismo diseño.
- `assets/`: tres fotos base generadas sin texto y registro de límites de texto.
- `assets/PROMPTS.md`: prompts de generación y referencia empleada.
- `build.py`, `src/brand.py`, `src/logo.py`: composición reproducible con Pillow.

## Reconstruir

```sh
uv run build.py
```

Pillow está declarado mediante PEP 723. El script lee fuentes y logo oficial
desde `../_comun/` y utiliza las bases ya guardadas: no necesita volver a generar fotos.
Todos los textos y el logo se agregan con Pillow. Se usan las tres texturas de OSB
originales y la foto real de estibas `osb.jpg`.

En esta sesión, con acceso a PyPI restringido, se aprovechó una copia local del
paquete que ya estaba en caché, sin instalar paquetes del sistema ni cambiar settings:

```sh
UV_CACHE_DIR="$PWD/.cache/uv" uv run --offline build.py
```

## Verificación

Se abrieron y revisaron las seis láminas finales individualmente y la hoja conjunta:
ortografía, texto completo, márgenes, contraste, recortes de foto y proporción del logo.
Se verificó el tamaño de todos los JPG. `ruff format` y `ruff check` aplicados al código.

La carpeta `bases/` conserva material de una versión anterior; el build actual
consume únicamente `assets/` y las fotografías originales de esta carpeta.
