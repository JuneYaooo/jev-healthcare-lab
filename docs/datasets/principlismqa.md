# PrinciplismQA

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

上游模型根据医学伦理教材构造题目，经医学专家审核；不是实际临床记录。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `principlismqa` |
| 上游入口 | [发布方页面](https://github.com/FreedomIntelligence/PrinciplismQA) |
| 收录情况 | 2 题 / 1 个任务 |
| 使用范围 | 开放许可核心集 |
| 登记的数据许可 | MIT |
| 收录语种 | 英语 2 题 |

## 来源与引用

Hong et al. (2026)

[论文或项目引用](https://aclanthology.org/2026.findings-acl.1806/) · [数据许可](https://opensource.org/license/mit)

许可与说明快照：[README.md](../../benchmarks/medical_decision_v1/sources/principlismqa/README.md) · [LICENSE](../../benchmarks/medical_decision_v1/sources/principlismqa/LICENSE)

### 使用限制

模型构题与筛选可能引入偏差；少量情境题只提供探索性覆盖，不能代表国际伦理共识或法律意见。

## 用于哪些任务

| 任务说明 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- |
| [知情与隐私处置选择](../tasks/consent_action.md) | 2 | 根据情境选择知情同意、隐私披露或尊重患者意愿的具体行动；不评价伦理原则名称。 |

## 答案与格式转换

保留固定清单中处置选择题的原问题、选项及 correct_answer；不纳入开放式问答或原则分类题。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`consent_action:principlismqa:21282`；语种：英语；来源组：`principlismqa:21282`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "Respect the patient's wishes and keep the HIV status confidential from family members and partners.",
        "B": "Disclose the patient's HIV status to family members and partners to prevent potential health risks to others.",
        "C": "Encourage the patient to disclose their HIV status to family members and partners while respecting their autonomy.",
        "D": "Automatically notify public health authorities and allow them to inform the family members and partners."
      },
      "instructions": "根据情境选择知情同意、隐私披露或尊重患者意愿的具体行动；不评价伦理原则名称。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "What is the most ethically appropriate action for a physician when a patient with HIV requests confidentiality from family and partners due to stigma concerns?"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `C`，对应选项：

```json
"Encourage the patient to disclose their HIV status to family members and partners while respecting their autonomy."
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "consent_action:principlismqa:21282", "choice": "C"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/FreedomIntelligence/PrinciplismQA/3538461406b045fa4bc777ac0c6e45fcb5e72968/data/knowledge-mcqa.json) · [数据集说明](../datasets/principlismqa.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "MIT",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "answer_field": "correct_answer",
    "row_index_zero_based": 503,
    "upstream_id": 21282
  },
  "material_kind": "expert_reviewed_model_created_exam_questions",
  "resource": "principlismqa__knowledge-mcqa.json",
  "resource_sha256": "7d35b7b4219d66e407a31caf0e1c6ff89991d68f1b0e56a1685caee039490ebf",
  "resource_url": "https://raw.githubusercontent.com/FreedomIntelligence/PrinciplismQA/3538461406b045fa4bc777ac0c6e45fcb5e72968/data/knowledge-mcqa.json",
  "source_id": "principlismqa",
  "source_url": "https://github.com/FreedomIntelligence/PrinciplismQA",
  "split": "published_benchmark_no_official_split",
  "upstream_group": "21282",
  "upstream_id": "21282",
  "version": "3538461406b045fa4bc777ac0c6e45fcb5e72968"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[知情与隐私处置选择](../tasks/consent_action.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
