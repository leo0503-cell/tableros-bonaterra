# Tableros Bonaterra — Cimbra y Parota

Dos carruseles listos para subir. 1080×1350 (4:5), en el orden numérico de cada
carpeta. Los dos tapan huecos del catálogo que nunca se han publicado en el feed:
construcción y maderas tropicales.

---

## POST 1 · CIMBRA — `cimbra/` (7 slides)

Sugerido en **martes o miércoles temprano**: el público de obra revisa el
teléfono antes de entrar, no en la noche.

```
🔨 No toda la cimbra es igual.

Con film o sin film, de 9 a 18 mm, C+C o CDX: la que le sirve a tu obra depende
del colado que traes. En este carrusel te dejamos las que manejamos y para qué
es cada una.

Desliza y checa cuál le toca a tu próximo colado.

📍 Disponible en Tableros Bonaterra.
📩 Dinos qué vas a colar y te decimos qué cimbra pedir.

#TablerosBonaterra #Cimbra #Construcción #Obra #Aguascalientes
```

**Primer comentario** (para que el algoritmo lo tome como conversación):

```
¿Qué cimbra usas tú y cuántos usos le sacas? 👇
```

---

## POST 2 · PAROTA — `parota/` (5 slides)

Sugerido en **jueves o viernes**: es el contenido más aspiracional de los dos y
pega mejor con el público de diseño y mueble.

```
🌿 Parota: la que se roba la mesa.

Veta marcada, tono cálido y piezas que no se repiten. Es la madera para lo que
queda a la vista: mesas, barras, cabeceras y puertas.

La tenemos en tablero fino y en madera aserrada. Desliza y checa las medidas.

📍 Disponible en Tableros Bonaterra.
📩 Escríbenos por disponibilidad del día.

#TablerosBonaterra #Parota #MaderaTropical #Carpintería #Aguascalientes
```

**Primer comentario:**

```
¿Para qué la usarías: mesa, barra o cabecera? 👇
```

---

## Antes de publicar — 3 cosas que debes revisar tú

1. **El teléfono.** Las piezas traen `449 205 0503`, que es el WhatsApp de la
   contraportada del catálogo. En los posts de 2025 aparecían `449 106 9377` y
   `449 205 0491`, de la sucursal de Mahatma Gandhi. Confirma cuál es el bueno
   hoy y, si cambia, edítalo en `build.py` (constante `WA`) y vuelve a correr.

2. **La foto de la parota.** La que usé es una textura que ya estaba en tu
   Downloads (se había usado para material de TMM). Se ve bien, pero **una foto
   del tablón real en el patio vale más** y es justo lo que le falta al feed.
   Si la consigues, cámbiala en `fotos/parota.jpg` y vuelve a correr `build.py`.

3. **Las medidas.** Todas salen del catálogo oficial (p.11 para tablero fino de
   parota, p.12 para aserrada, p.13 para cimbra). No inventé ninguna. Del
   catálogo **no** salen espesores para Parota MR / Parota Selecta, por eso ese
   slide manda a preguntar en vez de dar un número.

## Detalle técnico

- Tipografía: en esta Mac no hay Montserrat, así que las piezas usan **Futura**
  (titulares) y **Avenir Next** (texto), que es el par más cercano al catálogo.
  Si instalas Montserrat, cámbialo en `brand.py`.
- Paleta: la del **feed real** (`#F8F2E6` crema · `#85966F` salvia ·
  `#637356` franja · `#3E602D` verde del logo), no la del catálogo impreso,
  que es más oscura y usa café.
- El logo circular está recortado de la contraportada del catálogo
  (`fotos/logo.png`). Sigue pendiente que el cliente mande el logo vectorial.

Para regenerar todo:

```bash
cd ~/Documents/Tableros_Bonaterra/contenido/posts-cimbra-parota && uv run --with pillow python3 build.py
```
