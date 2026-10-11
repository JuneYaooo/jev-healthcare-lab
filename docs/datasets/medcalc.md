# MedCalc-Bench GitHub test release

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

文献提取、生成后人工编辑、模板混合；逐题保留 Note Type。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `medcalc` |
| 上游入口 | [发布方页面](https://github.com/ncbi-nlp/MedCalc-Bench) |
| 收录情况 | 100 题 / 1 个任务 |
| 评测用途 | 辅助评测（不计临床主分数） 100 题 |
| 使用范围 | 开放许可部分 |
| 登记的数据许可 | CC-BY-SA-4.0 |
| 收录语种 | 英语 100 题 |

## 来源与引用

Khandekar et al. (2024)

[论文或项目引用](https://arxiv.org/abs/2406.12036) · [数据许可](https://creativecommons.org/licenses/by-sa/4.0/)

许可与说明快照：[README.md](../../benchmarks/medical_decision_v1/sources/medcalc/README.md) · [medcalc__github_README.md](../../benchmarks/medical_decision_v1/sources/medcalc/medcalc__github_README.md)

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [临床量表计算](../tasks/bounded_score.md) | 辅助评测（不计临床主分数） | 100 | 根据病例选择 GCS、CURB-65、SIRS、CHA2DS2-VASc 或 FeverPAIN 的数值。 |

## 答案与格式转换

原测试 CSV Ground Truth Answer；完整整数范围作为候选，不由答案生成干扰项。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`bounded_score:medcalc:652`；语种：英语；来源组：`medcalc:trec-cds-2016-23`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4"
      },
      "instructions": "根据病例选择 GCS、CURB-65、SIRS、CHA2DS2-VASc 或 FeverPAIN 的数值。",
      "type": "choice"
    }
  },
  "state": {
    "patient_note": "85M dementia, colon cancer and recent colectomy with primary reanastomosis  p/w melena. HCT 30 to 23 but hemodynamically stable. NGL negative.  Exam notable for Tm 99 BP 128/50 HR 70 RR 16 with sat 100 on RA. WD man, NAD. Chest clear, JVP 8cm. RR s1s2. Soft abdomen, well healed surgical scar. No edema or cord. Labs notable for WBC 7K, HCT 24, K+ 4.0, Cr 0.7.",
    "question": "What are the number of SIRS critiera met by the patient? You should use the patient's medical values and health status when they were first admitted to the hospital prior to any treatment."
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `0`，对应选项：

```json
"0"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "bounded_score:medcalc:652", "choice": "0"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/ncbi-nlp/MedCalc-Bench/20b10f9d66a8c3b0356ae3138533f5ec91666b6a/datasets/test_data.csv) · [数据集说明](../datasets/medcalc.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-SA-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "csv_row": 653,
    "note_id": "trec-cds-2016-23",
    "row_number": "652"
  },
  "material_kind": "mixed_extracted_generated_template",
  "resource": "medcalc__datasets_test_data.csv",
  "resource_sha256": "c9d219a30e43f50646b73fa5fe5fe86d1ef47e7d9b2c7403a0edb7f3e5290e3a",
  "resource_url": "https://raw.githubusercontent.com/ncbi-nlp/MedCalc-Bench/20b10f9d66a8c3b0356ae3138533f5ec91666b6a/datasets/test_data.csv",
  "source_id": "medcalc",
  "source_url": "https://github.com/ncbi-nlp/MedCalc-Bench",
  "split": "official_github_test",
  "upstream_group": "trec-cds-2016-23",
  "upstream_id": "652",
  "version": "20b10f9d66a8c3b0356ae3138533f5ec91666b6a"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[临床量表计算](../tasks/bounded_score.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
