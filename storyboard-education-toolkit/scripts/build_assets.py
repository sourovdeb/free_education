"""Build nine original, parametric educational props with Blender 5.2.

blender --background --factory-startup --threads 2 --python build_assets.py -- --output ../assets
Optional --palette JSON object overriding navy, teal, gold, paper, coral hex colors.
GLBs use metre-scale units, local origin, reusable materials and named pivots.
"""
import argparse, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector

PALETTE = {'navy':'243653','teal':'35B8A8','gold':'FFC35A','paper':'F6EEDA','coral':'EF786A'}
def material(name, color):
    m=bpy.data.materials.new(name); m.diffuse_color=tuple((int(color[i:i+2],16)/255)**2.2 for i in (0,2,4))+(1,)
    m.use_nodes=True; p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=m.diffuse_color; p.inputs['Roughness'].default_value=.42
    return m
def finish(obj,name,mat,parent=None):
    obj.name=name
    if mat: obj.data.materials.append(MATS[mat])
    if parent: obj.parent=parent
    return obj
def cube(name,loc,scale,mat,parent=None,bevel=.06):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=finish(bpy.context.object,name,mat,parent); o.dimensions=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        mod=o.modifiers.new('Soft edges','BEVEL'); mod.width=bevel; mod.segments=3
        o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o
def sphere(name,loc,r,mat,parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=r,location=loc)
    o=finish(bpy.context.object,name,mat,parent)
    for p in o.data.polygons:p.use_smooth=True
    return o
def rod(name,a,b,r,mat,parent=None):
    a,b=Vector(a),Vector(b); d=b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=r,depth=d.length,location=(a+b)/2)
    o=finish(bpy.context.object,name,mat,parent); o.rotation_euler=d.to_track_quat('Z','Y').to_euler(); return o
def empty(name,loc=(0,0,0),parent=None):
    o=bpy.data.objects.new(name,None); bpy.context.collection.objects.link(o); o.location=loc; o.parent=parent; return o
def text(name,body,loc,size,mat,parent):
    c=bpy.data.curves.new(name,'FONT'); c.body=body;c.size=size;c.align_x='CENTER';c.extrude=.006
    o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(math.pi/2,0,0);o.parent=parent;c.materials.append(MATS[mat]);return o
def book(root):
    for s in [-1,1]:
        p=empty('Page_hinge_left' if s<0 else 'Page_hinge_right',parent=root)
        cube('Cloth_cover',(s*.52,0,.07),(1.05,1.5,.13),'teal',p)
        cube('Page_block',(s*.5,0,.18),(.94,1.4,.16),'paper',p)
        for y in [-.45,-.22,.01,.24,.47]:cube('Printed_line',(s*.52,y,.27),(.63,.022,.012),'navy',p,.002)
        p.rotation_euler[1]=s*-.12
    rod('Spine',(0,-.75,.09),(0,.75,.09),.075,'gold',root)
def pen(root):
    rod('Pen_barrel',(0,0,.2),(0,0,1.6),.11,'teal',root)
    rod('Grip',(0,0,.2),(0,0,.6),.125,'navy',root)
    bpy.ops.mesh.primitive_cone_add(vertices=24,radius1=0,radius2=.11,depth=.3,location=(0,0,.05));finish(bpy.context.object,'Nib','gold',root)
    rod('Clip',(.11,0,1.3),(.11,0,1.7),.025,'gold',root)
def panel(root):
    cube('Frame',(0,0,1),(2,.16,1.3),'gold',root)
    cube('Editable_panel',(0,-.1,1),(1.84,.06,1.14),'navy',root)
    text('Editable_text','YOUR WORDS',(0,-.15,1),.20,'paper',root)
    cube('Speech_tail',(-.6,0,.27),(.3,.12,.3),'gold',root).rotation_euler[1]=math.pi/4
def mask(root):
    o=sphere('Face',(0,0,1),.7,'coral',root);o.scale=(1,.32,1.18)
    for x in [-.27,.27]:
        o=sphere('Stylized_eye',(x,-.215,1.2),.14,'navy',root);o.scale=(1,.3,.7)
    rod('Mouth',(-.25,-.23,.73),(.25,-.23,.73),.04,'gold',root)
    sphere('Nose',(0,-.27,1),.09,'gold',root)
def mirror(root):
    cube('Foot',(0,0,.08),(1.1,.65,.16),'navy',root)
    rod('Stand',(0,0,.1),(0,0,.7),.06,'gold',root)
    o=sphere('Oval_frame',(0,0,1.35),.72,'gold',root);o.scale=(.8,.15,1)
    o=sphere('Mirror_surface',(0,-.10,1.35),.65,'paper',root);o.scale=(.8,.025,1)
    m=MATS['paper'].copy();m.name='Mirror_polished';m.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value=.92;m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.13;o.data.materials.clear();o.data.materials.append(m)
