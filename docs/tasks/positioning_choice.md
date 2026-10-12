# 护理与操作体位选择

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 方向适合，仅 10 题，覆盖病情和操作两类情境；作为护理子类。

## 任务是什么

根据患者病情或操作情境，从原始选项中选择合适体位。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `positioning_choice` |
| 医疗场景 | 住院与护理 |
| 能力维度 | 分类与标准化 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 10 / 100 |
| 来源组数 | 10 |
| 语种 | 中文 10 题 |
| 数据范围 | 开放许可部分 10 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CMB-Exam（中文病例单选子集）](../datasets/cmb.md) | 8 | [原始来源](https://github.com/FreedomIntelligence/CMB) |
| [CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md) | 2 | [原始来源](https://doi.org/10.5281/zenodo.18951465) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

本轮各模型使用相同题目进行测试；完整计时与失败明细见 [模型对比](../MODEL_RESULTS.md)。

## 模型结果

以下成绩使用本页全部已收录题目；耗时包括请求、响应处理及重试等待。

有效回答表示返回合法选项，不代表正确；平均值和分位数包含已启动题目的失败耗时。任务总秒为含并发调度的墙钟时间，不是单题耗时之和。响应链接包含该模型全部题目，可按本页任务的题目 ID 查找。

加粗表示本任务的最高准确率或最短用时；按显示精度并列时同时加粗，全部相同则不标记。

| 模型 | 准确率 ↑ | 有效回答 / 题数 | 平均秒 ↓ | P50 秒 ↓ | P95 秒 ↓ | 任务总秒 ↓ | 超时 / 请求失败 / 无效回答 | 原始记录 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JEV 1.13 | **90.00%** | 10 / 10 | 0.985 | 0.851 | 2.045 | 2.051 | 0 / 0 / 0 | [配置](../../results/clinical-v1/jev-1.13.0/config.json) · [响应](../../results/clinical-v1/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-v1/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | 80.00% | 10 / 10 | **0.474** | **0.479** | **0.608** | **0.963** | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-flash/config.json) · [响应](../../results/clinical-v1/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | **90.00%** | 10 / 10 | 0.740 | 0.679 | 0.946 | 1.592 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-v4-pro/config.json) · [响应](../../results/clinical-v1/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 60.00% | 10 / 10 | 0.967 | 0.760 | 3.377 | 3.954 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.5-9b/config.json) · [响应](../../results/clinical-v1/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 70.00% | 10 / 10 | 1.409 | 1.493 | 1.819 | 2.289 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.8-27b/config.json) · [响应](../../results/clinical-v1/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.8-27b/scores.json) |

## 多问题与并发性能

本轮多题结果（固定最大打包档，对比 Flash）：JEV 100.00%，Flash 73.33% ⚠；JEV 耗时多 0.6%；JEV 成本低 23.8%–61.9%。具体准确率与费用仅对应下述性能子集，不代表全量成绩或其他调用方式。

固定本任务 10 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。

取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。

表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。

**小样本任务：** 重复运行只观察性能波动，不增加独立题目数，不能据此稳定估计临床准确率或尾延迟。

| 模式 | 并发 | 每请求实际题数 | 模型 | 准确率 | 整组平均秒 | 有效 / 正确决策每秒 | 完整包 / 请求 | 失败或无效请求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 | 1 | 1 | JEV 1.13 | 93.33% | 2.635 | 3.80 / 3.54 | 30 / 30 | 0 |
| 逐题 | 1 | 1 | DeepSeek V4.1 Flash | 80.00% | 6.564 | 1.52 / 1.22 | 30 / 30 | 0 |
| 逐题 | 8 | 1 | JEV 1.13 | 90.00% | 0.775 | 12.91 / 11.62 | 30 / 30 | 0 |
| 逐题 | 8 | 1 | DeepSeek V4.1 Flash | 80.00% | 1.297 | 7.71 / 6.17 | 30 / 30 | 0 |
| 逐题 | 10 | 1 | JEV 1.13 | 96.67% | 0.704 | 14.21 / 13.74 | 30 / 30 | 0 |
| 逐题 | 10 | 1 | DeepSeek V4.1 Flash | 80.00% | 0.869 | 11.51 / 9.21 | 30 / 30 | 0 |
| 多题打包 | 1 | 2–8 | JEV 1.13 | 100.00% | 1.001 | 9.99 / 9.99 | 6 / 6 | 0 |
| 多题打包 | 1 | 2–8 | DeepSeek V4.1 Flash | 80.00% | 1.492 | 6.70 / 5.36 | 6 / 6 | 0 |
| 多题打包 | 1 | 10 | JEV 1.13 | 100.00% | 0.861 | 11.62 / 11.62 | 3 / 3 | 0 |
| 多题打包 | 1 | 10 | DeepSeek V4.1 Flash | 73.33% | 0.856 | 11.29 / 8.57 | 2 / 3 | 1 |

<details>
<summary>重复波动、请求耗时、失败与原始响应</summary>

| 模式 | 模型 | 整组秒范围 | 请求 P50 秒 | 请求 P95 秒 | 最长请求秒 | 429 | 请求失败 / 超时 / 无效 | 原始响应 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 2.368–2.955 | 0.241 | 0.310 | 0.737 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-023.jsonl) · [轮2](../../results/task-performance-v1/cell-361.jsonl) · [轮3](../../results/task-performance-v1/cell-602.jsonl) |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 6.157–7.348 | 0.615 | 1.046 | 1.563 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-130.jsonl) · [轮2](../../results/task-performance-v1/cell-328.jsonl) · [轮3](../../results/task-performance-v1/cell-693.jsonl) |
| 逐题 B≤1 / C8 | JEV 1.13 | 0.477–1.010 | 0.266 | 0.816 | 0.833 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-030.jsonl) · [轮2](../../results/task-performance-v1/cell-457.jsonl) · [轮3](../../results/task-performance-v1/cell-605.jsonl) |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 1.201–1.413 | 0.660 | 0.801 | 0.803 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-094.jsonl) · [轮2](../../results/task-performance-v1/cell-317.jsonl) · [轮3](../../results/task-performance-v1/cell-501.jsonl) |
| 逐题 B≤1 / C10 | JEV 1.13 | 0.285–0.963 | 0.306 | 0.952 | 0.962 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-082.jsonl) · [轮2](../../results/task-performance-v1/cell-409.jsonl) · [轮3](../../results/task-performance-v1/cell-563.jsonl) |
| 逐题 B≤1 / C10 | DeepSeek V4.1 Flash | 0.798–0.979 | 0.619 | 0.915 | 0.974 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-145.jsonl) · [轮2](../../results/task-performance-v1/cell-332.jsonl) · [轮3](../../results/task-performance-v1/cell-553.jsonl) |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.620–1.457 | 0.380 | 样本不足 | 0.974 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-216.jsonl) · [轮2](../../results/task-performance-v1/cell-239.jsonl) · [轮3](../../results/task-performance-v1/cell-478.jsonl) |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 1.341–1.668 | 0.806 | 样本不足 | 0.862 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-009.jsonl) · [轮2](../../results/task-performance-v1/cell-439.jsonl) · [轮3](../../results/task-performance-v1/cell-642.jsonl) |
| 多题打包 B≤10 / C1 | JEV 1.13 | 0.234–1.410 | 0.939 | 样本不足 | 1.410 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-193.jsonl) · [轮2](../../results/task-performance-v1/cell-467.jsonl) · [轮3](../../results/task-performance-v1/cell-690.jsonl) |
| 多题打包 B≤10 / C1 | DeepSeek V4.1 Flash | 0.640–1.227 | 0.701 | 样本不足 | 1.227 | 0 | 0 / 0 / 1 | [轮1](../../results/task-performance-v1/cell-060.jsonl) · [轮2](../../results/task-performance-v1/cell-433.jsonl) · [轮3](../../results/task-performance-v1/cell-611.jsonl) |

