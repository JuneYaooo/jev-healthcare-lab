# 文本剂型与药物关联

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 将剂型片段与药物配对，不选择适用剂型。

## 任务是什么

给定试验文本和剂型片段，从原文药物或干预候选中选择原 Has_Drug_Form 唯一关联的目标。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `drug_form_link` |
| 医疗场景 | 治疗与用药 |
| 能力维度 | 关联与匹配 |
| 评测类别 | 文本理解与标注 |
| 当前题数 / 目标题数 | 77 / 100 |
| 来源组数 | 39 |
| 语种 | 西班牙语 77 题 |
| 数据范围 | 非商业研究附加集 77 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CT-EBM-SP v3](../datasets/ct_ebm_sp.md) | 77 | [原始来源](https://github.com/lcampillos/ct-ebm-sp-v3) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`drug_form_link:ct_ebm_sp:ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2013-003228-35.ann:T18`；语种：西班牙语；来源组：`ct_ebm_sp:2013-003228-35`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "T1": "Estudio de la eficacia preliminar y seguridad [characters 33:78]",
        "T10": "solución viscosa [characters 116:132]",
        "T12": "cisteamina [characters 401:411]",
        "T2": "cisteamina [characters 85:95]",
        "T28": "asentimiento [characters 799:811]",
        "T30": "admisión en el estudio [characters 313:335]",
        "T5": "consentimiento [characters 782:796]",
        "T6": "tratamiento [characters 374:385]",
        "T7": "consentimiento [characters 604:618]",
        "T8": "tratamientos tópicos oculares [characters 736:765]"
      },
      "instructions": "给定试验文本和剂型片段，从原文药物或干预候选中选择原 Has_Drug_Form 唯一关联的目标。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_text": "EudraCT Nº:   \n\nTítulo público:  Estudio de la eficacia preliminar y seguridad de la cisteamina tópica formulada en solución viscosa en pacientes con cistinosis \n\nIndicación pública:  Cistinosis \n\nCriterios de inclusión:\nLos pacientes deben cumplir cada uno de los siguientes criterios para ser elegibles para su admisión en el estudio:\n- Pacientes afectos de cistinosis en tratamiento con colirio de cisteamina al 0,55%, fórmula magistral en colirio, formulada por el Servicio de Farmacia del Hospital Universitari Vall d'Hebron.\n- Edad ≥5 años\n- Paciente colaborador y cumplidor\n- Padres que firmen el consentimiento o asentimiento en pacientes de más de 12 años de edad. \n\nCriterios de exclusión:\n- Utilización concomitante de otros tratamientos tópicos oculares.\n- Retirada del consentimiento o asentimiento. \n\n",
    "target": {
      "end": 397,
      "start": 390,
      "text": "colirio"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `T12`，对应选项：

```json
"cisteamina [characters 401:411]"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "drug_form_link:ct_ebm_sp:ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2013-003228-35.ann:T18", "choice": "T12"}
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
    "answer_entity_id": "T12",
    "direction_reversed": true,
    "query_entity_id": "T18",
    "relation_ids": [
      "R13"
    ],
    "zip_member": "ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2013-003228-35.ann"
  },
  "material_kind": "clinical_trial_text_annotations",
  "resource": "ct_ebm_sp__corpus.zip",
  "resource_sha256": "15e2d7db735f18cb6726bb8316e2621154e96c7c460249e7a7134c12d8430bfe",
  "resource_url": "https://codeload.github.com/lcampillos/ct-ebm-sp-v3/zip/6dc68edd2fca44654cbecd3cb42586bb0e67e6fa",
  "source_id": "ct_ebm_sp",
  "source_url": "https://github.com/lcampillos/ct-ebm-sp-v3",
  "split": "official_test",
  "upstream_group": "2013-003228-35",
  "upstream_id": "ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/2013-003228-35.ann:T18",
  "version": "6dc68edd2fca44654cbecd3cb42586bb0e67e6fa"
}
```

该题的格式转换说明：

All valid entities of prespecified candidate types; unique explicit relation; no invented negatives.

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：T1 3 题、T10 1 题、T11 1 题、T12 5 题、T13 2 题、T14 3 题、T15 3 题、T17 3 题、T19 1 题、T2 3 题、T20 4 题、T21 2 题、T22 1 题、T23 2 题、T24 2 题、T27 1 题、T28 1 题、T29 1 题、T3 3 题、T30 1 题、T31 1 题、T33 1 题、T35 1 题、T36 1 题、T37 2 题、T38 2 题、T4 2 题、T41 1 题、T42 1 题、T43 1 题、T44 1 题、T45 1 题、T47 1 题、T49 1 题、T50 1 题、T54 2 题、T57 1 题、T6 1 题、T7 2 题、T8 4 题、T85 1 题、T9 5 题。

当前可用题目不足目标数量，保留实际题量；比较细小差异时须同时报告样本数。

**[CT-EBM-SP v3](../datasets/ct_ebm_sp.md)**：西班牙语试验注册文本与期刊摘要；不是患者就诊记录。 答案依据：使用 brat/test 原始人工属性和关系；频次与剂型关联另外使用 brat/dev，逐题保留划分。实体片段或关联目标有限选择；不导出 UMLS 术语库，不构造未标注负例。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/drug_form_link/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/drug_form_link/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
