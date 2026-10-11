# TCMEval-PA

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

考试题与规则情境题，经上游中医执业医师核验；不是实际处方审核日志。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `tcmeval_pa` |
| 上游入口 | [发布方页面](https://doi.org/10.6084/m9.figshare.29651261.v3) |
| 收录情况 | 11 题 / 1 个任务 |
| 评测用途 | 辅助评测（不计临床主分数） 11 题 |
| 使用范围 | 开放许可部分 |
| 登记的数据许可 | CC-BY-4.0 |
| 收录语种 | 中文 11 题 |

## 来源与引用

Wang B., Lu Y., Wang Z. et al., TCMEval-PA

[论文或项目引用](https://doi.org/10.1038/s41597-025-06387-6) · [数据许可](https://creativecommons.org/licenses/by/4.0/)

许可与说明快照：[figshare-metadata.json](../../benchmarks/medical_decision_v1/sources/tcmeval_pa/figshare-metadata.json)

### 使用限制

固定发布版本的上游答案；未作本项目独立临床或现行规范核验。数据许可按 Figshare 数据记录，区别于论文或仓库其他内容许可。

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [中药处方审核规范情境问答](../tasks/prescription_audit_action.md) | 辅助评测（不计临床主分数） | 11 | 给定处方审核情境，从原始选项中选择上游标注的处理行动或审核要求。按发布版本评分，不等同现行政策核验或完整个体处方审核。 |

## 答案与格式转换

保留原 Excel 单选答案；仅纳入固定清单的情境处置题，不使用解释字段作为输入。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`prescription_audit_action:tcmeval_pa:226`；语种：中文；来源组：`tcmeval_pa:5edec134991920173defec35`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "患者书面同意",
        "B": "医师双签字确认",
        "C": "药师加注备注",
        "D": "护士会诊",
        "E": "药房主任批准"
      },
      "instructions": "给定处方审核情境，从原始选项中选择上游标注的处理行动或审核要求。按发布版本评分，不等同现行政策核验或完整个体处方审核。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "若确因病情需要超规格使用药味数，通过审核前必须满足哪项要求？"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `B`，对应选项：

```json
"医师双签字确认"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "prescription_audit_action:tcmeval_pa:226", "choice": "B"}
```

### 样例溯源

[上游资源](https://ndownloader.figshare.com/files/56581880) · [数据集说明](../datasets/tcmeval_pa.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "answer_column": "D",
    "upstream_id": "226",
    "xlsx_row": 227,
    "xlsx_sheet": "单选-多选"
  },
  "material_kind": "exam_and_rule_based_scenarios",
  "resource": "tcmeval_pa__TCMEval-PA.xlsx",
  "resource_sha256": "905cb28f145ba50f3b1c912265ff6649e0bb38f56adf6cd588d77ca768db92c1",
  "resource_url": "https://ndownloader.figshare.com/files/56581880",
  "source_id": "tcmeval_pa",
  "source_url": "https://doi.org/10.6084/m9.figshare.29651261.v3",
  "split": "published_benchmark_no_official_split",
  "upstream_group": "5edec134991920173defec35",
  "upstream_id": "226",
  "version": "Figshare 29651261.v3"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[中药处方审核规范情境问答](../tasks/prescription_audit_action.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
