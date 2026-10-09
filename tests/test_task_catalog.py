"""Protect archive coverage and prevent training-only work being reported as measured."""
import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_task_catalog as catalog
import business_readme


class TaskCatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = catalog.load(ROOT / catalog.CATALOG)

    def test_catalog_matches_archive_without_training_package(self):
        catalog.validate(self.data)

    def test_missing_and_extra_benchmarks_are_rejected(self):
        for mode in ('missing', 'extra'):
            data = copy.deepcopy(self.data)
            if mode == 'missing':
                data['benchmark_tasks'].pop(next(iter(data['benchmark_tasks'])))
            else:
                data['benchmark_tasks']['not_an_archived_task'] = {'family': 'diagnosis', 'tags': []}
            with self.subTest(mode=mode), self.assertRaisesRegex(ValueError, 'exactly'):
                catalog.validate(data)

    def test_invalid_family_references_and_duplicate_families_are_rejected(self):
        for mode in ('reference', 'duplicate'):
            data = copy.deepcopy(self.data)
            if mode == 'reference':
                next(iter(data['training_snapshot']['tasks'].values()))['family'] = 'missing'
            else:
                data['families'].append(copy.deepcopy(data['families'][0]))
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                catalog.validate(data)

    def test_training_counts_and_explicit_missing_package_are_rejected(self):
        self.data['training_snapshot']['records'] += 1
        with self.assertRaisesRegex(ValueError, 'total mismatch'):
            catalog.validate(self.data)
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, 'Missing training split'):
                catalog.validate(catalog.load(ROOT / catalog.CATALOG), training_dir=folder)

    def test_training_and_external_requirements_do_not_imply_measured(self):
        component = {'scope': 'component'}
        external = {'scope': 'external_system'}
        self.assertEqual(catalog.status(component, 0, 2), '训练扩展；主评测未测')
        self.assertEqual(catalog.status(component, 0, 0), '未测')
        self.assertEqual(catalog.status(external, 0, 0), '需组合系统；未测')
        self.assertEqual(catalog.status(component, 1, 0), '部分已测')

    def test_research_navigation_is_preserved_but_not_the_generated_body(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            block = '<!-- research-extensions:start -->\n- Existing research\n<!-- research-extensions:end -->'
            (path / 'README.md').write_text('Unrelated text\n' + block)
            with patch.object(business_readme, 'ROOT', path):
                rendered = '\n'.join(business_readme.research_extensions())
                self.assertIn('- Existing research', rendered)
                self.assertNotIn('Unrelated text', rendered)
                (path / 'README.md').write_text('<!-- research-extensions:start -->')
                with self.assertRaises(ValueError):
                    business_readme.research_extensions()


if __name__ == '__main__':
    unittest.main()
