"""Frozen data must keep related cases together and exclude gold at inference."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import benchmark as b
from freeze_evaluation import freeze, partition, validate_config, verify


def make_row(i, group=None, state=None):
    request = b.choice(str(i) if state is None else state, 'test', {'yes': 'yes', 'no': 'no'})
    return {'task': 'demo', 'id': str(i), 'group': str(i) if group is None else group,
            'gold': 'yes', 'metadata': {}, 'request': request, 'request_sha256': b.sha(request)}


class FrozenTests(unittest.TestCase):
    def test_shared_case_or_state_cannot_cross_split(self):
        rows = [make_row(0, group='a'), make_row(1, group='a', state='shared'), make_row(2, state='shared')]
        result = partition(rows, 4, .3)
        self.assertEqual(len(set(result.values())), 1)

    def test_reordering_does_not_change_partition(self):
        rows = [make_row(i) for i in range(50)]
        self.assertEqual(partition(rows, 42, .3), partition(list(reversed(rows)), 42, .3))

    def test_duplicate_and_hash_mismatch_are_rejected(self):
        r = make_row(0)
        with self.assertRaises(ValueError):
            partition([r, r], 1, .3)
        r['request']['state'] = 'changed'
        with self.assertRaises(ValueError):
            partition([r], 1, .3)

    def test_historical_data_cannot_be_declared_prospective(self):
        config = json.loads((ROOT/'evaluation/protocol.example.json').read_text())
        config['study_status'] = 'prospective'
        with self.assertRaises(ValueError):
            validate_config(config)

    def test_roundtrip_no_gold_no_overwrite_detects_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp);data = base/'input.jsonl';out = base/'run'
            data.write_text(''.join(b.dumps(make_row(i))+'\n' for i in range(50)))
            config = ROOT/'evaluation/protocol.example.json'
            manifest = freeze(data, config, out)
            self.assertEqual(verify(out), manifest)
            for split in ('development', 'test'):
                for line in (out/(split+'_requests.jsonl')).read_text().splitlines():
                    r = json.loads(line)
                    self.assertEqual(set(r), {'task', 'id', 'request_sha256', 'request'})
            with self.assertRaises(FileExistsError):
                freeze(data, config, out)
            p = out/'test.jsonl';p.write_text(p.read_text()+'\n')
            with self.assertRaises(ValueError):
                verify(out)

    def test_single_component_cannot_fake_two_splits(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp);data = base/'input.jsonl';out = base/'run'
            data.write_text(b.dumps(make_row(0))+'\n')
            with self.assertRaises(ValueError):
                freeze(data, ROOT/'evaluation/protocol.example.json', out)
            self.assertFalse(out.exists())


if __name__ == '__main__':
    unittest.main()
