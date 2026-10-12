# 性能测试原始档案

[测试结果](../../docs/PERFORMANCE_RESULTS.md) · [协议](../../docs/PERFORMANCE.md)

`config.json` 保存模型、参数、价目、环境版本、随机执行顺序与代码哈希。`dataset/` 为执行时的工作负载快照；原临床材料继承各自来源许可，见 [数据说明](../../benchmarks/performance_v1/README.md)。

`cell-NNN.jsonl` 为各单元的逐请求记录，包含完整原始响应、状态、请求及供应商请求体哈希、排队与完整响应时间。单元顺序由 config.cells 对应；`summary.json` 保存逐单元汇总，`comparison.json` 为三轮聚合结果。

`tools/` 保留实际调用时的代码；`archive_manifest.json` 校验运行数据及代码快照。具体覆盖文件以清单为准；后生成的 comparison 由离线报告脚本验证。运行 `python3 scripts/build_performance_report.py --check` 可检查全部正式请求与派生统计，不调用 API。
