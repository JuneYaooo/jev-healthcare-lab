import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import run_performance_evaluation as perf


class PerformanceTests(unittest.TestCase):
    def setUp(self):
        state, questions, gold = perf.synthetic_case(0)
        self.item = {'id': 'test', 'request': {'state': state, 'questions': dict(list(questions.items())[:2])},
                     'gold': dict(list(gold.items())[:2])}

    def response(self, answers, reason='stop'):
        return {'choices': [{'finish_reason': reason, 'message': {'content': json.dumps(answers)}}]}

    def test_payload_gold_is_never_sent_and_output_scales(self):
        self.item['request']['gold'] = 'SECRET'
        for model in perf.MODELS:
            body = perf.payload(self.item['request'], model)
            self.assertNotIn('SECRET', json.dumps(body))
        state, questions, _ = perf.synthetic_case(0)
        body = perf.payload({'state': state, 'questions': questions}, 'deepseek-flash')
        self.assertEqual(body['max_tokens'], 6400)
        self.assertEqual(body['thinking'], {'type': 'disabled'})

    def test_clinical_payload_matches_original_protocol(self):
        row = next(perf.data.read_jsonl(perf.DATASET / 'clinical.jsonl'))
        for model in perf.MODELS:
            self.assertEqual(perf.payload(row['request'], model), perf.clinical.payload(row['request'], model))
        response = self.response({'choice': row['gold']['decision']})
        self.assertTrue(perf.evaluate(row, response, 'deepseek-flash')['all_correct'])

    def test_partial_wrong_missing_extra_and_truncated_answers(self):
        good = {k: {'choice': v} for k, v in self.item['gold'].items()}
        full = perf.evaluate(self.item, self.response(good), 'deepseek-flash')
        self.assertEqual(full['correct_decisions'], 2)
        self.assertTrue(full['all_correct'])
        partial = perf.evaluate(self.item, self.response({'q000': good['q000']}), 'deepseek-flash')
        self.assertEqual(partial['correct_decisions'], 1)
        self.assertFalse(partial['complete_valid'])
        extra = perf.evaluate(self.item, self.response({**good, 'unexpected': {'choice': 'A'}}), 'deepseek-flash')
        self.assertFalse(extra['complete_valid'])
        truncated = perf.evaluate(self.item, self.response(good, 'length'), 'deepseek-flash')
        self.assertEqual(truncated['valid_decisions'], 0)
        bad = copy.deepcopy(good)
        bad['q000']['choice'] = 1
        self.assertEqual(perf.evaluate(self.item, self.response(bad), 'deepseek-flash')['valid_decisions'], 1)
        duplicate = {'choices': [{'finish_reason': 'stop', 'message': {'content': '{"q000":{"choice":"A"},"q000":{"choice":"B"}}'}}]}
        self.assertEqual(perf.evaluate(self.item, duplicate, 'deepseek-flash')['valid_decisions'], 0)

    def test_synthetic_gold_independently_follows_priority_rules(self):
        for index in range(3):
            state, questions, gold = perf.synthetic_case(index)
            self.assertEqual(len(questions), 200)
            for uid, row in state['records'].items():
                expected = ('A' if row['identity'] == 'mismatch' else 'B' if not row['documents_complete']
                            else 'C' if row['authorization'] == 'pending' else 'D')
                self.assertEqual(gold[uid], expected)
            self.assertEqual({v: list(gold.values()).count(v) for v in 'ABCD'}, {v: 50 for v in 'ABCD'})

    def test_frozen_dataset_reuses_exact_clinical_gold_and_fixed_fanout_state(self):
        perf.verify_dataset(perf.DATASET)
        source = {r['id']: r for r in perf.data.evaluation_rows(perf.data.DEFAULT)}
        clinical = list(perf.data.read_jsonl(perf.DATASET / 'clinical.jsonl'))
        self.assertEqual(len(clinical), 128)
        self.assertEqual(len({r['id'] for r in clinical}), 128)
        for row in clinical:
            self.assertEqual(row['request'], source[row['id']]['request'])
            self.assertEqual(row['gold']['decision'], source[row['id']]['gold'])
        fanout = list(perf.data.read_jsonl(perf.DATASET / 'fanout.jsonl'))
        for repeat in range(3):
            subset = [r for r in fanout if r['repeat'] == repeat]
            self.assertEqual(len({perf.data.digest(r['request']['state']) for r in subset}), 1)
            self.assertEqual(sorted(len(r['gold']) for r in subset), perf.COUNTS)

    def test_failed_requests_stay_in_denominator_and_cost_missing_is_visible(self):
        records = [{'elapsed_s': 1, 'completion_s': 1, 'status': 'success', 'complete_valid': True,
                    'all_correct': False, 'valid_decisions': 2, 'correct_decisions': 1,
                    'response': {'usage': {'input_tokens': 1000}}},
                   {'elapsed_s': 2, 'completion_s': 3, 'status': 'request_error', 'http_status': 429,
                    'complete_valid': False, 'all_correct': False, 'valid_decisions': 0, 'correct_decisions': 0}]
        result = perf.summary(records, 4, 'jev-1.13.0', 3, 6)
        self.assertEqual(result['accuracy'], 1 / 6)
        self.assertEqual(result['valid_decisions_per_s'], .5)
        self.assertEqual(result['not_started'], 1)
        self.assertEqual(result['http_429_rate'], .5)
        self.assertEqual(result['cost']['unpriced_requests'], 1)
        self.assertIsNone(result['cost']['usd_per_1000_correct_lower'])
        self.assertAlmostEqual(result['cost']['usd_lower'], .000042)

    def test_costs_account_for_cache_and_output(self):
        rows = [{'valid_decisions': 2, 'correct_decisions': 1,
                 'response': {'usage': {'prompt_cache_hit_tokens': 1000, 'prompt_cache_miss_tokens': 2000, 'completion_tokens': 100}}}]
        result = perf.costs(rows, 'deepseek-flash')
        self.assertAlmostEqual(result['usd_lower'], .000363)
        self.assertAlmostEqual(result['usd_upper'], .000726)

    def test_worker_pool_does_not_drop_or_duplicate_items(self):
        def fake(session, item, model, timeout, epoch):
            self.assertIsNotNone(epoch)
            return {'id': item['id'], 'http_status': 200}
        items = [{'id': str(i)} for i in range(128)]
        with patch.object(perf, 'perform', side_effect=fake):
            records, wall, fatal = perf.run_cell(items, 'jev-1.13.0', 16, 'fake-secret', 1)
        self.assertFalse(fatal)
        self.assertGreater(wall, 0)
        self.assertEqual(sorted(r['id'] for r in records), sorted(r['id'] for r in items))
        self.assertNotIn('fake-secret', json.dumps(records))


if __name__ == '__main__':
    unittest.main()
