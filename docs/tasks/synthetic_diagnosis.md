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

## 多问题与并发性能

### 持续多题并发

本轮每请求 8 题，同时配置 8／32／64 个工作器；每个工作器收到完整响应后立即补入下一包。每档预热 5 秒，再统计 30 秒，重复两轮。固定 32 道原题循环施压，重放不增加独立医学样本数。

双方最高可比档为 32 并发，但仅第 1 轮均完整完成，以下为该轮观察，尚不能确认稳定优势。JEV 每秒返回 86.4 个合法判断，Flash 为 166.4；准确率分别为 81.25%、82.15%。该档有请求缺少用量，完整成本暂不能比较。

| 配置并发 | 模型 | 判断／秒 ↑ | 准确率 ↑ | 含排队 P95 秒 ↓ | 美元／千次正确 ↓ | 纳入轮次 |
| --- | --- | --- | --- | --- | --- | --- |
| 8 | JEV 1.13 | 85.3 | 81.25% | 0.860 | 0.0515 | 1/2 |
| 8 | Flash | 72.4 | 82.47% | 1.159 | 待核算 | 1/2 |
| 32 | JEV 1.13 | 86.4 | 81.25% | 4.153 | 0.0515 | 1/2 |
| 32 | Flash | 166.4 | 82.15% | 4.327 | 待核算 | 1/2 |
| 64 | JEV 1.13 | 85.7 | 81.25% | 6.165 | 0.0515 | 2/2 |
| 64 | Flash | 未纳入 | 未纳入 | 未纳入 | 未纳入 | 0/2 |

判断／秒只计合法选项，不代表全部答对。准确率按原题等权，失败和非法选项计错；P95 包含发出前的配额排队及收到完整结果的时间。单位成本包含答错消耗，缺少用量标为待核算。配置并发包含配额排队，实际在途并发见详细结果。

[持续负载协议](../SUSTAINED_THROUGHPUT.md) · [逐档实际并发、完整包率和失败](../../results/sustained-throughput-v1/README.md) · [原始响应与配置](../../results/sustained-throughput-v1/archive_manifest.json)

### 历史有限批次测试

以下记录把多题与并发分别测试，只处理有限的一组题，不能用作持续高吞吐证据。

固定本任务 32 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。

取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。

表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。

历史多题结果（固定最大打包档，对比 Flash）：JEV 81.25%，Flash 85.42%；JEV 耗时少 13.9%；取决于 Flash 闲时／高峰价格。具体准确率与费用仅对应下述性能子集，不代表全量成绩或其他调用方式。

| 模式 | 并发 | 每请求实际题数 | 模型 | 准确率 | 整组平均秒 | 有效 / 正确决策每秒 | 完整包 / 请求 | 失败或无效请求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 | 1 | 1 | JEV 1.13 | 80.21% | 9.474 | 3.38 / 2.71 | 96 / 96 | 0 |
| 逐题 | 1 | 1 | DeepSeek V4.1 Flash | 90.62% | 20.742 | 1.54 / 1.40 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | JEV 1.13 | 82.29% | 1.651 | 19.38 / 15.95 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | DeepSeek V4.1 Flash | 90.62% | 3.125 | 10.24 / 9.28 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | JEV 1.13 | 81.25% | 1.839 | 17.40 / 14.14 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | DeepSeek V4.1 Flash | 90.62% | 1.414 | 22.63 / 20.51 | 96 / 96 | 0 |
| 多题打包 | 1 | 8 | JEV 1.13 | 81.25% | 1.321 | 24.22 / 19.68 | 12 / 12 | 0 |
| 多题打包 | 1 | 8 | DeepSeek V4.1 Flash | 84.38% | 3.302 | 9.59 / 8.18 | 11 / 12 | 1 |
| 多题打包 | 1 | 8–24 | JEV 1.13 | 81.25% | 1.566 | 20.44 / 16.60 | 6 / 6 | 0 |
| 多题打包 | 1 | 8–24 | DeepSeek V4.1 Flash | 85.42% | 1.819 | 17.59 / 15.03 | 6 / 6 | 0 |

<details>
<summary>重复波动、请求耗时、失败与原始响应</summary>

