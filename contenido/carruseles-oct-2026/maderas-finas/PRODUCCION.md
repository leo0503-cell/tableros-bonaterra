# Producción del carrusel

Entregables: `slides/01.jpg` a `slides/06.jpg`, 1080 × 1350 px; `hoja.jpg`, los seis en una fila; `CAPTION.md`.

Regeneración: `uv run build.py`. Pillow está declarado con PEP 723. Se leen las fuentes y el logo original de `../_comun/`; no se modifican. Colores y fuentes están en `src/brand.py`, colocación del logo en `src/logo.py`.

La composición sigue `../_comun/BRIEF.md` y los textos/disponibilidades de `CONTENIDO.md`, que son los documentos solicitados para esta entrega. Las referencias de marca y el brief anterior se usaron para el sistema visual, las etiquetas, las muestras y la franja de servicios.

## Imágenes

- Portada nueva: `bases/01-parota-portada-v2.png`, herramienta integrada de generación de imágenes (`image_gen`), con `Madera aserrada parota.jpeg` como referencia de veta. Se conserva la base anterior.
- Interiores: se aprovecharon los cuatro renders sin texto que ya estaban en `bases/`.
- Cierre: fotos reales locales de parota, tzalam y nogal; la muestra de rosa morada es un recorte ilustrativo del render de puerta, pues no hay foto de textura real de esa especie en la carpeta.
- Ninguna base generada contiene texto o logos. Todos los textos, flechas, etiquetas, líneas e iconos se componen con Pillow. El logo es el PNG oficial, con proporción y color originales.

## Prompt de la portada

Use case: product-mockup. Create ONLY a photorealistic natural wood photograph, with absolutely no text, letters, symbols, logos, labels or watermarks. Wide landscape 3:2 composition for the photo area of a Mexican fine-woods carousel. A single substantial parota (guanacaste) live-edge wood slab, upright, a nearly square broad cut board in three-quarter frontal view, rich wide flowing amber and coffee brown grain faithfully matching the provided real parota reference photo. Matte satin natural finish, no artificial orange saturation. Cream warm seamless backdrop and floor, soft natural daylight, gentle realistic shadow. The whole slab is visible with ample cream margin around it. High-end honest carpentry material photograph, no furniture, no decorative objects, no typography. Reference is for wood grain appearance only. Do not reproduce its exact rectangular crop; show a real solid live-edge board with thickness.

## Revisión final

Se abrieron individualmente los seis JPG finales. Se revisaron acentos, contraste, composición, disponibilidades, integridad del logo y legibilidad. Se corrigió el recorte del borde inferior del tablón y se elevó el logo de los slides de producto. Se comprobó el formato JPEG y las dimensiones de los seis archivos, además de ejecutar Ruff y regenerar con el script.
