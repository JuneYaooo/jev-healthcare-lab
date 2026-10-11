# 临床文本否定与推测识别

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 识别否定或推测表达，且只覆盖两类，不判断患者是否确诊。

## 任务是什么

给定临床句子与标注目标，区分否定和不确定；本任务不覆盖肯定类。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `assertion_scope` |
| 医疗场景 | 诊断与鉴别 |
| 能力维度 | 事实与状态 |
| 评测类别 | 文本理解与标注 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 西班牙语 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [NUBes SAMPLE-001](../datasets/nubes.md) | 100 | [原始来源](https://github.com/Vicomtech/NUBes-negation-uncertainty-biomedical-corpus) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。固定语义标签计算准确率、宏 F1、召回与混淆矩阵。

合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`assertion_scope:nubes:nubes__NUBes_SAMPLE-001_sample-001.sugen.chico.ann:R29`；语种：西班牙语；来源组：`nubes:1f9152695bbd9facaa7b8162f8809294fad4e89805fe381a331545c133839c91`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "negative": "Negated or absent",
        "uncertain": "Possible or uncertain"
      },
      "instructions": "给定临床句子与标注目标，区分否定和不确定；本任务不覆盖肯定类。",
      "type": "choice"
    }
  },
  "state": {
    "excerpt": "Pendiente de decidir IQ .",
    "target": "IQ"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `uncertain`，对应选项：

```json
"Possible or uncertain"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "assertion_scope:nubes:nubes__NUBes_SAMPLE-001_sample-001.sugen.chico.ann:R29", "choice": "uncertain"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/Vicomtech/NUBes-negation-uncertainty-biomedical-corpus/91c81c1f5eee2b5b9d377cc78c2442e8e8b198a1/NUBes/SAMPLE-001/sample-001.sugen.chico.ann) · [数据集说明](../datasets/nubes.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-SA-3.0-ES",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "relation_id": "R29",
    "sentence_start": 3280,
    "target_id": "T80",
    "text_resource": "nubes__NUBes_SAMPLE-001_sample-001.sugen.chico.txt"
  },
  "material_kind": "deidentified_clinical",
  "resource": "nubes__NUBes_SAMPLE-001_sample-001.sugen.chico.ann",
  "resource_sha256": "00103145caa2a3faccfdc42fa6eb81a9e8efdcc70e4a72179ee3c14881b5365c",
  "resource_url": "https://raw.githubusercontent.com/Vicomtech/NUBes-negation-uncertainty-biomedical-corpus/91c81c1f5eee2b5b9d377cc78c2442e8e8b198a1/NUBes/SAMPLE-001/sample-001.sugen.chico.ann",
  "source_id": "nubes",
  "source_url": "https://github.com/Vicomtech/NUBes-negation-uncertainty-biomedical-corpus",
  "split": "SAMPLE-001_no_official_patient_split",
  "upstream_group": "1f9152695bbd9facaa7b8162f8809294fad4e89805fe381a331545c133839c91",
  "upstream_id": "nubes__NUBes_SAMPLE-001_sample-001.sugen.chico.ann:R29",
  "version": "91c81c1f5eee2b5b9d377cc78c2442e8e8b198a1"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：negative 50 题、uncertain 50 题。

**[NUBes SAMPLE-001](../datasets/nubes.md)**：西班牙语脱敏临床句子；句子打乱，不能据文件恢复患者。 答案依据：只用双标注及仲裁的 SAMPLE-001；作用域关系映射为否定/不确定。

其中 1 题材料或片段命中过往评测指纹；训练效果对比应核查材料暴露，并对各模型冻结相同子集。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/assertion_scope/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/assertion_scope/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
