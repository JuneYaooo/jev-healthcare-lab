import sys,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import benchmark as b
class SnapshotTests(unittest.TestCase):
 def test_identity_counts(self):
  rows=[json.loads(s) for s in (ROOT/'results/evaluation_index.jsonl').read_text().splitlines()];meta=json.loads((ROOT/'results/snapshot.json').read_text())
  self.assertEqual(len(rows),meta['evaluation_rows'])
  self.assertEqual(len(rows),len({(r['task'],r['id']) for r in rows}))
  self.assertEqual(sum(not r['deterministic_empty'] for r in rows),meta['successful_api_responses'])
 def test_metrics_penalize_missing_candidates(self):
  r=b.sets_metric([({'a','b'},{'a','c'})]);self.assertEqual((r['tp'],r['fp'],r['fn']),(1,1,1));self.assertEqual(r['micro_f1'],.5)
 def test_response_validation(self):
  req=b.choice('example','classify',{'a':'A','b':'B'})
  with self.assertRaises(ValueError):b.validate_response(req,{'answers':{}})
  with self.assertRaises(ValueError):b.validate_response(req,{'answers':{'decision':{'choice':'a','probabilities':{'a':.9,'b':.9}}}})
 def test_independent_paths(self):
  self.assertEqual(b.ROOT,ROOT);self.assertEqual(b.OUT,ROOT/'results')
 def test_example_has_no_gold(self):
  r=json.loads((ROOT/'examples/request.json').read_text());self.assertEqual(set(r),{'state','questions'})

 def test_aggregate_completeness(self):
  r=json.loads((ROOT/'results/all_results.json').read_text());s=r['summary']
  self.assertEqual(sum(t['successful'] for t in r['tasks'].values()),6586)
  self.assertEqual(s['successful_api_responses']+s['deterministic_empty_rows'],6586)
  self.assertFalse(any(t['failed_or_missing'] for t in r['tasks'].values()))
  self.assertFalse(any(t.startswith('media_') for t in r['tasks']))

if __name__=='__main__':unittest.main()
