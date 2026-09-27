#!/usr/bin/env python3
"""Render a silent six-chapter doodle video from lesson.json.

Runtime requirements:
  - Python 3
  - Pillow
  - ffmpeg on PATH

The offline lesson viewer has no dependencies.
"""

from __future__ import annotations

import json
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "lesson.json").read_text(encoding="utf-8"))
OUTPUT = ROOT / "history-investigation.mp4"
W, H = 1280, 720
SOURCE_FPS = 10
OUTPUT_FPS = int(DATA["video"]["fps"])
DURATION = int(DATA["video"]["duration_seconds"])
INTRO = 6
CHAPTER = 32
OUTRO = DURATION - INTRO - CHAPTER * len(DATA["chapters"])
assert OUTRO >= 0

FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


F12 = font(12, True)
F16 = font(16, True)
F18 = font(18)
F20 = font(20, True)
F24 = font(24)
F28 = font(28, True)
F34 = font(34, True)
F44 = font(44, True)
F58 = font(58, True)


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def reveal(local: float, start: float, length: float = 1.5) -> float:
    return ease((local - start) / length)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if draw.textbbox((0, 0), test, font=fnt)[2] <= width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text(draw, xy, value, fnt, max_width=None, spacing=8, fill=0, anchor=None):
    if max_width is None:
        draw.text(xy, value, font=fnt, fill=fill, anchor=anchor)
        return
    x, y = xy
    for line in wrap(draw, value, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing


def rough_line(draw, points, width=4, progress=1.0, seed=0):
    if len(points) < 2 or progress <= 0:
        return
    lengths = []
    total = 0.0
    for a, b in zip(points, points[1:]):
        d = math.dist(a, b)
        lengths.append(d)
        total += d
    target = total * min(progress, 1)
    rng = random.Random(seed)
    drawn = 0.0
    for idx, (a, b, seg) in enumerate(zip(points, points[1:], lengths)):
        if drawn >= target:
            break
        part = min(1.0, (target - drawn) / seg)
        end = (a[0] + (b[0] - a[0]) * part, a[1] + (b[1] - a[1]) * part)
        jitter = [(a[0] + rng.uniform(-1.3, 1.3), a[1] + rng.uniform(-1.3, 1.3)),
                  (end[0] + rng.uniform(-1.3, 1.3), end[1] + rng.uniform(-1.3, 1.3))]
        draw.line(jitter, fill=0, width=width)
        drawn += seg


def rough_box(draw, box, progress=1.0, width=4, seed=0):
    x1, y1, x2, y2 = box
    pts = [(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)]
    rough_line(draw, pts, width, progress, seed)


def arrow(draw, start, end, progress, seed=0):
    rough_line(draw, [start, end], 5, progress, seed)
    if progress > .92:
        ang = math.atan2(end[1] - start[1], end[0] - start[0])
        for off in (.65, -.65):
            tip = (end[0] - 18 * math.cos(ang + off), end[1] - 18 * math.sin(ang + off))
            rough_line(draw, [tip, end], 5, 1, seed + int(off * 10))


def circle(draw, center, radius, progress=1.0, width=4, seed=0):
    pts = []
    rng = random.Random(seed)
    count = 72
    for i in range(count + 1):
        a = math.tau * i / count
        r = radius + rng.uniform(-1.5, 1.5)
        pts.append((center[0] + math.cos(a) * r, center[1] + math.sin(a) * r))
    rough_line(draw, pts, width, progress, seed + 1)


def icon_newspaper(draw, x, y, p):
    rough_box(draw, (x, y, x + 190, y + 135), p, 5, 11)
    rough_line(draw, [(x + 18, y + 25), (x + 170, y + 25)], 6, reveal(p, .15, .35), 12)
    for i in range(4):
        rough_line(draw, [(x + 22, y + 50 + i * 18), (x + 160 - (i % 2) * 30, y + 50 + i * 18)], 3, reveal(p, .32 + i * .08, .3), 20 + i)


def icon_scroll(draw, x, y, p):
    rough_line(draw, [(x + 24, y + 12), (x + 170, y + 12), (x + 170, y + 125), (x + 24, y + 125), (x + 24, y + 12)], 5, p, 31)
    circle(draw, (x + 24, y + 12), 13, reveal(p, .18, .25), 4, 32)
    circle(draw, (x + 170, y + 125), 13, reveal(p, .35, .25), 4, 33)
    for i in range(4):
        rough_line(draw, [(x + 47, y + 38 + i * 18), (x + 148, y + 38 + i * 18)], 3, reveal(p, .45 + i * .08, .28), 35 + i)


def icon_table(draw, x, y, p):
    rough_line(draw, [(x + 20, y + 82), (x + 180, y + 82)], 7, p, 41)
    rough_line(draw, [(x + 55, y + 82), (x + 40, y + 135)], 5, reveal(p, .2, .3), 42)
    rough_line(draw, [(x + 145, y + 82), (x + 160, y + 135)], 5, reveal(p, .25, .3), 43)
    for i, cx in enumerate((45, 85, 125, 165)):
        circle(draw, (x + cx, y + 34), 16, reveal(p, .35 + i * .08, .3), 4, 44 + i)
        rough_line(draw, [(x + cx, y + 50), (x + cx, y + 75)], 4, reveal(p, .5 + i * .06, .3), 48 + i)


def icon_umbrella(draw, x, y, p):
    pts = [(x + 20, y + 72), (x + 45, y + 38), (x + 80, y + 20), (x + 120, y + 20), (x + 155, y + 38), (x + 180, y + 72)]
    rough_line(draw, pts, 5, p, 51)
    for cx in (45, 85, 125, 155):
        circle(draw, (x + cx, y + 78), 10, reveal(p, .3, .3), 3, 52 + cx)
    rough_line(draw, [(x + 100, y + 20), (x + 100, y + 120), (x + 84, y + 132), (x + 72, y + 120)], 5, reveal(p, .4, .5), 54)


def icon_gear(draw, x, y, p):
    center = (x + 100, y + 70)
    pts = []
    for i in range(25):
        a = math.tau * i / 24
        r = 68 if i % 2 == 0 else 52
        pts.append((center[0] + math.cos(a) * r, center[1] + math.sin(a) * r))
    rough_line(draw, pts, 5, p, 61)
    circle(draw, center, 20, reveal(p, .35, .35), 5, 62)
    rough_line(draw, [(x + 100, y + 70), (x + 168, y + 30)], 4, reveal(p, .55, .35), 63)


def icon_chatbot(draw, x, y, p):
    rough_box(draw, (x + 20, y + 12, x + 180, y + 112), p, 5, 71)
    rough_line(draw, [(x + 78, y + 112), (x + 62, y + 137), (x + 105, y + 112)], 5, reveal(p, .25, .25), 72)
    circle(draw, (x + 72, y + 60), 8, reveal(p, .4, .25), 5, 73)
    circle(draw, (x + 128, y + 60), 8, reveal(p, .48, .25), 5, 74)
    rough_line(draw, [(x + 72, y + 86), (x + 128, y + 86)], 4, reveal(p, .58, .3), 75)


ICONS = {
    "newspaper": icon_newspaper,
    "scroll": icon_scroll,
    "table": icon_table,
    "umbrella": icon_umbrella,
    "gear": icon_gear,
    "chatbot": icon_chatbot,
}


def header(draw, chapter_index: int):
    text(draw, (48, 26), "HISTORY INVESTIGATION", F16)
    for i in range(6):
        x = 1000 + i * 38
        circle(draw, (x, 35), 10, 1, 2, 100 + i)
        if i <= chapter_index:
            draw.ellipse((x - 5, 30, x + 5, 40), fill=0)
    rough_line(draw, [(48, 58), (1232, 58)], 3, 1, 120)


def intro_frame(t: float) -> Image.Image:
    im = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(im)
    p = reveal(t, .3, 2.3)
    rough_line(d, [(90, 155), (1180, 155)], 6, p, 201)
    if t > 1:
        text(d, (90, 205), "LABELS, LAW,", F58)
    if t > 2:
        text(d, (90, 277), "AND AGENCY", F58)
    if t > 3:
        text(d, (94, 380), "Six evidence-led chapters.", F28)
        text(d, (94, 425), "Facts. Interpretation. Limits.", F28)
    if t > 4:
        rough_box(d, (90, 520, 1190, 610), reveal(t, 4, 1), 5, 202)
        text(d, (120, 548), "Silent visual summary · 1280×720 · 25fps", F24)
    return im


def chapter_frame(chapter, idx: int, local: float) -> Image.Image:
    im = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(im)
    header(d, idx)
    text(d, (48, 82), f"CHAPTER {idx + 1:02d}", F16)
    if local > .4:
        title_lines = wrap(d, chapter["short_title"].upper(), F44, 620)
        y = 118
        for line in title_lines:
            text(d, (48, y), line, F44)
            y += 54
    icon_p = reveal(local, 1.2, 3.2)
    ICONS[chapter["visual"]["icon"]](d, 860, 105, icon_p)
    if local > 3.8:
        rough_line(d, [(48, 225), (1232, 225)], 3, reveal(local, 3.8, 1), 220 + idx)
    steps = chapter["visual"]["steps"]
    x0, y0, bw, gap = 48, 275, 260, 44
    for i, step in enumerate(steps):
        start = 5 + i * 3.1
        p = reveal(local, start, 1.2)
        box = (x0 + i * (bw + gap), y0, x0 + i * (bw + gap) + bw, y0 + 120)
        rough_box(d, box, p, 4, 300 + idx * 20 + i)
        if p > .65:
            text(d, (box[0] + 16, box[1] + 28), step, F20, bw - 32, 5)
        if i < 3:
            arrow(d, (box[2] + 6, y0 + 60), (box[2] + gap - 7, y0 + 60), reveal(local, start + 1.2, 1), 350 + idx * 20 + i)
    if local > 17:
        text(d, (48, 430), chapter["visual"]["caption"], F34, 1160)
        rough_line(d, [(48, 478), (min(1180, 48 + 18 * len(chapter["visual"]["caption"])), 478)], 5, reveal(local, 17, 1.5), 400 + idx)
    labels = [
        ("DOCUMENTED", chapter["documented_fact"].split(".")[0] + "."),
        ("INTERPRETATION", chapter["scholarly_interpretation"].split(".")[0] + "."),
        ("UNCERTAINTY", chapter["uncertainty"].split(".")[0] + "."),
    ]
    for i, (label, sentence) in enumerate(labels):
        start = 20 + i * 2.6
        p = reveal(local, start, .9)
        x = 48 + i * 400
        rough_box(d, (x, 525, x + 365, 650), p, 3, 500 + idx * 10 + i)
        if p > .65:
            text(d, (x + 16, 543), label, F12)
            text(d, (x + 16, 575), sentence, F18, 330, 4)
    if local > 28:
        text(d, (1060, 680), "NEXT →", F16)
    return im


def outro_frame(t: float) -> Image.Image:
    im = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(im)
    text(d, (70, 70), "READ THE RECORD.", F44)
    if t > 1:
        text(d, (70, 132), "TEST THE INTERPRETATION.", F44)
    if t > 2:
        text(d, (70, 194), "KEEP THE LIMITS.", F44)
    y = 300
    for i, chapter in enumerate(DATA["chapters"]):
        if t > 2.7 + i * .75:
            circle(d, (88, y + i * 48), 9, 1, 3, 700 + i)
            text(d, (115, y - 11 + i * 48), chapter["short_title"], F24)
    if t > 8:
        rough_box(d, (70, 620, 1210, 685), reveal(t, 8, 1), 4, 750)
        text(d, (95, 639), "Full bodies, sources, viewer, and SVG accompany this video.", F20)
    return im


def frame_at(t: float) -> Image.Image:
    if t < INTRO:
        return intro_frame(t)
    body = t - INTRO
    index = int(body // CHAPTER)
    if index < len(DATA["chapters"]):
        return chapter_frame(DATA["chapters"][index], index, body % CHAPTER)
    return outro_frame(t - INTRO - CHAPTER * len(DATA["chapters"]))


def main() -> int:
    if not shutil.which("ffmpeg"):
        print("ERROR: ffmpeg is required.", file=sys.stderr)
        return 2
    command = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}",
        "-r", str(SOURCE_FPS), "-i", "-",
        "-vf", f"fps={OUTPUT_FPS},format=yuv420p",
        "-frames:v", str(DURATION * OUTPUT_FPS),
        "-c:v", "libx264", "-preset", "medium", "-tune", "animation", "-crf", "36",
        "-movflags", "+faststart", "-an",
        "-metadata", f"title={DATA['title']}",
        "-metadata", "comment=Silent progressive doodle visual summary",
        str(OUTPUT),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    total = DURATION * SOURCE_FPS
    try:
        for i in range(total):
            process.stdin.write(frame_at(i / SOURCE_FPS).tobytes())
            if i and i % (30 * SOURCE_FPS) == 0:
                print(f"Rendered {i / SOURCE_FPS:.0f}s / {DURATION}s", flush=True)
    except BrokenPipeError:
        process.stdin.close()
        process.wait()
        return process.returncode or 1
    process.stdin.close()
    code = process.wait()
    if code:
        return code
    print(f"Created {OUTPUT.name}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
