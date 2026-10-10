# Jev Healthcare Lab

按医疗场景组织、可追溯到上游标注的医疗决策评测数据集。给定材料、规则和候选项，输出一个可计分的选择；不包含病历生成、自由问答或建议生成任务。

**v0.6.0：8 个场景，59 个有题任务，共 5,594 题。** 其中 51 个任务各 100 题，8 个任务保留实际可用数量；另有 18 个任务定义暂缺数据。中文共 1,012 题。当前尚未发布模型评测成绩。

## 下载与使用

| 数据包 | 题数 | 许可范围 |
| --- | ---: | --- |
| [开放许可核心集](releases/jev-medical-decision-v0.6.0-open.zip) | 4,051 | 各来源分别保留原许可；包含署名及相同方式共享要求 |
| [非商业研究附加集](releases/jev-medical-decision-v0.6.0-research-noncommercial.zip) | 1,543 | DDI、TCM-SD、E3C、CT-EBM-SP、CARE-Bench；适用原非商业等限制 |

[下载说明与校验和](releases/README.md) · [场景与任务详情](benchmarks/medical_decision_v1/README.md) · [来源、引用与许可](benchmarks/medical_decision_v1/SOURCES.md) · [待补任务的数据调研](benchmarks/medical_decision_v1/SCENARIO_RESEARCH.md) · [中文来源核验](docs/DATASET_EXPANSION.md) · [v0.4.0 扩展与协议](docs/EXPANSION_V040.md) · [v0.5.0 空缺核验与协议](docs/GAP_AUDIT_V050.md) · [v0.6.0 新任务与适配](docs/EXPANSION_V060.md)

每个包包含完整题目、无答案请求、独立答案、逐题溯源、原许可声明和离线工具。解压后执行（Python 3.10+，仅标准库）：

```bash
python3 tools/medical_decision_release.py verify --dataset .
python3 tools/medical_decision_release.py trace --dataset . --id bounded_score:medcalc:489
python3 tools/medical_decision_release.py score --dataset . --predictions predictions.jsonl --output scores.json
```

上面的题号属于开放核心集；每个包的 README 提供该包可用的题号。预测文件一行一条：

```json
{"id":"bounded_score:medcalc:489","choice":"选项键"}
```

模型输入使用 `requests.jsonl` 中的 `request`，不发送答案与来源标注。实际选项键以各题 `questions.decision.criteria` 为准。

## 场景覆盖

| 场景 | 有题任务 / 定义任务 | 题数 |
| --- | ---: | ---: |
| 接诊与分诊 | 4 / 7 | 400 |
| 检查与检验 | 6 / 10 | 556 |
| 诊断与鉴别 | 12 / 13 | 1,200 |
| 治疗与用药 | 11 / 14 | 928 |
| 住院与护理 | 7 / 10 | 610 |
| 出院与随访 | 2 / 4 | 200 |
| 临床试验筛选 | 8 / 8 | 800 |
| 病历与医疗质量控制 | 9 / 11 | 900 |

任务包括信息意图、否定与不确定状态、检查数值关联、药物剂量关联、量表评分、候选诊断、长病历证据选择、试验标准判断和临床错误识别等。场景归属用于组织评测，不表示已经覆盖该场景的完整临床工作流。原能力维度保留为可重叠标签，不重复计入题目总数。

## 来源与答案

题目选自 29 个上游来源，包括 MedQuAD、MedCalc-Bench、MACCROBAT2020、LongHealth、DDXPlus、SciFact、TrialGPT、CHIA 等。每题保留：

- 上游发布地址、论文或项目引用、固定版本及资源 SHA-256；
- 原始记录、行号或标注位置，以及原始数据划分；
- 原答案与机械映射方式、转换代码版本；
- 数据许可、材料性质和来源组；
- 冻结的训练指纹筛查与历史材料重合标记。

溯源链为 **题目 ID → 原始资源与固定版本 → 原文/标注位置 → 答案映射**。独立包的 `provenance.jsonl` 汇总这条链；`trace --fetch-source` 可下载对应源文件并核验哈希。

## 评测与限制

默认只导出和计分开放核心集。先计算每个任务的指标，再对同一场景内的任务等权平均，最后对有题场景等权汇总；空场景记为 `null`。[评测方法](docs/EVALUATION.md) 说明任务指标、缺失回答、分组和训练前后比较方式。

材料包含模拟病例、考试改编、病例报告、指南规则、试验报告和临床文本，不能统称真实患者病历。答案沿用上游标注，尚未经过本项目独立医生逐题审核。全体 5,594 题中，577 题材料或片段命中过往评测指纹；标记可能包含通用片段，不能把本集作为完全未暴露的盲测集。每任务目标 100 题，数量不足的任务为探索性覆盖；这些样本适合初步对照，不能据此确认细小提升或临床有效性。

新增中文病例中有 253 题来自上游公开训练划分，已逐题标记。若模型已用这些题训练，应单独剔除或报告该分层，不能视为盲测。新增脓毒症预测的 100 题也来自上游公开训练医院 A。该任务仅有 11 个阳性，须结合阳性召回查看，不能用总准确率代替预警能力。分诊轨迹、关系标注、考试题和真实记录结局的分数也应分别查看。

## 重建与本地验证

```bash
python3 scripts/medical_decision_dataset.py validate
python3 -m unittest discover -s tests -v
python3 scripts/medical_decision_dataset.py fetch
python3 scripts/medical_decision_dataset.py build
python3 scripts/medical_decision_release.py build
```

详细步骤见 [复建说明](docs/REPRODUCING.md)。`benchmarks/medical_decision_v1/` 路径保持稳定，具体数据版本以 `taxonomy.json` 和数据包 `release.json` 为准。

## 许可

代码采用 [MIT](LICENSE)。第三方数据逐来源保留原许可，代码许可不覆盖题目材料；参见 [第三方声明](THIRD_PARTY_NOTICES.md)、[来源登记](benchmarks/medical_decision_v1/SOURCES.md) 和包内 `LICENSE-DATA.md`。公开可下载与可无限制使用并不等同。
