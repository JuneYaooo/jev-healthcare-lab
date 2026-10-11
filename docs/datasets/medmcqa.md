# MedMCQA

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

印度医学考试题；不是患者观察队列。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `medmcqa` |
| 上游入口 | [发布方页面](https://huggingface.co/datasets/openlifescienceai/medmcqa) |
| 收录情况 | 2 题 / 2 个任务 |
| 评测用途 | 临床主评测 2 题 |
| 使用范围 | 开放许可部分 |
| 登记的数据许可 | Apache-2.0 |
| 收录语种 | 英语 2 题 |

## 来源与引用

Pal, Umapathi and Sankarasubbu (2022)

[论文或项目引用](https://proceedings.mlr.press/v174/pal22a.html) · [数据许可](https://www.apache.org/licenses/LICENSE-2.0)

许可与说明快照：[README.md](../../benchmarks/medical_decision_v1/sources/medmcqa/README.md)

### 使用限制

采用数据卡 Apache-2.0，而非代码仓库许可。仅固定范围清单病例题，未独立核验现行临床规范。

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [复查项目与随访时机选择](../tasks/followup_plan.md) | 临床主评测 | 1 | 根据完整病例选择复查项目或随访时机；不等同待办是否完成或逾期。 |
| [预防措施选择](../tasks/prevention_choice.md) | 临床主评测 | 1 | 根据病例、暴露或复发风险，选择预防行动；不评价预防等级概念。 |

## 答案与格式转换

仅用官方 validation、choice_type=single；cop 的 0–3 原样映射 opa–opd。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`prevention_choice:medmcqa:f9be858f-ef2f-475e-9c82-ced530a1a623`；语种：英语；来源组：`medmcqa:f9be858f-ef2f-475e-9c82-ced530a1a623`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "opa": "Hepatitis vaccine to the child",
        "opb": "Full course of Hepatitis B vaccine and immunoglobulin to the child",
        "opc": "Hepatitis B immunoglobulin to the mother",
        "opd": "Hepatitis B immunization to mother"
      },
      "instructions": "根据病例、暴露或复发风险，选择预防行动；不评价预防等级概念。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "A pregnant lady is diagnosed to be HBs Ag positive. Which of the following is the best way to prevent infection to the child:"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `opb`，对应选项：

```json
"Full course of Hepatitis B vaccine and immunoglobulin to the child"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "prevention_choice:medmcqa:f9be858f-ef2f-475e-9c82-ced530a1a623", "choice": "opb"}
```

### 样例溯源

[上游资源](https://huggingface.co/datasets/openlifescienceai/medmcqa/resolve/91c6572c454088bf71b679ad90aa8dffcd0d5868/data/validation-00000-of-00001.parquet) · [数据集说明](../datasets/medmcqa.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "Apache-2.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "answer_field": "cop",
    "row_index_zero_based": 584,
    "upstream_id": "f9be858f-ef2f-475e-9c82-ced530a1a623"
  },
  "material_kind": "medical_exam_questions",
  "resource": "medmcqa__validation-00000-of-00001.parquet",
  "resource_sha256": "b768a1ea34afc9f80d3106d9b21f80fa8a00ec450a1f6cd641af72ca9e591021",
  "resource_url": "https://huggingface.co/datasets/openlifescienceai/medmcqa/resolve/91c6572c454088bf71b679ad90aa8dffcd0d5868/data/validation-00000-of-00001.parquet",
  "source_id": "medmcqa",
  "source_url": "https://huggingface.co/datasets/openlifescienceai/medmcqa",
  "split": "official_validation",
  "upstream_group": "f9be858f-ef2f-475e-9c82-ced530a1a623",
  "upstream_id": "f9be858f-ef2f-475e-9c82-ced530a1a623",
  "version": "91c6572c454088bf71b679ad90aa8dffcd0d5868"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[预防措施选择](../tasks/prevention_choice.md)。

## 相关任务调研

以下为曾考虑使用此来源的任务，不代表已采用：

| 任务说明 | 任务内容 |
| --- | --- |
| [病例诊断选择：考试病例子集](../tasks/diagnosis_choice.md) | 从给定诊断候选中选择最符合病例者。 |
| [检查方案选择](../tasks/examination_choice.md) | 根据病例从给定候选中选择检查。 |
| [治疗方案选择](../tasks/treatment_choice.md) | 根据病例从给定候选中选择治疗。 |
| [用药方案选择](../tasks/medication_choice.md) | 根据病例从给定候选中选择用药。 |

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
