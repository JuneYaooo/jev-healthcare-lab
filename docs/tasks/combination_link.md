# 文本联合干预关系识别

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 识别原文哪些干预联合出现，不推荐联合方案。

## 任务是什么

给定试验文本和干预片段，从原文候选中选择原 Combined_with 唯一关联的联合对象。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `combination_link` |
| 医疗场景 | 临床试验筛选 |
| 能力维度 | 关联与匹配 |
| 评测类别 | 文本理解与标注 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 61 |
| 语种 | 西班牙语 100 题 |
| 数据范围 | 非商业研究附加集 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CT-EBM-SP v3](../datasets/ct_ebm_sp.md) | 100 | [原始来源](https://github.com/lcampillos/ct-ebm-sp-v3) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`combination_link:ct_ebm_sp:ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2011-004695-11.ann:T17`；语种：西班牙语；来源组：`ct_ebm_sp:2011-004695-11`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "T1": "Estudio de fase 3 de eficacia y seguridad [characters 46:87]",
        "T11": "tratamiento [characters 419:430]",
        "T12": "tratamiento [characters 483:494]",
        "T13": "Ribavirina [characters 520:530]",
        "T14": "Protocolo [characters 532:541]",
        "T18": "Peginterferón Lambda-1a [characters 91:114]",
        "T2": "Ribavirina [characters 117:127]",
        "T20": "sujetos [characters 353:360]",
        "T24": "Virus de la Hepatitis C [characters 662:685]",
        "T27": "Genotipo [characters 695:703]",
        "T28": "genotipo [characters 388:396]",
        "T3": "Telaprevir [characters 132:142]",
        "T4": "Estudio fase 3, enmascarado y aleatorizado [characters 165:207]",
        "T5": "Peginterferón Lambda-1a [characters 211:234]",
        "T6": "Ribavirina [characters 237:247]",
        "T7": "Peginterferón alfa-2a [characters 267:288]",
        "T8": "Ribavirina [characters 291:301]",
        "T9": "Telaprevir [characters 338:348]"
      },
      "instructions": "给定试验文本和干预片段，从原文候选中选择原 Combined_with 唯一关联的联合对象。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_text": "EudraCT Nº:  2011-004695-11\n\nTítulo público:  Estudio de fase 3 de eficacia y seguridad de Peginterferón Lambda-1a y Ribavirina con Telaprevir \n\nTítulo científico:  Estudio fase 3, enmascarado y aleatorizado de Peginterferón Lambda-1a y Ribavirina en comparación con Peginterferón alfa-2a y Ribavirina, cada uno de ellos administrado con Telaprevir, en sujetos con Hepatitis C crónica de genotipo-1 que no han recibido tratamiento con anterioridad o han sufrido una recidiva tras un tratamiento con Peginterferón Alfa y Ribavirina. Protocolo Revisado:01 - Incorpora Enmienda: 02 \n\nIndicación pública:  Hepatitis C Crónica \n\nIndicación científica:  Infección por Virus de la Hepatitis C Crónica (Genotipo-1) \n\nCriterios de inclusión:\nNA \n\nCriterios de exclusión:\nNA \n\n",
    "target": {
      "end": 517,
      "start": 499,
      "text": "Peginterferón Alfa"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `T13`，对应选项：

```json
"Ribavirina [characters 520:530]"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "combination_link:ct_ebm_sp:ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2011-004695-11.ann:T17", "choice": "T13"}
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
    "answer_entity_id": "T13",
    "direction_reversed": false,
    "query_entity_id": "T17",
    "relation_ids": [
      "R19"
    ],
    "zip_member": "ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2011-004695-11.ann"
  },
  "material_kind": "clinical_trial_text_annotations",
  "resource": "ct_ebm_sp__corpus.zip",
  "resource_sha256": "15e2d7db735f18cb6726bb8316e2621154e96c7c460249e7a7134c12d8430bfe",
  "resource_url": "https://codeload.github.com/lcampillos/ct-ebm-sp-v3/zip/6dc68edd2fca44654cbecd3cb42586bb0e67e6fa",
  "source_id": "ct_ebm_sp",
  "source_url": "https://github.com/lcampillos/ct-ebm-sp-v3",
  "split": "official_test",
  "upstream_group": "2011-004695-11",
  "upstream_id": "ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2011-004695-11.ann:T17",
  "version": "6dc68edd2fca44654cbecd3cb42586bb0e67e6fa"
}
```

该题的格式转换说明：

All valid entities of prespecified candidate types; unique explicit relation; no invented negatives.

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：T10 2 题、T11 5 题、T12 2 题、T13 2 题、T14 2 题、T15 3 题、T16 2 题、T17 2 题、T18 1 题、T19 5 题、T2 8 题、T20 2 题、T21 2 题、T23 2 题、T24 3 题、T25 1 题、T26 1 题、T27 2 题、T28 1 题、T29 3 题、T3 5 题、T30 3 题、T32 1 题、T35 1 题、T38 1 题、T39 1 题、T4 6 题、T41 2 题、T42 2 题、T43 1 题、T45 1 题、T49 1 题、T5 4 题、T50 1 题、T52 1 题、T53 1 题、T54 1 题、T55 1 题、T56 1 题、T57 1 题、T6 2 题、T67 1 题、T7 2 题、T78 1 题、T8 1 题、T9 6 题。

**[CT-EBM-SP v3](../datasets/ct_ebm_sp.md)**：西班牙语试验注册文本与期刊摘要；不是患者就诊记录。 答案依据：使用 brat/test 原始人工属性和关系；频次与剂型关联另外使用 brat/dev，逐题保留划分。实体片段或关联目标有限选择；不导出 UMLS 术语库，不构造未标注负例。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/combination_link/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/combination_link/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
