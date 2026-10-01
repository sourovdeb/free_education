"""Build an editable Blender rough edit for a narrated book-reading recording.

Example:
  blender --background --factory-startup --python book_reading_blender.py -- \
    --video "E:/recording.mp4" --output "E:/review/book_reading.blend" \
    --captions "E:/subtitle-review.csv"

CSV input should be the clean Resolve subtitle-review.csv. Original recognized
wording is used; corrected_text rows are deliberately ignored unless separately
approved and exported to SRT by the editor.
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import blender_edit_common as common

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--video', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--captions', help='Resolve subtitle-review.csv or SRT')
    p.add_argument('--review-csv', help='Optional reviewed Resolve pause/filler decisions')
    p.add_argument('--plan-json', help='Required with --review-csv; binds cuts to source')
    p.add_argument('--fps', type=float, default=25)
    p.add_argument('--overwrite', action='store_true', help='Replace an existing project and sidecars')
    p.add_argument('--storyboard-glb', default=(
        'C:/Program Files/Blackmagic Design/DaVinci Resolve/Fusion/blender-storyboard/'
        'asset-library/storyboard-pack/assets/A132-book-open.glb'))
    a = p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    cues = []
    cuts = []
    if a.review_csv:
        if not a.plan_json:
            p.error('--review-csv requires --plan-json')
        cuts, plan_fps = common.reviewed_keep_ranges(a.review_csv, a.plan_json, a.video)
        a.fps = plan_fps
    if a.captions:
        if a.captions.lower().endswith('.csv'):
            cues = common.cues_from_resolve_csv(a.captions, a.fps)
        else:
            cues = common.parse_srt(a.captions)
    return common.build_project(a.video, a.output, 'Book reading', cues, a.fps,
                                cuts=cuts, storyboard_glb=a.storyboard_glb, overwrite=a.overwrite)

if __name__ == '__main__':
    main()
