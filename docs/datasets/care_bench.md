# CARE-Bench

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

来源约束的重构咨询轨迹；GPT-5.5 辅助构建后人工审核（发布方说明），不是原始真实分诊记录。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `care_bench` |
| 上游入口 | [发布方页面](https://github.com/ningkko/CARE-bench) |
| 收录情况 | 100 题 / 1 个任务 |
| 使用范围 | 非商业研究附加集 |
| 登记的数据许可 | CC-BY-NC-4.0 |
| 收录语种 | 英语 100 题 |

## 来源与引用

CARE-Bench authors / ningkko

[论文或项目引用](https://arxiv.org/abs/2608.03731) · [数据许可](https://creativecommons.org/licenses/by-nc/4.0/)

许可与说明快照：[README.md](../../benchmarks/medical_decision_v1/sources/care_bench/README.md)

## 用于哪些任务

| 任务说明 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- |
| [当前分诊与升级行动](../tasks/triage_urgency.md) | 100 | 仅根据当前已披露消息，选择澄清信息、自护监测、非紧急就医或紧急就医；不生成建议文本。 |

## 答案与格式转换

只用 public_test_1 的四类 gold_label；只给当前已披露患者消息，不给后续轮次、参考回复、信息充分性和构造标签。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`triage_urgency:care_bench:meb_v1_case_0389_r01`；语种：英语；来源组：`care_bench:meb_v1_case_0389`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "0A_NO_ESCALATION_INFO_NEEDED": "Ask for necessary clarification",
        "0B_NO_ESCALATION_SELF_CARE_MONITOR": "Self-care or monitoring",
        "1A_ESCALATION_NONURGENT_CARE": "Nonurgent professional care",
        "1B_ESCALATION_URGENT_CARE": "Urgent or emergency care"
      },
      "instructions": "仅根据当前已披露消息，选择澄清信息、自护监测、非紧急就医或紧急就医；不生成建议文本。",
      "type": "choice"
    }
  },
  "state": {
    "patient_messages_so_far": [
      "My tummy hurts."
    ]
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `0A_NO_ESCALATION_INFO_NEEDED`，对应选项：

```json
"Ask for necessary clarification"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "triage_urgency:care_bench:meb_v1_case_0389_r01", "choice": "0A_NO_ESCALATION_INFO_NEEDED"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/ningkko/CARE-bench/090e84167f23c72d29c3a4d9c4f73e857afe0458/data/public/evaluation_prefixes_public.jsonl) · [数据集说明](../datasets/care_bench.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-NC-4.0",
  "distribution": "research_noncommercial",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "case_id": "meb_v1_case_0389",
    "jsonl_line": 774,
    "prefix_id": "meb_v1_case_0389_r01",
    "supporting_resources": [
      "care_bench__cases_public.jsonl"
    ]
  },
  "material_kind": "source_grounded_model_assisted_reconstructed",
  "resource": "care_bench__evaluation_prefixes_public.jsonl",
  "resource_sha256": "6d2850f303d05b8f92035c31a11233f41a965e77b3e878e1425f956a00cff534",
  "resource_url": "https://raw.githubusercontent.com/ningkko/CARE-bench/090e84167f23c72d29c3a4d9c4f73e857afe0458/data/public/evaluation_prefixes_public.jsonl",
  "source_id": "care_bench",
  "source_url": "https://github.com/ningkko/CARE-bench",
  "split": "official_public_test_1",
  "upstream_group": "meb_v1_case_0389",
  "upstream_id": "meb_v1_case_0389_r01",
  "version": "090e84167f23c72d29c3a4d9c4f73e857afe0458"
}
```

该题的格式转换说明：

Only disclosed patient turns; no reference response, future turns, or construction metadata.

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[当前分诊与升级行动](../tasks/triage_urgency.md)。

## 相关任务调研

以下为曾考虑使用此来源的任务，不代表已采用：

| 任务说明 | 任务内容 |
| --- | --- |
| [决策资料充分性](../tasks/input_sufficiency.md) | 判断给定临床记录是否包含回答目标问题的证据；当前以 LongHealth 缺失证据协议覆盖记录信息充分性，不覆盖计算缺项或冲突消解。 |
| [危急结果与人工升级](../tasks/critical_result_escalation.md) | 根据明确规则选择无需升级、复核或立即升级。 |

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
