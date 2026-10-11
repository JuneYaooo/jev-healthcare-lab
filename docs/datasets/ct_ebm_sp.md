# CT-EBM-SP v3

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

西班牙语试验注册文本与期刊摘要；不是患者就诊记录。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `ct_ebm_sp` |
| 上游入口 | [发布方页面](https://github.com/lcampillos/ct-ebm-sp-v3) |
| 收录情况 | 858 题 / 9 个任务 |
| 评测用途 | 辅助评测（不计临床主分数） 858 题 |
| 使用范围 | 非商业研究附加集 |
| 登记的数据许可 | CC-BY-NC-SA-4.0 |
| 收录语种 | 西班牙语 858 题 |

## 来源与引用

Campillos-Llanos et al.; CSIC

[论文或项目引用](https://github.com/lcampillos/ct-ebm-sp-v3) · [数据许可](https://creativecommons.org/licenses/by-nc-sa/4.0/)

许可与说明快照：[README.md](../../benchmarks/medical_decision_v1/sources/ct_ebm_sp/README.md) · [LICENSE](../../benchmarks/medical_decision_v1/sources/ct_ebm_sp/LICENSE) · [annotation.conf](../../benchmarks/medical_decision_v1/sources/ct_ebm_sp/annotation.conf)

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [否定与推测线索作用范围](../tasks/assertion_cue_target.md) | 辅助评测（不计临床主分数） | 100 | 给定试验文本及否定或推测线索，从原文候选中选择原 Negation/Speculation 唯一关联的对象。 |
| [文本因果关系识别](../tasks/cause_effect_link.md) | 辅助评测（不计临床主分数） | 100 | 给定试验文本及原因片段，从原文候选中选择原 Causes 唯一关联的结果；不推断未标注因果，也不认定患者级药物因果。 |
| [文本联合干预关系识别](../tasks/combination_link.md) | 辅助评测（不计临床主分数） | 100 | 给定试验文本和干预片段，从原文候选中选择原 Combined_with 唯一关联的联合对象。 |
| [文本剂型与药物关联](../tasks/drug_form_link.md) | 辅助评测（不计临床主分数） | 77 | 给定试验文本和剂型片段，从原文药物或干预候选中选择原 Has_Drug_Form 唯一关联的目标。 |
| [文本时长与对象关联](../tasks/duration_link.md) | 辅助评测（不计临床主分数） | 100 | 给定试验文本和持续时长片段，从原文候选中选择原 Has_Duration_or_Interval 唯一关联的临床对象。 |
| [临床文本主体角色识别](../tasks/experiencer.md) | 辅助评测（不计临床主分数） | 100 | 给定试验文本及主体片段，选择原标注角色：患者、家属或其他人。只评价文本角色。 |
| [文本频次与对象关联](../tasks/frequency_link.md) | 辅助评测（不计临床主分数） | 81 | 给定试验文本和频次片段，从原文候选中选择原 Has_Frequency 唯一关联的药物或事件。 |
| [文本干预用途关联](../tasks/indication_link.md) | 辅助评测（不计临床主分数） | 100 | 给定试验文本及干预片段，从原文候选中选择原 Used_for 唯一关联的用途；不评价个体适宜性。 |
| [文本给药途径与对象关联](../tasks/route_link.md) | 辅助评测（不计临床主分数） | 100 | 给定试验文本和给药途径片段，从原文药物或操作候选中选择原关系唯一关联的目标。 |

## 答案与格式转换

使用 brat/test 原始人工属性和关系；频次与剂型关联另外使用 brat/dev，逐题保留划分。实体片段或关联目标有限选择；不导出 UMLS 术语库，不构造未标注负例。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`experiencer:ct_ebm_sp:ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/S0370-41062001000100006.ann:A9`；语种：西班牙语；来源组：`ct_ebm_sp:S0370-41062001000100006`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "Family_member": "Family member",
        "Other": "Other",
        "Patient": "Patient / participant"
      },
      "instructions": "给定试验文本及主体片段，选择原标注角色：患者、家属或其他人。只评价文本角色。",
      "type": "choice"
    }
  },
  "state": {
    "target": {
      "end": 68,
      "start": 59,
      "text": "prematuro"
    },
    "trial_text": "\nLa vitamina B12 no modifica la evolución de la anemia del prematuro\n\nSe evalúa el efecto de 100 mg IM de vitamina B12 mensual por 4 veces, sobre la evolución de la anemia del prematuro, en un estudio controlado, aleatorizado y doble ciego, en 55 niños de edad gestacional menor a 33 semanas.\n\nNo se encontraron diferencias clínicamente significativas en la evolución hematológica ni en el crecimiento en los dos grupos estudiados.\n\nEl número de transfusiones fue significativamente menor en ambos grupos que los reportados en la literatura.\n"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `Patient`，对应选项：

```json
"Patient / participant"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "experiencer:ct_ebm_sp:ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/S0370-41062001000100006.ann:A9", "choice": "Patient"}
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
    "attribute_id": "A9",
    "target_id": "T18",
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
  "upstream_id": "ct-ebm-sp-v3-6dc68edd2fca44654cbecd3cb42586bb0e67e6fa/brat/test/S0370-41062001000100006.ann:A9",
  "version": "6dc68edd2fca44654cbecd3cb42586bb0e67e6fa"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[临床文本主体角色识别](../tasks/experiencer.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
