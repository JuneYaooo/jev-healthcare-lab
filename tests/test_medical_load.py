import asyncio
import copy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import run_medical_load as run
import build_medical_load_report as report


def item():
    return {'id': 'case', 'gold': {'q000': 'yes', 'q001': 'no'},
            'source_ids': {'q000': 'private-gold-id', 'q001': 'second-id'},
            'request': {'state': {'material': 'neutral'}, 'questions': {
                k: {'type': 'choice', 'instructions': 'decide', 'criteria': {'yes': 'present', 'no': 'absent'}}
                for k in ('q000', 'q001')}}}


def response(text='{"q000":"yes","q001":"no"}'):
    return {'choices': [{'finish_reason': 'stop', 'message': {'content': text}}],
            'usage': {'prompt_tokens': 1000, 'completion_tokens': 100,
                      'prompt_cache_hit_tokens': 200, 'prompt_cache_miss_tokens': 800}}


def row(uid='case', start=1., end=1.5):
    p = item()
    data = response()
    return {'item_id': uid, 'model': 'deepseek-flash', 'http_status': 200,
            'response': data, 'predicted': {'q000': 'yes', 'q001': 'no'}, 'correct': 2,
            'valid': 2, 'decisions': 2, 'cost_cny': run.cost(data, 'deepseek-flash'),
            'request_sha256': run.data.digest(run.payload(p, 'deepseek-flash')),
            'queued_s': start-.1, 'http_start_s': start, 'completion_s': end, 'http_s': end-start}


class MedicalLoadTests(unittest.TestCase):
    def test_payload_only_contains_blinded_input_and_provider_specific_controls(self):
        for model in run.MODELS:
            payload = run.payload(item(), model)
            self.assertNotIn('private-gold-id', str(payload))
            self.assertNotIn('gold', payload)
            if model.startswith('qwen'):
                self.assertFalse(payload['enable_thinking'])
                self.assertNotIn('thinking', payload)
                self.assertTrue(payload['model'].startswith('Qwen/'))
            elif model == 'deepseek-flash':
                self.assertEqual(payload['thinking'], {'type': 'disabled'})

    def test_no_answer_repair_and_duplicate_keys_rejected(self):
        self.assertEqual(run.choices(item(), response('{"q000":"present","q001":"no"}'), 'deepseek-flash'), {'q001': 'no'})
        self.assertEqual(run.choices(item(), response('{"q000":"yes","q000":"no"}'), 'deepseek-flash'), {})
        r = response(); r['choices'][0]['finish_reason'] = 'length'
        self.assertEqual(run.choices(item(), r, 'qwen3.8-27b'), {})

    def test_provider_prices_include_output_and_real_cache_usage(self):
        self.assertEqual(run.cost(response(), 'qwen3.5-9b'), [.0009, .0009])
        self.assertEqual(run.cost(response(), 'qwen3.8-27b'), [.0042, .0042])
        lo, hi = run.cost(response(), 'deepseek-flash')
        self.assertAlmostEqual(lo, (.003*200+.15*800+.6*100)*run.FX/1e6)
        self.assertEqual(hi, 2*lo)
        self.assertIsNone(run.cost({}, 'jev-1.13.0'))
        self.assertIsNone(run.cost({'usage': {'prompt_tokens': 1, 'completion_tokens': 1}}, 'deepseek-flash'))

    def test_full_fixed_dataset_required_and_invalid_answer_is_wrong(self):
        items = {'case': item(), 'second': {**item(), 'id': 'second'}}
        self.assertIsNone(report.quality([row()], items)['accuracy'])
        r = row('second'); r['predicted'] = {'q000': 'yes'}
        q = report.quality([row(), r], items, fixed=True)
        self.assertEqual(q['accuracy'], .75)
        self.assertAlmostEqual(q['macro_f1'], (1+2/3)/2)
        # Option-letter tests must never receive class-level F1.
        self.assertIsNone(report.quality([row()], {'case': item()}, fixed=False)['macro_f1'])

    def test_completions_and_admitted_latency_use_separate_cohorts(self):
        meta = {'warmup_s': 1, 'window_s': 2, 'stop': None, 'wall_s': 4}
        rows = [row(start=.5, end=1.5), row(start=2.5, end=3.5)]
        w = report.window(rows, meta)
        self.assertEqual(w['throughput'], 1)
        self.assertEqual(w['http_samples'], [1.])
        self.assertAlmostEqual(w['mean_http_concurrency'], .5)
        self.assertFalse(report.combine([w], 2)['complete'])
        meta['stop'] = 'budget_limit'
        self.assertIsNone(report.window(rows, meta)['throughput'])

    def test_archive_rechecks_scores_not_only_hashes(self):
        r = row(); report.validate(r, {'case': item()})
        r['correct'] = 0
        with self.assertRaisesRegex(ValueError, 'score mismatch'):
            report.validate(r, {'case': item()})

    def test_budget_includes_in_flight_reservations(self):
        budget = run.Budget(1.)
        budget.reserve(.8)
        with self.assertRaisesRegex(RuntimeError, 'budget_limit'):
            budget.reserve(.3)
        budget.settle(.8, .2)
        budget.reserve(.7)
        self.assertAlmostEqual(budget.used+budget.held, .9)

    def test_absent_candidate_classes_do_not_artificially_reduce_macro_f1(self):
        p = item()
        for q in p['request']['questions'].values():
            q['criteria']['unused'] = 'Category absent from fixed gold'
        result = report.quality([row()], {'case': p}, fixed=True)
        self.assertEqual(result['macro_f1'], 1.)


class MedicalLoadAsyncTests(unittest.IsolatedAsyncioTestCase):
    async def test_idle_quota_interval_does_not_shorten_the_observation_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = run.Runner('deepseek-flash', {'window_s': .04, 'warmup_s': .01}, {'case': item()}, run.Budget(1))
            runner.path = Path(tmp)
            runner.pacer.next_token = asyncio.get_running_loop().time() + .03
            async def no_more_admissions(*args):
                return None
            started = run.time.perf_counter()
            with patch.object(runner, 'request', no_more_admissions):
                await runner.load(None, {'id': 'idle', 'load_ids': ['case']}, 0, 3)
            elapsed = run.time.perf_counter()-started
            meta = run.json.loads((Path(tmp)/'idle-r0-c3.json').read_text())
            self.assertGreaterEqual(elapsed, .08)
            self.assertGreaterEqual(meta['wall_s'], .05)
            self.assertLess(meta['wall_s'], elapsed)
            self.assertTrue(report.window([], meta)['full'])

    async def test_connection_outage_stops_load_instead_of_busy_retrying(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = run.Runner('deepseek-flash', {'window_s': .05, 'warmup_s': 0}, {'case': item()}, run.Budget(1))
            runner.path = Path(tmp)
            calls = 0
            async def fake(*args):
                nonlocal calls
                calls += 1
                result = row(); result['http_status'] = 0
                return result
            with patch.object(runner, 'request', fake):
                with self.assertRaisesRegex(RuntimeError, 'service_or_connection_circuit'):
                    await runner.load(None, {'id': 'outage', 'load_ids': ['case']}, 0, 3)
            self.assertLessEqual(calls, 22)
            metadata = run.json.loads((Path(tmp)/'outage-r0-c3.json').read_text())
            self.assertEqual(metadata['stop'], 'service_or_connection_circuit')


if __name__ == '__main__':
    unittest.main()
