import collections
import copy
import json
from pathlib import Path
import sys
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import run_task_performance as task


class TaskPerformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = task.verify_dataset(task.DATASET)
        cls.inputs = list(task.data.read_jsonl(task.DATASET / 'inputs.jsonl'))
        cls.packets = list(task.data.read_jsonl(task.DATASET / 'packets.jsonl'))

    def test_all_task_panels_keep_source_gold_and_data(self):
        source = {r['id']: r for r in task.data.evaluation_rows(task.data.DEFAULT, True, 'clinical')}
        self.assertEqual(len(self.manifest['families']), 29)
        self.assertEqual(sum(bool(f['selected']) for f in self.manifest['families']), 26)
        self.assertEqual(len(self.inputs), 566)
        for row in self.inputs:
            self.assertEqual(row['gold'], source[row['id']]['gold'])
            self.assertEqual(row['request'], source[row['id']]['request'])
            self.assertEqual(row['provenance'], source[row['id']]['provenance'])
        for family in self.manifest['families']:
            self.assertEqual(family['selected'], min(32, family['available']))
            self.assertTrue(all(c <= family['selected'] for c in family['concurrency']))

    def test_packets_partition_exact_same_panel_without_padding_or_truncation(self):
        source = {r['id']: r for r in self.inputs}
        for family in self.manifest['families']:
            expected = {r['id'] for r in self.inputs if r['family'] == family['id']}
            for target in family['batch_targets']:
                seen = []
                packets = [p for p in self.packets if p['family'] == family['id'] and p['target'] == target]
                for p in packets:
                    self.assertTrue(task.fits(p))
                    self.assertLessEqual(len(p['gold']), target)
                    for key, uid in p['source_ids'].items():
                        seen.append(uid)
                        self.assertEqual(p['gold'][key], source[uid]['gold'])
                        if target == 1:
                            self.assertEqual(p['request'], source[uid]['request'])
                        else:
                            self.assertEqual(p['request']['state']['records'][key], source[uid]['request']['state'])
                            question = p['request']['questions'][key]
                            original = source[uid]['request']['questions']['decision']
                            self.assertEqual(question['criteria'], original['criteria'])
                            self.assertTrue(question['instructions'].endswith(original['instructions']))
                self.assertEqual(set(seen), expected)
                self.assertEqual(len(seen), len(expected))

    def test_budget_splits_long_cases_instead_of_claiming_32_questions(self):
        trial = next(f for f in self.manifest['families'] if f['id'] == 'trial_referral')
        self.assertGreater(len(trial['packet_sizes']['32']), 1)
        self.assertEqual(sum(trial['packet_sizes']['32']), 32)

    def test_matrix_is_complete_and_does_not_schedule_empty_tasks(self):
        cells = task.plan(self.manifest)
        self.assertEqual(len(cells), 708)
        keys = [tuple(c.values()) for c in cells]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(set(c['model'] for c in cells), set(task.MODELS))
        self.assertTrue(all(c['family'] not in ['dose_appropriateness', 'critical_result_escalation', 'department_routing'] for c in cells))

    def test_payload_never_sends_provenance_or_gold(self):
        item = next(p for p in self.packets if p['target'] == 8)
        dirty = {**item['request'], 'gold': 'PRIVATE_GOLD', 'provenance': 'PRIVATE_SOURCE'}
        for model in task.MODELS:
            body = task.payload(dirty, model)
            self.assertNotIn('PRIVATE', json.dumps(body))
        body = task.payload(dirty, 'deepseek-flash')
        self.assertEqual(body['max_tokens'], 512)
        self.assertEqual(body['thinking'], {'type': 'disabled'})

    def test_flat_json_validates_exact_keys_and_partial_outputs(self):
        item = next(p for p in self.packets if p['target'] == 8)
        response = lambda body, reason='stop': {'choices': [{'finish_reason': reason, 'message': {'content': json.dumps(body)}}]}
        good = task.evaluate(item, response(item['gold']), 'deepseek-flash')
        self.assertTrue(good['all_correct'])
        self.assertEqual(good['valid_decisions'], 8)
        short = dict(list(item['gold'].items())[:3])
        result = task.evaluate(item, response(short), 'deepseek-flash')
        self.assertEqual(result['correct_decisions'], 3)
        self.assertFalse(result['complete_valid'])
        nested = {key: {'choice': value} for key, value in item['gold'].items()}
        self.assertEqual(task.evaluate(item, response(nested), 'deepseek-flash')['valid_decisions'], 0)
        self.assertEqual(task.evaluate(item, response(item['gold'], 'length'), 'deepseek-flash')['valid_decisions'], 0)
        extra = {**item['gold'], 'unknown': 'A'}
        self.assertFalse(task.evaluate(item, response(extra), 'deepseek-flash')['complete_valid'])

    def test_persistent_pool_executes_once_and_records_no_secret(self):
        seen = []
        lock = threading.Lock()
        def fake(session, item, model, timeout, epoch):
            with lock:
                seen.append(item['id'])
            return {'id': item['id'], 'http_status': 200}
        items = [{'id': str(i)} for i in range(32)]
        pool = task.ModelPool('jev-1.13.0', 'private-secret', 1, workers=8)
        try:
            with patch.object(task, 'perform', side_effect=fake):
                first, _, fatal = pool.run(items, 8)
                sessions = {id(s) for s in pool.sessions}
                second, _, _ = pool.run(items, 8)
            self.assertFalse(fatal)
            self.assertEqual(len(first), 32)
            self.assertEqual(len(second), 32)
            self.assertEqual(sessions, {id(s) for s in pool.sessions})
            self.assertEqual(collections.Counter(seen), {str(i): 2 for i in range(32)})
            self.assertNotIn('private-secret', json.dumps(first))
        finally:
            pool.close()


if __name__ == '__main__':
    unittest.main()
