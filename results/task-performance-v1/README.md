# 逐任务性能原始档案

性能结果与原单题成绩共同展示在[各任务页](../../docs/tasks/README.md)和[首页任务表](../../README.md#场景与任务)。[完整测试协议](../../docs/TASK_PERFORMANCE.md)说明分包、并发、计时与许可范围。

`config.json` 保存预先确定的 708 个正式单元、接口参数、价目和环境版本。`dataset/` 保存当时的 566 道原题及分包；材料继承原来源许可，包括非商业限制。

`cell-NNN.jsonl` 对应 config.cells 的顺序，保存原始响应、请求哈希、题包决策数、排队与完整请求耗时。`summary.json` 为逐单元汇总；`comparison.json` 按任务、包大小、并发与模型聚合三轮结果。`warmup-*.json` 保存线程预热原始响应，不混入正式成绩。

`tools/` 保留当时的运行代码，`archive_manifest.json` 校验运行档案。后生成的 comparison 由报告复核器检查。运行以下命令可离线重算全部结果：

```bash
python3 scripts/build_task_performance_report.py --check
python3 scripts/generate_catalog_docs.py --check
```
