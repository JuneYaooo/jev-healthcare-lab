"""Prevent auxiliary tasks, option positions and tiny samples from distorting clinical scores."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from frozen_records import assert_frozen_records

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import medical_decision_dataset as data


def record(uid, task, gold='A', distribution='open'):
    return {'id': uid, 'task': task, 'gold': gold, 'group_id': uid,
            'request': {'state': {'case': uid}, 'questions': {'decision': {'type': 'choice', 'criteria': {'A': uid + ' diagnosis one', 'B': uid + ' diagnosis two'}}}},
            'primary_scenario': 'diagnosis', 'ability_tags': ['clinical'], 'dimension': 'clinical',
            'decision_stage': 'clinical_choice', 'decision_mode': 'clinical', 'language': 'en',
            'provenance': {'distribution': distribution, 'material_kind': 'fixture'},
            'exposure': {'historical_material_signature_match': False}}


class EvaluationScopeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.rows = [record('exam1', 'exam'), record('exam2', 'exam'),
                     record('sim1', 'simulation', gold='B'), record('sim2', 'simulation', gold='B'),
                     record('tiny1', 'tiny'), record('aux1', 'aux'), record('paused1', 'paused'),
                     record('nc1', 'exam', distribution='research_noncommercial')]
        data.write_jsonl(self.root / 'samples.jsonl', self.rows)
        self.policy = {'minimum_summary_questions': 2, 'tasks': {}}
        for tid in ['exam', 'simulation', 'tiny', 'aux', 'paused']:
            family = 'diagnosis' if tid in {'exam', 'simulation'} else tid
            self.policy['tasks'][tid] = {'scope': 'suspended' if tid == 'paused' else 'auxiliary' if tid == 'aux' else 'clinical',
                'family': family, 'family_title': family, 'title': tid, 'label_semantics': 'per_question'}
        data.write_json(self.root / 'evaluation_scope.json', self.policy)
        data.write_json(self.root / 'taxonomy.json', {'version': 'fixture', 'scenarios': [{'id': 'diagnosis', 'title': 'Diagnosis'}],
            'tasks': [{'id': tid, 'primary_scenario': 'diagnosis', 'ability_tags': ['clinical']} for tid in self.policy['tasks']]})
        data.write_json(self.root / 'manifest.json', {})
        self.predictions = self.root / 'predictions.jsonl'

    def test_default_export_filters_scope_license_and_suspension(self):
        self.assertEqual({r['id'] for r in data.evaluation_rows(self.root)}, {'exam1', 'exam2', 'sim1', 'sim2', 'tiny1'})
        self.assertEqual({r['id'] for r in data.evaluation_rows(self.root, True, 'auxiliary')}, {'aux1'})
        with self.assertRaises(ValueError):
            data.evaluation_rows(self.root, True, 'suspended')

    def test_merging_sources_and_excluding_tiny_tasks_changes_summary(self):
        data.write_jsonl(self.predictions, [{'id': r['id'], 'choice': 'A'} for r in data.evaluation_rows(self.root)])
        result = data.score(self.root, self.predictions)
        self.assertEqual(result['scored_tasks'], 2)  # diagnosis + exploratory tiny
        self.assertEqual(result['summary_eligible_tasks'], 1)
        self.assertEqual(result['task_families']['diagnosis']['n'], 4)
        self.assertEqual(result['primary_clinical_score'], 0.5)
        self.assertEqual(result['task_macro_accuracy'], 0.5)  # tiny's perfect answer is not averaged in
        self.assertTrue(result['tasks']['tiny']['exploratory'])
        self.assertIsNone(result['tasks']['exam']['macro_f1'])
        self.assertEqual(result['tasks']['exam']['per_class'], {})

    def test_all_exploratory_auxiliary_has_no_clinical_or_summary_score(self):
        data.write_jsonl(self.predictions, [{'id': 'aux1', 'choice': 'A'}])
        result = data.score(self.root, self.predictions, scope='auxiliary')
        self.assertEqual(result['tasks']['aux']['accuracy'], 1)
        self.assertIsNone(result['primary_clinical_score'])
        self.assertIsNone(result['scenario_macro_accuracy'])
        self.assertIsNone(result['task_macro_accuracy'])

    def test_predictions_cannot_silently_cross_scope_or_license(self):
        for uid in ['aux1', 'paused1', 'nc1']:
            with self.subTest(uid=uid):
                data.write_jsonl(self.predictions, [{'id': uid, 'choice': 'A'}])
                with self.assertRaisesRegex(ValueError, 'out-of-scope'):
                    data.score(self.root, self.predictions)

    def test_scope_and_ids_are_pinned_in_result(self):
        data.write_jsonl(self.predictions, [])
        result = data.score(self.root, self.predictions)
        self.assertEqual(result['evaluated_ids_sha256'], data.digest(sorted(r['id'] for r in data.evaluation_rows(self.root))))
        self.assertEqual(result['scope_policy_sha256'], data.file_sha(self.root / 'evaluation_scope.json'))
        self.assertEqual(result['primary_clinical_score'], 0)

    def test_fixed_semantic_risk_reports_baseline_and_misses(self):
        rows = [record(str(i), 'risk', 'yes' if i == 0 else 'no') for i in range(10)]
        for row in rows:
            row['request']['questions']['decision']['criteria'] = {'yes': 'Event', 'no': 'No event'}
        result = data.metrics(rows, {r['id']: 'no' for r in rows}, semantic_labels=True, positive_label='yes')
        self.assertEqual(result['accuracy'], 0.9)
        self.assertEqual(result['sample_majority_accuracy'], 0.9)
        self.assertEqual(result['positive_recall'], 0)
        self.assertEqual(result['specificity'], 1)
        self.assertEqual(result['balanced_accuracy'], 0.5)
        missing = data.metrics(rows, {}, semantic_labels=True, positive_label='yes')
        self.assertEqual(missing['specificity'], 0)
        self.assertEqual(missing['positive_recall'], 0)

    def test_fixed_labels_cannot_hide_changed_option_meanings(self):
        rows = [record('case1', 'risk'), record('case2', 'risk')]
        with self.assertRaisesRegex(ValueError, 'inconsistent option meanings'):
            data.metrics(rows, {}, semantic_labels=True)

    def test_policy_requires_complete_and_consistent_family_mapping(self):
        del self.policy['tasks']['aux']
        data.write_json(self.root / 'evaluation_scope.json', self.policy)
        with self.assertRaises(ValueError):
            data.evaluation_policy(self.root)

    def test_all_pre_scope_records_remain_byte_equivalent_as_objects(self):
        assert_frozen_records(self, list(data.read_jsonl(data.DEFAULT / 'samples.jsonl')))

    def test_real_clinical_scope_contains_no_text_tasks_or_paused_shortcut(self):
        rows = data.evaluation_rows(data.DEFAULT, True)
        self.assertEqual(len(rows), 1514)
        self.assertEqual(len(data.evaluation_rows(data.DEFAULT)), 1284)
        self.assertFalse({'assertion_scope', 'temporality', 'input_sufficiency'} & {r['task'] for r in rows})
        self.assertEqual(len(data.evaluation_rows(data.DEFAULT, True, 'auxiliary')), 4293)


if __name__ == '__main__':
    unittest.main()
