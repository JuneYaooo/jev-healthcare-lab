# 逐任务性能工作负载

[任务评估](../../docs/tasks/README.md) · [构造与计量协议](../../docs/TASK_PERFORMANCE.md)

本目录从原临床题库确定性抽取 566 道原题，覆盖全部 26 个有题临床任务族。每任务取最多 32 道；3 个空任务留空。没有新生成临床金标。

- `inputs.jsonl`：原题 ID、任务族、完整 request、原 gold 与 provenance。
- `packets.jsonl`：单题或同任务多题请求、逐项原金标及 `source_ids` 映射。题包会按共同的保守上下文预算拆分，原材料不截断。
- `manifest.json`：取样规则、固定种子、各任务实际题数、分包大小、源数据与输入文件哈希。

多题打包将不同原题材料分别嵌入 `state.records.qNNN`，每问仅依据对应记录。不是同一患者的多维度新标注。模型输入仅为 request，gold 与 source_ids 不发送。

所有记录继承原来源许可，包括非商业附加材料。见逐题 provenance、[第三方说明](../../THIRD_PARTY_NOTICES.md)和[来源许可登记](../medical_decision_v1/SOURCES.md)；不能把整个工作负载当作无限制商用数据。各模型、各档位使用相同原题，不能通过重复题量扩大独立样本数。
