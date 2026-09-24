#!/usr/bin/env python3
"""Validate coverage/continuity and optionally render a structured reading score.

No network, model calls, audio analysis, or third-party dependencies.
"""
import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path


def validate(data, source):
    errors = []
    checks = 0

    def check(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            errors.append(message)

    check(data.get('format_version') == 1, 'Unsupported format_version')
    check(data.get('source_sha256') == hashlib.sha256(source.encode()).hexdigest(), 'Source hash mismatch')
    segments = data.get('segments', [])
    check(isinstance(segments, list) and bool(segments), 'No segment list')
    if not isinstance(segments, list):
        return {'ok': False, 'checks': checks, 'errors': errors}
    keys = data.get('accent_keys', {})
    speakers = data.get('speakers', {})
    cues = data.get('cues', {})
    check(isinstance(keys, dict) and bool(keys), 'Missing accent keys')
    check(isinstance(speakers, dict) and bool(speakers), 'Missing speaker cards')
    check(isinstance(cues, dict), 'Cues must be a dictionary')
    if not all(isinstance(x, dict) for x in [keys, speakers, cues]):
        return {'ok': False, 'checks': checks, 'errors': errors}
    ids, used, cursor, words = [], [], 0, 0
    for seg in segments:
        if not isinstance(seg, dict):
            check(False, 'Segment must be an object')
            continue
        ident = seg.get('id')
        check(isinstance(ident, str) and bool(ident) and ident not in ids, f'Duplicate/missing ID: {ident}')
        ids.append(ident)
        start, end = seg.get('start'), seg.get('end')
        valid_span = type(start) is int and type(end) is int and cursor <= start < end <= len(source)
        check(valid_span, f'{ident}: invalid/overlapping source span')
        if not valid_span:
            continue
        check(not source[cursor:start].strip(), f'{ident}: skipped source text')
        raw = source[start:end]
        check(seg.get('reading') == raw, f'{ident}: reading differs from source')
        cursor = end
        tokens = raw.split()
        words += len(tokens)
        pairs = seg.get('word_guides', [])
        valid_pairs = isinstance(pairs, list) and all(isinstance(p, list) and len(p) == 2 and all(isinstance(t, str) and t for t in p) for p in pairs)
        check(valid_pairs, f'{ident}: invalid word_guides')
        if valid_pairs:
            check([p[0] for p in pairs] == tokens, f'{ident}: word coverage mismatch')
            check(' '.join(p[1] for p in pairs) == seg.get('pronunciation'), f'{ident}: guide rendering mismatch')
            check(all(not re.search(r'\s', p[1]) for p in pairs), f'{ident}: use hyphens inside one word guide')
        speaker = seg.get('speaker')
        key = seg.get('accent_key')
        check(speaker in speakers, f'{ident}: unknown speaker')
        check(key in keys, f'{ident}: undefined accent key')
        if speaker in speakers:
            expected = speakers[speaker].get('accent_key')
            if key != expected:
                check(bool(seg.get('accent_switch_reason')) and bool(seg.get('accent_switch_end_id')), f'{ident}: unscoped accent switch')
        focus = seg.get('focus', [])
        check(isinstance(focus, list) and all(type(i) is int and 0 <= i < len(tokens) for i in focus), f'{ident}: invalid focus token')
        rc, pc = seg.get('reading_cues'), seg.get('pronunciation_cues')
        check(rc == pc, f'{ident}: cue drift between scripts')
        check(isinstance(rc, dict) and set(rc) == {'before', 'after'}, f'{ident}: cue placement missing')
        if isinstance(rc, dict):
            for position in ['before', 'after']:
                refs = rc.get(position, [])
                check(isinstance(refs, list), f'{ident}: cue refs must be lists')
                if not isinstance(refs, list):
                    continue
                for ref in refs:
                    check(ref in cues, f'{ident}: unknown cue {ref}')
                    used.append(ref)
                    if ref in cues:
                        cue = cues[ref]
                        check(cue.get('segment_id') == ident and cue.get('position') == position, f'{ref}: anchor mismatch')
    check(not source[cursor:].strip(), 'Source tail omitted')
    check(len(used) == len(set(used)), 'Cue ID used more than once per take')
    check(set(used) == set(cues), 'Unrendered or unknown cue IDs')
    serial_time = 0.0
    for ref, cue in cues.items():
        kind = cue.get('kind')
        check(kind in {'VOICE', 'MOUTH', 'PROP', 'TRACK', 'ATM', 'PAUSE', 'ACCENT'}, f'{ref}: unsupported cue kind')
        check(bool(cue.get('text')), f'{ref}: missing cue instruction')
        if kind in {'MOUTH', 'PROP', 'TRACK'}:
            for field in ['purpose', 'basis', 'method', 'level', 'exit', 'fallback']:
                check(bool(cue.get(field)), f'{ref}: missing {field}')
            check(cue.get('basis') in {'TEXT', 'CHOICE', 'UNKNOWN'}, f'{ref}: invalid evidence basis')
            check(not (kind == 'MOUTH' and cue.get('overlap_speech')), f'{ref}: mouth/speech overlap')
            check(data.get('mode') != 'NARRATION', f'{ref}: effect active in NARRATION')
            if kind == 'TRACK':
                check(data.get('mode') == 'PRODUCTION-PLAN', f'{ref}: track outside production mode')
                check(cue.get('availability') in {'present', 'proposed', 'missing'}, f'{ref}: missing availability')
                check(bool(cue.get('rights_status')), f'{ref}: missing rights status')
                if cue.get('availability') == 'present':
                    check(bool(cue.get('asset')), f'{ref}: present track lacks asset')
        if kind in {'MOUTH', 'PROP', 'TRACK', 'PAUSE'}:
            duration = cue.get('duration_seconds')
            check(type(duration) in {int, float} and math.isfinite(duration) and duration >= 0, f'{ref}: invalid duration')
            if type(duration) in {int, float} and math.isfinite(duration) and duration >= 0 and not cue.get('overlap_speech'):
                serial_time += duration
        if cue.get('word_anchor'):
            selected = next((s for s in segments if isinstance(s, dict) and s.get('id') == cue.get('segment_id')), {})
            check(cue['word_anchor'] in selected.get('reading', ''), f'{ref}: word anchor absent')
    for seg in segments:
        if isinstance(seg, dict) and seg.get('accent_switch_end_id'):
            end_id = seg['accent_switch_end_id']
            check(end_id in ids and ids.index(end_id) >= ids.index(seg['id']), f"{seg['id']}: invalid switch end")
    return {'ok': not errors, 'checks': checks, 'errors': errors, 'segments': len(segments), 'source_words': words, 'cue_events_per_take': len(used), 'nonoverlap_cue_seconds': round(serial_time, 3), 'limits': ['No acoustic verification', 'No acting-quality assessment', 'No automatic sentence-boundary proof', 'Word alignment does not prove phonetic correctness']}


def emphasise(text, focus):
    tokens = list(re.finditer(r'\S+', text))
    result = text
    for i in sorted(set(focus), reverse=True):
        token = tokens[i]
        positions = [j for j, c in enumerate(token.group()) if c.isalnum()]
        if positions:
            start, end = token.start() + positions[0], token.start() + positions[-1] + 1
            result = result[:start] + '**' + result[start:end] + '**' + result[end:]
    return result


def render(data):
    out = ['# ' + data['title'], '', 'Version: 1.2.0.', '', '## SETTINGS AND KEY', '']
    out.extend(data.get('settings_lines', []))
    out.extend(['', 'Read ONE script per take.', 'Cues and IDs are silent.', ''])
    for heading, field, cue_field in [('READING SCRIPT', 'reading', 'reading_cues'), ('PRONUNCIATION SCRIPT', 'pronunciation', 'pronunciation_cues')]:
        out.extend(['## ' + heading, ''])
        for seg in data['segments']:
            out.extend([f"### {seg['id']} / {seg['speaker']} / {seg['accent_key']}", ''])
            for ref in seg[cue_field]['before']:
                cue = data['cues'][ref]
                out.extend([f"[{cue['kind']} {ref}: {cue['text']}]", ''])
            out.extend([emphasise(seg[field], seg.get('focus', [])), ''])
            for ref in seg[cue_field]['after']:
                cue = data['cues'][ref]
                out.extend([f"[{cue['kind']} {ref}: {cue['text']}]", ''])
    out.extend(['## COACHING NOTES', ''])
    out.extend(data.get('coaching_notes', []))
    out.extend(['', '## COVERAGE', ''])
    out.extend(data.get('coverage_notes', []))
    return '\n'.join(out).rstrip() + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('score', type=Path)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--render', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.score.read_text(encoding='utf-8'))
        source = args.source.read_bytes().decode('utf-8')
        report = validate(data, source)
        if args.render and report['ok']:
            if args.render.resolve() in {args.source.resolve(), args.score.resolve()}:
                raise ValueError('Render destination would overwrite input')
            args.render.parent.mkdir(parents=True, exist_ok=True)
            args.render.write_text(render(data), encoding='utf-8')
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report['ok'] else 1
    except (OSError, ValueError, TypeError, KeyError, AttributeError, IndexError) as exc:
        print(json.dumps({'ok': False, 'errors': [str(exc)]}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
