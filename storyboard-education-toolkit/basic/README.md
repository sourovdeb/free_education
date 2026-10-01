# Preserved basic Blender rough-edit scripts

These three Python files are byte-identical to the original local rough-edit tools; QA.json records hashes. Source recordings and cut plans are not bundled.

Use the root BOOK_ROUGH_EDIT.cmd / TUTORIAL_ROUGH_EDIT.cmd launchers after local-settings.json setup. They preserve the historical rough_edit.blend and create review_edit.blend with corrected caption-box margins and readable wrapping. Blender box_margin is a fraction of image width, not pixels; the old draft's large margins can darken the whole image. Review the corrected copy.

For direct use, run Blender in background factory-startup mode with --python book_reading_blender.py or tutorial_blender.py, then -- and the required --video and --output paths. Both accept --plan-json with --review-csv. Book accepts --captions (clean original-text Resolve CSV or SRT) and --storyboard-glb. Tutorial accepts --resolve-run or --captions SRT. Use --help after -- for options. Without a plan, all source footage is kept. A new recording requires its own source-bound cut review; these scripts do not decide new cuts or transcribe.

Existing outputs are protected unless --overwrite is explicitly supplied. Voice isolation, colour grading and final export are not reproduced. New timestamps prevent accidental replacement through the supplied launchers.
