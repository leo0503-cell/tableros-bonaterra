"""Logo de Tableros Bonaterra en los últimos 7 s del video de la melamina.

Replica la transición del video de referencia (Cream Bol): destello del logo
chico semitransparente, luego el logo grande entra desde la derecha frenando,
cruza lento por el centro y sale acelerando por la izquierda.
La trayectoria se midió cuadro por cuadro en la referencia (576x1024).

uv run --with numpy --with pillow --with imageio-ffmpeg python render.py [--preview]
"""

import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageFilter

AQUI = Path(__file__).parent
SRC = Path.home() / "Downloads" / "IMG_4904.MOV"
LOGO = AQUI / "logo-bonaterra-crema.png"
OUT = AQUI / "melamina_logo_bonaterra.mov"
FF = imageio_ffmpeg.get_ffmpeg_exe()

W, H, FPS = 1080, 1920, 30
DUR_LOGO = 7.0
REF_DUR = 6.26  # duración de la referencia; se estira a 7 s

# Centro X del logo en la referencia (px de 576, radio del logo = 300 px)
REF_T = [
    0.33,
    0.40,
    0.47,
    0.53,
    0.60,
    0.67,
    0.73,
    0.80,
    0.87,
    0.93,
    1.00,
    1.13,
    1.33,
    1.67,
    2.00,
    2.33,
    2.67,
    3.00,
    3.33,
    3.60,
    4.27,
    4.40,
    4.53,
    4.67,
    4.80,
    4.93,
    5.07,
    5.20,
    5.33,
    5.47,
    5.60,
    5.73,
    5.87,
    6.00,
    6.07,
    6.13,
    6.20,
]
REF_CX = [
    747,
    677,
    634,
    602,
    575,
    553,
    534,
    517,
    502,
    488,
    476,
    454,
    428,
    395,
    370,
    352,
    337,
    323,
    311,
    300,
    271,
    262,
    252,
    241,
    229,
    215,
    199,
    180,
    159,
    133,
    103,
    66,
    18,
    -50,
    -102,
    -194,
    -330,
]
GHOST_END = 0.33

# Geometría en el video vertical
LOGO_W = int(W * 0.96)  # ancho del emblema en reposo
CY = 640  # centro vertical del emblema
GHOST_W = int(W * 0.57)
GHOST_CY = 690
BLANCO_HLG = 0.97  # señal HLG del blanco del logo (0-1)


def cargar_logo():
    im = Image.open(LOGO).convert("RGBA")
    im = im.crop(im.getbbox())
    # sombra suave para que el crema se lea sobre el fondo claro
    pad = 60
    base = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    sombra = Image.new("RGBA", base.size, (0, 0, 0, 0))
    a = im.split()[3].point(lambda v: v * 0.55)
    negro = Image.new("RGBA", im.size, (25, 30, 20, 255))
    negro.putalpha(a)
    sombra.paste(negro, (pad, pad + 12))
    sombra = sombra.filter(ImageFilter.GaussianBlur(22))
    base = Image.alpha_composite(sombra, base)
    base.alpha_composite(im, (pad, pad))
    return base, im.width


def escalado(logo, ancho_emblema, ancho_real):
    f = ancho_emblema / ancho_real
    return logo.resize((round(logo.width * f), round(logo.height * f)), Image.LANCZOS)


def ease(x):
    return 1 - (1 - x) ** 2


