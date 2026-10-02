"""Regression probes for source loss, accent drift, and impossible cues."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('score_validator', ROOT / 'scripts/validate_score.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class ScoreChecks(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'examples/puppy.score.json').read_text())
        self.source = (ROOT / 'examples/SOURCE_TEXT.txt').read_bytes().decode()

    def check_bad(self, text):
        report = v.validate(self.data, self.source)
        self.assertFalse(report['ok'])
        self.assertTrue(any(text in e for e in report['errors']), report)

    def test_complete_fixture(self):
        report = v.validate(self.data, self.source)
        self.assertTrue(report['ok'], report)
        self.assertEqual(report['source_words'], 64)
        self.assertEqual(report['segments'], 14)
        self.assertEqual(report['nonoverlap_cue_seconds'], 3.6)

    def test_missing_word(self):
        self.data['segments'][0]['reading'] = 'Rain tapped the window.'
        self.check_bad('reading differs')

    def test_source_changed(self):
        self.source = self.source.replace('lost', 'found')
        self.check_bad('Source hash')

    def test_missing_guide(self):
        self.data['segments'][0]['word_guides'].pop()
        self.check_bad('word coverage')

    def test_empty_guide(self):
        self.data['segments'][0]['word_guides'][0][1] = ''
        self.check_bad('invalid word_guides')

    def test_guide_display_drift(self):
        self.data['segments'][0]['pronunciation'] = 'rayn tapt.'
        self.check_bad('guide rendering')

    def test_omitted_source_tail(self):
        self.data['segments'].pop()
        self.check_bad('Source tail')

    def test_missing_segment(self):
        self.data['segments'].pop(2)
        self.check_bad('skipped source text')

    def test_unscoped_accent_change(self):
        self.data['accent_keys']['GA-R'] = 'test target'
        self.data['segments'][7]['accent_key'] = 'GA-R'
        self.check_bad('unscoped accent switch')

    def test_undefined_key(self):
        self.data['segments'][0]['accent_key'] = 'UNKNOWN-KEY'
        self.check_bad('undefined accent key')

    def test_mouth_overlap(self):
        self.data['cues']['FX01']['overlap_speech'] = True
        self.check_bad('mouth/speech overlap')

    def test_effect_without_exit(self):
        del self.data['cues']['FX01']['exit']
        self.check_bad('missing exit')

    def test_cue_lane_drift(self):
        self.data['segments'][0]['pronunciation_cues']['before'] = []
        self.check_bad('cue drift')

    def test_duplicate_cue(self):
        for key in ['reading_cues', 'pronunciation_cues']:
            self.data['segments'][0][key]['before'].append('FX01')
        self.check_bad('more than once')

    def test_effect_in_narration(self):
        self.data['mode'] = 'NARRATION'
        self.check_bad('effect active in NARRATION')

    def test_nan_duration(self):
        self.data['cues']['FX01']['duration_seconds'] = float('nan')
        self.check_bad('invalid duration')

    def test_bad_word_anchor(self):
        self.data['cues']['V01']['word_anchor'] = 'monster'
        self.check_bad('word anchor absent')

    def test_script_order_and_single_count(self):
        out = v.render(self.data)
        self.assertLess(out.index('## READING SCRIPT'), out.index('## PRONUNCIATION SCRIPT'))
        self.assertLess(out.index('## PRONUNCIATION SCRIPT'), out.index('## COACHING NOTES'))
        self.assertEqual(out.count('### P01-'), 28)
        self.assertEqual(out.count('[MOUTH FX01:'), 2)
        self.assertEqual(v.validate(self.data, self.source)['cue_events_per_take'], 12)

    def test_literal_cue_and_negation_are_source(self):
        text = 'No, [VOICE: erase] is text.'
        tokens = text.split()
        data = {'format_version': 1, 'title': 'Literal source', 'source_sha256': hashlib.sha256(text.encode()).hexdigest(), 'mode': 'NARRATION', 'accent_keys': {'USER': 'literal drill'}, 'speakers': {'N': {'accent_key': 'USER'}}, 'cues': {}, 'segments': [{'id': 'S01', 'speaker': 'N', 'accent_key': 'USER', 'start': 0, 'end': len(text), 'reading': text, 'pronunciation': text, 'word_guides': [[t,t] for t in tokens], 'focus': [], 'reading_cues': {'before': [], 'after': []}, 'pronunciation_cues': {'before': [], 'after': []}}]}
        self.assertTrue(v.validate(data, text)['ok'])
        self.assertIn(text, v.render(data))
        data['segments'][0]['reading'] = text.replace('No, ', '')
        self.assertFalse(v.validate(data, text)['ok'])

    def test_refuses_overwriting_input(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'source.txt'
            score = Path(folder) / 'score.json'
            source.write_text(self.source)
            score.write_text(json.dumps(self.data))
            proc = subprocess.run([sys.executable, str(ROOT/'scripts/validate_score.py'), str(score), '--source', str(source), '--render', str(source)], capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(source.read_text(), self.source)


if __name__ == '__main__':
    unittest.main(verbosity=2)
