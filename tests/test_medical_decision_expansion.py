"""Release-level checks for time boundaries, source splits, and frozen rows."""
import collections
import json
from pathlib import Path
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'benchmarks/medical_decision_v1'

class ExpansionIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = [json.loads(line) for line in (DATA / 'samples.jsonl').read_text().splitlines()]

    def test_previous_release_records_remain_exactly_unchanged(self):
        current = {r['id']: r for r in self.rows}
        count = 0
        for path in (ROOT / 'releases').glob('*v0.3.0-*.zip'):
            with zipfile.ZipFile(path) as archive:
                for line in archive.read(next(n for n in archive.namelist() if n.endswith('/samples.jsonl'))).splitlines():
                    old = json.loads(line)
                    self.assertEqual(current[old['id']], old)
                    count += 1
        self.assertEqual(count, 2200)

    def test_outcomes_do_not_expose_post_outcome_columns(self):
        for row in self.rows:
            if row['task'] not in {'readmission_30d', 'mortality_90d', 'maternal_risk', 'postoperative_disposition'}:
                continue
            state = row['request']['state']
            fields = set(state['clinical_features']) | set(state['feature_definitions'])
            self.assertFalse(fields & {'time', 'DEATH_EVENT', 'death_event', 'readmitted',
                                       'patient_nbr', 'encounter_id', 'RiskLevel', 'ADM-DECS'})
            self.assertIn('supporting_resources', row['provenance']['locator'])
        patients = [r['group_id'] for r in self.rows if r['task'] == 'readmission_30d']
        self.assertEqual(len(patients), len(set(patients)))

    def test_care_uses_only_public_test_patient_messages(self):
        rows = [r for r in self.rows if r['provenance']['source_id'] == 'care_bench']
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row['provenance']['split'], 'official_public_test_1')
            self.assertEqual(set(row['request']['state']), {'patient_messages_so_far'})
            self.assertTrue(all(isinstance(x, str) for x in row['request']['state']['patient_messages_so_far']))

    def test_e3c_is_official_test_with_document_attribution(self):
        import re
        train = set(re.findall(r"'([^']+)'", (DATA / 'sources/e3c/train_test_split.txt').read_text()))
        for row in self.rows:
            if row['provenance']['source_id'] != 'e3c':
                continue
            self.assertNotIn(row['provenance']['upstream_group'], train)
            self.assertEqual(row['provenance']['split'], 'official_test')
            self.assertTrue(row['metadata']['original_document']['docDOI'])
            self.assertTrue(row['metadata']['original_document']['docLicense'])

    def test_task_coverage_reports_actual_counts_and_small_tasks(self):
        summary = json.loads((DATA / 'summary.json').read_text())
        counts = collections.Counter(r['task'] for r in self.rows)
        self.assertEqual(len(counts), summary['ready_tasks'] + summary['partial_tasks'])
        self.assertGreater(len(counts), 50)
        for task in summary['tasks']:
            self.assertEqual(task['count'], counts[task['id']])
            if task['status'] == 'partial':
                self.assertLess(task['count'], task['target_count'])
                self.assertGreater(task['count'], 0)

if __name__ == '__main__':
    unittest.main()
