"""New source joins, multi-select meaning, no leakage, and full v0.6 freeze."""
import collections
import importlib.util
import json
from pathlib import Path
import unittest
from frozen_records import assert_frozen_records
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'benchmarks/medical_decision_v1'
spec = importlib.util.spec_from_file_location('benchmark_v070', ROOT / 'scripts/medical_decision_dataset.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


class ExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = list(b.read_jsonl(DATA / 'samples.jsonl'))

    def test_full_v060_records_unchanged(self):
        assert_frozen_records(self, self.rows, '0.6.0', 5594)

    def test_candidate_membership_and_case_groups(self):
        folder = DATA / 'sources/tcmeval_sdt'
        questions = json.loads((folder / 'Test_TCM_Data_v1.json').read_text())
        lines = (folder / 'Test_data_result.txt').read_text().splitlines()
        rows = [r for r in self.rows if r['task'] == 'tcm_pathogenesis_candidate']
        self.assertEqual(len(rows), 100)
        groups = collections.defaultdict(list)
        for row in rows:
            loc = row['provenance']['locator']; state = row['request']['state']
            question = questions[loc['json_index']]
            answer = lines[loc['answer_line'] - 1].split('@')
            self.assertEqual(question['Medical Record ID'], answer[0])
            self.assertEqual(state['clinical_case'], question['Clinical Data'])
            selected = answer[2].split(';')
            self.assertEqual(row['gold'], 'yes' if state['target_candidate']['key'] in selected else 'no')
            self.assertEqual(set(state), {'clinical_case', 'original_candidates', 'target_candidate'})
            self.assertEqual(row['provenance']['split'], 'official_test')
            groups[row['group_id']].append(row['gold'])
        self.assertEqual(len(groups), 50)
        self.assertTrue(all(sorted(labels) == ['no', 'yes'] for labels in groups.values()))

    def test_prescription_action_original_answers_and_no_explanations_in_input(self):
        original = b.read_prescription_sheet(DATA / 'sources/tcmeval_pa/TCMEval-PA.xlsx')
        rows = [r for r in self.rows if r['task'] == 'prescription_audit_action']
        self.assertEqual(len(rows), 11)
        for row in rows:
            upstream = original[row['provenance']['locator']['xlsx_row']]
            self.assertEqual(row['gold'], upstream['Answer'])
            self.assertEqual(row['request']['state'], {'clinical_question': upstream['Question']})
            self.assertEqual(row['metadata']['upstream_explanation'], upstream['Explanation'])
            expected = dict(line.strip().split('. ', 1) for line in upstream['Candidate Answers'].splitlines())
            self.assertEqual(row['request']['questions']['decision']['criteria'], {k: v.strip() for k, v in expected.items()})

    def test_new_questions_do_not_repeat_other_clinical_questions(self):
        tasks = {'nutrition_plan': 11, 'positioning_choice': 10}
        for task, expected in tasks.items():
            new = [r for r in self.rows if r['task'] == task]
            self.assertEqual(len(new), expected)
            other = {b.norm(r['request']['state']['clinical_question']) for r in self.rows
                     if r['task'] != task and 'clinical_question' in r['request']['state']}
            self.assertFalse(other & {b.norm(r['request']['state']['clinical_question']) for r in new})


if __name__ == '__main__':
    unittest.main()
