"""Frozen records, source-label parity, shared materials and missing-evidence targets."""
import collections
import importlib.util
import json
from pathlib import Path
import unittest
from frozen_records import assert_frozen_records
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'benchmarks/medical_decision_v1'
spec = importlib.util.spec_from_file_location('benchmark_v080', ROOT / 'scripts/medical_decision_dataset.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


class ExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = list(b.read_jsonl(DATA / 'samples.jsonl'))

    def test_full_v070_records_unchanged(self):
        assert_frozen_records(self, self.rows, '0.7.0', 5726)

    def test_message_pairs_keep_order_gold_and_disjoint_materials(self):
        rows = [r for r in self.rows if r['task'] == 'message_urgency_pair']
        self.assertEqual(len(rows), 30)
        messages, ehrs = [], []
        for row in rows:
            loc = row['provenance']['locator']
            raw = json.loads((DATA / 'sources/pmr_synth' / (loc['inbox'] + '-00000-of-00001.json')).read_text())[loc['row_index_zero_based']]
            self.assertEqual(row['gold'], raw['Label'])
            for i in [1, 2]:
                self.assertEqual(row['request']['state'][f'patient_{i}'], {'message': raw[f'MSG #{i}'], 'ehr': raw[f'EHR #{i}']})
                messages.append(raw[f'MSG #{i}']); ehrs.append(raw[f'EHR #{i}'])
            self.assertEqual(row['provenance']['split'], 'published_inboxes_train_test_mapping_unresolved')
            self.assertEqual(row['provenance']['distribution'], 'research_noncommercial')
        self.assertEqual(len(set(messages)), 60)
        self.assertEqual(len(set(ehrs)), 60)

    def test_sufficiency_gold_and_documents_follow_upstream_ablation(self):
        source = b.CACHE / 'longhealth__data_benchmark_v5.json'
        if not source.is_file():
            self.skipTest('Run dataset fetch for optional full-source parity check')
        original = json.loads(source.read_text())
        rows = [r for r in self.rows if r['task'] == 'input_sufficiency']
        self.assertEqual(collections.Counter(r['gold'] for r in rows), {'yes': 50, 'no': 50})
        self.assertEqual(set(collections.Counter(r['group_id'] for r in rows).values()), {5})
        for row in rows:
            loc = row['provenance']['locator']; pid = loc['patient_key']; state = row['request']['state']
            q = next(q for q in original[pid]['questions'] if q['No'] == loc['question_No'])
            self.assertEqual(state['question'], q['question'])
            actual = {k.split('/', 1)[1] for k in loc['display_document_keys'] if k.startswith(pid + '/')}
            self.assertEqual(actual, set(q['answer_location']) if row['gold'] == 'yes' else set())
            for doc, key in zip(state['documents'], loc['display_document_keys']):
                p, text = key.split('/', 1)
                self.assertEqual(doc['text'], original[p]['texts'][text])
            self.assertNotIn('original_answer', state)
            self.assertNotIn('evidence_included', state)

    def test_selected_original_exam_targets_and_no_explanation_in_request(self):
        selected = json.loads((DATA / 'selection_v080.json').read_text())['items']
        rows = [r for r in self.rows if r['metadata'].get('eligibility') == 'fixed_scope_review_v080']
        self.assertEqual(len(rows), len(selected))
        for row in rows:
            self.assertEqual(set(row['request']['state']), {'clinical_question'})
            sid = row['provenance']['source_id']; loc = row['provenance']['locator']
            if sid == 'medmcqa':
                raw = json.loads((DATA / 'sources/medmcqa/validation-00000-of-00001.json').read_text())[loc['row_index_zero_based']]
                self.assertEqual(raw['choice_type'], 'single')
                self.assertEqual(row['gold'], ['opa', 'opb', 'opc', 'opd'][raw['cop']])
            elif sid == 'principlismqa':
                raw = json.loads((DATA / 'sources/principlismqa/knowledge-mcqa.json').read_text())[loc['row_index_zero_based']]
                self.assertEqual(row['gold'], raw['correct_answer'])
                self.assertEqual(row['request']['questions']['decision']['criteria'], raw['options'])
        questions = [b.norm(r['request']['state']['clinical_question']) for r in self.rows if 'clinical_question' in r['request']['state']]
        for row in rows:
            self.assertEqual(questions.count(b.norm(row['request']['state']['clinical_question'])), 1)

    def test_table_exports_and_remaining_gap_audit(self):
        for entry in json.loads((DATA / 'table_exports.json').read_text())['exports']:
            path = DATA / entry['path']
            self.assertEqual(b.file_sha(path), entry['sha256'])
            self.assertEqual(len(json.loads(path.read_text())), entry['rows'])
        gaps = json.loads((DATA / 'expansion_audit_v080.json').read_text())['remaining_gaps']
        self.assertEqual(len(gaps), 16)
        counts = collections.Counter(r['task'] for r in self.rows)
        self.assertTrue(all(counts[g['task_id']] == 0 for g in gaps))


if __name__ == '__main__':
    unittest.main()
