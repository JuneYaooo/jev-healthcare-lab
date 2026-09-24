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
