# 干预用途关联

[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)

## 任务是什么

给定试验文本及干预片段，从原文候选中选择原 Used_for 唯一关联的用途；不评价个体适宜性。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `indication_link` |
| 医疗场景 | 临床试验筛选 |
| 能力维度 | 关联与匹配 |
| 决策类型 | 材料判断 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 西班牙语 100 题 |
| 数据范围 | 非商业研究附加集 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CT-EBM-SP v3](../datasets/ct_ebm_sp.md) | 100 | [原始来源](https://github.com/lcampillos/ct-ebm-sp-v3) |

## 如何作答与评分

根据题目给定的材料和规则，从 `request.questions.decision.criteria` 选择一个选项键。选项随题目变化；`gold` 保存标准选项键，不向模型发送。按选项键计准确率、宏 F1 和逐类召回，缺失或无效回答按错计。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`indication_link:ct_ebm_sp:ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2010-020803-63.ann:T6`；语种：西班牙语；来源组：`ct_ebm_sp:2010-020803-63`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "T1": "Estudio Fase III, prospectivo, multicéntrico, randomizado, doble ciego, controlado con placebo, de 2 grupos paralelos [characters 46:163]",
        "T10": "2010 [characters 13:17]",
        "T11": "6 mg/kg [characters 247:254]",
        "T12": "/día [characters 254:258]",
        "T13": "pacientes [characters 279:288]",
        "T14": "orales [characters 340:346]",
        "T2": "comparar la eficacia y seguridad [characters 170:202]",
        "T3": "tratamiento [characters 207:218]",
        "T4": "placebo [characters 268:275]",
        "T5": "asma persistente grave [characters 293:315]",
        "T7": "masitinib [characters 223:232]",
        "T8": "asma [characters 371:375]",
        "T9": "tratado [characters 316:323]"
      },
      "instructions": "给定试验文本及干预片段，从原文候选中选择原 Used_for 唯一关联的用途；不评价个体适宜性。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_text": "EudraCT Nº:  2010-020803-63\n\nTítulo público:  Estudio Fase III, prospectivo, multicéntrico, randomizado, doble ciego, controlado con placebo, de 2 grupos paralelos, para comparar la eficacia y seguridad del tratamiento con masitinib a la dosis de 6 mg/kg/día frente a placebo en pacientes con asma persistente grave tratado con corticoides orales. \n\nIndicación pública:  asma \n\nCriterios de inclusión:\nNA \n\nCriterios de exclusión:\nNA \n\n",
    "target": {
      "end": 339,
      "start": 328,
      "text": "corticoides"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `T9`，对应选项：

```json
"tratado [characters 316:323]"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "indication_link:ct_ebm_sp:ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2010-020803-63.ann:T6", "choice": "T9"}
```

### 样例溯源

[上游资源](https://codeload.github.com/lcampillos/ct-ebm-sp-v3/zip/6dc68edd2fca44654cbecd3cb42586bb0e67e6fa) · [数据集说明](../datasets/ct_ebm_sp.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-NC-SA-4.0",
  "distribution": "research_noncommercial",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "answer_entity_id": "T9",
    "direction_reversed": false,
    "query_entity_id": "T6",
    "relation_ids": [
      "R8"
    ],
    "zip_member": "ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2010-020803-63.ann"
  },
  "material_kind": "clinical_trial_text_annotations",
  "resource": "ct_ebm_sp__corpus.zip",
  "resource_sha256": "15e2d7db735f18cb6726bb8316e2621154e96c7c460249e7a7134c12d8430bfe",
  "resource_url": "https://codeload.github.com/lcampillos/ct-ebm-sp-v3/zip/6dc68edd2fca44654cbecd3cb42586bb0e67e6fa",
  "source_id": "ct_ebm_sp",
  "source_url": "https://github.com/lcampillos/ct-ebm-sp-v3",
  "split": "official_test",
  "upstream_group": "2010-020803-63",
  "upstream_id": "ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2010-020803-63.ann:T6",
  "version": "6dc68edd2fca44654cbecd3cb42586bb0e67e6fa"
}
```

该题的格式转换说明：

All valid entities of prespecified candidate types; unique explicit relation; no invented negatives.

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：T1 5 题、T10 1 题、T11 3 题、T12 3 题、T13 3 题、T15 3 题、T16 1 题、T17 3 题、T18 1 题、T19 2 题、T2 4 题、T20 1 题、T21 2 题、T23 1 题、T24 2 题、T25 2 题、T27 3 题、T28 4 题、T29 3 题、T3 3 题、T30 2 题、T31 1 题、T33 1 题、T34 3 题、T36 2 题、T37 1 题、T38 1 题、T39 1 题、T4 3 题、T41 3 题、T43 5 题、T44 2 题、T45 1 题、T47 1 题、T49 1 题、T5 5 题、T52 1 题、T53 1 题、T55 1 题、T56 1 题、T6 1 题、T60 1 题、T62 1 题、T67 1 题、T7 1 题、T70 1 题、T72 1 题、T77 1 题、T8 3 题、T9 2 题。

**[CT-EBM-SP v3](../datasets/ct_ebm_sp.md)**：西班牙语试验注册文本与期刊摘要；不是患者就诊记录。 答案依据：使用 brat/test 原始人工属性和关系；频次与剂型关联另外使用 brat/dev，逐题保留划分。实体片段或关联目标有限选择；不导出 UMLS 术语库，不构造未标注负例。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/indication_link/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/indication_link/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
