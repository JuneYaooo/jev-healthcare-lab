# 否定与推测线索作用范围

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 定位线索作用对象，属于语义范围标注，不是临床诊断核实。

## 任务是什么

给定试验文本及否定或推测线索，从原文候选中选择原 Negation/Speculation 唯一关联的对象。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `assertion_cue_target` |
| 医疗场景 | 病历与医疗质量控制 |
| 能力维度 | 关联与匹配 |
| 评测类别 | 文本理解与标注 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 西班牙语 100 题 |
| 数据范围 | 非商业研究附加集 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CT-EBM-SP v3](../datasets/ct_ebm_sp.md) | 100 | [原始来源](https://github.com/lcampillos/ct-ebm-sp-v3) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`assertion_cue_target:ct_ebm_sp:ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/S0370-41062001000100006.ann:T14`；语种：西班牙语；来源组：`ct_ebm_sp:S0370-41062001000100006`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "T1": "vitamina B12 [characters 4:16]",
        "T10": "mensual [characters 119:126]",
        "T11": "niños [characters 247:252]",
        "T12": "menor a 33 semanas [characters 273:291]",
        "T15": "crecimiento [characters 390:401]",
        "T16": "edad gestacional [characters 256:272]",
        "T17": "gestacional [characters 261:272]",
        "T18": "prematuro [characters 59:68]",
        "T19": "prematuro [characters 176:185]",
        "T2": "anemia del prematuro [characters 48:68]",
        "T20": "modifica la evolución [characters 20:41]",
        "T21": "evolución [characters 32:41]",
        "T22": "efecto [characters 83:89]",
        "T23": "4 veces [characters 131:138]",
        "T24": "evolución [characters 149:158]",
        "T25": "evolución [characters 358:367]",
        "T26": "hematológica [characters 368:380]",
        "T27": "número de transfusiones [characters 436:459]",
        "T28": "clínicamente significativas [characters 324:351]",
        "T3": "vitamina B12 [characters 106:118]",
        "T4": "anemia del prematuro [characters 165:185]",
        "T5": "estudio controlado, aleatorizado y doble ciego [characters 193:239]",
        "T6": "transfusiones [characters 446:459]",
        "T7": "diferencias [characters 312:323]",
        "T8": "100 mg [characters 93:99]",
        "T9": "IM [characters 100:102]"
      },
      "instructions": "给定试验文本及否定或推测线索，从原文候选中选择原 Negation/Speculation 唯一关联的对象。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_text": "\nLa vitamina B12 no modifica la evolución de la anemia del prematuro\n\nSe evalúa el efecto de 100 mg IM de vitamina B12 mensual por 4 veces, sobre la evolución de la anemia del prematuro, en un estudio controlado, aleatorizado y doble ciego, en 55 niños de edad gestacional menor a 33 semanas.\n\nNo se encontraron diferencias clínicamente significativas en la evolución hematológica ni en el crecimiento en los dos grupos estudiados.\n\nEl número de transfusiones fue significativamente menor en ambos grupos que los reportados en la literatura.\n",
    "target": {
      "end": 19,
      "start": 17,
      "text": "no"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `T20`，对应选项：

```json
"modifica la evolución [characters 20:41]"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "assertion_cue_target:ct_ebm_sp:ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/S0370-41062001000100006.ann:T14", "choice": "T20"}
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
    "answer_entity_id": "T20",
    "direction_reversed": false,
    "query_entity_id": "T14",
    "relation_ids": [
      "R2"
    ],
    "zip_member": "ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/S0370-41062001000100006.ann"
  },
  "material_kind": "clinical_trial_text_annotations",
  "resource": "ct_ebm_sp__corpus.zip",
  "resource_sha256": "15e2d7db735f18cb6726bb8316e2621154e96c7c460249e7a7134c12d8430bfe",
  "resource_url": "https://codeload.github.com/lcampillos/ct-ebm-sp-v3/zip/6dc68edd2fca44654cbecd3cb42586bb0e67e6fa",
  "source_id": "ct_ebm_sp",
  "source_url": "https://github.com/lcampillos/ct-ebm-sp-v3",
  "split": "official_test",
  "upstream_group": "S0370-41062001000100006",
  "upstream_id": "ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/S0370-41062001000100006.ann:T14",
  "version": "6dc68edd2fca44654cbecd3cb42586bb0e67e6fa"
}
```

该题的格式转换说明：

All valid entities of prespecified candidate types; unique explicit relation; no invented negatives.

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：T10 1 题、T102 1 题、T104 1 题、T11 1 题、T12 1 题、T14 3 题、T15 4 题、T16 2 题、T17 2 题、T18 3 题、T19 2 题、T20 1 题、T21 1 题、T22 1 题、T24 2 题、T25 1 题、T26 1 题、T27 1 题、T28 1 题、T30 1 题、T31 1 题、T32 1 题、T35 2 题、T37 1 题、T38 1 题、T39 2 题、T40 1 题、T44 1 题、T45 1 题、T46 2 题、T47 2 题、T49 1 题、T50 1 题、T51 2 题、T52 4 题、T53 1 题、T54 3 题、T56 3 题、T57 1 题、T58 2 题、T59 3 题、T60 1 题、T61 2 题、T62 2 题、T63 2 题、T64 2 题、T66 1 题、T67 1 题、T68 2 题、T70 1 题、T71 1 题、T72 5 题、T73 1 题、T74 1 题、T76 1 题、T78 1 题、T79 2 题、T8 1 题、T80 1 题、T87 1 题、T91 1 题、T92 1 题、T96 1 题、T99 1 题。

**[CT-EBM-SP v3](../datasets/ct_ebm_sp.md)**：西班牙语试验注册文本与期刊摘要；不是患者就诊记录。 答案依据：使用 brat/test 原始人工属性和关系；频次与剂型关联另外使用 brat/dev，逐题保留划分。实体片段或关联目标有限选择；不导出 UMLS 术语库，不构造未标注负例。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/assertion_cue_target/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/assertion_cue_target/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
