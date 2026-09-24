# 临床量表语义分级：无关说明

配对主任务：[原实验](../../README.md)。固定抽取 20 个原始案例，金标与原样本身份可由 metadata.original_task / original_id 关联。

在临床输入外添加与病例无关的行政说明，其余条件保持一致。

记录数 **20**；预测改变 **0**；原条件正确 **16**；扰动后正确 **16**。

[真实样本与金标](samples.jsonl) · [实际响应](responses.jsonl) · [完整提示词](prompts.json) · [完整示例](example.json) · [结果](results.json) · [来源与哈希](provenance.json)

比较预测变化时恢复标签，判断扰动样本正确性时使用该样本自身的 gold；不能把 300 条扰动当作新增独立患者。
