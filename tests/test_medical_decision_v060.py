"""Checks for source joins, numerical meaning and frozen v0.5 compatibility."""
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'benchmarks/medical_decision_v1'
spec = importlib.util.spec_from_file_location('benchmark_v060', ROOT / 'scripts/medical_decision_dataset.py')
bench = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bench)


class ExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = list(bench.read_jsonl(DATA / 'samples.jsonl'))

    def test_previous_complete_records_are_preserved(self):
        current = {r['id']: r for r in self.rows}
        count = 0
        for path in (ROOT / 'releases').glob('*v0.5.0-*.zip'):
            with zipfile.ZipFile(path) as z:
                for line in z.read(next(n for n in z.namelist() if n.endswith('/samples.jsonl'))).splitlines():
                    row = json.loads(line)
                    self.assertEqual(current[row['id']], row)
                    count += 1
        self.assertEqual(count, 5210)

    def test_lab_labels_have_their_stated_numerical_meaning(self):
        rows = [r for r in self.rows if r['task'] == 'lab_value_classification']
        self.assertEqual(len(rows), 100)
        labels = collections.Counter()
        for row in rows:
            state = row['request']['state']
            value = float(re.search(r"range' is (-?\d+(?:\.\d+)?)\.", state['question'])[1])
            low, high = [state['provided_reference_interval'][k] for k in ['lower_bound', 'upper_bound']]
            self.assertLess(low, high)
            self.assertNotIn(value, {low, high})
            expected = 'Low' if value < low else 'High' if value > high else 'Normal'
            self.assertEqual(row['request']['questions']['decision']['criteria'][row['gold']], expected)
            labels[expected] += 1
        self.assertEqual(set(labels), {'Low', 'Normal', 'High'})

    def test_cpic_joins_and_target_fields_are_separated(self):
        folder = DATA / 'sources/cpic'
        lookup = {x['id']: x for x in json.loads((folder / 'gene_result_lookup.json').read_text())}
        results = {x['id']: x for x in json.loads((folder / 'gene_result.json').read_text())}
        actions = {x['recommendationid']: x for x in json.loads((folder / 'recommendation_view.json').read_text())}
        rows = [r for r in self.rows if r['provenance']['source_id'] == 'cpic']
        self.assertEqual(len(rows), 184)
        for row in rows:
            loc = row['provenance']['locator']; state = row['request']['state']
            answer = row['request']['questions']['decision']['criteria'][row['gold']]
            if row['task'] == 'pgx_function_phenotype':
                original = lookup[loc['lookup_id']]
                result = results[original['phenotypeid']]
                self.assertEqual(answer, result['result'])
                self.assertEqual(state['gene'], result['genesymbol'])
                self.assertEqual(state['genetic_findings'], original['lookupkey'])
                self.assertNotIn('consultationtext', state)
                self.assertNotIn('result', state)
            else:
                original = actions[loc['recommendation_id']]
                self.assertEqual(answer, original['drugrecommendation'])
                self.assertEqual(state['gene_results'], original['lookupkey'])
                self.assertEqual(state['population'], original['population'])
                self.assertNotIn('drugrecommendation', state)
                self.assertNotIn('implications', state)

    def test_trial_records_retain_article_specific_rights(self):
        rows = [r for r in self.rows if r['task'] == 'trial_effect_direction']
        self.assertEqual(len(rows), 100)
        self.assertEqual(set(r['gold'] for r in rows), {'-1', '0', '1'})
        for row in rows:
            source = row['metadata']['article_attribution']
            self.assertRegex(source['license_url'], r'^https?://creativecommons.org/licenses/by/[0-9.]+/?$')
            self.assertTrue(source['title'] and source['authors'] and source['license_statement'])
            self.assertEqual(row['provenance']['split'], 'official_test_articles')
            self.assertNotIn('annotation', row['request']['state'])

    def test_frozen_api_response_works_offline_and_rejects_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); file = root / 'snapshot.json'; file.write_bytes(b'{"id":1}')
            entry = {'name': 'fixture', 'snapshot_path': file.name,
                     'sha256': hashlib.sha256(file.read_bytes()).hexdigest(), 'url': 'https://invalid.example'}
            with patch('urllib.request.urlopen', side_effect=AssertionError('must stay offline')):
                self.assertEqual(bench.locked_source_bytes(root, entry), file.read_bytes())
                file.write_bytes(b'{"id":2}')
                with self.assertRaises(ValueError):
                    bench.locked_source_bytes(root, entry)
                entry['snapshot_path'] = '../outside.json'
                with self.assertRaises(ValueError):
                    bench.locked_source_bytes(root, entry)


if __name__ == '__main__':
    unittest.main()
