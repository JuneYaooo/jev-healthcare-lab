# 医疗多问题与持续并发原始记录

[结果总览](../../README.md) · [方法](../../docs/MEDICAL_LOAD.md)

本轮冻结 27 个任务、1,578 项独立判断，比较 JEV 1.13、DeepSeek V4.1 Flash、Qwen3.5-9B、Qwen3.8-27B。各模型的未完成项标注为缺失。

- [配置与题量](config.json)、[请求题包与评分金标](packets.jsonl)、[逐题来源与许可](lineage.jsonl)、[计价依据](pricing.json)。金标保存在本地归档，只发送 payload 白名单字段。
- 各模型目录的 `quality.jsonl.gz` 是全部固定题集请求；`任务-r轮次-c并发.jsonl.gz` 是逐请求负载响应；同名 JSON 记录窗口边界。原始响应均保留供应商 usage。
- [复算结果](comparison.json)、[文件哈希](archive_manifest.json)、[源代码快照](source/)。中断窗口保留为 `interrupted-*`，不参与性能汇总。
- 总体图不混入新增共享患者面板；该面板与既有转介题集可能有重合。

当前归档可核算的用量标价上界合计约 ¥48.43，不等于最终账单；缺失 usage、在途中断可能留下未观测费用。README 成本列另按最终响应、无缓存、不含重试的统一条件估算。

本地复算，无模型调用：

```bash
.venv/bin/python scripts/build_medical_load_report.py --check
.venv/bin/python scripts/generate_catalog_docs.py --check
```

重新生成图表与页面：

```bash
.venv/bin/python scripts/build_medical_load_report.py
.venv/bin/python scripts/render_medical_load_docs.py
.venv/bin/python scripts/generate_catalog_docs.py
```

重新调用会产生费用，需有效凭据与相应账户额度。运行器默认复用已完成题包与窗口；原归档应先复制留存，避免混淆不同时期模型版本。数据的研究／非商业许可仍分别适用，见[数据来源](../../docs/datasets/README.md)。
