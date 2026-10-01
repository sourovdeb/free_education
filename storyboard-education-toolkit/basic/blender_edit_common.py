"""Shared Blender 5.x VSE helpers for the Sourov Resolve-to-Blender drafts.

Run from Blender: blender --background --factory-startup --python SCRIPT -- [args]
"""
import bpy
import csv
import json
import os
import sys
from pathlib import Path


def cli():
    args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    if not args:
        raise SystemExit('Missing command line arguments; see the script --help text.')
    return args


def parse_srt(path):
    if not path:
        return []
    import re
    raw = Path(path).read_text(encoding='utf-8-sig')
    cues = []
    for block in re.split(r'\r?\n\s*\r?\n', raw.strip()):
        lines = block.splitlines()
        if len(lines) < 3 or '-->' not in lines[1]:
            continue
        def seconds(value):
            h, m, tail = value.strip().replace(',', '.').split(':')
            return int(h)*3600 + int(m)*60 + float(tail)
        a, b = (seconds(x) for x in lines[1].split('-->'))
        cues.append((a, b, '\n'.join(lines[2:])))
    return cues


def cues_from_resolve_csv(path, fps=25.0, timeline_origin=None):
    """Read preserved recognized wording. Normalize Resolve absolute frame numbers."""
    with open(path, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return []
    first = (min(int(r['start_frame']) for r in rows) // int(fps) * int(fps)
             if timeline_origin is None else timeline_origin)
    return [(max(0, (int(r['start_frame'])-first)/fps),
             max(0, (int(r['end_frame'])-first)/fps), r['original_text']) for r in rows]


def cues_from_resolve_receipt(path, fps=25.0):
    """Convert subtitle geometry in a Resolve first-pass run.json into VSE cues."""
    state = json.loads(Path(path).read_text(encoding='utf-8'))
    rows = [r for r in state.get('geometry', []) if r[0] == 'subtitle']
    if not rows:
        raise ValueError('Resolve run receipt contains no subtitle geometry.')
    origin = (min(int(r[2]) for r in rows) // int(fps)) * int(fps)
    return [(max(0, (int(r[2])-origin)/fps), max(0, (int(r[3])-origin)/fps), str(r[4]))
            for r in rows]


def reviewed_keep_ranges(review_csv, plan_json, media):
    """Verify a Resolve source-bound cut plan, then return retained source ranges."""
    media = Path(media).resolve()
    plan = json.loads(Path(plan_json).read_text(encoding='utf-8'))
    source = plan.get('source', {})
    if Path(source.get('path', '')).resolve() != media:
        raise ValueError('Cut plan source path does not match the supplied video.')
    stat = media.stat()
    if int(source.get('bytes', -1)) != stat.st_size or int(source.get('mtime_ns', -1)) != stat.st_mtime_ns:
        raise ValueError('Video changed since the Resolve cut plan was created.')
    total = int(source['frames'])
    with open(review_csv, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    proposed = plan.get('cuts', [])
    if len(rows) != len(proposed):
        raise ValueError('Cut review row count differs from the source-bound plan.')
    removed = []
    for i, (row, cut) in enumerate(zip(rows, proposed), 1):
        a, b = int(cut[0]), int(cut[1])
        if int(row['cut_id']) != i or int(row['start_frame']) != a or int(row['end_frame_exclusive']) != b:
            raise ValueError('Cut review IDs or frame boundaries changed; no edit built.')
        decision = row['decision'].strip().upper()
        if decision not in ('CUT', 'KEEP'):
            raise ValueError('Cut decisions must be CUT or KEEP.')
        if decision == 'CUT': removed.append((a, b))
    keep, pos = [], 0
    for a, b in sorted(removed):
        if a > pos: keep.append((pos, a))
        pos = max(pos, b)
    if pos < total: keep.append((pos, total))
    if not keep: raise ValueError('Review removes the entire recording.')
    return keep, float(source.get('fps') or 25)


def build_project(media, out_blend, title, subtitles=(), fps=25, width=1920, height=1080,
                  cuts=(), storyboard_glb=None, preview_frame=None, overwrite=False):
    media = str(Path(media).resolve())
    if not os.path.isfile(media):
        raise FileNotFoundError(media)
    out_blend = Path(out_blend).resolve()
    out_blend.parent.mkdir(parents=True, exist_ok=True)
    protected = [out_blend, out_blend.with_suffix('.json')]
    if storyboard_glb:
        protected.append(out_blend.with_name('storyboard_open_book.png'))
    existing = [path for path in protected if path.exists()]
    if existing and not overwrite:
        raise FileExistsError('Output already exists; add --overwrite to replace it: ' + ', '.join(map(str, existing)))
    scene = bpy.context.scene
    scene.name = title
    for other in list(bpy.data.scenes):
        if other != scene:
            bpy.data.scenes.remove(other)
    bpy.context.window.scene = scene
    scene.render.resolution_x, scene.render.resolution_y = width, height
    scene.render.resolution_percentage = 100
    scene.render.fps = int(fps)
    scene.render.image_settings.file_format = 'PNG'
    scene.render.engine = 'BLENDER_EEVEE'
    scene.view_settings.view_transform = 'Standard'
    scene.sequence_editor_create()
    strips = scene.sequence_editor.strips
    cursor = 1
    if cuts:
        for i, (a, b) in enumerate(cuts):
            if b <= a:
                continue
            strip = strips.new_movie(f'Video {i+1:03d}', media, 1, cursor, fit_method='FIT')
            strip.frame_offset_start = int(a)
            strip.frame_offset_end = max(0, strip.frame_duration-int(b))
            strip.frame_start = cursor-int(a)
            segment_len = int(strip.frame_final_duration)
            audio = strips.new_sound(f'Audio {i+1:03d}', media, 2, cursor)
            audio.frame_offset_start = int(a)
            audio.frame_offset_end = max(0, audio.frame_duration-int(b))
            audio.frame_start = cursor-int(a)
            # Some MP4s report the audio stream a couple of frames shorter than
            # the video stream. Match strip boundaries and pad that tail with silence.
            audio.frame_final_duration = segment_len
            cursor += segment_len
    else:
        strip = strips.new_movie('Source video - preserved', media, 1, 1, fit_method='FIT')
        cursor = strip.frame_final_duration + 1
        strips.new_sound('Source audio - preserved', media, 2, 1)
    scene.frame_start, scene.frame_end = 1, max(2, cursor-1)
    # Readable 2D captions and a restrained opening slate, all editable VSE text strips.
    for i, (a, b, text) in enumerate(subtitles):
        start = max(1, 1 + round(a*fps))
        end = max(start+1, 1 + round(b*fps))
        st = strips.new_effect(f'Subtitle {i+1:02d}', 'TEXT', 4, start, length=end-start)
        st.text = text
        st.font_size = 46
        st.color = (1.0, .97, .88, 1.0)
        st.location = (.5, .105)
        st.anchor_x, st.anchor_y = 'CENTER', 'CENTER'
        st.use_shadow = True
        st.shadow_color = (0, 0, 0, .95)
        st.shadow_offset, st.shadow_blur = 3.0, 2.0
        st.use_box = True
        st.box_color = (.025, .035, .055, .78)
        st.box_margin = 12
    slate = strips.new_effect('Opening label - editorial', 'TEXT', 5, 1, length=min(100, scene.frame_end))
    slate.text = title.upper() + '  |  ROUGH EDIT'
    slate.font_size = 36
    slate.color = (.94, .76, .40, 1)
    slate.location = (.035, .94)
    slate.anchor_x, slate.anchor_y = 'LEFT', 'TOP'
    slate.use_box = True
    slate.box_color = (.025, .035, .055, .74)
    slate.box_margin = 14
    if storyboard_glb:
        _add_storyboard_scene(scene, storyboard_glb, min(125, scene.frame_end),
                              out_blend.with_name('storyboard_open_book.png'))
    scene.frame_set(preview_frame if preview_frame is not None else 1)
    bpy.ops.wm.save_as_mainfile(filepath=str(out_blend))
    report = {'blend': str(out_blend), 'source': media, 'fps': fps,
              'frames': scene.frame_end, 'duration_seconds': round(scene.frame_end/fps, 3),
              'video_segments': len(cuts) if cuts else 1, 'subtitle_cues': len(subtitles),
              'storyboard_3d': bool(storyboard_glb),
              'storyboard_still_rendered': bool(storyboard_glb and out_blend.with_name('storyboard_open_book.png').is_file()),
              'final_video_rendered': False}
    out_blend.with_suffix('.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('SOuROV_BLENDER_RESULT ' + json.dumps(report))
    return report


def _add_storyboard_scene(main, glb, length, still_path):
    """Render installed generic open-book GLB as a transparent 3D VSE inset."""
    glb = str(Path(glb).resolve())
    if not os.path.isfile(glb):
        print('Storyboard GLB missing; leaving the project without the 3D storyboard strip.')
        return
    board = bpy.data.scenes.new('3D storyboard - open book')
    board.render.resolution_x, board.render.resolution_y = 1920, 1080
    board.render.resolution_percentage = 100
    board.render.fps = main.render.fps
    board.render.film_transparent = True
    board.render.engine = 'BLENDER_EEVEE'
    bpy.context.window.scene = board
    bpy.ops.import_scene.gltf(filepath=glb)
    imported = list(board.objects)
    meshes = [o for o in imported if o.type == 'MESH']
    if not meshes:
        print('Storyboard GLB imported without mesh objects; overlay omitted.')
        bpy.context.window.scene = main
        return
    # Keep the supplied geometry editable and stage a small left-side vignette.
    from mathutils import Vector, Matrix
    corners = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
    lo = Vector(tuple(min(v[i] for v in corners) for i in range(3)))
    hi = Vector(tuple(max(v[i] for v in corners) for i in range(3)))
    center = (lo + hi) / 2
    scale = 3.8 / max((hi-lo).length, .01)
    for obj in meshes:
        key = obj.name.casefold()
        color = ((.78,.70,.50,1) if 'paper' in key else
                 (.12,.22,.30,1) if ('cover' in key or 'spine' in key) else
                 (.12,.09,.06,1))
        material = bpy.data.materials.new('Storyboard material - ' + obj.name)
        material.diffuse_color = color
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get('Principled BSDF')
        if bsdf:
            bsdf.inputs['Base Color'].default_value = color
            bsdf.inputs['Roughness'].default_value = .82
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = color
                bsdf.inputs['Emission Strength'].default_value = .18
        obj.data.materials.clear()
        obj.data.materials.append(material)
    top_level = [o for o in imported if o.parent is None]
    root = bpy.data.objects.new('Storyboard asset group - editable GLB hierarchy', None)
    board.collection.objects.link(root)
    root.location = Vector((-5.2, 0, .45)) - center*scale
    root.scale = (scale, scale, scale)
    for obj in top_level:
        world = obj.matrix_world.copy()
        obj.parent = root
        obj.matrix_parent_inverse = Matrix.Identity(4)
        obj.matrix_basis = world
    # A simple storyboard card and 3D label, kept separate from the source video.
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-5.2, .45, -.3))
    card = bpy.context.object
    card.name = 'Storyboard card - open book'
    card.dimensions = (6.2, .18, 4.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bevel = card.modifiers.new('Soft card corners', 'BEVEL'); bevel.width=.16; bevel.segments=3
    mat = bpy.data.materials.new('Storyboard deep blue'); mat.diffuse_color=(.035,.055,.085,1)
    mat.use_nodes = True
    bsdf=mat.node_tree.nodes.get('Principled BSDF')
    if bsdf: bsdf.inputs['Base Color'].default_value=(.035,.055,.085,1)
    card.data.materials.append(mat)
    font_curve = bpy.data.curves.new('3D storyboard label', 'FONT')
    font_curve.body = 'OPEN BOOK'
    font_curve.size = .42
    label = bpy.data.objects.new('3D storyboard label - OPEN BOOK', font_curve)
    board.collection.objects.link(label)
    label.location = (-7.9, -.28, -1.85)
    label.rotation_euler = (1.5708, 0, 0)
    label_mat=bpy.data.materials.new('Warm gold label'); label_mat.diffuse_color=(.94,.72,.35,1)
    label_mat.use_nodes=True
    bsdf=label_mat.node_tree.nodes.get('Principled BSDF')
    if bsdf: bsdf.inputs['Base Color'].default_value=(.94,.72,.35,1)
    label.data.materials.append(label_mat)
    cam_data = bpy.data.cameras.new('Storyboard camera')
    cam = bpy.data.objects.new('Storyboard camera', cam_data)
    board.collection.objects.link(cam)
    cam.location = (0, -15, 0)
    cam.rotation_euler = (Vector((0, 0, 0))-cam.location).to_track_quat('-Z', 'Z').to_euler()
    cam_data.type, cam_data.ortho_scale = 'ORTHO', 21.3
    board.camera = cam
    light_data = bpy.data.lights.new('Storyboard key', 'AREA')
    light = bpy.data.objects.new('Storyboard key', light_data)
    board.collection.objects.link(light)
    light.location = (-5.2, -5, 5)
    light_data.energy, light_data.shape, light_data.size = 500, 'DISK', 5
    board.frame_start, board.frame_end = 1, main.frame_end
    board.render.filepath = str(still_path)
    bpy.context.window.scene = board
    bpy.context.view_layer.update()
    bpy.ops.render.render(scene=board.name, write_still=True)
    bpy.context.window.scene = main
    overlay = main.sequence_editor.strips.new_image('Storyboard 3D - open book (opening)', str(still_path), 3, 1)
    overlay.frame_final_duration = min(int(length), int(main.frame_end))
    overlay.blend_type = 'ALPHA_OVER'
