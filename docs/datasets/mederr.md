# MedErrBench CN

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

考试病例改编及专家补充，不声称全部是原始病历。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `mederr` |
| 上游入口 | [发布方页面](https://github.com/congboma/MedErrBench) |
| 收录情况 | 100 题 / 2 个任务 |
| 使用范围 | 开放许可核心集 |
| 登记的数据许可 | MIT |
| 收录语种 | 中文 100 题 |

## 来源与引用

Ma et al., MedErrBench (2026)

[论文或项目引用](https://arxiv.org/abs/2602.05692) · [数据许可](https://opensource.org/license/mit)

许可与说明快照：[mederr__README.md](../../benchmarks/medical_decision_v1/sources/mederr/mederr__README.md) · [mederr__LICENSE](../../benchmarks/medical_decision_v1/sources/mederr/mederr__LICENSE)

## 用于哪些任务

| 任务说明 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- |
| [医疗叙述错误检出](../tasks/clinical_error_detection.md) | 50 | 判断给定病例文本是否含原数据标注的医学错误。 |
| [医疗叙述错误定位](../tasks/clinical_error_location.md) | 50 | 在明确含错误的病例中，选择原始标注的错误句。 |

## 答案与格式转换

发布方 reviewed_data_CN_test 的错误标记和句子标记。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`clinical_error_detection:mederr:cn-test-17`；语种：中文；来源组：`mederr:cn-test-17`。

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
    "clinical_text": "男，43岁。外伤致右胸积血，右侧呼吸音弱，叩诊为浊音，胸穿抽出混浊胸液。进行胸穿。"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `1`，对应选项：

```json
"Contains an annotated medical error"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "clinical_error_detection:mederr:cn-test-17", "choice": "1"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/congboma/MedErrBench/754c2e083b794f2922f002b893bc2e8890feb16d/datasets/test/reviewed_data_CN_test.csv) · [数据集说明](../datasets/mederr.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "MIT",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "csv_row": 19,
    "text_id": "cn-test-17"
  },
  "material_kind": "exam_and_expert_authored",
  "resource": "mederr__datasets_test_reviewed_data_CN_test.csv",
  "resource_sha256": "79fcad4ed1c587904e2ad26f655c373ac7bcbe65cd867f5dcc09f76bc614655d",
  "resource_url": "https://raw.githubusercontent.com/congboma/MedErrBench/754c2e083b794f2922f002b893bc2e8890feb16d/datasets/test/reviewed_data_CN_test.csv",
  "source_id": "mederr",
  "source_url": "https://github.com/congboma/MedErrBench",
  "split": "official_test",
  "upstream_group": "cn-test-17",
  "upstream_id": "cn-test-17",
  "version": "754c2e083b794f2922f002b893bc2e8890feb16d"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[医疗叙述错误检出](../tasks/clinical_error_detection.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
