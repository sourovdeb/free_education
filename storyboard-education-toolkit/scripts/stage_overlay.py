"""Blender: build a reusable transparent overlay from explicit JSON settings.

blender -b --factory-startup --python-exit-code 1 --python stage_overlay.py -- --config job.json --output E:/new-run
No text interpretation, automatic tracking, background removal or source edits.
"""
import argparse
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Vector, Matrix

def material(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = tuple(color)
    m.use_nodes = True
    bs = m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = tuple(color)
    bs.inputs['Roughness'].default_value = .45
    return m

def text_object(name, text, position, max_width, color, extrude=0):
    data = bpy.data.curves.new(name, 'FONT')
    data.body = text
    data.align_x = 'CENTER'
    data.align_y = 'CENTER'
    data.size = .45
    data.extrude = extrude
    data.bevel_depth = min(.005, extrude/3)
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = position
    obj.rotation_euler = (math.pi/2, 0, 0)
    mat = material(name + ' ink', color)
    bs = mat.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Emission Color'].default_value = tuple(color)
    bs.inputs['Emission Strength'].default_value = .7
    data.materials.append(mat)
    bpy.context.view_layer.update()
    if obj.dimensions.x > max_width:
        obj.scale *= max_width/obj.dimensions.x
    return obj

def import_fitted(path, name, size):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(path))
    imported = list(set(bpy.data.objects) - before)
    meshes = [o for o in imported if o.type == 'MESH']
    if not meshes:
        raise ValueError('GLB contains no mesh: ' + str(path))
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(p) for o in meshes for p in o.bound_box]
    lo = Vector([min(p[i] for p in pts) for i in range(3)])
    hi = Vector([max(p[i] for p in pts) for i in range(3)])
    diagonal = max(hi-lo)
    if diagonal <= 0:
        raise ValueError('Zero-size mesh')
    root = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(root)
    for obj in imported:
        if obj.parent not in imported:
            world = obj.matrix_world.copy()
            obj.parent = root
            obj.matrix_parent_inverse = Matrix.Identity(4)
            obj.matrix_basis = world
    root.scale = (size/diagonal,) * 3
    center = (lo+hi)/2
    # A second parent keeps object-centering independent of motion.
    root.location = -center * (size/diagonal)
    mover = bpy.data.objects.new(name + ' motion', None)
    bpy.context.collection.objects.link(mover)
    root.parent = mover
    return mover

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--render', action='store_true', help='Render all bounded frames to RGBA PNG')
    p.add_argument('--preview', action='store_true', help='Render one representative frame')
    a = p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    cfgpath = Path(a.config).resolve()
    c = json.loads(cfgpath.read_text(encoding='utf-8-sig'))
    out = Path(a.output).resolve()
    if out.exists() and any(out.iterdir()):
        raise FileExistsError('Use a new empty output directory; existing work is protected.')
    width, height = int(c.get('width',1920)), int(c.get('height',1080))
    fps = float(c.get('fps',25))
    seconds = float(c.get('seconds',6))
    if not (256 <= width <= 3840 and 256 <= height <= 2160 and 1 <= fps <= 60 and 0 < seconds <= 120):
        raise ValueError('Expected 256..3840 x 256..2160, 1..60 fps, and <=120 seconds per shot')
    n = round(seconds*fps)
    if n < 2 or n > 3000:
        raise ValueError('Use 2..3000 frames per shot; split longer work into shots.')
    mode = c.get('mode','static')
    if mode not in ('static','side','orbit'):
        raise ValueError('mode must be static, side or orbit')
    assets = c.get('assets',[])
    if not 1 <= len(assets) <= 8:
        raise ValueError('Provide 1..8 explicitly selected assets')
    resolved = []
    for item in assets:
        path = Path(item['path'])
        if not path.is_absolute(): path = (cfgpath.parent/path).resolve()
        if not path.is_file() or path.suffix.lower() != '.glb':
            raise FileNotFoundError(str(path))
        resolved.append((item,path))
    # Subject rectangle is a user-supplied layout contract, not inferred tracking.
    safe = c.get('subject_safe_rect',[.34,.16,.66,.88])
    if len(safe)!=4 or not (0<=safe[0]<safe[2]<=1 and 0<=safe[1]<safe[3]<=1):
        raise ValueError('safe rectangle is normalized [left,bottom,right,top]')
    out.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    s = bpy.context.scene
    s.name = 'Transparent overlay - ' + mode
    s.render.engine = 'BLENDER_EEVEE'
    s.render.threads_mode, s.render.threads = 'FIXED',2
    s.render.resolution_x,s.render.resolution_y = width,height
    s.render.resolution_percentage = 100
    s.render.fps = round(fps)
    s.render.fps_base = round(fps)/fps
    s.frame_start,s.frame_end = 1,n
    s.render.film_transparent = True
    s.render.image_settings.file_format = 'PNG'
    s.render.image_settings.color_mode = 'RGBA'
    s.view_settings.view_transform = 'Standard'
    s.world.color = (.2,.2,.2)
    scene_width,scene_height = 16,16*height/width
    bpy.ops.object.camera_add(location=(0,-24,0))
    camera = bpy.context.object
    camera.rotation_euler = (Vector((0,0,0))-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = max(scene_width,scene_height)
    s.camera = camera
    # Camera ortho_scale is horizontal in landscape, vertical in portrait.
    if width < height:
        scene_width = scene_height*width/height
    for loc,power,size in [((-5,-10,7),1800,7),((6,-5,3),1200,5),((0,4,6),1600,5)]:
        bpy.ops.object.light_add(type='AREA',location=loc)
        light = bpy.context.object
        light.data.energy,light.data.shape,light.data.size = power,'DISK',size
        light.rotation_euler = (-light.location).to_track_quat('-Z','Y').to_euler()
    placements=[]
    for index,(item,path) in enumerate(resolved):
        # Place each object in a fixed side lane; orbit moves in 3D inside its lane.
        right = index%2 == 1
        xnorm = (safe[2]+1)/2 if right else safe[0]/2
        available = (1-safe[2]) if right else safe[0]
        lane_index = index//2
        lane_count = (len(assets)+(0 if right else 1))//2
        vertical_step=.50*scene_height/max(1,lane_count)
        requested=float(item.get('size',1.3))
        if requested<=0: raise ValueError('size must be positive')
        # Any rotation stays inside this sphere, even with nonuniform GLB bounds.
        # Auto-shrink keeps up to eight objects separated and outside the subject.
        size=min(requested,1.6,(available*scene_width-.65)/math.sqrt(3),
                 (vertical_step-.45)/math.sqrt(3))
        if size<.1: raise ValueError('Not enough space for readable assets; reduce count or safe rectangle')
        radius=size*math.sqrt(3)/2
        mover = import_fitted(path,item.get('id',path.stem),size)
        znorm = .25 + .50*(lane_index+.5)/max(1,lane_count)
        center = Vector(((xnorm-.5)*scene_width,0,(znorm-.5)*scene_height))
        mover.location = center
        mover.rotation_euler = tuple(math.radians(v) for v in item.get('rotation',[0,0,0]))
        if mode == 'orbit':
            rx = max(0,min(.35,available*scene_width/2-radius-.25))
            for frame in sorted(set([1]+list(range(1,n+1,max(1,round(fps/4))))+[n])):
                t=2*math.pi*(frame-1)/(n-1)+index*math.pi/2
                mover.location = center+Vector((rx*math.cos(t),.6*math.sin(t),.18*math.sin(t)))
                mover.rotation_euler.z = math.radians(item.get('rotation',[0,0,0])[2])+t*.12
                mover.keyframe_insert(data_path='location',frame=frame)
                mover.keyframe_insert(data_path='rotation_euler',frame=frame)
        elif mode == 'side':
            final = center.copy()
            mover.location.x = (-scene_width if not right else scene_width)
            mover.keyframe_insert(data_path='location',frame=1)
            mover.location = final
            mover.keyframe_insert(data_path='location',frame=min(n,max(2,round(fps*.5))))
        placements.append({'id':item.get('id',path.stem),'path':str(path),'center':list(center),'size':size})
    title=str(c.get('title',''))
    caption=str(c.get('caption',''))
    if len(title)>100 or len(caption)>160:
        raise ValueError('Split long text into several readable cards (title<=100, caption<=160).')
    if title:
        text_object('Editable title',title,(0,-2,scene_height*.43),scene_width*.88,[1,.78,.38,1],.015 if c.get('text_3d',True) else 0)
    if caption:
        text_object('Exact user caption',caption,(0,-2,-scene_height*.43),scene_width*.88,[1,1,1,1])
    s.frame_set(max(1,round(n/2)))
    s.render.filepath = str(out/'frames'/'overlay_')
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'overlay.blend'))
    receipt={'schema':1,'mode':mode,'frames':n,'fps':fps,'width':width,'height':height,'placements':placements,
             'subject_safe_rect':safe,'tracking':False,'person_occlusion':False,'semantic_selection':'EXPLICIT_USER_ASSET_LIST',
             'config':c,'preview_rendered':False,'sequence_rendered':False}
    if a.preview:
        s.render.filepath=str(out/'preview.png')
        bpy.ops.render.render(write_still=True)
        receipt['preview_rendered']=True
    if a.render:
        (out/'frames').mkdir(exist_ok=True)
        s.render.filepath=str(out/'frames'/'overlay_')
        bpy.ops.render.render(animation=True)
        receipt['sequence_rendered']=True
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print(json.dumps({'saved':str(out/'overlay.blend'),'frames':n,'mode':mode}))

if __name__=='__main__': main()
