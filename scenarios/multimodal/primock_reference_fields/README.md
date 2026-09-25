# 参考转写病史字段判断

任务 ID：`primock_reference_fields` · 场景：[ 语音病历、医疗文档 OCR 与报告断言 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 20 | 3 | 20 | 0 | Accuracy | **100.0%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| Accuracy | 100.0% | 100.0% |
| 最终未能按要求作答 | 0 | 0 |
| 成功请求典型等待（中位数） | 0.64 秒 | 0.57 秒 |
| 每千条 API 费用估算 | $0.036 | $0.100 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

共 3 个公开扮演患者病例、20 个字段问题：原病例的完整 457.92 秒患者声道保留 12 个字段，另外两个病例各使用前 90 秒患者声道、4 个字段。参考文本来自原数据集的对齐转写；ASR 文本来自 Whisper tiny.en-q5_1 的真实转写。字段金标先按参考文本人工标注并保留证据短语，再对两种输入使用相同题目与金标。20 个字段不是 20 个独立患者，新增片段也不代表完整问诊。

实际模型为 `jev-1.13.0`。3 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`完整文本字符串`。
- 问题类型与总数：`choice` 20 个。
- 去重后的完整问题对象：20 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "no": "absent",
    "unknown": "not established",
    "yes": "present"
  },
  "instructions": "Is diarrhea currently present? Only use what this transcript says.",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`3`：1，`6_7`：1，`accountant`：1，`before`：1，`chest_hands_arms`：1，`impaired`：1，`left`：2，`low`：1，`midday`：1，`no`：5，`worse`：1，`yes`：4。

## 数据与实验记录

| 文件 | 内容 |
| --- | --- |
| [samples.jsonl](samples.jsonl) | 本任务全部真实评测输入、完整请求、gold、group、适配元数据及请求哈希 |
| [responses.jsonl](responses.jsonl) | 对应的原始成功响应记录；空候选时保留程序输出标记 |
| [prompts.json](prompts.json) | 从真实请求提取的全部问题／提示词／选项变体 |
| [example.json](example.json) | 一条完整实际样本与其对应响应，无合成替换 |
| [results.json](results.json) | 指标、置信区间、逐类表现、校准、token 与延迟 |
| [index.jsonl](index.jsonl) | 样本身份、请求哈希和响应原文件哈希 |
| [provenance.json](provenance.json) | 来源、归档文件哈希与原准备分片 |

通过 `(task, id)` 关联输入、响应与索引；响应哈希针对 JSONL 每行去掉换行分隔符后的原始字节计算。

数据适配：[ prepare_media_expansion.py ](../../../scripts/prepare_media_expansion.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [PriMock57](https://github.com/babylonhealth/primock57)：3 个公开扮演患者病例：原完整声道与两个 90 秒片段；真实 Whisper 转写和参考文本各测 20 个字段，金标由参考文本人工定义。

原始适配元数据：

- PriMock57 public acted consultation; first 90 seconds of patient channel; gold annotated from reference before model calls
- one patient audio channel;12manually authored field gold from reference; gold reused for ASR propagation, not original published field annotations

原准备分片：`final_tasks_prepared.jsonl`。

配对实验与原音频：[ASR 条件](../primock_asr_fields/README.md)。
