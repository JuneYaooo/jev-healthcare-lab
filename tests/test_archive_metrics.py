"""Cross-version float comparisons must not hide genuine result changes."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from verify_experiments import same_metrics


class ArchiveMetricTests(unittest.TestCase):
    def test_float_summation_roundoff_is_accepted(self):
        self.assertTrue(same_metrics({'macro_f1': sum([0.1] * 10)}, {'macro_f1': 1.0}))

    def test_metric_and_count_changes_are_rejected(self):
        self.assertFalse(same_metrics({'accuracy': 0.67}, {'accuracy': 0.68}))
        self.assertFalse(same_metrics({'tp': 1000000000000}, {'tp': 1000000000001}))
        self.assertFalse(same_metrics({'accuracy': float('nan')}, {'accuracy': float('nan')}))
        self.assertFalse(same_metrics({'accuracy': 0.67}, {'accuracy': 0.67, 'n': 100}))


class TimingCohortTests(unittest.TestCase):
    def test_later_additions_do_not_change_frozen_cohort(self):
        from verify_batch_time import timing_sources
        import benchmark as b
        row={'request': {'state': 'x', 'questions': {}}}
        row['request_sha256']=b.sha(row['request'])
        item={'task': 'a', 'id': '1', 'request_sha256': row['request_sha256']}
        result=timing_sources([item], {('a','1'):row, ('a','2'):row})
        self.assertEqual(set(result), {('a','1')})
        with self.assertRaises(ValueError):timing_sources([item,item], {('a','1'):row})
        with self.assertRaises(ValueError):timing_sources([{**item,'request_sha256':'changed'}], {('a','1'):row})
        with self.assertRaises(ValueError):timing_sources([item], {})
