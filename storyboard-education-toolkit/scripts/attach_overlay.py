"""Attach a rendered transparent PNG or sequence to a COPY of a Blender edit."""
import argparse
import json
import sys
from pathlib import Path
import bpy

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project',required=True)
    p.add_argument('--images',required=True,help='PNG file or folder containing overlay_*.png')
    p.add_argument('--output',required=True)
    p.add_argument('--start',type=int,default=1)
    p.add_argument('--still-seconds',type=float,default=6)
    p.add_argument('--channel',type=int,default=6)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    src,out=Path(a.project).resolve(),Path(a.output).resolve()
    if out.exists() or out==src: raise FileExistsError('Choose a new project output.')
    path=Path(a.images).resolve()
    images=sorted(path.glob('overlay_*.png')) if path.is_dir() else [path]
    if not images or any(not f.is_file() or f.suffix.lower()!='.png' for f in images):
        raise ValueError('No PNG images found')
    if a.start<1 or a.channel<1 or a.still_seconds<=0: raise ValueError('Invalid timing/channel')
    if len(images)>1:
        nums=[int(f.stem.rsplit('_',1)[1]) for f in images]
        if nums!=list(range(nums[0],nums[0]+len(nums))): raise ValueError('Sequence has missing frames')
    bpy.ops.wm.open_mainfile(filepath=str(src))
    s=bpy.context.scene
    strips=s.sequence_editor_create().strips
    fps=s.render.fps/s.render.fps_base
    frames=len(images) if len(images)>1 else round(a.still_seconds*fps)
    if frames<1: raise ValueError('Overlay duration rounds to zero frames')
    if a.start+frames-1>s.frame_end: raise ValueError('Overlay exceeds edit; choose shorter duration')
    if len(images)>1:
        receipt=path.parent/'receipt.json'
        if receipt.exists():
            r=json.loads(receipt.read_text(encoding='utf-8'))
            if abs(r['fps']-fps)>.001: raise ValueError('Overlay and edit frame rates differ')
    if any(st.channel==a.channel and st.frame_final_start<a.start+frames and st.frame_final_end>a.start for st in strips):
        raise ValueError('Selected channel overlaps existing work; choose a free channel')
    st=strips.new_image('Reviewed transparent overlay',str(images[0]),a.channel,a.start,fit_method='FIT')
    for im in images[1:]: st.elements.append(im.name)
    st.frame_final_duration=frames
    st.blend_type='ALPHA_OVER'
    out.parent.mkdir(parents=True,exist_ok=True)
    # Absolute references make the copy independent of its previous folder depth.
    bpy.ops.file.make_paths_absolute()
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    print(json.dumps({'project':str(out),'frames':frames,'channel':a.channel}))

if __name__=='__main__': main()
