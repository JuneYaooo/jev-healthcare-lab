import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from compare_deepseek import normalize

class ComparisonAdapterTests(unittest.TestCase):
    def test_numeric_label_is_unambiguous_without_gold(self):
        row={'request':{'questions':{'x':{'type':'choice','criteria':{'-1':'decrease','1':'increase'}}}}}
        response={'choices':[{'message':{'content':'{"answers":{"x":-1}}'}}]}
        self.assertEqual(normalize(row,response),{'x':{'choice':'-1'}})

    def test_invalid_labels_and_missing_answers_are_rejected(self):
        row={'request':{'questions':{'x':{'type':'choice','criteria':{'1':'one'}}}}}
        for content in ['{"answers":{"x":true}}','{"answers":{"x":"unknown"}}','{"answers":{}}']:
            with self.assertRaises(ValueError):normalize(row,{'choices':[{'message':{'content':content}}]})

    def test_binary_output_is_not_a_confidence_estimate(self):
        row={'request':{'questions':{'x':{'type':'noul'}}}}
        self.assertEqual(normalize(row,{'choices':[{'message':{'content':'{"answers":{"x":false}}'}}]}),{'x':{'noul':0}})