| 模式 | 模型 | 整组秒范围 | 请求 P50 秒 | 请求 P95 秒 | 最长请求秒 | 429 | 请求失败 / 超时 / 无效 | 原始响应 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 8.683–10.692 | 0.270 | 0.560 | 0.692 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-129.jsonl) · [轮2](../../results/task-performance-v1/cell-277.jsonl) · [轮3](../../results/task-performance-v1/cell-585.jsonl) |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 19.973–21.262 | 0.658 | 0.860 | 1.177 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-081.jsonl) · [轮2](../../results/task-performance-v1/cell-423.jsonl) · [轮3](../../results/task-performance-v1/cell-629.jsonl) |
| 逐题 B≤1 / C8 | JEV 1.13 | 1.402–2.112 | 0.301 | 0.924 | 0.983 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-212.jsonl) · [轮2](../../results/task-performance-v1/cell-285.jsonl) · [轮3](../../results/task-performance-v1/cell-640.jsonl) |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 2.871–3.321 | 0.679 | 1.019 | 1.291 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-057.jsonl) · [轮2](../../results/task-performance-v1/cell-403.jsonl) · [轮3](../../results/task-performance-v1/cell-664.jsonl) |
| 逐题 B≤1 / C32 | JEV 1.13 | 1.594–2.124 | 0.610 | 1.500 | 2.113 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-010.jsonl) · [轮2](../../results/task-performance-v1/cell-303.jsonl) · [轮3](../../results/task-performance-v1/cell-667.jsonl) |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 0.854–2.021 | 0.847 | 1.801 | 2.020 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-064.jsonl) · [轮2](../../results/task-performance-v1/cell-327.jsonl) · [轮3](../../results/task-performance-v1/cell-671.jsonl) |
| 多题打包 B≤8 / C1 | JEV 1.13 | 1.103–1.727 | 0.283 | 样本不足 | 0.607 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-019.jsonl) · [轮2](../../results/task-performance-v1/cell-314.jsonl) · [轮3](../../results/task-performance-v1/cell-522.jsonl) |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 3.085–3.579 | 0.768 | 样本不足 | 1.504 | 0 | 0 / 0 / 1 | [轮1](../../results/task-performance-v1/cell-204.jsonl) · [轮2](../../results/task-performance-v1/cell-443.jsonl) · [轮3](../../results/task-performance-v1/cell-583.jsonl) |
| 多题打包 B≤32 / C1 | JEV 1.13 | 1.423–1.849 | 0.888 | 样本不足 | 0.960 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-085.jsonl) · [轮2](../../results/task-performance-v1/cell-360.jsonl) · [轮3](../../results/task-performance-v1/cell-700.jsonl) |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 1.497–1.984 | 0.776 | 样本不足 | 1.359 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-053.jsonl) · [轮2](../../results/task-performance-v1/cell-442.jsonl) · [轮3](../../results/task-performance-v1/cell-676.jsonl) |

请求耗时包含完整接收与校验，不含客户端排队；整组耗时包含排队。少于 20 次请求不展示 P95。

</details>

<details>
<summary>每千次正确决策成本</summary>

| 模式 | 模型 | 估算 USD / 千次正确决策 | 缺用量请求 |
| --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 0.0622 | 0 |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 0.0366–0.0731 | 0 |
| 逐题 B≤1 / C8 | JEV 1.13 | 0.0607 | 0 |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 0.0366–0.0731 | 0 |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.0614 | 0 |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 0.0366–0.0731 | 0 |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.0515 | 0 |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 0.0294–0.0588 | 0 |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.0507 | 0 |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 0.0381–0.0762 | 0 |

按归档价目与实际 usage 估算；Flash 含缓存命中与输出费用，区间对应闲时至高峰价格。缺用量时不填完整单位成本，非账单费用。

</details>

连接池显式预热并跨单元复用，网络与供应商缓存仍会影响结果；各模式是有限批次测试，不能外推持续服务容量。[完整协议](../TASK_PERFORMANCE.md) · [冻结题目](../../benchmarks/task_performance_v1/README.md) · [运行配置](../../results/task-performance-v1/config.json)

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
