# 医疗决策数据底稿

[项目首页](../../README.md) · [主评测任务](../../docs/tasks/README.md) · [辅助任务](../../docs/tasks/AUXILIARY.md) · [下载整理包](../../releases/README.md)

主评测有 29 个任务定义、26 个有题任务，共 1,514 题。诊断的考试与模拟病例合为一个任务，按来源分层。

本目录 samples.jsonl、requests.jsonl、answers.jsonl 是包含主评测、辅助及暂停任务的完整溯源底稿。模型评测应使用下方按范围导出的请求或下载对应整理包，不能把底稿全部题目当作临床主评测。

| 范围 | 定义任务 | 有题任务 | 题数 |
| --- | ---: | ---: | ---: |
| 临床主评测 | 29 | 26 | 1514 |
| 辅助评测 | 58 | 45 | 4293 |
| 暂停使用 | 1 | 1 | 100 |

[执行范围与任务合并规则](evaluation_scope.json) · [范围统计](evaluation-summary.json) · [全部来源](SOURCES.md) · [来源锁定](sources.lock.json)

## 导出与评分

```bash
python3 scripts/medical_decision_dataset.py export --output work/clinical-requests.jsonl
python3 scripts/medical_decision_dataset.py score --predictions work/predictions.jsonl --output work/clinical-scores.json
python3 scripts/medical_decision_dataset.py export --scope auxiliary --output work/auxiliary-requests.jsonl
```

默认仅处理临床主评测的开放许可部分。需要相应非商业数据时添加 --include-research。辅助范围必须显式传入 --scope auxiliary；暂停任务不导出、不评分。

数据复建命令与来源筛查见 [复建说明](../../docs/REPRODUCING.md)；评分口径见 [评测方法](../../docs/EVALUATION.md)。源题 ID、请求和原金标保留用于追溯；范围变化由独立策略文件及其哈希记录。
