# MEDDOCAN / SPACCC

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

西班牙语公开病例报告经筛选、补入合成个人信息；不能视为原始患者身份记录。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `meddocan` |
| 上游入口 | [发布方页面](https://github.com/PlanTL-GOB-ES/SPACCC_MEDDOCAN) |
| 收录情况 | 100 题 / 1 个任务 |
| 评测用途 | 辅助评测（不计临床主分数） 100 题 |
| 使用范围 | 开放许可部分 |
| 登记的数据许可 | CC-BY-4.0 |
| 收录语种 | 西班牙语 100 题 |

## 来源与引用

Marimon et al. (2019), Automatic De-identification of Medical Texts in Spanish: the MEDDOCAN Track, Corpus, Guidelines, Methods and Evaluation of Results; SEAD / BSC / CNIO.

[论文或项目引用](https://ceur-ws.org/Vol-2421/MEDDOCAN_overview.pdf) · [数据许可](https://raw.githubusercontent.com/PlanTL-GOB-ES/SPACCC_MEDDOCAN/783a6df385c975b328c99bcffb54196a9ba4078a/LICENSE)

许可与说明快照：[README.md](../../benchmarks/medical_decision_v1/sources/meddocan/README.md) · [LICENSE](../../benchmarks/medical_decision_v1/sources/meddocan/LICENSE)

### 使用限制

仅评估给定词是否落入原 PHI 片段，不是整份文档脱敏召回率。负例沿用完整标注语料的闭世界假设，仍可能受到上游漏标影响。

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [医疗文本个人标识识别](../tasks/privacy_candidate.md) | 辅助评测（不计临床主分数） | 100 | 给定目标片段，判断是否属于需处理的个人标识。 |

## 答案与格式转换

官方 test BRAT 人工 PHI 片段标注。目标词完全落在标注片段内映射为 yes，完全不重叠映射为 no（闭世界 O 标签）；跨边界目标排除，不生成隐私标识。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

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

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[医疗文本个人标识识别](../tasks/privacy_candidate.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
