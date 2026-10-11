# 文本因果结果关联

[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)

## 任务是什么

给定试验文本及原因片段，从原文候选中选择原 Causes 唯一关联的结果；不推断未标注因果，也不认定患者级药物因果。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `cause_effect_link` |
| 医疗场景 | 病历与医疗质量控制 |
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

题目 ID：`cause_effect_link:ct_ebm_sp:ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/S0104-11692001000600009.ann:T2`；语种：西班牙语；来源组：`ct_ebm_sp:S0104-11692001000600009`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "T1": "ENEMAS [characters 11:17]",
        "T10": "PARTO [characters 44:49]",
        "T11": "trabajo de parto [characters 494:510]",
        "T12": "parto [characters 195:200]",
        "T15": "partos normales [characters 302:317]",
        "T18": "disminuyó [characters 471:480]",
        "T22": "redujo la contaminación fecal [characters 516:545]",
        "T23": "trabajo de parto [characters 173:189]",
        "T24": "efectos [characters 111:118]",
        "T26": "contaminación fecal [characters 142:161]",
        "T4": "cesárea [characters 343:350]",
        "T5": "ensayo clínico aleatorio [characters 368:392]",
        "T6": "enemas [characters 428:434]",
        "T7": "enema [characters 462:467]",
        "T9": "enema [characters 587:592]"
      },
      "instructions": "给定试验文本及原因片段，从原文候选中选择原 Causes 唯一关联的结果；不推断未标注因果，也不认定患者级药物因果。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_text": "\nEL USO DE ENEMAS EN LA PREPARACIÓN PARA EL PARTO: ANALISIS DE SUS VENTAJAS Y DESVENTAJAS\n\nSe investigaron los efectos de los enemas sobre la contaminación fecal durante el trabajo de parto y el parto, entre mujeres atendidas en un hospital-escuela.\n\nLa población estuvo constituida por 90 mujeres (43 partos normales, 27 con fórceps y 20 por cesárea).\n\nSe realizó un ensayo clínico aleatorio, se consideraron grupos: con y sin enemas.\n\nSe puede concluir que el enema no disminuyó el tiempo de trabajo de parto y no redujo la contaminación fecal. Aun así, las mujeres, que realizaron el enema tuvieron opinión más favorable sobre éste que aquellas que no lo realizaron.\n\n",
    "target": {
      "end": 132,
      "start": 126,
      "text": "enemas"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `T24`，对应选项：

```json
"efectos [characters 111:118]"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "cause_effect_link:ct_ebm_sp:ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/S0104-11692001000600009.ann:T2", "choice": "T24"}
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
    "answer_entity_id": "T24",
    "direction_reversed": false,
    "query_entity_id": "T2",
    "relation_ids": [
      "R3"
    ],
    "zip_member": "ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/S0104-11692001000600009.ann"
  },
  "material_kind": "clinical_trial_text_annotations",
  "resource": "ct_ebm_sp__corpus.zip",
  "resource_sha256": "15e2d7db735f18cb6726bb8316e2621154e96c7c460249e7a7134c12d8430bfe",
  "resource_url": "https://codeload.github.com/lcampillos/ct-ebm-sp-v3/zip/6dc68edd2fca44654cbecd3cb42586bb0e67e6fa",
  "source_id": "ct_ebm_sp",
  "source_url": "https://github.com/lcampillos/ct-ebm-sp-v3",
  "split": "official_test",
  "upstream_group": "S0104-11692001000600009",
  "upstream_id": "ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/S0104-11692001000600009.ann:T2",
  "version": "6dc68edd2fca44654cbecd3cb42586bb0e67e6fa"
}
```

该题的格式转换说明：

All valid entities of prespecified candidate types; unique explicit relation; no invented negatives.

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：T10 5 题、T100 1 题、T11 1 题、T112 1 题、T12 2 题、T126 1 题、T13 1 题、T14 4 题、T15 1 题、T17 1 题、T18 2 题、T20 3 题、T21 4 题、T22 3 题、T23 5 题、T24 4 题、T25 1 题、T26 2 题、T27 3 题、T28 2 题、T29 1 题、T3 1 题、T31 1 题、T32 1 题、T33 2 题、T35 1 题、T39 3 题、T4 2 题、T40 1 题、T42 1 题、T43 1 题、T44 1 题、T47 2 题、T5 4 题、T54 1 题、T56 1 题、T57 1 题、T59 1 题、T6 3 题、T61 2 题、T62 1 题、T64 1 题、T65 1 题、T66 1 题、T68 2 题、T69 1 题、T7 2 题、T73 1 题、T74 1 题、T76 1 题、T79 1 题、T80 1 题、T86 1 题、T87 1 题、T88 1 题、T92 2 题、T93 1 题、T94 1 题、T95 1 题。

**[CT-EBM-SP v3](../datasets/ct_ebm_sp.md)**：西班牙语试验注册文本与期刊摘要；不是患者就诊记录。 答案依据：使用 brat/test 原始人工属性和关系；频次与剂型关联另外使用 brat/dev，逐题保留划分。实体片段或关联目标有限选择；不导出 UMLS 术语库，不构造未标注负例。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/cause_effect_link/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/cause_effect_link/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
