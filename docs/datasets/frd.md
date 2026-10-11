# Clinical Trial Parser annotated test data

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

真实试验条件，公开测试文本经过规范化，数字替换为 @NUMBER。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `frd` |
| 上游入口 | [发布方页面](https://github.com/facebookresearch/Clinical-Trial-Parser) |
| 收录情况 | 100 题 / 1 个任务 |
| 使用范围 | 开放许可核心集 |
| 登记的数据许可 | Apache-2.0 |
| 收录语种 | 英语 100 题 |

## 来源与引用

Tseo, Salkola, Mohamed, Kumar and Abnousi (2020)

[论文或项目引用](https://arxiv.org/abs/2006.07296) · [数据许可](https://www.apache.org/licenses/LICENSE-2.0)

许可与说明快照：[frd__LICENSE](../../benchmarks/medical_decision_v1/sources/frd/frd__LICENSE) · [frd__README.md](../../benchmarks/medical_decision_v1/sources/frd/frd__README.md) · [frd__data_README.md](../../benchmarks/medical_decision_v1/sources/frd/frd__data_README.md)

## 用于哪些任务

| 任务说明 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- |
| [条件上界与下界](../tasks/criterion_bound.md) | 100 | 给定条件与数值限制片段，判断该限制是上界还是下界。 |

## 答案与格式转换

专业标注员 upper_bound/lower_bound；这里只判断方向，不做数值推理。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`criterion_bound:frd:2301:1`；语种：英语；来源组：`frd:e97bc0b10c78cbbc9243b50e276b43da6c59024488dd2bc9edc4fe20b5960762`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "lower_bound": "Lower bound / minimum",
        "upper_bound": "Upper bound / maximum"
      },
      "instructions": "给定条件与数值限制片段，判断该限制是上界还是下界。",
      "type": "choice"
    }
  },
  "state": {
    "criterion": "anc > @NUMBER",
    "end_exclusive": 13,
    "start": 6,
    "target": "@NUMBER"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `lower_bound`，对应选项：

```json
"Lower bound / minimum"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "criterion_bound:frd:2301:1", "choice": "lower_bound"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/facebookresearch/Clinical-Trial-Parser/03ea0d3f5efe7d1bee713d05bb026201230d9409/data/ner/test_processed_medical_ner.tsv) · [数据集说明](../datasets/frd.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "Apache-2.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "annotation_index": 1,
    "line": 2301,
    "original_annotation": "7:14:lower_bound"
  },
  "material_kind": "clinical_trial_registry_normalized",
  "resource": "frd__data_ner_test_processed_medical_ner.tsv",
  "resource_sha256": "0a2f14cd8045e15327657962b999fddb651b01c132b092addb12b12b67d74b9e",
  "resource_url": "https://raw.githubusercontent.com/facebookresearch/Clinical-Trial-Parser/03ea0d3f5efe7d1bee713d05bb026201230d9409/data/ner/test_processed_medical_ner.tsv",
  "source_id": "frd",
  "source_url": "https://github.com/facebookresearch/Clinical-Trial-Parser",
  "split": "official_test",
  "upstream_group": "e97bc0b10c78cbbc9243b50e276b43da6c59024488dd2bc9edc4fe20b5960762",
  "upstream_id": "2301:1",
  "version": "03ea0d3f5efe7d1bee713d05bb026201230d9409"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[条件上界与下界](../tasks/criterion_bound.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
