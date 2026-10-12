import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_performance_report as report


@unittest.skipUnless((report.RUN / 'archive_manifest.json').exists(), 'Full performance archive is not complete yet')
class PerformanceArchiveTests(unittest.TestCase):
    def test_all_cells_recompute_from_raw_responses(self):
        _, verified = report.verify(report.RUN)
        self.assertEqual(len(verified), 60)
        self.assertEqual(sum(len(rows) for _, rows in verified), 3870)
        grouped = report.aggregate(verified)
        self.assertEqual(len(grouped), 20)
        self.assertTrue(all(r['repeats'] == 3 for r in grouped))
        for group in grouped:
            self.assertAlmostEqual(group['valid_decisions_per_s'], group['valid_decisions'] / sum(group['wall_per_repeat_s']))

    def test_modified_response_is_detected_even_if_archive_hash_is_updated(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'run'
            shutil.copytree(report.RUN, target)
            path = target / 'cell-000.jsonl'
            rows = list(report.data.read_jsonl(path))
            rows[0]['correct_decisions'] = 2
            report.data.write_jsonl(path, rows)
            manifest = json.loads((target / 'archive_manifest.json').read_text())
            manifest['files']['cell-000.jsonl'] = report.data.file_sha(path)
            report.data.write_json(target / 'archive_manifest.json', manifest)
            with self.assertRaisesRegex(ValueError, 'score mismatch'):
                report.verify(target)

    def test_duplicate_matrix_cannot_masquerade_as_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'run'
            shutil.copytree(report.RUN, target)
            config = json.loads((target / 'config.json').read_text())
            config['cells'][1] = config['cells'][0]
            report.data.write_json(target / 'config.json', config)
            manifest = json.loads((target / 'archive_manifest.json').read_text())
            manifest['files']['config.json'] = report.data.file_sha(target / 'config.json')
            report.data.write_json(target / 'archive_manifest.json', manifest)
            with self.assertRaisesRegex(ValueError, 'experiment matrix'):
                report.verify(target)


if __name__ == '__main__':
    unittest.main()
