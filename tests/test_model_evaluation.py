import io
import json
from pathlib import Path
import sys
import threading
import tempfile
import shutil
import unittest
from unittest.mock import patch
import urllib.error

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import run_model_evaluation as runner


class ModelEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.request = {'state': {'case': 'Example'}, 'questions': {'decision': {
            'type': 'choice', 'instructions': 'Choose', 'criteria': {'0': 'No', '1': 'Yes'}}}}

    def test_payload_only_sends_request_and_same_content(self):
        dirty = {**self.request, 'gold': 'SECRET_GOLD', 'provenance': 'SECRET_SOURCE'}
        for model in runner.MODELS:
            body = runner.payload(dirty, model)
            self.assertNotIn('SECRET', json.dumps(body))
            if runner.MODELS[model]['provider'] != 'typesafe':
                self.assertEqual(json.loads(body['messages'][1]['content']), self.request)
                if runner.MODELS[model]['provider'] == 'siliconflow':
                    self.assertIs(body['enable_thinking'], False)
                    self.assertNotIn('thinking', body)
                    self.assertEqual(body['model'], runner.MODELS[model]['remote_model'])
                else:
                    self.assertEqual(body['thinking'], {'type': 'disabled'})
            else:
                self.assertEqual({k: body[k] for k in self.request}, self.request)

    def test_strict_answer_keys_no_numeric_or_explanation_repair(self):
        for value in [0, 'No', '0 because...', None]:
            response = {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps({'choice': value})}}]}
            with self.assertRaises(ValueError):
                runner.normalize(self.request, response, 'deepseek-flash')
        response = {'choices': [{'finish_reason': 'length', 'message': {'content': '{"choice":"0"}'}}]}
        with self.assertRaises(ValueError):
            runner.normalize(self.request, response, 'deepseek-flash')

    def test_qwen_models_share_deepseek_prompt_and_generation_limits(self):
        reference = runner.payload(self.request, 'deepseek-flash')
        for model, remote in [('qwen3.5-9b', 'Qwen/Qwen3.5-9B'),
                              ('qwen3.8-27b', 'Qwen/Qwen3.8-27B')]:
            body = runner.payload(self.request, model)
            self.assertEqual(body['model'], remote)
            for field in ['messages', 'temperature', 'max_tokens', 'response_format']:
                self.assertEqual(body[field], reference[field])
            self.assertIs(body['enable_thinking'], False)

    def test_retry_preserves_attempts_and_full_latency(self):
        item = {'id': 'x', 'task': 'a', 'family': 'a', 'request': self.request}
        config = {'run_id': 'test', 'model': 'jev-1.13.0', 'endpoint': 'https://api.typesafe.ai/v1/systemone',
                  'timeout_s': 120, 'max_attempts': 3}
        response = {'model': 'jev-1.13.0', 'answers': {'decision': {'choice': '1'}}, 'usage': {'input_tokens': 10}}
        err = urllib.error.HTTPError(config['endpoint'], 503, 'Unavailable', {}, None)
        with patch.object(runner.urllib.request, 'urlopen', side_effect=[err, io.BytesIO(json.dumps(response).encode())]), \
             patch.object(runner.time, 'sleep') as sleep, \
             patch.object(runner.time, 'perf_counter', side_effect=[0, 0, 1, 2, 3, 3]):
            result = runner.perform(item, config, 'private-test-key', threading.Event())
        self.assertEqual(result['attempts'], 2)
        self.assertEqual(result['elapsed_s'], 3)
        self.assertEqual(result['choice'], '1')
        self.assertEqual(result['attempt_history'][0]['http_status'], 503)
        sleep.assert_called_once_with(1)
        self.assertNotIn('private-test-key', json.dumps(result))

    def test_timing_includes_failure_excludes_unstarted_and_resume_wall(self):
        records = [{'elapsed_s': 1, 'status': 'success', 'attempts': 1},
                   {'elapsed_s': 120, 'status': 'timeout', 'attempts': 3}]
        result = runner.timing(records, 3, [])
        self.assertEqual(result['mean_elapsed_s'], 60.5)
        self.assertEqual(result['p95_elapsed_s'], 120)
        self.assertEqual(result['timeout_rate'], .5)
        self.assertEqual(result['not_started'], 1)
        self.assertEqual(result['retries'], 2)
        self.assertIsNone(result['task_wall_s'])
        span = {'completed': 2, 'selected': 2, 'wall_s': 121}
        self.assertEqual(runner.timing(records, 2, [span])['task_wall_s'], 121)
        self.assertIsNone(runner.timing(records, 2, [span, span])['task_wall_s'])

    def test_invalid_answer_not_retried(self):
        response = {'answers': {'decision': {'choice': 'unknown'}}}
        config = {'run_id': 'test', 'model': 'jev-1.13.0', 'endpoint': 'https://api.typesafe.ai/v1/systemone',
                  'timeout_s': 120, 'max_attempts': 3}
        item = {'id': 'x', 'task': 'a', 'family': 'a', 'request': self.request}
        with patch.object(runner.urllib.request, 'urlopen', return_value=io.BytesIO(json.dumps(response).encode())) as api:
            result = runner.perform(item, config, 'private', threading.Event())
        self.assertEqual(result['status'], 'invalid_answer')
        self.assertIsNone(result['choice'])
        self.assertEqual(api.call_count, 1)

    def test_auth_failure_stops_queued_calls(self):
        config = {'run_id': 'test', 'model': 'jev-1.13.0', 'endpoint': 'https://api.typesafe.ai/v1/systemone',
                  'timeout_s': 120, 'max_attempts': 3}
        item = {'id': 'x', 'task': 'a', 'family': 'a', 'request': self.request}
        stop = threading.Event()
        err = urllib.error.HTTPError(config['endpoint'], 401, 'Unauthorized', {}, None)
        with patch.object(runner.urllib.request, 'urlopen', side_effect=err) as api:
            result = runner.perform(item, config, 'private', stop)
            self.assertIsNone(runner.perform(item, config, 'private', stop))
        self.assertEqual(result['status'], 'request_error')
        self.assertEqual(api.call_count, 1)


