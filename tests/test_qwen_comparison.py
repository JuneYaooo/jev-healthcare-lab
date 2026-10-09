"""Protect fixed inputs, comparable adaptation and auditable retry accounting."""
import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import analyze_qwen
from compare_qwen import MODEL, request_payload
from compare_deepseek import request_payload as reference_payload, sha


class QwenComparisonTests(unittest.TestCase):
    def setUp(self):
        self.row = {'task': 'aci_note_section', 'id': 'test', 'gold': 'a', 'metadata': {},
                    'request': {'state': 'source text', 'questions': {'decision': {'type': 'choice', 'instructions': 'Choose', 'criteria': {'a': 'first', 'b': 'second'}}}}}
        self.row['request_sha256'] = sha(self.row['request'])
        self.record = {'task': self.row['task'], 'id': 'test', 'request_sha256': self.row['request_sha256'],
                       'provider_request_sha256': sha(request_payload(self.row)), 'status': 'ok', 'elapsed_s': 2.0,
                       'normalized_answers': {'decision': {'choice': 'a'}}, 'prior_attempts': [], 'reported_total_tokens': 110,
                       'response': {'model': MODEL, 'choices': [{'finish_reason': 'stop', 'message': {'content': '{"answers":{"decision":"a"}}'}}],
                                    'usage': {'prompt_tokens': 100, 'completion_tokens': 10, 'total_tokens': 110}}}

    def summarize(self, records):
        with patch.object(analyze_qwen, 'load_rows', return_value=[self.row]):
            return analyze_qwen.summarize(records)

    def test_payload_uses_reference_prompt_without_gold(self):
        actual = request_payload(self.row)
        expected = reference_payload(self.row)
        expected.pop('thinking')
        expected.update(model=MODEL, enable_thinking=False)
        self.assertEqual(actual, expected)
        changed = copy.deepcopy(self.row)
        changed['gold'] = 'b'
        self.assertEqual(actual, request_payload(changed))

    def test_failed_attempt_usage_is_included_but_latency_is_not(self):
        prior = copy.deepcopy(self.record)
        prior.pop('prior_attempts')
        prior.update(status='error', error_type='ValueError', elapsed_s=50)
        prior['response']['choices'][0]['finish_reason'] = 'length'
        self.record['prior_attempts'] = [prior]
        self.record['reported_total_tokens'] = 220
        task = self.summarize([self.record])['tasks'][self.row['task']]
        self.assertAlmostEqual(task['cost_cny'], 2*(100*1.5+10*12)/1e6)
        self.assertEqual(task['latency_median_s'], 2)
        self.assertEqual(task['prior_attempts'], 1)

    def test_failed_classification_stays_in_denominator(self):
        self.record.update(status='http_error', http_status=429, reported_total_tokens=0)
        self.record.pop('response')
        self.record.pop('normalized_answers')
        result = self.summarize([self.record])
        self.assertTrue(result['summary']['complete'])
        self.assertEqual(result['summary']['failed_rows'], 1)
        self.assertEqual(result['tasks'][self.row['task']]['quality']['accuracy'], 0)
        self.assertIsNone(result['tasks'][self.row['task']]['latency_median_s'])

    def test_duplicate_changed_input_and_missing_rows(self):
        with self.assertRaises(ValueError):
            self.summarize([self.record, self.record])
        self.assertFalse(self.summarize([])['summary']['complete'])
        self.record['provider_request_sha256'] = 'changed'
        with self.assertRaises(ValueError):
            self.summarize([self.record])

    def test_changed_normalization_and_thinking_are_rejected(self):
        self.record['normalized_answers']['decision']['choice'] = 'b'
        with self.assertRaises(ValueError):
            self.summarize([self.record])
        self.record['normalized_answers']['decision']['choice'] = 'a'
        self.record['response']['usage']['completion_tokens_details'] = {'reasoning_tokens': 5}
        with self.assertRaises(ValueError):
            self.summarize([self.record])


if __name__ == '__main__':
    unittest.main()