def ballot(root):
    cube('Box',(0,0,.55),(1.3,1.05,1.1),'teal',root)
    cube('Lid',(0,0,1.14),(1.4,1.15,.15),'navy',root)
    cube('Slot',(0,0,1.22),(.8,.13,.012),'navy',root,.01)
    cube('Ballot_card',(0,0,1.52),(.65,.04,.65),'paper',root).rotation_euler[1]=-.15
    text('Vote_mark','X',(0,-.04,1.45),.25,'teal',root)
def columns(root):
    cube('Foundation',(0,0,.08),(2.1,.85,.16),'navy',root)
    for x in [-.7,0,.7]:
        rod('Column',(x,0,.22),(x,0,1.6),.14,'paper',root)
        for z in [.22,1.6]:cube('Capital',(x,0,z),(.42,.46,.14),'gold',root)
    cube('Entablature',(0,0,1.78),(2.1,.65,.22),'teal',root)
def nodes(root):
    pts=[(-.7,0,.4),(.7,0,.4),(0,0,1.7)]
    for i,(a,b) in enumerate([(0,1),(1,2),(2,0)]):rod('Editable_link_'+str(i),pts[a],pts[b],.04,'gold',root)
    for i,p in enumerate(pts):sphere('Node_'+str(i+1),p,.23,['teal','coral','navy'][i],root)
def figure(root):
    rod('Torso',(0,0,.85),(0,0,1.5),.09,'teal',root);sphere('Head',(0,0,1.8),.22,'gold',root)
    for side,s in [('L',-1),('R',1)]:
        for limb,z,dx,dz in [('Arm',1.45,.5,-.55),('Leg',.85,.28,-.72)]:
            pivot=empty(side+'_'+limb+'_PIVOT',(0,0,z),root)
            rod(side+'_'+limb,(0,0,0),(s*dx,0,dz),.065,'navy',pivot)
            sphere(side+'_'+limb+'_joint',(0,0,0),.095,'coral',pivot)

