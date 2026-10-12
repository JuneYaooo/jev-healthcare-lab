# 病例诊断选择

[返回首页](../../README.md) · [临床主评测任务](README.md)

根据给定病例资料，从候选中选择诊断。考试病例与模拟病例作为同一个评测任务的来源子集；题目和原答案保留，不因拆分来源重复增加任务权重。

共 200 题。合并后按全部题目计算任务准确率，并保留每个来源子集的结果。选项含义随题变化，不计算临床类别 F1。

| 来源子集与完整样例 | 题数 |
| --- | --- |
| [病例诊断选择：模拟病例子集](../tasks/synthetic_diagnosis.md) | 100 |
| [病例诊断选择：考试病例子集](../tasks/diagnosis_choice.md) | 100 |

## 样例与来源

两个来源子集的说明页分别给出完整输入、原选项、标准答案和溯源。以下为考试病例子集中的一题：

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`diagnosis_choice:cmb:9865`；语种：中文；来源组：`zh_exam_case:462c68717b08a15194bac182`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "肠结核",
        "B": "溃疡性结肠炎",
        "C": "克罗恩病",
        "D": "结肠癌",
        "E": "结肠息肉"
      },
      "instructions": "从给定诊断候选中选择最符合病例者。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "男性，36岁。黏液脓血便1年，无发热，常伴里急后重。查体：左下腹轻压痛，未触及包块。胸部X线检查：未见异常。最可能的诊断是"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `B`，对应选项：

```json
"溃疡性结肠炎"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "diagnosis_choice:cmb:9865", "choice": "B"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/FreedomIntelligence/CMB/6c8ece46097dae736c6805dd3b831e1a38c08971/data/CMB.zip) · [数据集说明](../datasets/cmb.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "Apache-2.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "answer_field": "answer",
    "answer_json_index": 9864,
    "json_index": 9864,
    "question_id": 9865,
    "supporting_resources": [
      "cmb__CMB-test-choice-answer.json"
    ],
    "zip_member": "CMB/CMB-Exam/CMB-test/CMB-test-choice-question-merge.json"
  },
  "material_kind": "medical_examination_vignettes",
  "resource": "cmb__CMB.zip",
  "resource_sha256": "c2e4288127fa5e6c03cc3659d893b0bbb19e699f74fdadce8e7fa10ac5bfdd94",
  "resource_url": "https://raw.githubusercontent.com/FreedomIntelligence/CMB/6c8ece46097dae736c6805dd3b831e1a38c08971/data/CMB.zip",
  "source_id": "cmb",
  "source_url": "https://github.com/FreedomIntelligence/CMB",
  "split": "official_test",
  "upstream_group": "9865",
  "upstream_id": "9865",
  "version": "6c8ece46097dae736c6805dd3b831e1a38c08971"
}
```

## 模型结果

两个诊断来源合并为 200 题。有效回答不代表答对；任务总秒为墙钟时间，单题平均值与分位数包含失败耗时。响应链接包含该模型全部题目。

加粗表示本任务的最高准确率或最短用时；按显示精度并列时同时加粗，全部相同则不标记。

| 模型 | 准确率 ↑ | 有效回答 / 题数 | 平均秒 ↓ | P50 秒 ↓ | P95 秒 ↓ | 任务总秒 ↓ | 超时 / 请求失败 / 无效回答 | 原始记录 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JEV 1.13 | 79.50% | 200 / 200 | 1.047 | 0.990 | 1.377 | 26.649 | 0 / 0 / 0 | [配置](../../results/clinical-v1/jev-1.13.0/config.json) · [响应](../../results/clinical-v1/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-v1/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | **84.00%** | 200 / 200 | **0.586** | **0.473** | **0.777** | **24.209** | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-flash/config.json) · [响应](../../results/clinical-v1/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | 81.00% | 200 / 200 | 0.994 | 0.961 | 1.323 | 25.291 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-v4-pro/config.json) · [响应](../../results/clinical-v1/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 66.00% | 200 / 200 | 1.283 | 0.821 | 4.233 | 33.379 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.5-9b/config.json) · [响应](../../results/clinical-v1/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 77.00% | 200 / 200 | 3.025 | 2.486 | 6.496 | 76.025 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.8-27b/config.json) · [响应](../../results/clinical-v1/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.8-27b/scores.json) |

[完整得分、耗时与运行条件](../MODEL_RESULTS.md)

## 多问题与并发性能

固定本任务 32 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。

取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。

表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。

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

## 评测边界

考试病例与模拟病例分别报告，不能把模拟患者当成真实患者。候选数量与题型不同，比较模型时冻结同一批题目和选项。

[返回首页](../../README.md)
