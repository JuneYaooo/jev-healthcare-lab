# 医疗材料隐私候选

[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)

## 任务是什么

给定目标片段，判断是否属于需处理的个人标识。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `privacy_candidate` |
| 医疗场景 | 病历与医疗质量控制 |
| 能力维度 | 风险与升级 |
| 决策类型 | 材料判断 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 西班牙语 100 题 |
| 数据范围 | 开放许可核心集 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [MEDDOCAN / SPACCC](../datasets/meddocan.md) | 100 | [原始来源](https://github.com/PlanTL-GOB-ES/SPACCC_MEDDOCAN) |

## 如何作答与评分

根据题目给定的材料和规则，从 `request.questions.decision.criteria` 选择一个选项键。选项随题目变化；`gold` 保存标准选项键，不向模型发送。按选项键计准确率、宏 F1 和逐类召回，缺失或无效回答按错计。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`privacy_candidate:meddocan:S1135-76062011000200009-1:234:238`；语种：西班牙语；来源组：`meddocan:S1135-76062011000200009-1`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "no": "Outside all PHI spans under MEDDOCAN annotation rules",
        "yes": "Inside a PHI span under MEDDOCAN annotation rules"
      },
      "instructions": "给定目标片段，判断是否属于需处理的个人标识。",
      "type": "choice"
    }
  },
  "state": {
    "annotation_scope": "MEDDOCAN PHI: patient and professional names, ages, sex, dates, addresses, locations, institutions, contact details and identifiers. Judge this target token in context.",
    "clinical_text": "Datos del paciente.\nNombre: Mateo.\nApellidos: Sanchez Rodriguez.\nNHC: 4790356.\nNASS: 47 52670894 67.\nDomicilio: C/ Principe de Vergara, 55, 3 B.\nLocalidad/ Provincia: Madrid.\nCP: 28015.\nDatos asistenciales.\nFecha de nacimiento: 30/04/1985.\nPaís de nacimiento: España.\nEdad: 33 años Sexo: H.\nFecha de Ingreso: 27/06/2018.\nMédico: Antonio Rico García NºCol: 28 28 55680.\nInforme clínico del paciente: Varón de 33 años, sin antecedentes patológicos conocidos, que ingresó en un servicio de urgencias hospitalario a las 7.43 h, procedente de su domicilio, con el diagnóstico de \"traumatismo craneal ocasionando ictus isquémico\". La tarde anterior había sufrido un golpe con un balón en el cuello mientras jugaba un partido de fútbol como portero.\nDurante su ingreso se practicó TAC craneal, que puso de manifiesto un infarto isquémico en el territorio de la arteria cerebral media derecha como consecuencia de una disección traumática de la arteria carótida interna derecha.\nPresentó hipertensión endocraneal y herniación cerebral con evolución hacia muerte encefálica, por lo que entró en programa de donación de órganos falleciendo 10 días después de su ingreso.\nResponsable clínico: Dr. Antonio Rico García. E-mail: anricoga@gmail.com\n",
    "target": {
      "end": 238,
      "start": 234,
      "text": "1985"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `yes`，对应选项：

```json
"Inside a PHI span under MEDDOCAN annotation rules"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "privacy_candidate:meddocan:S1135-76062011000200009-1:234:238", "choice": "yes"}
```

### 样例溯源

[上游资源](https://codeload.github.com/PlanTL-GOB-ES/SPACCC_MEDDOCAN/zip/783a6df385c975b328c99bcffb54196a9ba4078a) · [数据集说明](../datasets/meddocan.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "annotation_ids": [
      "T11"
    ],
    "annotation_member": "SPACCC_MEDDOCAN-783a6df385c975b328c99bcffb54196a9ba4078a/corpus/test/brat/S1135-76062011000200009-1.ann",
    "end": 238,
    "start": 234,
    "text_member": "SPACCC_MEDDOCAN-783a6df385c975b328c99bcffb54196a9ba4078a/corpus/test/brat/S1135-76062011000200009-1.txt"
  },
  "material_kind": "synthetic_enriched_clinical_cases",
  "resource": "meddocan__corpus.zip",
  "resource_sha256": "555470b36d90d04094aedf1a72bff079cb5dbcef98c8e40627a6beafc205ed1b",
  "resource_url": "https://codeload.github.com/PlanTL-GOB-ES/SPACCC_MEDDOCAN/zip/783a6df385c975b328c99bcffb54196a9ba4078a",
  "source_id": "meddocan",
  "source_url": "https://github.com/PlanTL-GOB-ES/SPACCC_MEDDOCAN",
  "split": "official_test",
  "upstream_group": "S1135-76062011000200009-1",
  "upstream_id": "S1135-76062011000200009-1:234:238",
  "version": "783a6df385c975b328c99bcffb54196a9ba4078a"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：no 50 题、yes 50 题。

**[MEDDOCAN / SPACCC](../datasets/meddocan.md)**：西班牙语公开病例报告经筛选、补入合成个人信息；不能视为原始患者身份记录。 答案依据：官方 test BRAT 人工 PHI 片段标注。目标词完全落在标注片段内映射为 yes，完全不重叠映射为 no（闭世界 O 标签）；跨边界目标排除，不生成隐私标识。

仅评估给定词是否落入原 PHI 片段，不是整份文档脱敏召回率。负例沿用完整标注语料的闭世界假设，仍可能受到上游漏标影响。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [n2c2/i2b2](../datasets/n2c2.md) | 需要相应数据使用协议，不纳入公开题目 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/privacy_candidate/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/privacy_candidate/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