BUILDERS=[('EDU001','Open book',book),('EDU002','Writing pen',pen),('EDU003','Speech panel',panel),('EDU004','Theatrical mask',mask),('EDU005','Standing mirror',mirror),('EDU006','Ballot box',ballot),('EDU007','Civic columns',columns),('EDU008','Relationship nodes',nodes),('EDU009','Pivot figure',figure)]
SVG_SHAPES=[
 '<path d="M128 64 Q74 38 30 58 V193 Q76 176 128 202 Q178 176 226 193 V58 Q180 38 128 64Z"/><path d="M128 64V202M49 84L106 95M49 112L106 123M150 95L208 84M150 123L208 112" fill="none"/>',
 '<path d="M109 35H146V188L128 222L109 188Z"/><path d="M111 167H144M146 43H162V101" fill="none"/>',
 '<path d="M26 48H230V184H96L60 214V184H26Z"/><path d="M57 85H197M57 114H176M57 143H148" fill="none"/>',
 '<path d="M48 47Q128 15 208 47L197 150Q178 225 128 232Q76 222 58 150Z"/><ellipse cx="91" cy="104" rx="22" ry="13" fill="#243653"/><ellipse cx="165" cy="104" rx="22" ry="13" fill="#243653"/><path d="M92 170Q128 197 164 170" fill="none"/>',
 '<ellipse cx="128" cy="99" rx="65" ry="78"/><ellipse cx="128" cy="99" rx="54" ry="67" fill="#F6EEDA"/><path d="M128 177V221M72 228H184M100 63L142 40" fill="none"/>',
 '<path d="M43 112H213V223H43Z"/><path d="M37 95H219V116H37Z"/><path d="M93 28H165V98H93Z" fill="#F6EEDA"/><path d="M115 47L145 78M145 47L115 78" fill="none"/>',
 '<path d="M23 40H233V68H23ZM23 202H233V229H23ZM44 68H74V202H44ZM113 68H143V202H113ZM182 68H212V202H182Z"/>',
 '<path d="M55 191L128 51L205 191Z" fill="none"/><circle cx="55" cy="191" r="26"/><circle cx="128" cy="51" r="26"/><circle cx="205" cy="191" r="26"/>',
 '<circle cx="128" cy="43" r="23"/><path d="M128 68V146M128 91L64 139M128 91L192 139M128 146L86 220M128 146L170 220" fill="none" stroke-linecap="round"/>'
]
def main():
    global MATS
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--palette');p.add_argument('--overwrite',action='store_true')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
    if (out/'manifest.json').exists() and not a.overwrite:raise RuntimeError('Assets already exist; use --overwrite deliberately')
    if a.palette:PALETTE.update(json.loads(Path(a.palette).read_text()))
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    MATS={k:material(k,v) for k,v in PALETTE.items()}
    sc=bpy.context.scene;sc.render.engine='BLENDER_EEVEE';sc.render.threads_mode='FIXED';sc.render.threads=2
    sc.render.resolution_x=1280;sc.render.resolution_y=720;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.world.color=(.7,.7,.7);sc.view_settings.view_transform='Standard'
    entries=[]
    for idx,(aid,label,build) in enumerate(BUILDERS):
        root=empty(aid);build(root);bpy.context.view_layer.update()
        objs=[root]+list(root.children_recursive)
        # GLTF text must be converted to mesh; original text remains editable in blend.
        bpy.ops.object.select_all(action='DESELECT')
        for o in objs:o.select_set(True)
        copies=[]
        for o in objs:
            if o.type=='FONT':
                o.select_set(False)
                mesh=bpy.data.meshes.new_from_object(o.evaluated_get(bpy.context.evaluated_depsgraph_get()))
                copy=bpy.data.objects.new(o.name+'_GLB_mesh',mesh);bpy.context.collection.objects.link(copy);copy.parent=o.parent;copy.matrix_local=o.matrix_local.copy();copy.select_set(True);copies.append(copy)
        bpy.context.view_layer.objects.active=root
        bpy.ops.export_scene.gltf(filepath=str(out/(aid+'.glb')),export_format='GLB',use_selection=True,export_apply=True)
        for copy in copies:bpy.data.objects.remove(copy,do_unlink=True)
        bounds=[o.matrix_world@Vector(v) for o in objs if o.type=='MESH' for v in o.bound_box]
        dims=[round(max(v[i] for v in bounds)-min(v[i] for v in bounds),3) for i in range(3)]
        (out/(aid+'.svg')).write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><title>'+label+'</title><g fill="#'+PALETTE['teal']+'" stroke="#'+PALETTE['navy']+'" stroke-width="7" stroke-linejoin="round">'+SVG_SHAPES[idx]+'</g></svg>',encoding='utf-8')
        entries.append({'id':aid,'name':label,'glb':aid+'.glb','svg':aid+'.svg','png':aid+'.png','root':aid,'dimensions_m':dims,'original':True,'source_meaning':'UNASSIGNED','notes':'Named parent pivots; not a skinned rig' if aid=='EDU009' else 'Parametric original geometry'})
        root.location=((idx%3-1)*3.8,0,(1-idx//3)*3.0)
        text(aid+'_caption',aid+'  '+label,(root.location.x,-.8,root.location.z-.38),.17,'navy',None)
    bpy.ops.object.camera_add(location=(3,-30,10));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,.8))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=17.2;sc.camera=cam
    for loc,power,size in [((0,-10,12),1100,10),((-8,-3,5),700,8),((7,3,9),900,8)]:
        bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
    sc.render.film_transparent=False;sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.78,.81,.86,1);sc.world.node_tree.nodes['Background'].inputs[1].default_value=.7
    sc.render.filepath=str(out/'contact-sheet.png');bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'education-library.blend'))
    # Preview each prop with alpha, independent of gallery coordinates.
    sc.render.resolution_x=512;sc.render.resolution_y=512;sc.render.film_transparent=True;cam.data.ortho_scale=3.3
    for item in entries:
        for entry in entries:
            r=bpy.data.objects[entry['id']]
            for o in [r]+list(r.children_recursive):o.hide_render=entry['id']!=item['id']
            bpy.data.objects[entry['id']+'_caption'].hide_render=True
        root=bpy.data.objects[item['id']];target=root.location+Vector((0,0,.85))
        if item['id']=='EDU001':target=root.location+Vector((0,0,.1))
        cam.location=target+Vector((2,-6,3));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
        sc.render.filepath=str(out/item['png']);bpy.ops.render.render(write_still=True)
    manifest={'version':'1.0','license':'CC0-1.0','units':'metres','palette':PALETTE,'assets':entries,'semantic_gate':'UNKNOWN: TypeSafe credential unavailable; no literary or historical interpretation assigned','limitations':['Figure uses object parenting, not skinning or an armature','Mirror appearance depends on target renderer','Speech text remains editable in Blender; GLB contains fixed mesh text','Gallery placement is presentation only; exported GLBs have local origins','SVG counterparts are simplified original icons, not orthographic geometry exports']}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    bpy.ops.wm.open_mainfile(filepath=str(out/'education-library.blend'))
    assert all(bpy.data.objects.get(x['id']) for x in entries)
    assert all((out/x['glb']).stat().st_size>100 for x in entries)
    imports=[]
    for entry in entries:
        bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
        bpy.ops.import_scene.gltf(filepath=str(out/entry['glb']))
        assert bpy.data.objects.get(entry['id'])
        meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
        assert meshes
        imports.append({'id':entry['id'],'mesh_count':len(meshes),'imported':True})
    (out/'validation.json').write_text(json.dumps({'reopened':True,'asset_roots':len(entries),'glb_files':len(entries),'glb_imports':imports,'contact_sheet':(out/'contact-sheet.png').stat().st_size,'blender':bpy.app.version_string},indent=2))
    print('ASSET_BUILD_VERIFIED '+str(out))
if __name__=='__main__':main()
