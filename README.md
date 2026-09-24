# Jev 在医疗任务中表现如何？

这份对比帮助医疗机构、医疗产品团队和行业从业者判断：**Jev 能做好哪些工作，和 DeepSeek 相比准不准、快不快、花多少钱。**

## 先看结论

- **Jev 在部分明确、范围小的判断任务上表现较好。** 已分段病历的章节分类正确率 99%，已给定实体的类型识别 96%，给定完整长病历的选择题 95%。这些结果支持进一步做场景验证，不能当作整份病历处理准确率。
- **入组判断、复杂抽取和临床评分仍不可靠。** 患者与试验适配三分类正确率 48%，五种量表数值判断 25%，研究要素抽取综合分 12.7/100；这些任务目前不能直接交给 Jev 自动决策。
- **同题对比中，Jev 在更多任务上得分更高。** 72 项公开数据测试中，Jev 更高 39 项，DeepSeek 更高 27 项，持平 6 项。不同任务不能混成一个“医疗总准确率”。
- **费用和速度要分开看。** 这批题每千条 API 费用约为 Jev $0.057、DeepSeek $0.130，Jev 费用约低 56%；典型等待分别为 0.75 秒和 0.55 秒。下面列出具体口径。

## Jev 与 DeepSeek：效果、等待时间、费用

两者使用同一批 **6,586 条输入**，覆盖 **12 类医疗工作、96 项具体测试**。其中 72 项来自公开数据，24 项为自编小样本边界测试；上面的胜负统计只使用前 72 项。

| 对比项 | Jev 1.13 | DeepSeek V4.1 Flash（非思考模式） |
| --- | ---: | ---: |
| 得分更高的公开数据任务 | 39 / 72 | 27 / 72 |
| 最终未能按要求作答的输入 | 0 | 29 |
| 成功请求典型等待：一半在此时间内完成 | 0.75 秒 | 0.55 秒 |
| 每千条输入的 API 费用估算 | $0.057 | $0.130 |
| 这批 6,586 条输入的 API 费用估算 | $0.376 | $0.853 |

**怎么看时间和费用**：时间是成功请求从发出到收到完整回答的网络等待，失败尝试和重试前的等待不计入中位数，Jev 来自历史真实记录，DeepSeek 为本次调用，**不是同期测速**。费用按实际 token 用量和官方价格估算，以美元统一列示；DeepSeek 包含实际缓存命中折扣。每条输入可能是一段文本、一道题或一个字段，**不是一份完整病历**；费用不包含 OCR、语音识别、人工复核和系统接入。

DeepSeek 的旧名 `deepseek-v4-flash` 已转接到 V4.1 Flash，本表使用实际提供服务的版本。两者接收相同内容和问题，输出格式按各自接口适配。未能作答的输入仍计入评分，不从题数中删除；完整计分方法、失败记录及用量见 [对比实验详情](comparisons/deepseek-flash/README.md)。

## 放到具体医疗工作里，表现怎样？

下表为事先选定的代表任务，不是各场景平均分。**正确率**表示有多少题答对；**抽取综合分**同时衡量漏检和误报，满分 100，不能当作正确率。

| 医疗工作 | 测了什么 | 题数 | Jev | DeepSeek | 读结果时注意 |
| --- | --- | ---: | ---: | ---: | --- |
| 病历信息整理 | [识别已圈出的症状、药品等实体类型](scenarios/records/imcs_entity_type_oracle_span/README.md) | 100 | 96.0% 正确率 | 92.0% 正确率 | 这里只判断类型，实体位置已给出 |
| 病历信息整理 | [从中文句子中找出医疗实体](scenarios/records/imcs_ner_dictionary_pipeline/README.md) | 100 | 59.5 分·抽取综合分 | 59.2 分·抽取综合分 | 同时看漏检和误报 |
| 文书归档 | [判断文本属于哪一类病历章节](scenarios/documentation/aci_note_section/README.md) | 100 | 99.0% 正确率 | 100.0% 正确率 | 章节边界已给出，不是自动写病历 |
| 患者咨询 | [判断患者在问症状、病因还是其他信息](scenarios/service/medquad_question_type/README.md) | 100 | 96.0% 正确率 | 97.0% 正确率 | 评测问题分类，不是回复质量 |
| 病历质控 | [发现病历中的医学错误](scenarios/quality/medec_error_detection/README.md) | 100 | 65.0% 正确率 | 60.0% 正确率 | 不能只看总体分，还要看漏错 |
| 回答核查 | [结合参考证据识别医学回答幻觉](scenarios/quality/medhallu_with_evidence/README.md) | 200 | 82.0% 正确率 | 82.5% 正确率 | 已提供证据，不含联网检索 |
| 药物信息 | [筛选出院带药候选](scenarios/medication/cdrugred_discharge_candidate_pipeline/README.md) | 100 | 48.6 分·抽取综合分 | 47.9 分·抽取综合分 | 不是可直接用于处方的验证 |
| 临床试验 | [初筛患者是否适合某个试验](scenarios/trials/trialgpt_sigir_referral/README.md) | 150 | 48.0% 正确率 | 54.7% 正确率 | 还需人工逐条核对纳排标准 |
| 医学研究 | [识别研究人群、干预和结局片段](scenarios/evidence/ebm_pico_fixed_windows/README.md) | 100 | 12.7 分·抽取综合分 | 25.4 分·抽取综合分 | 评测固定文本窗口，不是全文综述 |
| 临床评分 | [从病历判断五种量表的数值](scenarios/calculators/medcalc_verified_bounded_score/README.md) | 100 | 25.0% 正确率 | 31.0% 正确率 | 未提供公式，不能外推所有计算器 |
| 医学知识 | [回答中文医学选择题](scenarios/knowledge/medqa_zh_test/README.md) | 100 | 89.0% 正确率 | 84.0% 正确率 | 考试成绩不等于临床诊断能力 |
| 语音病历 | [从语音转写中判断病史字段](scenarios/multimodal/primock_asr_fields/README.md) | 12 | 91.7% 正确率 | 91.7% 正确率 | 只有一段扮演患者音频、12 个字段 |
| 病例判断 | [为合成病例选择主要诊断](scenarios/acute/ddxplus_synthetic_primary/README.md) | 100 | 67.0% 正确率 | 71.0% 正确率 | 合成病例，不是真实临床诊断 |
| 中医辨证 | [从中医病例中选择证型](scenarios/tcm/tcm_syndrome/README.md) | 100 | 33.0% 正确率 | 40.0% 正确率 | 候选共 148 个证型及无法判断选项 |

## 有哪些场景和测试？

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

点击场景可看全部任务；点击任务可看测试数据、提示词、模型回答、逐项分数和费用。原有的重复调用、选项换序等稳定性测试保留在 [实验统计详情](docs/完整任务统计.md)，不计入本次模型对比分数。

这些是公开数据及人工构造材料上的离线测试，尚未证明医院实际节省了多少工时。选择模型时，应以准备接入的具体工作为准，尤其要核对错误类型和人工复核成本。
