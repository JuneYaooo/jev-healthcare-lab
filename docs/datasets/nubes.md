# NUBes SAMPLE-001

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

西班牙语脱敏临床句子；句子打乱，不能据文件恢复患者。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `nubes` |
| 上游入口 | [发布方页面](https://github.com/Vicomtech/NUBes-negation-uncertainty-biomedical-corpus) |
| 收录情况 | 100 题 / 1 个任务 |
| 使用范围 | 开放许可核心集 |
| 登记的数据许可 | CC-BY-SA-3.0-ES |
| 收录语种 | 西班牙语 100 题 |

## 来源与引用

Lima Lopez, Perez, Cuadros and Rigau (2020)

[论文或项目引用](https://aclanthology.org/2020.lrec-1.708/) · [数据许可](https://creativecommons.org/licenses/by-sa/3.0/es/)

许可与说明快照：[nubes__LICENSE](../../benchmarks/medical_decision_v1/sources/nubes/nubes__LICENSE) · [nubes__README.md](../../benchmarks/medical_decision_v1/sources/nubes/nubes__README.md)

## 用于哪些任务

| 任务说明 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- |
| [否定与不确定状态](../tasks/assertion_scope.md) | 100 | 给定临床句子与标注目标，区分否定和不确定；本任务不覆盖肯定类。 |

## 答案与格式转换

只用双标注及仲裁的 SAMPLE-001；作用域关系映射为否定/不确定。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`assertion_scope:nubes:nubes__NUBes_SAMPLE-001_sample-001.sugen.chico.ann:R29`；语种：西班牙语；来源组：`nubes:1f9152695bbd9facaa7b8162f8809294fad4e89805fe381a331545c133839c91`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "negative": "Negated or absent",
        "uncertain": "Possible or uncertain"
      },
      "instructions": "给定临床句子与标注目标，区分否定和不确定；本任务不覆盖肯定类。",
      "type": "choice"
    }
  },
  "state": {
    "excerpt": "Pendiente de decidir IQ .",
    "target": "IQ"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `uncertain`，对应选项：

```json
"Possible or uncertain"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "assertion_scope:nubes:nubes__NUBes_SAMPLE-001_sample-001.sugen.chico.ann:R29", "choice": "uncertain"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/Vicomtech/NUBes-negation-uncertainty-biomedical-corpus/91c81c1f5eee2b5b9d377cc78c2442e8e8b198a1/NUBes/SAMPLE-001/sample-001.sugen.chico.ann) · [数据集说明](../datasets/nubes.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-SA-3.0-ES",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "relation_id": "R29",
    "sentence_start": 3280,
    "target_id": "T80",
    "text_resource": "nubes__NUBes_SAMPLE-001_sample-001.sugen.chico.txt"
  },
  "material_kind": "deidentified_clinical",
  "resource": "nubes__NUBes_SAMPLE-001_sample-001.sugen.chico.ann",
  "resource_sha256": "00103145caa2a3faccfdc42fa6eb81a9e8efdcc70e4a72179ee3c14881b5365c",
  "resource_url": "https://raw.githubusercontent.com/Vicomtech/NUBes-negation-uncertainty-biomedical-corpus/91c81c1f5eee2b5b9d377cc78c2442e8e8b198a1/NUBes/SAMPLE-001/sample-001.sugen.chico.ann",
  "source_id": "nubes",
  "source_url": "https://github.com/Vicomtech/NUBes-negation-uncertainty-biomedical-corpus",
  "split": "SAMPLE-001_no_official_patient_split",
  "upstream_group": "1f9152695bbd9facaa7b8162f8809294fad4e89805fe381a331545c133839c91",
  "upstream_id": "nubes__NUBes_SAMPLE-001_sample-001.sugen.chico.ann:R29",
  "version": "91c81c1f5eee2b5b9d377cc78c2442e8e8b198a1"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[否定与不确定状态](../tasks/assertion_scope.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
