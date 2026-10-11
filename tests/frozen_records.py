"""Check complete historical records without retaining obsolete download archives."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def assert_frozen_records(case, rows, version=None, expected_count=5907):
    baseline = json.loads((ROOT / 'tests/fixtures/frozen_record_sha256.json').read_text())['records']
    identities = (json.loads((ROOT / f'benchmarks/medical_decision_v1/history/v{version}_sample_identity.json').read_text())
                  if version else baseline)
    case.assertEqual(len(identities), expected_count)
    current = {r['id']: r for r in rows}
    for uid in identities:
        case.assertIn(uid, current)
        raw = json.dumps(current[uid], ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
        case.assertEqual(hashlib.sha256(raw).hexdigest(), baseline[uid], uid)
