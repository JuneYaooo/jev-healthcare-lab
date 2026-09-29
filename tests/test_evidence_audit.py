"""Regression tests for clinical denominators, paired uncertainty and failures."""
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import benchmark as b
from evaluate_evidence import audit_task, index, paired_interval, selection, stats, wilson


def row(id_='a', gold='harmful'):
    request = b.choice('test', 'classify', {'benign': 'benign', 'harmful': 'harmful'})
    return {'task': 'medsafety_request_gate', 'id': id_, 'group': id_, 'metadata': {},
            'request': request, 'request_sha256': b.sha(request), 'gold': gold}


def response(r, label, provider='jev'):
    answer = {'choice': label, 'probabilities': {label: 1.0, 'benign' if label == 'harmful' else 'harmful': 0.0}, 'confidence': 1.0}
    value = {k: r[k] for k in ('task', 'id', 'request_sha256')}
    value['status'] = 'ok'
    if provider == 'jev':
        value['response'] = {'answers': {'decision': answer}}
    else:
        value['normalized_answers'] = {'decision': {'choice': label}}
    return value


class EvidenceTests(unittest.TestCase):
    def test_identical_providers_have_zero_paired_difference(self):
        r = paired_interval([('a', (1, 1), (1, 1)), ('b', (0, 1), (0, 1))], repeats=100)
        self.assertEqual(r['ci95']['difference'], {'lower': 0, 'upper': 0})
        self.assertLess(r['ci95']['jev']['lower'], r['ci95']['jev']['upper'])

    def test_repeated_fields_are_one_bootstrap_group(self):
        r = paired_interval([('a', (1, 1), (0, 1))]*20, repeats=100)
        self.assertEqual(r['groups'], 1)
        self.assertIsNone(r['ci95'])

    def test_micro_f1_uses_counts_not_mean_row_f1(self):
        r = paired_interval([('a', stats({'x'}, {'x'}), stats({'x'}, set())),
                             ('b', stats(set('abcdefghi'), set()), stats(set('abcdefghi'), set()))], repeats=100)
        self.assertAlmostEqual(r['jev'], 2/11)

    def test_zero_errors_still_have_risk(self):
        self.assertGreater(wilson(0, 20)['upper'], .1)
        self.assertIsNone(wilson(0, 0))

    def test_no_accepted_samples_is_not_zero_risk(self):
        r = selection([{'valid': False, 'correct': False, 'case': 'a'}], .95, 'probability')
        self.assertEqual(r['review_required'], 1)
        self.assertIsNone(r['error_rate'])
        self.assertIsNone(r['case_error_wilson95'])

    def test_probability_and_confidence_are_separate(self):
        obs = [{'valid': True, 'correct': False, 'case': 'a', 'probability': .99, 'confidence': .5}]
        self.assertEqual(selection(obs, .95, 'probability')['errors'], 1)
        self.assertEqual(selection(obs, .95, 'confidence')['accepted'], 0)

    def test_failure_not_removed_from_accuracy_or_safety_denominator(self):
        r = row()
        rules = [{'id': 'harm', 'gold': ['harmful'], 'prediction': ['benign']}]
        report = audit_task([r], index([response(r, 'benign')]), {}, rules)
        self.assertEqual(report['paired']['deepseek'], 0)
        self.assertEqual(report['safety_events']['harm']['jev']['events'], 1)
        self.assertEqual(report['safety_events']['harm']['deepseek'], {'eligible': 1, 'events': 0, 'unresolved': 1})
        self.assertEqual(report['case_all_correct']['deepseek']['rate'], 0)

    def test_failed_empty_set_is_not_successful_empty_case(self):
        r = row();r['gold'] = [];r['metadata'] = {'scoring': 'multi_question_keys'}
        r['request']['questions'] = {};r['request_sha256'] = b.sha(r['request'])
        jr = {k:r[k] for k in ('task', 'id', 'request_sha256')}
        jr.update(status='ok', response={'answers': {}}, deterministic_empty=True)
        report = audit_task([r], index([jr]), {}, [])
        self.assertEqual(report['case_all_correct']['jev']['rate'], 1)
        self.assertEqual(report['case_all_correct']['deepseek']['rate'], 0)
        self.assertEqual(report['failures']['deepseek'], 1)

    def test_wrong_hash_and_duplicate_response_rejected(self):
        r = row();j = response(r, 'benign');j['request_sha256'] = 'wrong'
        with self.assertRaises(ValueError):
            audit_task([r], index([j]), {}, [])
        with self.assertRaises(ValueError):
            index([j, j])

    def test_high_probability_error_is_auditable_by_id(self):
        r = row()
        report = audit_task([r], index([response(r, 'benign')]), {}, [])
        self.assertEqual(report['high_probability_errors'], ['a'])
        self.assertEqual(report['calibration']['brier_sum_mean'], 2.0)


class ArchivedEvidenceTests(unittest.TestCase):
    def test_audit_matches_all_archived_point_scores_and_case_counts(self):
        root = Path(__file__).resolve().parents[1]
        audit = json.loads((root/'results/evidence_audit.json').read_text())['tasks']
        comparison = json.loads((root/'comparisons/deepseek-flash/summary.json').read_text())['tasks']
        inventory = json.loads((root/'results/case_inventory.json').read_text())['tasks']
        self.assertEqual(set(audit), set(comparison))
        for task, r in audit.items():
            self.assertEqual(r['cases'], inventory[task]['cases'])
            self.assertEqual(r['records'], inventory[task]['records'])
            for provider in ('jev', 'deepseek'):
                self.assertAlmostEqual(r['paired'][provider], comparison[task][provider]['quality'][r['metric']])


if __name__ == '__main__':
    unittest.main()
