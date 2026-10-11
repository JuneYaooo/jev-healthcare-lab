# TCMEval-SDT

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

整理的经典医案、网络及医院病例材料；不是统一采集的前瞻性患者队列。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `tcmeval_sdt` |
| 上游入口 | [发布方页面](https://doi.org/10.6084/m9.figshare.27184596.v5) |
| 收录情况 | 100 题 / 1 个任务 |
| 评测用途 | 临床主评测 100 题 |
| 使用范围 | 开放许可部分 |
| 登记的数据许可 | CC-BY-4.0 |
| 收录语种 | 中文 100 题 |

## 来源与引用

Wang Z., Hao M., Peng S. et al. (2025), TCMEval-SDT

[论文或项目引用](https://doi.org/10.1038/s41597-025-04772-9) · [数据许可](https://creativecommons.org/licenses/by/4.0/)

许可与说明快照：[figshare-metadata.json](../../benchmarks/medical_decision_v1/sources/tcmeval_sdt/figshare-metadata.json)

### 使用限制

固定发布版本的上游答案；未作本项目独立临床或现行规范核验。数据许可按 Figshare 数据记录，区别于论文或仓库其他内容许可。

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [中医候选病机判断](../tasks/tcm_pathogenesis_candidate.md) | 临床主评测 | 100 | 根据病例和原始候选病机，判断目标候选是否被上游专家选中。否仅表示不属于本题原始答案集合，不表示医学上不可能。 |

## 答案与格式转换

v5 官方测试答案按病例 ID 连接；从病机多选答案机械映射候选是否入选。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`tcm_pathogenesis_candidate:tcmeval_sdt:病例252:J`；语种：中文；来源组：`tcmeval_sdt:病例252`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "no": "不属于本题上游所选病机集合",
        "yes": "属于上游专家所选病机集合"
      },
      "instructions": "根据病例和原始候选病机，判断目标候选是否被上游专家选中。否仅表示不属于本题原始答案集合，不表示医学上不可能。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_case": "25岁。主诉及病史：体质素弱，骤然血崩不止，唇甲俱白，目合神昏，额汗如珠，手足逆冷。诊查：脉濡舌淡。",
    "original_candidates": {
      "A": "血海失营",
      "B": "肝肾之阴不足",
      "C": "冲任受损",
      "D": "血不归经",
      "E": "脾不统血",
      "F": "痰火互结",
      "G": "热病伤阴",
      "H": "痰浊阻膈",
      "I": "气滞血瘀",
      "J": "血虚"
    },
    "target_candidate": {
      "key": "J",
      "text": "血虚"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `no`，对应选项：

```json
"不属于本题上游所选病机集合"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "tcm_pathogenesis_candidate:tcmeval_sdt:病例252:J", "choice": "no"}
```

### 样例溯源

[上游资源](https://ndownloader.figshare.com/files/51198842) · [数据集说明](../datasets/tcmeval_sdt.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "answer_field_zero_based": 2,
    "answer_line": 16,
    "case_id": "病例252",
    "json_index": 15,
    "supporting_resources": [
      "tcmeval_sdt__Test_data_result.txt"
    ]
  },
  "material_kind": "curated_case_and_expert_annotation",
  "resource": "tcmeval_sdt__Test_TCM_Data_v1.json",
  "resource_sha256": "4b9f69308b46125ea6d979613d4b2717b1d930d7acefd2e3c58d274975420bff",
  "resource_url": "https://ndownloader.figshare.com/files/51198842",
  "source_id": "tcmeval_sdt",
  "source_url": "https://doi.org/10.6084/m9.figshare.27184596.v5",
  "split": "official_test",
  "upstream_group": "病例252",
  "upstream_id": "病例252:J",
  "version": "Figshare 27184596.v5"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[中医候选病机判断](../tasks/tcm_pathogenesis_candidate.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
