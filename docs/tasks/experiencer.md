# 临床文本主体角色识别

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 给定标注片段判断患者、家属等角色，是文本主体分类。

## 任务是什么

给定试验文本及主体片段，选择原标注角色：患者、家属或其他人。只评价文本角色。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `experiencer` |
| 医疗场景 | 接诊与分诊 |
| 能力维度 | 事实与状态 |
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

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。固定语义标签计算准确率、宏 F1、召回与混淆矩阵。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

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

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：Family_member 12 题、Other 40 题、Patient 48 题。

**[CT-EBM-SP v3](../datasets/ct_ebm_sp.md)**：西班牙语试验注册文本与期刊摘要；不是患者就诊记录。 答案依据：使用 brat/test 原始人工属性和关系；频次与剂型关联另外使用 brat/dev，逐题保留划分。实体片段或关联目标有限选择；不导出 UMLS 术语库，不构造未标注负例。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [n2c2/i2b2](../datasets/n2c2.md) | 需要相应数据使用协议，不纳入公开题目 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/experiencer/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/experiencer/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
