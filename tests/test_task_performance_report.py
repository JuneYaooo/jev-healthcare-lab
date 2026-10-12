import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_task_performance_report as report


@unittest.skipUnless((report.RUN / 'archive_manifest.json').exists(), 'Task performance run still in progress')
class TaskPerformanceArchiveTests(unittest.TestCase):
    def test_every_task_mode_recomputes_from_original_gold(self):
        manifest, verified = report.verify(report.RUN)
        result = report.aggregate(manifest, verified)
        self.assertEqual(len(verified), 708)
        self.assertEqual(result['measured_requests'], 10656)
        self.assertEqual(len(result['families']), 29)
        for family in result['families'].values():
            for mode in family['modes']:
                self.assertEqual(mode['repeats'], 3)
                self.assertEqual(mode['decisions'], family['selected'] * 3)
                self.assertAlmostEqual(mode['valid_decisions_per_s'], mode['valid_decisions'] / sum(mode['wall_per_repeat_s']))
            self.assertEqual(bool(family['modes']), bool(family['selected']))

    def test_tampered_score_rejected_even_with_updated_archive_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'run'
            shutil.copytree(report.RUN, target)
            path = target / 'cell-000.jsonl'
            rows = list(report.data.read_jsonl(path))
            rows[0]['correct_decisions'] = rows[0]['decisions'] + 1
            report.data.write_jsonl(path, rows)
            archive = json.loads((target / 'archive_manifest.json').read_text())
            archive['files']['cell-000.jsonl'] = report.data.file_sha(path)
            report.data.write_json(target / 'archive_manifest.json', archive)
            with self.assertRaisesRegex(ValueError, 'score mismatch'):
                report.verify(target)

    def test_readme_and_task_pages_contain_task_scoped_results(self):
        root = report.runner.ROOT
        readme = (root / 'README.md').read_text()
        self.assertNotIn('## 多问题与并发性能补充', readme)
        sustained = (root / 'results/sustained-throughput-v1/comparison.json').exists()
        if sustained:
            self.assertEqual(readme.count('| 配置并发 | 模型 | 判断／秒 ↑ |'), 5)
            self.assertEqual(readme.count('| JEV 1.13 |'), 14)
            self.assertEqual(readme.count('| Flash |'), 14)
            self.assertIn('每请求 8 题', readme)
            self.assertIn('客户端配额保护', readme)
            self.assertIn('同一份病历一次读取', readme)
        else:
            self.assertEqual(readme.count('| 任务与测试题数 | 处理方式 | 模型 | 准确率 |'), 8)
            self.assertEqual(readme.count('| JEV 1.13 |'), 52)
            self.assertEqual(readme.count('| Flash |'), 52)
        self.assertNotIn('## 模型得分与耗时对比', readme)
        self.assertNotIn('全量准确率：五模型比较', readme)
        self.assertNotIn('jev-medical-score-time-v1.svg', readme)
        if not sustained:
            self.assertIn('多题请求同时并发的组合尚未测试', readme)
        manifest = report.runner.verify_dataset(report.runner.DATASET)
        for family in manifest['families']:
            page = (root / 'docs/tasks' / (family['id'] + '.md')).read_text()
            self.assertIn('## 多问题与并发性能', page)
            if sustained and family['id'] in {'case_complication','medication_choice','diagnosis','tcm_syndrome'}:
                self.assertIn('### 持续多题并发', page)
                self.assertIn('### 历史有限批次测试', page)
            if family['selected']:
                self.assertIn(f"固定本任务 {family['selected']} 道原题", page)
            else:
                self.assertIn('测试均待补', page)


if __name__ == '__main__':
    unittest.main()
