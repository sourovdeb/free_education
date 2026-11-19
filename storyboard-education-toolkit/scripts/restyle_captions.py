"""Improve caption layout in a new Blender copy without changing the words."""
import argparse
import json
import sys
import textwrap
from pathlib import Path
import bpy

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--preview',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    src,out=Path(a.project).resolve(),Path(a.output).resolve()
    protected=[out,out.with_suffix('.json')]
    if a.preview: protected.append(out.with_suffix('.png'))
    if any(f.exists() for f in protected) or src==out: raise FileExistsError('Use new project and sidecar outputs')
    bpy.ops.wm.open_mainfile(filepath=str(src))
    s=bpy.context.scene
    if not s.sequence_editor: raise ValueError('Project has no sequencer')
    font=None
    for font_path in (Path('C:/Windows/Fonts/segoeui.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')):
        if font_path.is_file():
            font=bpy.data.fonts.load(str(font_path),check_existing=True)
            break
    changed=[]
    for strip in s.sequence_editor.strips:
        if strip.type=='TEXT' and strip.use_box:
            # Blender stores this as a fraction of image width, not pixels.
            strip.box_margin=.01
        if strip.type!='TEXT' or not strip.name.startswith('Subtitle '): continue
        if font: strip.font=font
        original=strip.text
        words=' '.join(original.split())
        base_size=56*s.render.resolution_y/1080
        wrap_chars=max(12,min(42,int(s.render.resolution_x*.82/(base_size*.62))))
        lines=textwrap.wrap(words,width=wrap_chars,break_long_words=False,break_on_hyphens=False)
        strip.text='\n'.join(lines)
        if strip.text.split()!=original.split(): raise ValueError('Word-preservation check failed')
        strip.font_size=round(min(56,112/max(2,len(lines)))*s.render.resolution_y/1080)
        # Conservative pixel budget also handles unusually long unbroken words.
        strip.font_size=min(strip.font_size,max(8,int(s.render.resolution_x*.82/(max(map(len,lines),default=1)*.7))))
        strip.location=(.5,.115)
        strip.anchor_x=strip.anchor_y='CENTER'
        strip.color=(1,1,1,1)
        strip.use_box=True
        strip.box_color=(.018,.026,.042,.94)
        strip.box_margin=.01
        strip.use_shadow=True
        strip.shadow_color=(0,0,0,1)
        changed.append({'strip':strip.name,'words_preserved':True,'lines':len(lines),'start':strip.frame_final_start})
    bpy.ops.file.make_paths_absolute()
    out.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    if a.preview:
        s.frame_set(changed[0]['start'] if changed else s.frame_start)
        s.render.resolution_percentage=50
        s.render.image_settings.file_format='PNG'
        s.render.filepath=str(out.with_suffix('.png'))
        bpy.ops.render.render(write_still=True)
    out.with_suffix('.json').write_text(json.dumps({'source':str(src),'changed':changed,'word_changes':False},indent=2),encoding='utf-8')
    print('Restyled',len(changed),'captions; words and timings preserved.')

if __name__=='__main__': main()
