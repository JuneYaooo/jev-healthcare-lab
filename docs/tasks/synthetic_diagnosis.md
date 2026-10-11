# 病例诊断选择：模拟病例子集

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 方向适合，但与临床病例候选诊断同属诊断选择；建议合并为任务下的数据来源分层，保留模拟性质。

本页为来源子集，统一并入 [病例诊断选择](diagnosis.md) 计分，不另增加任务权重。

## 任务是什么

给定 DDXPlus 观察到的症状与背景，从完整病种表选择模拟主诊断。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `synthetic_diagnosis` |
| 医疗场景 | 诊断与鉴别 |
| 能力维度 | 临床候选方案 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [DDXPlus](../datasets/ddxplus.md) | 100 | [原始来源](https://doi.org/10.6084/m9.figshare.20043374) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

本轮各模型使用相同题目进行测试；完整计时与失败明细见 [模型对比](../MODEL_RESULTS.md)。

## 模型结果

以下为合并后的病例诊断任务成绩，两个来源子集共 200 题；逐来源结果保存在评分文件中。

有效回答表示返回合法选项，不代表正确；平均值和分位数包含已启动题目的失败耗时。任务总秒为含并发调度的墙钟时间，不是单题耗时之和。响应链接包含该模型全部题目，可按本页任务的题目 ID 查找。

加粗表示本任务的最高准确率或最短用时；按显示精度并列时同时加粗，全部相同则不标记。

| 模型 | 准确率 ↑ | 有效回答 / 题数 | 平均秒 ↓ | P50 秒 ↓ | P95 秒 ↓ | 任务总秒 ↓ | 超时 / 请求失败 / 无效回答 | 原始记录 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JEV 1.13 | 79.50% | 200 / 200 | 1.047 | 0.990 | 1.377 | 26.649 | 0 / 0 / 0 | [配置](../../results/clinical-v1/jev-1.13.0/config.json) · [响应](../../results/clinical-v1/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-v1/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | **84.00%** | 200 / 200 | **0.586** | **0.473** | **0.777** | **24.209** | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-flash/config.json) · [响应](../../results/clinical-v1/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | 81.00% | 200 / 200 | 0.994 | 0.961 | 1.323 | 25.291 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-v4-pro/config.json) · [响应](../../results/clinical-v1/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 66.00% | 200 / 200 | 1.283 | 0.821 | 4.233 | 33.379 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.5-9b/config.json) · [响应](../../results/clinical-v1/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 77.00% | 200 / 200 | 3.025 | 2.486 | 6.496 | 76.025 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.8-27b/config.json) · [响应](../../results/clinical-v1/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.8-27b/scores.json) |

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

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：d0 2 题、d1 2 题、d10 2 题、d11 2 题、d13 3 题、d14 2 题、d15 2 题、d16 3 题、d17 2 题、d18 2 题、d2 2 题、d20 2 题、d21 2 题、d22 2 题、d23 2 题、d24 2 题、d25 2 题、d26 2 题、d27 2 题、d28 2 题、d29 2 题、d3 3 题、d30 2 题、d31 2 题、d32 2 题、d33 3 题、d34 2 题、d35 2 题、d36 2 题、d37 2 题、d38 2 题、d39 2 题、d4 2 题、d40 2 题、d41 2 题、d42 2 题、d43 2 题、d44 2 题、d45 2 题、d46 3 题、d47 3 题、d48 2 题、d5 2 题、d6 2 题、d7 2 题、d8 2 题、d9 2 题。

**[DDXPlus](../datasets/ddxplus.md)**：模拟器生成症状与诊断，不是实际病历。 答案依据：PATHOLOGY 为模拟主诊断；不把 differential distribution 当患者结局。

其中 100 题材料或片段命中过往评测指纹；训练效果对比应核查材料暴露，并对各模型冻结相同子集。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/synthetic_diagnosis/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/synthetic_diagnosis/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
