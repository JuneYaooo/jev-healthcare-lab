# MEDEC-MS

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

MedQA 考试病例改编与专家错误注入；未使用 UW 受控病历。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `medec` |
| 上游入口 | [发布方页面](https://github.com/abachaa/MEDEC) |
| 收录情况 | 100 题 / 2 个任务 |
| 评测用途 | 辅助评测（不计临床主分数） 100 题 |
| 使用范围 | 开放许可部分 |
| 登记的数据许可 | CC-BY-4.0 |
| 收录语种 | 英语 100 题 |

## 来源与引用

Abacha et al. (2025)

[论文或项目引用](https://aclanthology.org/2025.findings-acl.1159/) · [数据许可](https://creativecommons.org/licenses/by/4.0/)

许可与说明快照：[README.md](../../benchmarks/medical_decision_v1/sources/medec/README.md) · [medec__README.md](../../benchmarks/medical_decision_v1/sources/medec/medec__README.md)

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [病例医学错误检出](../tasks/clinical_error_detection.md) | 辅助评测（不计临床主分数） | 50 | 判断给定病例文本是否含原数据标注的医学错误。 |
| [病例医学错误定位](../tasks/clinical_error_location.md) | 辅助评测（不计临床主分数） | 50 | 在明确含错误的病例中，选择原始标注的错误句。 |

## 答案与格式转换

原始 Error Flag 与 Error Sentence ID；原文和更正文均不作模型参考答案。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`clinical_error_detection:medec:ms-test-64`；语种：英语；来源组：`medec:ms-test-64`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "0": "No annotated medical error",
        "1": "Contains an annotated medical error"
      },
      "instructions": "判断给定病例文本是否含原数据标注的医学错误。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_text": "An 11-year-old child complains of pain in the leg while playing. Blood pressure in the upper limb is 140/90 mm Hg and lower limbs are 110/70 mm Hg. There is a brachiofemoral delay in the pulse. Auscultation shows a loud S1, loud S2, and S4. There is a presence of an ejection systolic murmur in the interscapular area. Chest X-ray reveals the notching of the ribs. Patient is diagnosed with coarctation of the aorta."
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `0`，对应选项：

```json
"No annotated medical error"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "clinical_error_detection:medec:ms-test-64", "choice": "0"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/abachaa/MEDEC/e9173f861b39706946b6a127394992c00535b1e3/MEDEC-MS/MEDEC-MS-TestSet-with-GroundTruth-and-ErrorType.csv) · [数据集说明](../datasets/medec.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "csv_row": 66,
    "text_id": "ms-test-64"
  },
  "material_kind": "exam_derived_expert_errors",
  "resource": "medec__MEDEC-MS_MEDEC-MS-TestSet-with-GroundTruth-and-ErrorType.csv",
  "resource_sha256": "f35e2c3c1e4d98ca900394c4fcff14c2a84752e48ddc83698401da6a360c707e",
  "resource_url": "https://raw.githubusercontent.com/abachaa/MEDEC/e9173f861b39706946b6a127394992c00535b1e3/MEDEC-MS/MEDEC-MS-TestSet-with-GroundTruth-and-ErrorType.csv",
  "source_id": "medec",
  "source_url": "https://github.com/abachaa/MEDEC",
  "split": "official_test",
  "upstream_group": "ms-test-64",
  "upstream_id": "ms-test-64",
  "version": "e9173f861b39706946b6a127394992c00535b1e3"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[病例医学错误检出](../tasks/clinical_error_detection.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
