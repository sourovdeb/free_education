# Blender storyboard: start with one scene

This guide serves all ten classic-fiction kits. Download the book ZIP from the series index. Keep its folders together.

## 1. Unzip and open Blender

1. Right-click the ZIP and choose **Extract All**.
2. Open Blender. Choose **General**.
3. Save a new file: **File → Save As**. Name it `book_scene_01.blend`.
4. In the top-left corner of the 3D viewport, select **Object Mode**.
5. Keep the pointer over the viewport when pressing shortcuts.

**Check:** The Outliner appears at right. Your file name appears in Blender's title bar.

## 2. Import the starter assets

1. For Karamazov v1.1, open `03_Blender/Scene_Starts`. Select `SCENE_01_family_v001.glb` to get a named scene and camera. For loose pieces, open `02_Assets`.
2. Choose a filename that names the thing, such as `CHAR_alyosha_v001.glb`.
3. In Blender, choose **File → Import → glTF 2.0 (.glb/.gltf)**.
4. Select the GLB and choose **Import glTF 2.0**.
5. With a scene start, its pieces arrive together. With loose pieces, repeat for a location and prop.
6. Expand each import in the Outliner. Select its parent or ROOT to move all pieces.

**Check:** Three named groups appear. If nothing appears, press Home while over the viewport.

## 3. Arrange one panel

1. Select the character parent.
2. Press **G**, then **X**. Move the mouse sideways. Left-click.
3. Press **G**, then **Z**. Move vertically. Left-click.
4. Press **G**, then **Y**. Change depth.
5. Press **R**, then **Y**. Rotate the cutout within the picture.
6. Press **S**. Resize uniformly.
7. Press **Ctrl+Z** after a mistake.

**Check:** The character stays assembled. If a hand separates, undo. Select the parent.

**Change a colour:** Expand the parent in the Outliner. Select one mesh piece. Open Material Properties, marked by the sphere icon. Choose its material. Under Surface, change Base Color. If several pieces share that material, they change together. Click the number beside its name to make a separate copy first. Switch to Material Preview to inspect.

## 4. Choose a view

1. Choose a supplied camera in the Outliner, if present.
2. Hover over the viewport. Press **Numpad 0**.
3. Without a numpad, use **View → Cameras → Active Camera**.
4. If there is no camera, use **Add → Camera**.
5. Position the view, then press **Ctrl+Alt+Numpad 0** to align the camera.
6. Set **Output Properties → Resolution X: 640; Y: 360; frame rate: 25** for a video panel.

**Check:** Faces and props fit inside the frame. No caption covers a face.

## 5. Make another shot

1. Save with **Ctrl+S**.
2. Choose **File → Save As** and increment the scene number.
3. Move a character or prop. Ask what changed in the story.
4. Give each scene one action: enter, offer, refuse, reveal, or leave.
5. Record a one-sentence caption in a separate text file.
6. Leave the source book unchanged. Label invented staging as interpretation.

**Check:** Two .blend files exist. Opening either restores its own composition.

## 6. Add simple motion

1. Set the timeline start to frame 1.
2. Select one character parent.
3. Hover over its Location field. Press **I** to add a keyframe.
4. Set the current frame to 75.
5. Press **G**, then **X**. Move the character. Left-click.
6. Hover over Location again. Press **I**.
7. Press Spacebar to play. The character should travel.
8. For a four-second shot, end at frame 100.

**Check:** Only the chosen parent moves.

## 7. Render and inspect

1. Set **Render Properties → Render Engine → Eevee** if the kit needs it.
2. Set the output folder in **Output Properties**.
3. Press **F12** to render one frame.
4. Inspect the full frame. Fix cut-off limbs, unreadable text, and hidden props.
5. Choose **Image → Save As** for a still. Use **Render → Render Animation** for timed motion.
6. Save the .blend project again. A PNG does not preserve editable objects.

**Check:** The exported picture matches the camera view.

## Troubleshooting

| Problem | Action |
| --- | --- |
| Only one body part moves | Undo. Choose the parent/ROOT in the Outliner. |
| Object invisible | Select it; hover viewport; press keypad period, or use View → Frame Selected. |
| Colours look grey | Use Material Preview or render the camera. |
| Entire scene moves | Select only the intended parent. |
| Imported asset is huge | Select its parent; press S; enter 0.1. |
| Missing textures | Use supplied GLB materials; keep the ZIP folder intact. |
| Blender menu differs | Use F3 to search the command name. |

The [59-page visual manual](https://drive.google.com/file/d/1A-gEzBPxaFO9R3KHbPLYRV0k9KFCFtVM/view) offers more screenshots and checkpoints. Its example kit uses different filenames. Use the asset manifest inside each book ZIP for exact names.

The first Karamazov ZIP contains GLB/SVG assets and a Blender builder. It contains no verified native .blend files. Test imports on your Blender installation before relying on its builder.