请求耗时包含完整接收与校验，不含客户端排队；整组耗时包含排队。少于 20 次请求不展示 P95。

</details>

<details>
<summary>每千次正确决策成本</summary>

| 模式 | 模型 | 估算 USD / 千次正确决策 | 缺用量请求 |
| --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 0.0210 | 0 |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 0.0440–0.0880 | 0 |
| 逐题 B≤1 / C8 | JEV 1.13 | 0.0218 | 0 |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 0.0440–0.0880 | 0 |
| 逐题 B≤1 / C10 | JEV 1.13 | 0.0203 | 0 |
| 逐题 B≤1 / C10 | DeepSeek V4.1 Flash | 0.0440–0.0880 | 0 |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.0125 | 0 |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 0.0209–0.0419 | 0 |
| 多题打包 B≤10 / C1 | JEV 1.13 | 0.0113 | 0 |
| 多题打包 B≤10 / C1 | DeepSeek V4.1 Flash | 0.0149–0.0298 | 0 |

按归档价目与实际 usage 估算；Flash 含缓存命中与输出费用，区间对应闲时至高峰价格。缺用量时不填完整单位成本，非账单费用。

</details>

连接池显式预热并跨单元复用，网络与供应商缓存仍会影响结果；各模式是有限批次测试，不能外推持续服务容量。[完整协议](../TASK_PERFORMANCE.md) · [冻结题目](../../benchmarks/task_performance_v1/README.md) · [运行配置](../../results/task-performance-v1/config.json)

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`positioning_choice:cmb:upstream_train_reserved_for_local_evaluation:113165`；语种：中文；来源组：`zh_exam_case:c34600e68c86f5a8608f2e51`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "俯卧位",
        "B": "坐位",
        "C": "立位",
        "D": "患侧卧位",
        "E": "健侧卧位"
      },
      "instructions": "根据患者病情或操作情境，从原始选项中选择合适体位。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "男性，23岁。午后低热、盗汗1个月，少量咯血半日。体检：肩胛间区可闻及少许湿啰音。经治疗未好转，出现中等量咯血，此时最恰当的体位是"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `D`，对应选项：

