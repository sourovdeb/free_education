#!/usr/bin/env python3
"""Render caption-led history videos from video_storyboards.json.

Usage: python render_videos.py video_storyboards.json --output-dir .
       python render_videos.py --sample --output-dir . --preview-only

Requires Pillow, ffmpeg and ffprobe. No network or image service is used.
Diagrams are schematic illustrations, not reconstructions or evidence.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 25
INK = '#152d35'
PAPER = '#f5f0e6'
PANEL = '#e9e4d8'
TEAL = '#14766f'
OCHRE = '#ba721c'
MUTED = '#53666a'
WHITE = '#ffffff'
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')


def font(size, bold=False):
    path = FONT_DIR / ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')
    return ImageFont.truetype(str(path), size)


def wrap(draw, text, face, width):
    words = str(text).split()
    lines, current = [], ''
    for word in words:
        test = f'{current} {word}'.strip()
        if draw.textlength(test, font=face) > width and current:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)
    return lines


def center(draw, xy, text, face, fill=INK):
    draw.text(xy, text, font=face, fill=fill, anchor='mm')


def arrow(draw, start, end, fill=TEAL, width=4):
    draw.line([start, end], fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    head = [end,
            (end[0] - 12 * math.cos(angle - .5), end[1] - 12 * math.sin(angle - .5)),
            (end[0] - 12 * math.cos(angle + .5), end[1] - 12 * math.sin(angle + .5))]
    draw.polygon(head, fill=fill)


def diagram(draw, kind):
    """Neutral schematics use only generic process or component labels."""
    left, top, right, bottom = 850, 195, 1215, 496
    draw.rounded_rectangle((left, top, right, bottom), radius=18, fill=PANEL)
    center(draw, (1032, 223), 'SCHEMATIC', font(18, True), MUTED)
    if kind == 'network':
        points = [(930, 292), (1135, 292), (1032, 365), (930, 439), (1135, 439)]
        for i in [0, 1, 3, 4]:
            draw.line((points[2], points[i]), fill=TEAL, width=4)
        for x, y in points:
            draw.rounded_rectangle((x - 58, y - 25, x + 58, y + 25), 10, fill=PAPER, outline=TEAL, width=3)
            center(draw, (x, y), 'Branch', font(24, True))
    elif kind == 'ownership':
        for x, label in [(917, 'Family'), (1032, 'Partners'), (1147, 'Investors')]:
            draw.rounded_rectangle((x-54, 274, x+54, 329), 8, fill=PAPER, outline=TEAL, width=2)
            center(draw, (x, 301), label, font(19, True))
            arrow(draw, (x, 337), (1032+(x-1032)*.2, 388))
        draw.rounded_rectangle((947, 395, 1117, 453), 10, fill=TEAL)
        center(draw, (1032, 424), 'Company', font(26, True), PAPER)
    elif kind == 'drill':
        # A tube's cross-section leaves a central stone core.
        draw.rounded_rectangle((888, 339, 1175, 435), 5, fill=OCHRE, outline=INK, width=2)
        draw.rectangle((1005, 339, 1075, 405), fill=PAPER)
        draw.rectangle((1030, 339, 1050, 405), fill=OCHRE)
        draw.rectangle((1008, 276, 1023, 398), fill=TEAL)
        draw.rectangle((1057, 276, 1072, 398), fill=TEAL)
        draw.arc((1008, 265, 1072, 289), 180, 360, fill=TEAL, width=5)
        for x,y in [(1008,402),(1016,405),(1022,401),(1057,403),(1063,406),(1070,402)]:
            draw.ellipse((x-2,y-2,x+2,y+2), fill=INK)
        center(draw, (1134, 292), 'Tube', font(26, True))
        arrow(draw, (1111, 307), (1078, 320), width=2)
        center(draw, (938, 383), 'Stone', font(24, True), PAPER)
        center(draw, (1025, 465), 'Abrasive grains', font(24, True))
        arrow(draw, (1015, 447), (1015, 414), width=2)
    elif kind == 'sled':
        draw.line((875, 426, 1190, 426), fill=OCHRE, width=5)
        for x,y in [(895,438),(935,445),(980,436),(1022,445),(1088,438),(1130,448),(1171,438)]:
            draw.ellipse((x,y,x+3,y+3), fill=OCHRE)
        draw.rounded_rectangle((915, 317, 1080, 382), 4, fill=OCHRE, outline=INK, width=2)
        center(draw, (998, 349), 'Stone', font(25, True), PAPER)
        draw.rectangle((901, 388, 1091, 401), fill=INK)
        draw.line((915, 405, 930, 416, 1074, 416, 1092, 405), fill=INK, width=5)
        arrow(draw, (1095, 394), (1180, 394), width=3)
        center(draw, (1145, 285), 'Water', font(25, True))
        for x,y in [(1124,337),(1155,357),(1174,332)]:
            draw.polygon([(x,y-13),(x-6,y),(x+6,y)], fill=TEAL)
            draw.ellipse((x-6,y-5,x+6,y+7), fill=TEAL)
        center(draw, (1032, 465), 'Sledge and sand', font(24, True))
    elif kind == 'strata':
        colors = [OCHRE, '#d2a469', TEAL, '#83aaa1']
        for i, col in enumerate(colors):
            y = 277 + 34*i
            draw.rectangle((878, y, 995, y+34), fill=col)
            draw.rounded_rectangle((1080, y+3, 1185, y+30), 3, fill=col, outline=INK, width=1)
            arrow(draw, (1008, y+17), (1065, y+17), fill=MUTED, width=2)
        draw.rectangle((878, 277, 995, 413), outline=INK, width=2)
        center(draw, (937, 451), 'Quarry', font(25, True))
        center(draw, (1133, 451), 'Blocks', font(25, True))
    elif kind == 'quarry':
        rock = [(880, 438), (880, 280), (970, 280), (970, 320), (1050, 320),
                (1050, 360), (1140, 360), (1140, 398), (1190, 398), (1190, 438)]
        draw.polygon(rock, fill=OCHRE, outline=INK)
        for p in [(967, 278, 967, 320), (1047, 318, 1047, 360), (1137, 358, 1137, 398)]:
            draw.line(p, fill=PAPER, width=5)
        center(draw, (1035, 463), 'Rock removal', font(26, True))
        arrow(draw, (1100, 271), (1100, 325))
    elif kind == 'tools':
        draw.rounded_rectangle((890, 361, 1175, 436), 9, fill=OCHRE, outline=INK, width=3)
        draw.polygon([(1005, 279), (1030, 270), (1080, 354), (1072, 368)], fill=TEAL)
        draw.line((1040, 260, 995, 307), fill=INK, width=12)
        draw.rounded_rectangle((964, 274, 1005, 314), 5, fill=INK)
        center(draw, (1134, 306), 'Tool', font(26, True))
        center(draw, (1032, 464), 'Stone', font(26, True))
        for x in (1049, 1080, 1098):
            draw.line((x, 347, x - 8, 329), fill=OCHRE, width=3)
    elif kind == 'wax':
        for x, label, col in [(914, 'Wax', OCHRE), (1032, 'Mould', INK), (1150, 'Bronze', TEAL)]:
            if label == 'Mould':
                draw.rounded_rectangle((x - 35, 284, x + 35, 397), 8, fill=col)
                draw.ellipse((x - 15, 298, x + 15, 328), fill=PAPER)
                draw.polygon([(x - 10, 328), (x + 10, 328), (x + 20, 382), (x - 20, 382)], fill=PAPER)
                draw.rectangle((x - 4, 282, x + 4, 300), fill=PAPER)
            else:
                draw.ellipse((x - 16, 298, x + 16, 330), fill=col)
                draw.polygon([(x - 10, 330), (x + 10, 330), (x + 25, 382), (x - 25, 382)], fill=col)
                draw.rectangle((x - 31, 382, x + 31, 393), fill=col)
            center(draw, (x, 430), label, font(24, True))
        arrow(draw, (953, 345), (989, 345))
        arrow(draw, (1071, 345), (1107, 345))
    elif kind == 'bank':
        draw.polygon([(891, 297), (1032, 254), (1173, 297)], fill=INK)
        draw.rectangle((891, 303, 1173, 316), fill=TEAL)
        for x in [918, 984, 1050, 1116]:
            draw.rectangle((x, 323, x + 30, 393), fill=INK)
        draw.rectangle((891, 401, 1173, 416), fill=INK)
        center(draw, (1032, 459), 'Finance', font(27, True))
    elif kind == 'temple':
        draw.rectangle((903, 397, 1161, 415), fill=INK)
        draw.rectangle((925, 329, 1139, 397), fill=OCHRE)
        for x in [944, 1001, 1058, 1115]:
            draw.rectangle((x, 347, x + 10, 397), fill=PAPER)
        for i, (width, y) in enumerate([(240, 318), (186, 297), (132, 276), (76, 255)]):
            draw.rectangle((1032-width/2, y, 1032+width/2, y+19), fill=INK)
        center(draw, (1032, 460), 'Temple form', font(26, True))
    else:
        for x, label in [(927, 'Claim'), (1137, 'Record')]:
            draw.rounded_rectangle((x - 64, 275, x + 64, 335), 9, fill=PAPER, outline=INK, width=3)
            center(draw, (x, 305), label, font(25, True))
        arrow(draw, (927, 344), (1007, 389))
        arrow(draw, (1137, 344), (1057, 389))
        draw.rounded_rectangle((947, 390, 1117, 448), 10, fill=TEAL)
        center(draw, (1032, 419), 'Assess', font(28, True), PAPER)


def timeline(draw, items, active, track_label='Timeline · spacing schematic'):
    items = items[:5]
    draw.line((65, 561, 1215, 561), fill='#d2d6ce', width=2)
    label_width = draw.textlength(track_label, font=font(16, True))
    draw.rectangle((630-label_width/2, 551, 650+label_width/2, 568), fill=PAPER)
    center(draw, (640, 559), track_label, font(16, True), MUTED)
    if not items:
        center(draw, (640, 605), 'Sources accompany this video.', font(26), MUTED)
        return
    xs = [640] if len(items) == 1 else [100 + i * 1080 / (len(items) - 1) for i in range(len(items))]
    draw.line((xs[0], 603, xs[-1], 603), fill='#c1cac3', width=4)
    for i, (x, item) in enumerate(zip(xs, items)):
        color = TEAL if i <= active else MUTED
        r = 8 if i == active else 5
        draw.ellipse((x-r, 603-r, x+r, 603+r), fill=color)
        center(draw, (x, 583), str(item.get('date', '')), font(24, i == active), color)
        lines = wrap(draw, item.get('label', ''), font(22), 196)
        if len(lines) > 2:
            raise ValueError('Timeline labels must fit two lines.')
        for n, label in enumerate(lines):
            center(draw, (x, 631 + n*25), label, font(22, i == active), color)


def scene_image(video, scene, index, elapsed, total):
    canvas = Image.new('RGB', (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, W, 85), fill=INK)
    video_title = str(video['title'])
    title_face = font(27, True)
    while draw.textlength(video_title, font=title_face) > 1030 and title_face.size > 21:
        title_face = font(title_face.size - 1, True)
    if draw.textlength(video_title, font=title_face) > 1030:
        raise ValueError('Video title exceeds header width.')
    draw.text((65, 24), video_title, font=title_face, fill=PAPER)
    draw.text((1215, 33), f'{index+1:02d} / {len(video["scenes"]):02d}', font=font(22), fill=PAPER, anchor='rm')
    status = str(scene.get('status', 'Evidence review')).upper()
    date = str(scene.get('date', ''))
    draw.text((65, 103), status, font=font(21, True), fill=TEAL)
    draw.text((1215, 103), date, font=font(24, True), fill=OCHRE, anchor='ra')
    headings = wrap(draw, scene['title'], font(43, True), 752)
    if len(headings) > 2:
        raise ValueError(f'Scene title exceeds two lines: {scene["title"]}')
    for n, heading in enumerate(headings):
        draw.text((65, 145+n*54), heading, font=font(43, True), fill=INK)
    body_y = 271 if len(headings) > 1 else 250
    body_lines = []
    for line in scene.get('lines', []):
        body_lines.extend(wrap(draw, line, font(32), 738))
    if len(body_lines) > 5:
        raise ValueError(f'Scene body exceeds five display lines: {scene["title"]}')
    for n, line in enumerate(body_lines):
        draw.text((65, body_y+n*44), line, font=font(32), fill=INK)
    diagram(draw, scene.get('diagram', 'evidence'))
    src = str(scene.get('source', ''))
    source_lines = wrap(draw, f'SOURCE  {src}', font(18), 1120)
    if len(source_lines) > 2:
        raise ValueError('Source line exceeds two lines; use a short source name.')
    for n, line in enumerate(source_lines):
        draw.text((65, 509 + n * 22), line, font=font(18), fill=MUTED)
    timeline(draw, scene.get('timeline', []), int(scene.get('active', 0)),
             scene.get('track_label', 'Timeline · spacing schematic'))
    draw.rectangle((0, 680, W, 687), fill='#d2d6ce')
    draw.rectangle((0, 688, W, H), fill=INK)
    draw.text((65, 695), 'CAPTIONS • NO AUDIO', font=font(13, True), fill=PAPER)
    center(draw, (640, 704), 'Timeline spacing is schematic.', font(13), PAPER)
    draw.text((1215, 695), f'SCENE START {elapsed:03.0f}s • {total:03.0f}s TOTAL', font=font(13), fill=PAPER, anchor='ra')
    return canvas


def timestamp(seconds):
    ms = int(round(seconds * 1000))
    return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d}.{ms%1000:03d}'


def write_vtt(video, path):
    output, elapsed = ['WEBVTT', ''], 0
    for i, scene in enumerate(video['scenes']):
        end = elapsed + float(scene.get('duration', 15))
        caption = '\n'.join([str(scene.get('date', '')), scene['title']] + scene.get('lines', []))
        output.extend([str(i+1), f'{timestamp(elapsed)} --> {timestamp(end)}', caption.strip(), ''])
        elapsed = end
    path.write_text('\n'.join(output), encoding='utf-8')


def render(video, output_dir, preview_only=False, crf=29):
    identifier = str(video['id'])
    if not re.fullmatch(r'[A-Za-z0-9_-]+', identifier):
        raise ValueError('Video id must be a filename-safe identifier.')
    scenes = video['scenes']
    if not scenes:
        raise ValueError('At least one scene is required.')
    total = sum(float(s.get('duration', 15)) for s in scenes)
    if total <= 0:
        raise ValueError('Video duration must be positive.')
    output_dir.mkdir(parents=True, exist_ok=True)
    pngs, elapsed = [], 0
    thumb_w, thumb_h = 640, 360
    sheet = Image.new('RGB', (thumb_w*2, thumb_h*math.ceil(len(scenes)/2)), INK)
    with tempfile.TemporaryDirectory(prefix=f'{identifier}_render_') as folder:
        temp = Path(folder)
        marker = Image.new('RGBA', (W, 8), TEAL)
        ImageDraw.Draw(marker).rounded_rectangle((W-14, 0, W-1, 7), 3, fill=OCHRE)
        marker.save(temp / 'marker.png')
        for i, scene in enumerate(scenes):
            frame = scene_image(video, scene, i, elapsed, total)
            frame.save(temp / f'scene_{i:02d}.png')
            sheet.paste(frame.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS), ((i%2)*thumb_w, (i//2)*thumb_h))
            pngs.append(temp / f'scene_{i:02d}.png')
            elapsed += float(scene.get('duration', 15))
        contact = output_dir / f'{identifier}_contact_sheet.jpg'
        sheet.save(contact, quality=94)
        write_vtt(video, output_dir / f'{identifier}.vtt')
        if preview_only:
            print(json.dumps({'id': identifier, 'contact_sheet': str(contact), 'duration': total}), flush=True)
            return
        parts, elapsed = [], 0
        for i, (scene, png) in enumerate(zip(scenes, pngs)):
            duration = float(scene.get('duration', 15))
            if duration <= 0:
                raise ValueError('Every scene requires positive duration.')
            dest = temp / f'part_{i:02d}.mp4'
            # The marker is playback progress, separate from dated timeline nodes.
            xpos = f'min(0,-1280+1280*({elapsed}+t)/{total})'
            filters = f'[0:v][1:v]overlay=x=\'{xpos}\':y=680:eval=frame:shortest=1,format=yuv420p[v]'
            cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                   '-loop', '1', '-framerate', str(FPS), '-i', str(png),
                   '-loop', '1', '-framerate', str(FPS), '-i', str(temp/'marker.png'),
                   '-filter_complex', filters, '-map', '[v]', '-t', str(duration),
                   '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-tune', 'stillimage',
                   '-crf', str(crf), '-pix_fmt', 'yuv420p', '-r', str(FPS),
                   '-threads', '2', '-filter_complex_threads', '1', str(dest)]
            subprocess.run(cmd, check=True)
            parts.append(dest)
            elapsed += duration
        concat_file = temp/'concat.txt'
        concat_file.write_text(''.join(f"file '{p}'\n" for p in parts), encoding='utf-8')
        destination = output_dir/f'{identifier}.mp4'
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                        '-f', 'concat', '-safe', '0', '-i', str(concat_file), '-c', 'copy',
                        '-movflags', '+faststart', str(destination)], check=True)
        info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
                          '-show_entries', 'format=duration,size:stream=codec_name,width,height,pix_fmt,r_frame_rate',
                          '-of', 'json', str(destination)]))
        print(json.dumps({'id': identifier, 'mp4': str(destination), 'contact_sheet': str(contact),
                          'verification': info}), flush=True)


def sample_video():
    items = [{'date': 'c. 2500 BCE', 'label': 'Stone carving'}, {'date': 'c. 800 CE', 'label': 'Rock cutting'},
             {'date': 'c. 1000 CE', 'label': 'Bronze casting'}, {'date': '1800s', 'label': 'Finance'},
             {'date': 'Today', 'label': 'Evidence'}]
    kinds = ['tools', 'quarry', 'wax', 'temple', 'network', 'bank', 'evidence', 'evidence']
    scenes = []
    for i, kind in enumerate(kinds):
        scenes.append({'duration': 15, 'date': 'PREVIEW', 'title': ['How were sculptures made?', 'Carving removes the rock.',
            'Casting replaces the wax.', 'Process leaves physical traces.', 'Branches form a network.',
            'Finance creates influence.', 'Claims require supporting records.', 'Questions remain open.'][i],
            'lines': ['This is a layout preview.', 'Labels illustrate the design.', 'Evidence belongs in the sources.', 'Timelines provide the context.'],
            'status': 'Renderer preview', 'source': 'Preview only; no historical claims.', 'diagram': kind,
            'timeline': items, 'active': min(i, 4)})
    return {'id': 'renderer_preview', 'title': 'History • Evidence and influence',
            'subtitle': 'Renderer demonstration', 'scenes': scenes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('storyboards', nargs='?', type=Path)
    parser.add_argument('--output-dir', type=Path, default=Path('.'))
    parser.add_argument('--preview-only', action='store_true')
    parser.add_argument('--sample', action='store_true')
    parser.add_argument('--crf', type=int, default=29)
    args = parser.parse_args()
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        parser.error('ffmpeg and ffprobe are required.')
    if args.sample:
        videos = [sample_video()]
    elif args.storyboards:
        videos = json.loads(args.storyboards.read_text(encoding='utf-8'))
        if isinstance(videos, dict):
            videos = videos.get('videos', [videos])
    else:
        parser.error('Provide storyboards JSON, or --sample.')
    for video in videos:
        render(video, args.output_dir, args.preview_only, args.crf)


if __name__ == '__main__':
    main()
