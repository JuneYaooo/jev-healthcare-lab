# 文本时长与对象关联

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 识别已有时长描述关联哪个对象，不制定疗程。

## 任务是什么

给定试验文本和持续时长片段，从原文候选中选择原 Has_Duration_or_Interval 唯一关联的临床对象。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `duration_link` |
| 医疗场景 | 临床试验筛选 |
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

题目 ID：`duration_link:ct_ebm_sp:ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2016-002915-17.ann:T18`；语种：西班牙语；来源组：`ct_ebm_sp:2016-002915-17`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "T1": "análogos de insulina [characters 79:99]",
        "T10": "DM1 [characters 489:492]",
        "T11": "Tratamiento intensivo con MDI [characters 544:573]",
        "T12": "consentimiento informado [characters 650:674]",
        "T13": "HbA1c [characters 528:533]",
        "T15": "personas [characters 103:111]",
        "T16": "personas [characters 229:237]",
        "T2": "diabetes tipo 1 [characters 116:131]",
        "T20": "MDI [characters 570:573]",
        "T22": "efecto [characters 58:64]",
        "T24": "inicio del estudio [characters 622:640]",
        "T3": "estrés oxidativo [characters 171:187]",
        "T4": "análogos de insulina [characters 205:225]",
        "T5": "diabetes tipo 1 [characters 242:257]",
        "T6": "Ensayo clínico [characters 259:273]",
        "T7": "intervención [characters 291:303]",
        "T8": "DIABETES [characters 342:350]",
        "T9": "DIABETES TIPO 1 [characters 377:392]"
      },
      "instructions": "给定试验文本和持续时长片段，从原文候选中选择原 Has_Duration_or_Interval 唯一关联的临床对象。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_text": "EudraCT Nº:  2016-002915-17\n\nTítulo público:  Estudio del efecto de los nuevos análogos de insulina en personas con diabetes tipo 1 \n\nTítulo científico:  Impacto sobre el estrés oxidativo de los distintos análogos de insulina en personas con diabetes tipo 1. Ensayo clínico de bajo nivel de intervención. Estudio Ineox \n\nIndicación pública:  DIABETES \n\nIndicación científica:  DIABETES TIPO 1 \n\nCriterios de inclusión:\n- Edad comprendida entre los 18 años y los 65 años (ambos incuidos)\n- DM1 de más de dos años de evolución \n- HbA1c ≤ 10 % \n- Tratamiento intensivo con MDI basal - Bolo durante más de 12 meses previos al inicio del estudio\n- Otorga consentimiento informado. \n\nCriterios de exclusión:\nNA \n\n",
    "target": {
      "end": 511,
      "start": 496,
      "text": "más de dos años"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `T10`，对应选项：

```json
"DM1 [characters 489:492]"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "duration_link:ct_ebm_sp:ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2016-002915-17.ann:T18", "choice": "T10"}
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
    "answer_entity_id": "T10",
    "direction_reversed": true,
    "query_entity_id": "T18",
    "relation_ids": [
      "R10"
    ],
    "zip_member": "ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2016-002915-17.ann"
  },
  "material_kind": "clinical_trial_text_annotations",
  "resource": "ct_ebm_sp__corpus.zip",
  "resource_sha256": "15e2d7db735f18cb6726bb8316e2621154e96c7c460249e7a7134c12d8430bfe",
  "resource_url": "https://codeload.github.com/lcampillos/ct-ebm-sp-v3/zip/6dc68edd2fca44654cbecd3cb42586bb0e67e6fa",
  "source_id": "ct_ebm_sp",
  "source_url": "https://github.com/lcampillos/ct-ebm-sp-v3",
  "split": "official_test",
  "upstream_group": "2016-002915-17",
  "upstream_id": "ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2016-002915-17.ann:T18",
  "version": "6dc68edd2fca44654cbecd3cb42586bb0e67e6fa"
}
```

该题的格式转换说明：

All valid entities of prespecified candidate types; unique explicit relation; no invented negatives.

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：T1 1 题、T10 2 题、T100 2 题、T103 1 题、T11 4 题、T12 4 题、T13 3 题、T14 2 题、T15 3 题、T16 3 题、T17 2 题、T18 2 题、T19 3 题、T2 1 题、T20 1 题、T22 1 题、T23 4 题、T24 2 题、T25 1 题、T26 2 题、T27 2 题、T28 1 题、T29 1 题、T3 5 题、T30 2 题、T31 2 题、T33 1 题、T34 1 题、T37 2 题、T38 3 题、T4 3 题、T42 1 题、T43 1 题、T44 1 题、T46 2 题、T47 2 题、T49 1 题、T5 1 题、T50 1 题、T54 1 题、T55 1 题、T56 1 题、T6 4 题、T61 1 题、T62 1 题、T64 1 题、T68 2 题、T7 3 题、T72 1 题、T78 1 题、T8 3 题、T81 1 题、T84 1 题、T9 1 题。

**[CT-EBM-SP v3](../datasets/ct_ebm_sp.md)**：西班牙语试验注册文本与期刊摘要；不是患者就诊记录。 答案依据：使用 brat/test 原始人工属性和关系；频次与剂型关联另外使用 brat/dev，逐题保留划分。实体片段或关联目标有限选择；不导出 UMLS 术语库，不构造未标注负例。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/duration_link/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/duration_link/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