```json
"患侧卧位"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "positioning_choice:cmb:upstream_train_reserved_for_local_evaluation:113165", "choice": "D"}
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
    "json_index": 113165,
    "zip_member": "CMB/CMB-Exam/CMB-train/CMB-train-merge.json"
  },
  "material_kind": "medical_examination_vignettes",
  "resource": "cmb__CMB.zip",
  "resource_sha256": "c2e4288127fa5e6c03cc3659d893b0bbb19e699f74fdadce8e7fa10ac5bfdd94",
  "resource_url": "https://raw.githubusercontent.com/FreedomIntelligence/CMB/6c8ece46097dae736c6805dd3b831e1a38c08971/data/CMB.zip",
  "source_id": "cmb",
  "source_url": "https://github.com/FreedomIntelligence/CMB",
  "split": "upstream_train_reserved_for_local_evaluation",
  "upstream_group": "c34600e68c86f5a8608f2e51",
  "upstream_id": "upstream_train_reserved_for_local_evaluation:113165",
  "version": "6c8ece46097dae736c6805dd3b831e1a38c08971"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：B 3 题、C 1 题、D 2 题、E 2 题、opa 1 题、opd 1 题。

当前可用题目不足目标数量，保留实际题量；比较细小差异时须同时报告样本数。

**[CMB-Exam（中文病例单选子集）](../datasets/cmb.md)**：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。 答案依据：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

**[CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md)**：中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。 答案依据：只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/positioning_choice/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/positioning_choice/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
