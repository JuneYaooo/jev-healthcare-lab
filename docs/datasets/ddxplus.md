# DDXPlus

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

模拟器生成症状与诊断，不是实际病历。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `ddxplus` |
| 上游入口 | [发布方页面](https://doi.org/10.6084/m9.figshare.20043374) |
| 收录情况 | 100 题 / 1 个任务 |
| 使用范围 | 开放许可核心集 |
| 登记的数据许可 | CC-BY-4.0 |
| 收录语种 | 英语 100 题 |

## 来源与引用

Fansi Tchango et al. (2022)

[论文或项目引用](https://arxiv.org/abs/2205.09148) · [数据许可](https://creativecommons.org/licenses/by/4.0/)

许可与说明快照：[ddxplus__README.md](../../benchmarks/medical_decision_v1/sources/ddxplus/ddxplus__README.md) · [README.md](../../benchmarks/medical_decision_v1/sources/ddxplus/README.md) · [figshare-metadata.json](../../benchmarks/medical_decision_v1/sources/ddxplus/figshare-metadata.json)

## 用于哪些任务

| 任务说明 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- |
| [模拟病例主诊断选择](../tasks/synthetic_diagnosis.md) | 100 | 给定 DDXPlus 观察到的症状与背景，从完整病种表选择模拟主诊断。 |

## 答案与格式转换

PATHOLOGY 为模拟主诊断；不把 differential distribution 当患者结局。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`synthetic_diagnosis:ddxplus:108735`；语种：英语；来源组：`ddxplus:108735`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "d0": "Acute COPD exacerbation / infection",
        "d1": "Acute dystonic reactions",
        "d10": "Boerhaave",
        "d11": "Bronchiectasis",
        "d12": "Bronchiolitis",
        "d13": "Bronchitis",
        "d14": "Bronchospasm / acute asthma exacerbation",
        "d15": "Chagas",
        "d16": "Chronic rhinosinusitis",
        "d17": "Cluster headache",
        "d18": "Croup",
        "d19": "Ebola",
        "d2": "Acute laryngitis",
        "d20": "Epiglottitis",
        "d21": "GERD",
        "d22": "Guillain-Barré syndrome",
        "d23": "HIV (initial infection)",
        "d24": "Influenza",
        "d25": "Inguinal hernia",
        "d26": "Larygospasm",
        "d27": "Localized edema",
        "d28": "Myasthenia gravis",
        "d29": "Myocarditis",
        "d3": "Acute otitis media",
        "d30": "PSVT",
        "d31": "Pancreatic neoplasm",
        "d32": "Panic attack",
        "d33": "Pericarditis",
        "d34": "Pneumonia",
        "d35": "Possible NSTEMI / STEMI",
        "d36": "Pulmonary embolism",
        "d37": "Pulmonary neoplasm",
        "d38": "SLE",
        "d39": "Sarcoidosis",
        "d4": "Acute pulmonary edema",
        "d40": "Scombroid food poisoning",
        "d41": "Spontaneous pneumothorax",
        "d42": "Spontaneous rib fracture",
        "d43": "Stable angina",
        "d44": "Tuberculosis",
        "d45": "URTI",
        "d46": "Unstable angina",
        "d47": "Viral pharyngitis",
        "d48": "Whooping cough",
        "d5": "Acute rhinosinusitis",
        "d6": "Allergic sinusitis",
        "d7": "Anaphylaxis",
        "d8": "Anemia",
        "d9": "Atrial fibrillation"
      },
      "instructions": "给定 DDXPlus 观察到的症状与背景，从完整病种表选择模拟主诊断。",
      "type": "choice"
    }
  },
  "state": {
    "age": 4,
    "observed_evidence": [
      {
        "question": "Have you or any member of your family ever had croup?",
        "value": "present"
      },
      {
        "question": "Do you have nasal congestion or a clear runny nose?",
        "value": "present"
      },
      {
        "question": "Does the person have a whooping cough?",
        "value": "present"
      },
      {
        "question": "Have you traveled out of the country in the last 4 weeks?",
        "value": "N"
      },
      {
        "question": "Are your vaccinations up to date?",
        "value": "present"
      }
    ],
    "sex": "F"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `d18`，对应选项：

```json
"Croup"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "synthetic_diagnosis:ddxplus:108735", "choice": "d18"}
```

### 样例溯源

[上游资源](https://ndownloader.figshare.com/files/40495565) · [数据集说明](../datasets/ddxplus.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "csv_row": 108736,
    "zip_member": "release_test_patients"
  },
  "material_kind": "simulated_patients",
  "resource": "ddxplus__release_test_patients.zip",
  "resource_sha256": "ad3bb981f3453fd7abffb35cc595a1c02197e409c581bff97c1265c33eb00d23",
  "resource_url": "https://ndownloader.figshare.com/files/40495565",
  "source_id": "ddxplus",
  "source_url": "https://doi.org/10.6084/m9.figshare.20043374",
  "split": "official_test",
  "upstream_group": "108735",
  "upstream_id": "108735",
  "version": "figshare:20043374.v15"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[模拟病例主诊断选择](../tasks/synthetic_diagnosis.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
