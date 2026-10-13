import copy
import json
from pathlib import Path
import sys
import unittest
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import run_medical_load as direct
import run_jev_gateway as gateway
import build_medical_load_report as reporting
from test_medical_load import item


class GatewayTests(unittest.TestCase):
    def test_gateway_alias_and_credentials_do_not_change_direct_provider(self):
        providers = copy.deepcopy(direct.clinical.MODELS)
        runtime = gateway.adapter()
        self.assertEqual(runtime.payload(item(), gateway.MODEL)['model'], 'jev-latest')
        self.assertEqual(direct.payload(item(), gateway.MODEL)['model'], gateway.MODEL)
        self.assertEqual(runtime.clinical.MODELS[gateway.MODEL]['endpoint'], gateway.ENDPOINT)
        self.assertEqual(runtime.clinical.MODELS[gateway.MODEL]['key_env'], 'JEV_GATEWAY_API_KEY')
        self.assertEqual(providers, direct.clinical.MODELS)
        self.assertNotIn('gold', runtime.payload(item(), gateway.MODEL))
        self.assertEqual(runtime.RATES[gateway.MODEL], (None, None))
        self.assertEqual(direct.RATES[gateway.MODEL], (76, 90000))

    def test_gateway_request_hash_validates_alias_not_official_model(self):
        runtime = gateway.adapter()
        p = item()
        response = {'model': gateway.MODEL, 'answers': {'q000': {'choice': 'yes'}, 'q001': {'choice': 'no'}},
                    'usage': {'input_tokens': 100}}
        row = {'item_id': 'case', 'model': gateway.MODEL, 'response': response,
               'http_status': 200, 'predicted': {'q000': 'yes', 'q001': 'no'},
               'correct': 2, 'valid': 2, 'decisions': 2, 'cost_cny': runtime.cost(response, gateway.MODEL),
               'queued_s': 0., 'http_start_s': 1., 'completion_s': 2., 'http_s': 1.,
               'request_sha256': direct.data.digest(runtime.payload(p, gateway.MODEL))}
        with gateway.report_adapter():
            reporting.validate(row, {'case': p})
        self.assertIs(reporting.run, direct)
        with self.assertRaisesRegex(ValueError, 'Request hash mismatch'):
            reporting.validate(row, {'case': p})

    def test_reporting_restores_context_after_error(self):
        with self.assertRaises(RuntimeError):
            with gateway.report_adapter():
                raise RuntimeError('abort')
        self.assertIs(reporting.run, direct)

    def test_alias_cannot_silently_change_backend_version_in_report(self):
        row = {'channel': gateway.ENDPOINT, 'http_status': 200,
               'response': {'model': gateway.MODEL}}
        gateway.validate_identity(row)
        with self.assertRaisesRegex(ValueError, 'response model mismatch'):
            gateway.validate_identity({**row, 'response': {'model': 'jev-2'}})
        with self.assertRaisesRegex(ValueError, 'response model mismatch'):
            gateway.validate_identity({**row, 'response': {}})
        with self.assertRaisesRegex(ValueError, 'channel mismatch'):
            gateway.validate_identity({**row, 'channel': 'official'})

    def test_resume_archives_interrupted_windows_and_preserves_complete_ones(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            for name, stop, wall in [('budget', 'budget_limit', 9), ('early', None, 19), ('valid', None, 24)]:
                stem = name + '-r0-c32'
                (directory / (stem + '.jsonl.gz')).write_bytes(b'original response bytes')
                (directory / (stem + '.json')).write_text(json.dumps({
                    'stop': stop, 'wall_s': wall, 'warmup_s': 3, 'window_s': 20,
                    'raw_file': stem + '.jsonl.gz'}))
            gateway.archive_incomplete(directory)
            self.assertEqual([p.name for p in directory.glob('*-r*-c*.json')], ['valid-r0-c32.json'])
            archived = list((directory / 'excluded').rglob('*.jsonl.gz'))
            self.assertEqual(len(archived), 2)
            self.assertTrue(all(p.read_bytes() == b'original response bytes' for p in archived))


if __name__ == '__main__':
    unittest.main()
