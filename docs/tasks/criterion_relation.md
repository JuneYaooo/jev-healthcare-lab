# 入排标准要素关系识别

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 选择已标注要素的限定关系，且主要是正关系；不是患者级入排判断。

## 任务是什么

给定已标注关联的两个要素，判断数值、时间、限定等关系类型。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `criterion_relation` |
| 医疗场景 | 临床试验筛选 |
| 能力维度 | 资格与适宜性 |
| 评测类别 | 文本理解与标注 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [Chia](../datasets/chia.md) | 100 | [原始来源](https://doi.org/10.6084/m9.figshare.11855817) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。固定语义标签计算准确率、宏 F1、召回与混淆矩阵。

合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`criterion_relation:chia:NCT03013790_inc.ann:R2`；语种：英语；来源组：`chia:NCT03013790`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "Has_context": "Has_context",
        "Has_index": "Has_index",
        "Has_mood": "Has_mood",
        "Has_multiplier": "Has_multiplier",
        "Has_negation": "Has_negation",
        "Has_qualifier": "Has_qualifier",
        "Has_temporal": "Has_temporal",
        "Has_value": "Has_value",
        "Subsumes": "Subsumes"
      },
      "instructions": "给定已标注关联的两个要素，判断数值、时间、限定等关系类型。",
      "type": "choice"
    }
  },
  "state": {
    "criteria_text": "Non-ventilated Patients over the age of 65\r\n",
    "entity_1": {
      "end": 14,
      "start": 4,
      "text": "ventilated"
    },
    "entity_2": {
      "end": 3,
      "start": 0,
      "text": "Non"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `Has_negation`，对应选项：

```json
"Has_negation"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "criterion_relation:chia:NCT03013790_inc.ann:R2", "choice": "Has_negation"}
```

### 样例溯源

[上游资源](https://ndownloader.figshare.com/files/21728853) · [数据集说明](../datasets/chia.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "entity_ids": [
      "T3",
      "T4"
    ],
    "relation_id": "R2",
    "zip_member": "NCT03013790_inc.ann"
  },
  "material_kind": "clinical_trial_registry",
  "resource": "chia_without_scope.zip",
  "resource_sha256": "723457a4eb0ad57ac352b4976d1cdfc81b96e36233906474dc9c845cdc759c7c",
  "resource_url": "https://ndownloader.figshare.com/files/21728853",
  "source_id": "chia",
  "source_url": "https://doi.org/10.6084/m9.figshare.11855817",
  "split": "published_corpus_no_official_split",
  "upstream_group": "NCT03013790",
  "upstream_id": "NCT03013790_inc.ann:R2",
  "version": "figshare:11855817.v2"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：Has_context 11 题、Has_index 11 题、Has_mood 11 题、Has_multiplier 11 题、Has_negation 11 题、Has_qualifier 12 题、Has_temporal 11 题、Has_value 11 题、Subsumes 11 题。

**[Chia](../datasets/chia.md)**：真实 Phase IV 试验入排标准；无患者临床记录。 答案依据：医学专业人员的 BRAT 实体与关系；只转换已有标签，不合成患者。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/criterion_relation/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/criterion_relation/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
