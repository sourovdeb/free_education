"""Blender-only, one-item adapter. SYNTAX CHECKED; NOT RUNTIME TESTED in this delivery.
Run ONLY in a new background Blender process with --factory-startup.
blender --background --factory-startup --python scripts/build_native.py -- --id subject_ballot_box
Native output: output/native/<id>/<id>.blend. Never overwrites existing files.
"""
from __future__ import annotations
import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    import bpy
    from mathutils import Vector
    if not bpy.app.background:
        raise RuntimeError("Use a separate background Blender process; this adapter must not modify an open interactive project.")
    p = argparse.ArgumentParser()
    p.add_argument("--id", required=True)
    p.add_argument("--render", action="store_true", help="Explicitly render one preview PNG after saving.")
    args = p.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    found = [x for x in catalog["assets"] + catalog["scenes"] if x["id"] == args.id]
    if len(found) != 1:
        raise ValueError("Unknown or duplicated catalogue ID.")
    item = found[0]
    if not args.id.replace("_", "").isalnum():
        raise ValueError("Unsafe item ID.")
    source = (ROOT / item["glb"]).resolve()
    if not source.is_relative_to(ROOT) or not source.is_file():
        raise ValueError("Missing or unsafe source path.")
    output = ROOT / "output" / "native" / args.id
    output.mkdir(parents=True, exist_ok=True)
    dest = output / (args.id + ".blend")
    if dest.exists():
        raise FileExistsError(f"Existing master preserved: {dest}")
    # Background factory-startup has no user work to erase; still delete only this scene's objects.
    scene = bpy.context.scene
    for ob in list(scene.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    collection = bpy.data.collections.new(item["name"])
    scene.collection.children.link(collection)
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(source))
    imported = set(bpy.data.objects) - before
    if not imported:
        raise RuntimeError("glTF import created no objects.")
    for ob in imported:
        for parent in list(ob.users_collection):
            parent.objects.unlink(ob)
        collection.objects.link(ob)
    roots = [ob for ob in imported if ob.parent not in imported and ob.type != "CAMERA"]
    master = bpy.data.objects.new(args.id + "__MOVE_THIS_ROOT", None)
    collection.objects.link(master)
    for ob in roots:
        world = ob.matrix_world.copy()
        ob.parent = master
        ob.matrix_world = world
    master["asset_id"] = args.id
    master["source_kind"] = item.get("kind", "scene composition")
    master["not_armature"] = True
    collection.asset_mark()
    if collection.asset_data:
        collection.asset_data.description = item.get("note", item.get("design_note", item["name"]))[:1000]
        for tag in ["StoryFactory", item["group"].split("/")[0].strip()]:
            collection.asset_data.tags.new(tag)
    # Compute fitted camera from geometry, excluding inherited cameras/helpers.
    bpy.context.view_layer.update()
    corners = [ob.matrix_world @ Vector(v) for ob in imported if ob.type == "MESH" for v in ob.bound_box]
    if not corners:
        raise RuntimeError("No mesh geometry imported.")
    low = Vector(tuple(min(v[i] for v in corners) for i in range(3)))
    high = Vector(tuple(max(v[i] for v in corners) for i in range(3)))
    target = (low + high) / 2
    width, height = max(high.x-low.x, .1), max(high.z-low.z, .1)
    span = max(width, height, .5)
    cam_data = bpy.data.cameras.new("Preview_Camera")
    cam = bpy.data.objects.new("Preview_Camera", cam_data)
    scene.collection.objects.link(cam)
    cam.location = target + Vector((0, -span*2.5, 0))
    cam.rotation_euler = (target-cam.location).to_track_quat("-Z", "Y").to_euler()
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = max(width, height*16/9)*1.18
    scene.camera = cam
    engines = {e.identifier for e in scene.render.bl_rna.properties["engine"].enum_items}
    selected = next((x for x in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "BLENDER_WORKBENCH") if x in engines), None)
    if not selected:
        raise RuntimeError("No supported lightweight render engine found; no Cycles fallback was attempted.")
    scene.render.engine = selected
    # Area light provides a fallback for materials that are not unlit.
    light_data = bpy.data.lights.new("Soft_Key", "AREA")
    light_data.energy = 800
    light_data.shape = "DISK"
    light_data.size = span
    light = bpy.data.objects.new("Soft_Key", light_data)
    scene.collection.objects.link(light)
    light.location = target + Vector((span, -span, span*1.5))
    light.rotation_euler = (target-light.location).to_track_quat("-Z", "Y").to_euler()
    scene.render.resolution_x, scene.render.resolution_y = 960, 540
    scene.render.resolution_percentage = 100
    scene.render.fps = 25
    scene.frame_start, scene.frame_end = 1, 300
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.filepath = str(output / "preview.png")
    try:
        scene.view_settings.view_transform = "Standard"
    except (TypeError, ValueError):
        pass
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(dest))
    record = {"status": "NATIVE_MASTER_SAVED", "blender_version": bpy.app.version_string,
              "engine": selected, "item_id": args.id, "imported_objects": len(imported),
              "render_status": "NOT_REQUESTED", "output": str(dest.relative_to(ROOT)),
              "warning": "Import alone is not full visual or Resolve validation."}
    if args.render:
        try:
            bpy.ops.render.render(write_still=True)
            record["render_status"] = "RENDERED_REQUIRES_VISUAL_REVIEW"
        except Exception as exc:
            record["status"] = "PARTIAL_NATIVE_SAVED_RENDER_FAILED"
            record["render_status"] = str(exc)
            (output / "native_report.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
            raise
    (output / "native_report.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