def cuadro(t, grande, chico_por_frame):
    """t en segundos de la referencia."""
    lienzo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if t < GHOST_END:
        p = t / GHOST_END
        chico = chico_por_frame(p)
        op = 0.15 + 0.55 * ease(p)
        a = np.array(chico)
        a[..., 3] = (a[..., 3] * op).astype(np.uint8)
        chico = Image.fromarray(a)
        lienzo.alpha_composite(
            chico, (W // 2 - chico.width // 2, GHOST_CY - chico.height // 2)
        )
    else:
        cx_ref = np.interp(t, REF_T, REF_CX)
        cx = W / 2 + (cx_ref - 288) / 300 * (LOGO_W / 2)
        x, y = round(cx - grande.width / 2), CY - grande.height // 2
        if x < W and x + grande.width > 0:
            lienzo.alpha_composite(grande, (max(x, 0), y), (max(-x, 0), 0))
    return lienzo


def a_hlg(im):
    """RGBA sRGB (8 bit) -> RGBA en señal HLG BT.2020 (16 bit).

    El blanco del logo va a BLANCO_HLG de señal. El video es muy brillante
    (mediana ~69 %, luces arriba de 100 %): con el 75 % de BT.2408 el crema
    se ve gris, por eso va casi al tope.
    """
    a = np.asarray(im, dtype=np.float32) / 255
    rgb = a[..., :3]
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    m = np.array(
        [[0.6274, 0.3293, 0.0433], [0.0691, 0.9195, 0.0114], [0.0164, 0.0880, 0.8956]],
        dtype=np.float32,
    )
    ha, hb, hc = 0.17883277, 0.28466892, 0.55991073
    escala = (np.exp((BLANCO_HLG - hc) / ha) + hb) / 12
    e = np.clip(lin @ m.T, 0, None) * escala
    sig = np.where(
        e <= 1 / 12, np.sqrt(3 * e), ha * np.log(np.maximum(12 * e - hb, 1e-6)) + hc
    )
    out = np.concatenate([sig, a[..., 3:]], axis=-1)
    return (np.clip(out, 0, 1) * 65535 + 0.5).astype("<u2")


def duracion():
    r = subprocess.run(
        [FF, "-i", str(SRC)], capture_output=True, text=True, check=False
    ).stderr
    hms = r.split("Duration: ")[1].split(",")[0]
    h, m, s = hms.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def main():
    logo, ancho = cargar_logo()
    grande = escalado(logo, LOGO_W, ancho)
    cache = {}

    def chico_por_frame(p):
        k = round(p * 10)
        if k not in cache:
            cache[k] = escalado(logo, GHOST_W * (0.93 + 0.07 * k / 10), ancho)
        return cache[k]

    n = round(DUR_LOGO * FPS)
    k = REF_DUR / DUR_LOGO

    if "--preview" in sys.argv:
        tms = [0.1, 0.25, 0.5, 1.0, 2.0, 3.5, 4.5, 5.5, 6.3, 6.8]
        for t in tms:
            cuadro(t * k, grande, chico_por_frame).save(AQUI / f"prev_{t:.1f}.png")
        return

    inicio = duracion() - DUR_LOGO
    # Se conserva el original tal cual: HEVC 10-bit HDR (HLG, BT.2020),
    # 1920x1080 guardado con la rotación del iPhone y la cadencia original.
    # El logo se gira al sentido en que está guardado el video y se pasa a HLG.
    filtro = (
        "[1:v]scale=out_color_matrix=bt2020:out_range=tv,format=yuva444p10le,"
        f"setpts=PTS-STARTPTS+{inicio:.4f}/TB[logo];"
        "[0:v][logo]overlay=0:0:eof_action=pass:format=yuv444p10,"
        "format=yuv420p10le[v]"
    )
    x265 = "colorprim=bt2020:transfer=arib-std-b67:colormatrix=bt2020nc:range=limited"
    cmd = [
        FF, "-y", "-v", "error",
        "-noautorotate", "-i", str(SRC),
        "-f", "rawvideo", "-pix_fmt", "rgba64le", "-s", f"{H}x{W}", "-r", str(FPS),
        "-i", "-",
        "-filter_complex", filtro,
        "-map", "[v]", "-map", "0:a",
        "-fps_mode", "passthrough",
        "-c:v", "libx265", "-preset", "medium", "-crf", "14",
        "-profile:v", "main10", "-tag:v", "hvc1", "-x265-params", x265,
        "-color_primaries", "bt2020", "-color_trc", "arib-std-b67",
        "-colorspace", "bt2020nc", "-color_range", "tv",
        "-c:a", "copy", "-map_metadata", "0",
        "-movflags", "+faststart",
        str(OUT),
    ]  # fmt: skip
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        lienzo = cuadro(i / FPS * k, grande, chico_por_frame).rotate(90, expand=True)
        proc.stdin.write(a_hlg(lienzo).tobytes())
    proc.stdin.close()
    proc.wait()
    print("listo:", OUT, "logo desde", round(inicio, 2), "s")


if __name__ == "__main__":
    main()
