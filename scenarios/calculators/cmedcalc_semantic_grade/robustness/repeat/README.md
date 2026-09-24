# 临床量表语义分级：重复调用

配对主任务：[原实验](../../README.md)。固定抽取 20 个原始案例，金标与原样本身份可由 metadata.original_task / original_id 关联。

保持输入与选项不变，额外调用一次，比较预测稳定性。

记录数 **20**；预测改变 **0**；原条件正确 **16**；扰动后正确 **16**。

[真实样本与金标](samples.jsonl) · [实际响应](responses.jsonl) · [完整提示词](prompts.json) · [完整示例](example.json) · [结果](results.json) · [来源与哈希](provenance.json)

比较预测变化时恢复标签，判断扰动样本正确性时使用该样本自身的 gold；不能把 300 条扰动当作新增独立患者。
