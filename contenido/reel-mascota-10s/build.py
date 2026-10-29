# /// script
# dependencies = ["imageio-ffmpeg", "pillow", "numpy"]
# ///
"""Reel Bonaterra 10 s: clip IA de la mascota (8 s) + cierre con logo (2 s) + música.

uv run build.py
"""

import subprocess
import wave
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 1080, 1920, 30
CREMA, SALVIA, OSCURO = (248, 242, 230), (133, 150, 111), (99, 115, 86)
AVENIR = "/System/Library/Fonts/Avenir Next.ttc"
CLIP, CLIP_S, OUTRO_S = AQUI / "clip_ia.mp4", 8.0, 2.0

TEXTOS = [  # (inicio, fin, texto) sobre el clip
    (0.3, 3.6, "¿Tu proyecto\nnecesita tableros?"),
    (4.2, 7.8, "Melamina · MDF · Triplay\nWPC · PVC mármol"),
]


def font(size, idx=0):  # 0 = Bold, 5 = Medium (Avenir Next)
    return ImageFont.truetype(AVENIR, size, index=idx)


def pastilla(texto, size=64):
    f = font(size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    x0, y0, x1, y1 = tmp.multiline_textbbox((0, 0), texto, font=f, align="center", spacing=14)
    pw, ph = int(x1 - x0 + 90), int(y1 - y0 + 70)
    im = Image.new("RGBA", (pw, ph))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, pw - 1, ph - 1), radius=38, fill=SALVIA + (240,))
    d.multiline_text((pw / 2, ph / 2), texto, font=f, fill=CREMA, anchor="mm", align="center", spacing=14)
    return im


def overlay(i, t):
    nombre = AQUI / f"ov{i}.png"
    lienzo = Image.new("RGBA", (W, H))
    p = pastilla(t)
    lienzo.alpha_composite(p, ((W - p.width) // 2, 230))
    lienzo.save(nombre)
    return nombre


def outro():
    im = Image.new("RGB", (W, H), CREMA)
    logo = Image.open(AQUI.parent / "assets/logo-circular.png").convert("RGBA")
    logo = logo.resize((620, 620), Image.LANCZOS)
    im.paste(logo, ((W - 620) // 2, 470), logo)
    d = ImageDraw.Draw(im)
    d.text((W / 2, 1220), "Todo en tableros, en un solo lugar", font=font(56), fill=OSCURO, anchor="mm")
    d.rounded_rectangle((190, 1330, W - 190, 1450), radius=60, fill=SALVIA)
    d.text((W / 2, 1390), "¡Cotiza por WhatsApp!", font=font(54), fill=CREMA, anchor="mm")
    d.text((W / 2, 1560), "Aguascalientes", font=font(40, 5), fill=OSCURO, anchor="mm")
    im.save(AQUI / "outro.png")


def musica(dur):
    sr = 44100
    t = np.arange(int(sr * dur)) / sr
    bpm = 112
    beat = 60 / bpm
    y = np.zeros_like(t)
    # bombo suave + hi-hat + acordes tipo pluck (Do mayor alegre)
    for k in np.arange(0, dur, beat):
        i = int(k * sr)
        n = min(len(t) - i, int(0.25 * sr))
        tt = np.arange(n) / sr
        y[i : i + n] += 0.5 * np.sin(2 * np.pi * (55 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 12)
        j = int((k + beat / 2) * sr)
        if j < len(t):
            m = min(len(t) - j, int(0.05 * sr))
            y[j : j + m] += 0.06 * np.random.default_rng(j).standard_normal(m) * np.exp(-np.arange(m) / sr * 80)
    acordes = [[261.6, 329.6, 392.0], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 392.0]]
    for b, k in enumerate(np.arange(0, dur, beat / 2)):
        i = int(k * sr)
        n = min(len(t) - i, int(0.4 * sr))
        tt = np.arange(n) / sr
        f = acordes[(b // 8) % 4][b % 3]
        y[i : i + n] += 0.12 * np.sin(2 * np.pi * f * 2 * tt) * np.exp(-tt * 9)
    # "whoosh" al entrar el cierre
    i0 = int((CLIP_S - 0.35) * sr)
    n = int(0.7 * sr)
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    y[i0 : i0 + n] += 0.25 * np.random.default_rng(1).standard_normal(n) * env
    y *= np.clip((dur - t) / 0.6, 0, 1)  # fade out
    y = (y / np.abs(y).max() * 0.8 * 32767).astype(np.int16)
    with wave.open(str(AQUI / "musica.wav"), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(y.tobytes())


def ff(*args):
    subprocess.run([FF, "-y", "-loglevel", "error", *map(str, args)], check=True)


def main():
    outro()
    musica(CLIP_S + OUTRO_S)
    ovs = [overlay(i, t) for i, (_, _, t) in enumerate(TEXTOS)]
    enc = ["-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-r", FPS]
    # 1) clip IA con textos
    ins, fc, prev = ["-i", CLIP], [], "0:v"
    fc.append(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1[b]")
    prev = "b"
    for i, ((a, b, _), o) in enumerate(zip(TEXTOS, ovs)):
        ins += ["-loop", "1", "-t", CLIP_S, "-i", o]
        fc.append(f"[{i + 1}:v]format=rgba,fade=in:st={a}:d=0.25:alpha=1,fade=out:st={b - 0.25}:d=0.25:alpha=1[o{i}]")
        fc.append(f"[{prev}][o{i}]overlay=0:0:shortest=1[v{i}]")
        prev = f"v{i}"
    ff(*ins, "-filter_complex", ";".join(fc), "-map", f"[{prev}]", "-t", CLIP_S, "-an", *enc, AQUI / "_a.mp4")
    # 2) cierre con zoom suave
    n = int(OUTRO_S * FPS)
    ff("-loop", "1", "-i", AQUI / "outro.png", "-vf",
       f"scale=2160:3840,zoompan=z='1.10-0.10*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={n}:s={W}x{H}:fps={FPS},setsar=1",
       "-frames:v", n, *enc, AQUI / "_b.mp4")
    # 3) transición + música
    total = CLIP_S + OUTRO_S - 0.4
    ff("-i", AQUI / "_a.mp4", "-i", AQUI / "_b.mp4", "-i", AQUI / "musica.wav", "-filter_complex",
       f"[0:v][1:v]xfade=transition=zoomin:duration=0.4:offset={CLIP_S - 0.4}[v]",
       "-map", "[v]", "-map", "2:a", *enc, "-preset", "slow", "-c:a", "aac", "-b:a", "192k",
       "-t", total, "-movflags", "+faststart", AQUI / "reel_bonaterra_mascota.mp4")


if __name__ == "__main__":
    main()