class ArchivedModelTests(unittest.TestCase):
    root = Path(__file__).resolve().parents[1] / 'results/clinical-20261012'

    def test_frozen_inputs_and_scores_match_for_all_models(self):
        inputs = None
        for model in runner.MODELS:
            folder = self.root / model
            if not folder.exists():
                continue
            actual = list(runner.dataset_tools.read_jsonl(folder / 'inputs.jsonl'))
            if inputs is None:
                inputs = actual
            self.assertEqual(actual, inputs)
            self.assertEqual(len({r['id'] for r in actual}), 1514)
            self.assertTrue(all(set(r) == {'id', 'task', 'family', 'request'} for r in actual))
            score = runner.dataset_tools.score(runner.dataset_tools.DEFAULT, folder / 'predictions.jsonl', True)
            self.assertEqual(score, json.loads((folder / 'scores.json').read_text()))
            self.assertEqual(score['scored_tasks'], 26)
            self.assertEqual(score['summary_eligible_tasks'], 26)
            self.assertEqual(sum(t['small_sample'] for t in score['task_families'].values()), 11)

    def test_archive_hashes(self):
        manifest = json.loads((self.root / 'archive_manifest.json').read_text())
        for name, sha in manifest['files'].items():
            self.assertEqual(runner.dataset_tools.file_sha(self.root / name), sha, name)

    def test_rescoring_rejects_changed_gold_and_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            dataset = Path(tmp)
            for name in ['samples.jsonl', 'answers.jsonl', 'requests.jsonl', 'taxonomy.json',
                         'sources.json', 'sources.lock.json', 'evaluation_scope.json']:
                shutil.copy2(runner.dataset_tools.DEFAULT / name, dataset / name)
            rows = list(runner.dataset_tools.read_jsonl(dataset / 'samples.jsonl'))
            rows[0]['gold'] = 'tampered'
            runner.dataset_tools.write_jsonl(dataset / 'samples.jsonl', rows)
            with self.assertRaisesRegex(ValueError, 'changed frozen data'):
                runner.summarize(self.root / 'jev-1.13.0', dataset,
                                 archived_dataset=self.root / 'dataset_at_run')
            shutil.copy2(runner.dataset_tools.DEFAULT / 'samples.jsonl', dataset / 'samples.jsonl')
            policy = json.loads((dataset / 'evaluation_scope.json').read_text())
            policy['tasks']['medication_choice']['positive_label'] = 'changed'
            runner.dataset_tools.write_json(dataset / 'evaluation_scope.json', policy)
            with self.assertRaisesRegex(ValueError, 'scope or mapping'):
                runner.summarize(self.root / 'jev-1.13.0', dataset,
                                 archived_dataset=self.root / 'dataset_at_run')

    def test_verifier_rejects_duplicate_and_altered_response(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source = self.root / 'jev-1.13.0'
            for name in ['config.json', 'inputs.jsonl', 'responses.jsonl', 'task-spans.jsonl']:
                shutil.copy2(source / name, folder / name)
            rows = list(runner.dataset_tools.read_jsonl(folder / 'responses.jsonl'))
            runner.dataset_tools.write_jsonl(folder / 'responses.jsonl', rows + rows[:1])
            with self.assertRaisesRegex(ValueError, 'duplicate'):
                runner.summarize(folder, runner.dataset_tools.DEFAULT, archived_dataset=self.root / 'dataset_at_run')
            rows[0]['choice'] = 'tampered'
            runner.dataset_tools.write_jsonl(folder / 'responses.jsonl', rows)
            with self.assertRaisesRegex(ValueError, 'Normalized answer mismatch'):
                runner.summarize(folder, runner.dataset_tools.DEFAULT, archived_dataset=self.root / 'dataset_at_run')


if __name__ == '__main__':
    unittest.main()
