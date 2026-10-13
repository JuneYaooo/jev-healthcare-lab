# JEV 医疗多问题与并发测试

[结果总览](../../README.md) · [评估方法](../../docs/MEDICAL_LOAD.md)

JEV 通过第三方 API 接入：请求 `jev-latest`，逐条核对返回版本为 `jev-1.13.0`，后端身份未独立验证。延迟与吞吐包含接入平台及共享服务影响；不能据此推断官方直连的极限性能。JEV 成本按返回 usage 与官方标价折算，接入平台实际计费未知。Flash、Qwen 沿用 2026-10-12 的同题实测，JEV 于 2026-10-13 补测（日期均为 UTC），未同时运行。

27 个任务、1,578 项判断，沿用[原测试归档](../medical-load-v2/README.md)完全相同的题包和金标。JEV 的原始响应在本目录；Flash 与两款 Qwen 的原始响应继续保存在原归档。汇总文件记录两个来源，不将旧响应当作重新调用。

- [配置与渠道](config.json)、[题包](packets.jsonl)、[逐题来源](lineage.jsonl)、[价格快照](pricing.json)。
- [JEV 原始响应](jev-1.13.0/)、[合并复算结果](comparison.json)、[文件哈希](archive_manifest.json)、[接口适配源码](source/)。公共运行器沿用原归档中的冻结源码。
- 固定题集用于准确率与成本；预先选定的题包用于每任务 8／32 并发、各两轮持续负载。中断或不完整窗口不进入性能比较。

```bash
.venv/bin/python scripts/run_jev_gateway.py --check
.venv/bin/python scripts/generate_catalog_docs.py --check
```

重新生成报告、图表和文档不调用模型：

```bash
.venv/bin/python scripts/run_jev_gateway.py --report
.venv/bin/python scripts/render_medical_load_docs.py
.venv/bin/python scripts/generate_catalog_docs.py
```

运行测试使用本地 `JEV_GATEWAY_API_KEY`，调用命令为 `.venv/bin/python scripts/run_jev_gateway.py`。已完成题包和窗口可续跑复用；需要重新测量时应建立独立归档。费用保护按官方标价等价用量设置，不能保证接入平台的实际账单上限。
