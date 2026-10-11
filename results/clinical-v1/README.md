# 临床模型评测原始结果

[返回首页](../../README.md) · [逐任务得分与耗时](../../docs/MODEL_RESULTS.md)

5 组各 1,514 道题。每组保存冻结输入、配置、逐次原始响应、最终预测、质量评分、耗时汇总和任务墙钟记录。inputs.jsonl 包含开放及非商业材料，继承 [各来源许可](../../THIRD_PARTY_NOTICES.md)，不能将整组输入当作无限制开放数据。

| 模型 | 配置 | 输入 | 原始响应 | 评分 | 耗时 |
| --- | --- | --- | --- | --- | --- |
| JEV 1.13 | [jev-1.13.0/config.json](jev-1.13.0/config.json) | [输入](jev-1.13.0/inputs.jsonl) | [响应](jev-1.13.0/responses.jsonl) | [评分](jev-1.13.0/scores.json) | [耗时](jev-1.13.0/summary.json) |
| DeepSeek V4.1 Flash | [deepseek-flash/config.json](deepseek-flash/config.json) | [输入](deepseek-flash/inputs.jsonl) | [响应](deepseek-flash/responses.jsonl) | [评分](deepseek-flash/scores.json) | [耗时](deepseek-flash/summary.json) |
| DeepSeek V4 Pro | [deepseek-v4-pro/config.json](deepseek-v4-pro/config.json) | [输入](deepseek-v4-pro/inputs.jsonl) | [响应](deepseek-v4-pro/responses.jsonl) | [评分](deepseek-v4-pro/scores.json) | [耗时](deepseek-v4-pro/summary.json) |
| Qwen3.5-9B | [qwen3.5-9b/config.json](qwen3.5-9b/config.json) | [输入](qwen3.5-9b/inputs.jsonl) | [响应](qwen3.5-9b/responses.jsonl) | [评分](qwen3.5-9b/scores.json) | [耗时](qwen3.5-9b/summary.json) |
| Qwen3.8-27B | [qwen3.8-27b/config.json](qwen3.8-27b/config.json) | [输入](qwen3.8-27b/inputs.jsonl) | [响应](qwen3.8-27b/responses.jsonl) | [评分](qwen3.8-27b/scores.json) | [耗时](qwen3.8-27b/summary.json) |

tools/ 保存调用时的运行和评分代码快照，dataset_at_run/ 保存调用时的数据清单与范围策略。config.json 保留调用时的哈希；当前 scores.json、summary.json 和 comparison.json 按所有有题任务计入总分的现行规则离线重算，并记录当前评分策略哈希。原始输入、配置、响应及计时记录不变。archive_manifest.json 对档案文件记录 SHA-256；当前仓库可执行下列命令复核响应、重新计分并检查报告：

```bash
python3 scripts/build_model_report.py --check
```

逐题选择、错误和耗时均来自实际调用。失败保留在分母；没有按答案正确与否筛选或重跑。
