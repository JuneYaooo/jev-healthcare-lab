# 药物相互作用关系

[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)

## 任务是什么

给定药物对，判断无关系或原文标注的相互作用类型。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `drug_interaction` |
| 医疗场景 | 治疗与用药 |
| 能力维度 | 关联与匹配 |
| 决策类型 | 材料判断 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 英语 100 题 |
| 数据范围 | 非商业研究附加集 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [DDI Corpus 2013](../datasets/ddi.md) | 100 | [原始来源](https://github.com/isegura/DDICorpus) |

## 如何作答与评分

根据题目给定的材料和规则，从 `request.questions.decision.criteria` 选择一个选项键。选项随题目变化；`gold` 保存标准选项键，不向模型发送。按选项键计准确率、宏 F1 和逐类召回，缺失或无效回答按错计。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`drug_interaction:ddi:DDI-DrugBank.d619.s2.p0`；语种：英语；来源组：`ddi:DDI-DrugBank.d619`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "advise": "Advice or recommendation about joint use",
        "effect": "Pharmacodynamic effect",
        "int": "Interaction without specified mechanism or effect",
        "mechanism": "Pharmacokinetic mechanism",
        "none": "No annotated interaction"
      },
      "instructions": "给定药物对，判断无关系或原文标注的相互作用类型。",
      "type": "choice"
    }
  },
  "state": {
    "drug_1": "meperidine",
    "drug_2": "MAOIs",
    "sentence": "This is typical of the interaction of meperidine and MAOIs. "
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `int`，对应选项：

```json
"Interaction without specified mechanism or effect"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "drug_interaction:ddi:DDI-DrugBank.d619.s2.p0", "choice": "int"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/isegura/DDICorpus/819b0fa538ed83ab2a8b4f5417bba3c03249b7f3/DDICorpus-2013.zip) · [数据集说明](../datasets/ddi.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-NC-4.0",
  "distribution": "research_noncommercial",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "pair_id": "DDI-DrugBank.d619.s2.p0",
    "zip_member": "DDICorpus/Test/Test for DDI Extraction task/DrugBank/Selegiline.xml"
  },
  "material_kind": "drug_reference_and_literature",
  "resource": "ddi__DDICorpus-2013.zip",
  "resource_sha256": "87fc63e32ebce20d9841c372e0c594ec72d60882ab5621550ca73c3eaf80ab60",
  "resource_url": "https://raw.githubusercontent.com/isegura/DDICorpus/819b0fa538ed83ab2a8b4f5417bba3c03249b7f3/DDICorpus-2013.zip",
  "source_id": "ddi",
  "source_url": "https://github.com/isegura/DDICorpus",
  "split": "official_test",
  "upstream_group": "DDI-DrugBank.d619",
  "upstream_id": "DDI-DrugBank.d619.s2.p0",
  "version": "819b0fa538ed83ab2a8b4f5417bba3c03249b7f3"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：advise 21 题、effect 21 题、int 15 题、mechanism 22 题、none 21 题。

**[DDI Corpus 2013](../datasets/ddi.md)**：DrugBank / MEDLINE 文本，不是患者处方。 答案依据：沿用公开测试集药物实体对及 ddi/type 标签。

其中 28 题材料或片段命中过往评测指纹；训练效果对比应核查材料暴露，并对各模型冻结相同子集。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/drug_interaction/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/drug_interaction/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
