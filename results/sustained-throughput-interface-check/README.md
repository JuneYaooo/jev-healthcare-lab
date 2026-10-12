# 持续负载接口检查（DNS 处理修正前）

这是正式测试前的短检：每请求 8 题、8 并发、1 秒预热、3 秒统计窗口。仅确认接口、计时和持续补入请求能运行，不作为正式吞吐或医学准确率结论。

| 模型 | 总请求数（含预热） | 中止原因 |
| --- | ---: | --- |
| jev-1.13.0 | 74 | 无 |
| deepseek-flash | 43 | 无 |

[配置](config.json) · [逐档统计](summary.json) · [完整性清单](archive_manifest.json) · [正式协议](../../docs/SUSTAINED_THROUGHPUT.md)
