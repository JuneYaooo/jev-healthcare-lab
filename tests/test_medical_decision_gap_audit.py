"""Clinical time boundaries, span mapping and compatibility of the v0.5 additions."""
import collections
import importlib.util
import json
from pathlib import Path
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'benchmarks/medical_decision_v1'
spec = importlib.util.spec_from_file_location('benchmark', ROOT / 'scripts/medical_decision_dataset.py')
bench = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bench)


def trajectory(first_positive=None, length=24):
    return [{'ICULOS': str(i), 'SepsisLabel': str(int(first_positive is not None and i >= first_positive))}
            for i in range(1, length + 1)]


class ClinicalBoundaryTests(unittest.TestCase):
    def test_shift_and_landmark_boundaries(self):
        # Source label starts six hours before inferred clinical onset.
        self.assertIsNone(bench.sepsis_at_24h(trajectory(6)))  # onset at landmark
        self.assertEqual(bench.sepsis_at_24h(trajectory(7)), 'yes')  # onset 13
        self.assertEqual(bench.sepsis_at_24h(trajectory(18)), 'yes')  # onset 24
        self.assertEqual(bench.sepsis_at_24h(trajectory(19, 30)), 'no')  # onset 25
        self.assertEqual(bench.sepsis_at_24h(trajectory()), 'no')

    def test_censoring_and_time_gaps_do_not_become_negatives(self):
        self.assertIsNone(bench.sepsis_at_24h(trajectory(1)))
        self.assertIsNone(bench.sepsis_at_24h(trajectory(length=23)))
        self.assertEqual(bench.sepsis_at_24h(trajectory(7, 13)), 'yes')
        self.assertIsNone(bench.sepsis_at_24h(trajectory(7, 12)))  # inferred event not observed
        rows = trajectory()
        rows[3]['ICULOS'] = '5'
        self.assertIsNone(bench.sepsis_at_24h(rows))
        rows = trajectory(7)
        rows[-1]['SepsisLabel'] = '0'
        self.assertIsNone(bench.sepsis_at_24h(rows))

    def test_privacy_partial_overlap_is_not_outside(self):
        text = 'Alice has pain'
        entities = {'T1': {'start': 0, 'end': 5, 'text': 'Alice'}}
        candidates = bench.privacy_token_candidates(text, entities)
        self.assertEqual([(x['text'], x['gold']) for x in candidates],
                         [('Alice', 'yes'), ('has', 'no'), ('pain', 'no')])
        entities['T1'].update(end=3, text='Ali')
        self.assertNotIn('Alice', [c['text'] for c in bench.privacy_token_candidates(text, entities)])
        entities['T1']['text'] = 'bad offset'
        self.assertEqual(bench.privacy_token_candidates(text, entities), [])

    def test_reference_conditions_are_not_swallowed_by_age(self):
        question = ("For the lab test 'Estradiol' measuring in 'pmol/L' in Specimen 'Serum' "
                    "for 'Female' and 'any age group' with the condition 'Follicular phase' "
                    "in the category 'Unconjugated', what is the correct lower and upper bound "
                    "range values in SI reference range?")
        context = bench.labqar_context(question)
        self.assertEqual(context['age_group'], 'any age group')
        self.assertEqual(context['condition'], 'Follicular phase')
        self.assertEqual(context['category'], 'Unconjugated')
        self.assertIsNone(bench.labqar_context('unparseable'))


class GapReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = [json.loads(x) for x in (DATA / 'samples.jsonl').read_text().splitlines()]

    def test_all_previous_full_records_are_unchanged(self):
        current = {r['id']: r for r in self.rows}
        count = 0
        for path in (ROOT / 'releases').glob('*v0.4.0-*.zip'):
            with zipfile.ZipFile(path) as z:
                for line in z.read(next(n for n in z.namelist() if n.endswith('/samples.jsonl'))).splitlines():
                    row = json.loads(line)
                    self.assertEqual(current[row['id']], row)
                    count += 1
        self.assertEqual(count, 4938)

    def test_audit_matches_all_prior_empty_tasks(self):
        audit = json.loads((DATA / 'gap_audit.json').read_text())['tasks']
        self.assertEqual(len(audit), 21)
        counts = collections.Counter(r['task'] for r in self.rows)
        self.assertEqual(sum(a['result'] == 'adopted' for a in audit), 3)
        for a in audit:
            self.assertEqual(a['result'] == 'adopted', counts[a['task_id']] > 0)
            self.assertTrue(a['sources'])
            self.assertTrue(a['finding'])

    def test_sepsis_preselection_and_no_future_inputs(self):
        folder = DATA / 'sources/sepsis2019'
        frame = json.loads((folder / 'selection_frame.json').read_text())['filenames']
        pre = json.loads((folder / 'preselection.json').read_text())['files']
        import hashlib
        expected = sorted(frame, key=lambda x: hashlib.sha256(('20261010:sepsis2019:setA:' + x).encode()).hexdigest())[:1000]
        self.assertEqual(pre, expected)
        rows = [r for r in self.rows if r['task'] == 'deterioration_prediction']
        self.assertEqual(len(rows), 100)
        self.assertEqual(len({r['group_id'] for r in rows}), 100)
        self.assertEqual(collections.Counter(r['gold'] for r in rows), {'yes': 11, 'no': 89})
        for row in rows:
            self.assertEqual(row['provenance']['split'], 'upstream_train_reserved_for_local_evaluation')
            state = row['request']['state']
            self.assertEqual([r['hour'] for r in state['hourly_observations']], list(range(1, 13)))
            self.assertEqual(set(state), {'prediction_hour', 'outcome_window_hours', 'hourly_observations', 'feature_definitions', 'missing_value_meaning'})
            self.assertEqual(set(state['feature_definitions']), set(bench.SEPSIS_FEATURES))
            for observation in state['hourly_observations']:
                self.assertEqual(set(observation), {'hour'} | set(bench.SEPSIS_FEATURES))

    def test_reference_answer_matches_unique_source_context(self):
        rows = [r for r in self.rows if r['task'] == 'reference_range']
        self.assertEqual(len(rows), 72)
        for row in rows:
            state = row['request']['state']
            answers = {r['range'] for r in state['reference_entries']
                       if {k: v for k, v in r.items() if k != 'range'} == state['target_context']}
            self.assertEqual(len(answers), 1)
            self.assertEqual(next(iter(answers)), row['metadata']['original_answer'])
            self.assertEqual(row['request']['questions']['decision']['criteria'][row['gold']],
                             row['metadata']['original_answer'] + ' ' + state['target_context']['unit'])

    def test_privacy_has_two_classes_and_no_reused_documents(self):
        rows = [r for r in self.rows if r['task'] == 'privacy_candidate']
        self.assertEqual(collections.Counter(r['gold'] for r in rows), {'yes': 50, 'no': 50})
        self.assertEqual(len({r['group_id'] for r in rows}), 100)
        for row in rows:
            self.assertEqual(row['provenance']['split'], 'official_test')
            state = row['request']['state']; target = state['target']
            self.assertEqual(state['clinical_text'][target['start']:target['end']], target['text'])
            self.assertNotIn('annotation_ids', state)


if __name__ == '__main__':
    unittest.main()
