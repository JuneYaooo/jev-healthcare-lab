# Jev 医疗场景评测

覆盖 **12 类医疗场景、96 项任务、6,586 条测试输入**，了解 Jev 适合做哪些医疗工作、表现怎样、使用成本多高。DeepSeek Flash 作为同题参考。

## 先看结论

- **信息分类是目前更值得尝试的方向。** 医疗实体类型识别、病历章节归类、患者问题分类的正确率为 96%–99%；相较 DeepSeek，分数接近或更高，模型调用费用低约 39%–56%，适合优先试用在批量整理和分流环节。
- **长病历中的指定问题回答，也显示出较好的性价比。** 在 100 道给定完整病历的选择题上，Jev 正确率为 95%，DeepSeek 为 83%；Jev 的调用费用低约 68%。这一结果对应指定问题回答，整份病历的自动总结仍需另行验证。
- **复杂医疗判断仍有明显短板。** 试验入组判断正确率 48%、临床量表数值判断 25%、中医证型判断 33%；这些任务即使调用便宜，也不足以支持自动决策。

## 哪些工作更值得优先试用？

以下任务兼具较好的答对率和较低的调用费用。费用按每千条同类输入估算，单位为美元。

| 具体工作 | 测试题数 | Jev 正确率 | DeepSeek 正确率 | 每千条费用：Jev / DeepSeek |
| --- | ---: | ---: | ---: | ---: |
| [给已圈出的症状、药品等信息分类](scenarios/records/imcs_entity_type_oracle_span/README.md) | 100 | 96.0% | 92.0% | $0.019 / $0.031 |
| [把已分段的病历内容归入对应章节](scenarios/documentation/aci_note_section/README.md) | 100 | 99.0% | 100.0% | $0.021 / $0.048 |
| [把患者提问分为症状、病因等类别](scenarios/service/medquad_question_type/README.md) | 100 | 96.0% | 97.0% | $0.020 / $0.034 |
| [根据完整长病历回答指定选择题](scenarios/records/longhealth_full_context/README.md) | 100 | 95.0% | 83.0% | $0.537 / $1.697 |

## 其他医疗工作表现怎样？

下表展示各场景中的具体测试。正确率表示答对比例；抽取综合分兼顾漏检和误报，满分 100。每行代表一个任务，不能当作整个场景的平均水平。

| 医疗工作与测试内容 | 题数 | Jev | DeepSeek | 适用范围 |
| --- | ---: | ---: | ---: | --- |
| [病历信息整理：从中文句子中找出医疗实体](scenarios/records/imcs_ner_dictionary_pipeline/README.md) | 100 | 59.5 分·抽取综合分 | 59.2 分·抽取综合分 | 同时看漏检和误报 |
| [病历质控：发现病历中的医学错误](scenarios/quality/medec_error_detection/README.md) | 100 | 65.0% 正确率 | 60.0% 正确率 | 不能只看总体分，还要看漏错 |
| [回答核查：结合参考证据识别医学回答幻觉](scenarios/quality/medhallu_with_evidence/README.md) | 200 | 82.0% 正确率 | 82.5% 正确率 | 已提供证据，不含联网检索 |
| [药物信息：筛选出院带药候选](scenarios/medication/cdrugred_discharge_candidate_pipeline/README.md) | 100 | 48.6 分·抽取综合分 | 47.9 分·抽取综合分 | 不是可直接用于处方的验证 |
| [临床试验：初筛患者是否适合某个试验](scenarios/trials/trialgpt_sigir_referral/README.md) | 150 | 48.0% 正确率 | 54.7% 正确率 | 还需人工逐条核对纳排标准 |
| [医学研究：识别研究人群、干预和结局片段](scenarios/evidence/ebm_pico_fixed_windows/README.md) | 100 | 12.7 分·抽取综合分 | 25.4 分·抽取综合分 | 评测固定文本窗口，不是全文综述 |
| [临床评分：从病历判断五种量表的数值](scenarios/calculators/medcalc_verified_bounded_score/README.md) | 100 | 25.0% 正确率 | 31.0% 正确率 | 未提供公式，不能外推所有计算器 |
| [医学知识：回答中文医学选择题](scenarios/knowledge/medqa_zh_test/README.md) | 100 | 89.0% 正确率 | 84.0% 正确率 | 考试成绩不等于临床诊断能力 |
| [语音病历：从语音转写中判断病史字段](scenarios/multimodal/primock_asr_fields/README.md) | 12 | 91.7% 正确率 | 91.7% 正确率 | 只有一段扮演患者音频、12 个字段 |
| [病例判断：为合成病例选择主要诊断](scenarios/acute/ddxplus_synthetic_primary/README.md) | 100 | 67.0% 正确率 | 71.0% 正确率 | 合成病例，不是真实临床诊断 |
| [中医辨证：从中医病例中选择证型](scenarios/tcm/tcm_syndrome/README.md) | 100 | 33.0% 正确率 | 40.0% 正确率 | 候选共 148 个证型及无法判断选项 |

## 花多少钱，等多久？

按全部测试输入合计，Jev 的模型调用费用比 DeepSeek **低约 56%**。具体能否节省业务成本，还取决于该任务的准确率和人工复核量。

| 对比项 | Jev | DeepSeek Flash |
| --- | ---: | ---: |
| 每千条输入的模型调用费用 | $0.057 | $0.130 |
| 成功请求的典型等待（中位数） | 0.75 秒 | 0.55 秒 |

费用为美元估算，仅含模型调用，不含文档识别、语音转写、系统接入和人工复核；一条输入不等于一份完整病历。等待时间来自两批实际记录，非同期测速，仅供参考。

## 覆盖哪些医疗场景？

共 72 项公开数据任务和 24 项自编边界测试。点击场景可查看全部任务，点击任务可查看测试数据、方法和结果。

| 场景 | 具体测试数 | 输入记录数 |
| --- | ---: | ---: |
| [病历实体、否定状态与术语标准化](scenarios/records/README.md) | 18 | 1,128 |
| [病历章节、文书质控与随访记录](scenarios/documentation/README.md) | 5 | 212 |
| [患者咨询、服务路由与就医流程](scenarios/service/README.md) | 9 | 708 |
| [医疗质控、幻觉识别与请求安全](scenarios/quality/README.md) | 11 | 1,109 |
| [药物关系、用药变更与出院带药](scenarios/medication/README.md) | 7 | 366 |
| [患者入组预筛与临床试验匹配](scenarios/trials/README.md) | 3 | 350 |
| [循证研究、PICO 与公共卫生核查](scenarios/evidence/README.md) | 10 | 859 |
| [临床计算、参数选择与评分量表](scenarios/calculators/README.md) | 8 | 514 |
| [医学知识与考试对照](scenarios/knowledge/README.md) | 5 | 400 |
| [语音病历、医疗文档 OCR 与报告断言](scenarios/multimodal/README.md) | 5 | 40 |
| [合成病例主要诊断](scenarios/acute/README.md) | 1 | 100 |
| [中医知识、辨证与安全](scenarios/tcm/README.md) | 14 | 800 |
| **合计** | **96** | **6,586** |

[完整任务结果](docs/完整任务统计.md) · [对比实验详情](comparisons/deepseek-flash/README.md)
