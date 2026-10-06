"""Build an editable Blender VSE tutorial draft from an optional Resolve review.

Example:
  blender --background --factory-startup --python tutorial_blender.py -- \
    --video "E:/screen-recording.mp4" --output "E:/review/tutorial.blend" \
    --review-csv "E:/plan/review.csv" --plan-json "E:/plan/plan.json" \
    --captions "E:/captions.srt"

Only CUT rows in the Resolve review.csv are removed. The source remains intact;
without a review plan, the complete recording is kept. The edit is a draft.
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
    p.add_argument('--captions', help='Optional SRT subtitle file')
    p.add_argument('--resolve-run', help='Resolve first-pass run.json; reuse its exact subtitle cues')
    p.add_argument('--review-csv', help='Optional reviewed Resolve cut decisions')
    p.add_argument('--plan-json', help='Source-bound plan.json paired with review.csv')
    p.add_argument('--fps', type=float, default=30)
    p.add_argument('--overwrite', action='store_true', help='Replace an existing project and sidecars')
    a = p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    cuts = []
    if a.review_csv:
        if not a.plan_json: p.error('--review-csv requires --plan-json')
        cuts, a.fps = common.reviewed_keep_ranges(a.review_csv, a.plan_json, a.video)
    cues = (common.cues_from_resolve_receipt(a.resolve_run, a.fps) if a.resolve_run
            else common.parse_srt(a.captions) if a.captions else [])
    return common.build_project(a.video, a.output, 'Software tutorial', cues, a.fps, cuts=cuts,
                                overwrite=a.overwrite)

if __name__ == '__main__':
    main()
