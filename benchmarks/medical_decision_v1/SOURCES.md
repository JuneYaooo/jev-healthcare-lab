# 数据来源与引用

各来源分别保留其数据许可；本仓库代码的 MIT 许可不改变题目材料的许可。`research_noncommercial` 为研究/非商业附加部分，不计入默认开放许可核心分数。

## ACI-Bench

来源：[发布方](https://github.com/microsoft/clinical_visit_note_summarization_corpus)。

引用：Microsoft / Yim et al. (2023)，[论文/项目](https://www.nature.com/articles/s41597-023-02487-3)。

数据许可：[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)；分发类别：`open`。

材料性质：合成就诊会话与人工文书；不是自然发生的医院记录。

答案依据：沿用人工文书的章节标题；去除标题后作分类。

许可与来源快照：[aci_bench__LICENSE](sources/aci_bench/aci_bench__LICENSE)、[LICENSE](sources/aci_bench/LICENSE)、[aci_bench__README.md](sources/aci_bench/aci_bench__README.md)、[README.md](sources/aci_bench/README.md)。

## MedQuAD

来源：[发布方](https://github.com/abachaa/MedQuAD)。

引用：Abacha and Demner-Fushman (2019)，[论文/项目](https://doi.org/10.1016/j.jbi.2019.103217)。

数据许可：[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)；分发类别：`open`。

材料性质：NIH 旗下网站信息形成的问题；不属于真实患者问诊。

答案依据：原 XML 的 question qtype 元数据；不评价原答案临床正确性。

许可与来源快照：[LICENSE.txt](sources/medquad/LICENSE.txt)、[readme.txt](sources/medquad/readme.txt)。

## MEDEC-MS

来源：[发布方](https://github.com/abachaa/MEDEC)。

引用：Abacha et al. (2025)，[论文/项目](https://aclanthology.org/2025.findings-acl.1159/)。

数据许可：[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)；分发类别：`open`。

材料性质：MedQA 考试病例改编与专家错误注入；未使用 UW 受控病历。

答案依据：原始 Error Flag 与 Error Sentence ID；原文和更正文均不作模型参考答案。

许可与来源快照：[README.md](sources/medec/README.md)、[medec__README.md](sources/medec/medec__README.md)。

## MedErrBench CN

来源：[发布方](https://github.com/congboma/MedErrBench)。

引用：Ma et al., MedErrBench (2026)，[论文/项目](https://arxiv.org/abs/2602.05692)。

数据许可：[MIT](https://opensource.org/license/mit)；分发类别：`open`。

材料性质：考试病例改编及专家补充，不声称全部是原始病历。

答案依据：发布方 reviewed_data_CN_test 的错误标记和句子标记。

许可与来源快照：[mederr__README.md](sources/mederr/mederr__README.md)、[mederr__LICENSE](sources/mederr/mederr__LICENSE)。

## NUBes SAMPLE-001

来源：[发布方](https://github.com/Vicomtech/NUBes-negation-uncertainty-biomedical-corpus)。

引用：Lima Lopez, Perez, Cuadros and Rigau (2020)，[论文/项目](https://aclanthology.org/2020.lrec-1.708/)。

数据许可：[CC-BY-SA-3.0-ES](https://creativecommons.org/licenses/by-sa/3.0/es/)；分发类别：`open`。

材料性质：西班牙语脱敏临床句子；句子打乱，不能据文件恢复患者。

答案依据：只用双标注及仲裁的 SAMPLE-001；作用域关系映射为否定/不确定。

许可与来源快照：[nubes__LICENSE](sources/nubes/nubes__LICENSE)、[nubes__README.md](sources/nubes/nubes__README.md)。

## DDI Corpus 2013

来源：[发布方](https://github.com/isegura/DDICorpus)。

引用：Herrero-Zazo, Segura-Bedmar, Martinez and Declerck (2013)，[论文/项目](https://doi.org/10.1016/j.jbi.2013.07.011)。

数据许可：[CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/)；分发类别：`research_noncommercial`。

材料性质：DrugBank / MEDLINE 文本，不是患者处方。

答案依据：沿用公开测试集药物实体对及 ddi/type 标签。

许可与来源快照：[ddi__README](sources/ddi/ddi__README)。

## LongHealth

来源：[发布方](https://github.com/kbressem/LongHealth)。

引用：Bressem et al., LongHealth，[论文/项目](https://github.com/kbressem/LongHealth)。

数据许可：[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0)；分发类别：`open`。

材料性质：20 个虚构患者；100 道题不是 100 个患者。

答案依据：沿用发布问题、五个选项和 correct 字段。

许可与来源快照：[longhealth__README.md](sources/longhealth/longhealth__README.md)、[longhealth__LICENSE](sources/longhealth/longhealth__LICENSE)。

## MedCalc-Bench GitHub test release

来源：[发布方](https://github.com/ncbi-nlp/MedCalc-Bench)。

引用：Khandekar et al. (2024)，[论文/项目](https://arxiv.org/abs/2406.12036)。

数据许可：[CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/)；分发类别：`open`。

材料性质：文献提取、生成后人工编辑、模板混合；逐题保留 Note Type。

答案依据：原测试 CSV Ground Truth Answer；完整整数范围作为候选，不由答案生成干扰项。

许可与来源快照：[README.md](sources/medcalc/README.md)、[medcalc__github_README.md](sources/medcalc/medcalc__github_README.md)。

## SciFact

来源：[发布方](https://github.com/allenai/scifact)。

引用：Wadden et al. (2020)，[论文/项目](https://aclanthology.org/2020.emnlp-main.609/)。

数据许可：[CC-BY-4.0 AND ODC-By-1.0](https://github.com/allenai/scifact/blob/master/LICENSE.md)；分发类别：`open`。

材料性质：科学论文摘要，不全是临床医学。

答案依据：原始 claim evidence 标签；无该文证据标注记为未标注支持或反驳。

许可与来源快照：[LICENSE.md](sources/scifact/LICENSE.md)、[README.md](sources/scifact/README.md)。

## Chia

来源：[发布方](https://doi.org/10.6084/m9.figshare.11855817)。

引用：Kury et al. (2020)，[论文/项目](https://doi.org/10.1038/s41597-020-00620-0)。

数据许可：[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)；分发类别：`open`。

材料性质：真实 Phase IV 试验入排标准；无患者临床记录。

答案依据：医学专业人员的 BRAT 实体与关系；只转换已有标签，不合成患者。

许可与来源快照：[figshare-metadata.json](sources/chia/figshare-metadata.json)。

## Clinical Trial Parser annotated test data

来源：[发布方](https://github.com/facebookresearch/Clinical-Trial-Parser)。

引用：Tseo, Salkola, Mohamed, Kumar and Abnousi (2020)，[论文/项目](https://arxiv.org/abs/2006.07296)。

数据许可：[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0)；分发类别：`open`。

材料性质：真实试验条件，公开测试文本经过规范化，数字替换为 @NUMBER。

答案依据：专业标注员 upper_bound/lower_bound；这里只判断方向，不做数值推理。

许可与来源快照：[frd__LICENSE](sources/frd/frd__LICENSE)、[frd__README.md](sources/frd/frd__README.md)、[frd__data_README.md](sources/frd/frd__data_README.md)。

## TrialGPT SIGIR

来源：[发布方](https://github.com/ncbi-nlp/TrialGPT)。

引用：Jin et al., Matching Patients to Clinical Trials with Large Language Models，[论文/项目](https://github.com/ncbi-nlp/TrialGPT)。

数据许可：[LicenseRef-NCBI-Public-Domain](https://github.com/ncbi-nlp/TrialGPT/blob/main/LICENSE)；分发类别：`open`。

材料性质：患者题设配真实试验文件；不是实际入组结局。

答案依据：SIGIR 公开 relevance 0/1/2；0 不相关、1 可能转介、2 高度适合转介。

许可与来源快照：[trialgpt__LICENSE](sources/trialgpt/trialgpt__LICENSE)、[trialgpt__README.md](sources/trialgpt/trialgpt__README.md)。

## DDXPlus

来源：[发布方](https://doi.org/10.6084/m9.figshare.20043374)。

引用：Fansi Tchango et al. (2022)，[论文/项目](https://arxiv.org/abs/2205.09148)。

数据许可：[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)；分发类别：`open`。

材料性质：模拟器生成症状与诊断，不是实际病历。

答案依据：PATHOLOGY 为模拟主诊断；不把 differential distribution 当患者结局。

许可与来源快照：[ddxplus__README.md](sources/ddxplus/ddxplus__README.md)、[README.md](sources/ddxplus/README.md)、[figshare-metadata.json](sources/ddxplus/figshare-metadata.json)。

## TCM-SD

来源：[发布方](https://github.com/borororo/zy-bert)。

引用：Ren et al. (2022)，[论文/项目](https://aclanthology.org/2022.ccl-1.80/)。

数据许可：[CC-BY-NC-SA-4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)；分发类别：`research_noncommercial`。

材料性质：发布论文称真实临床记录；不评价疗效。

答案依据：原始 norm_syndrome；不使用病名/证型字段作为输入。

许可与来源快照：[tcm_sd__README.md](sources/tcm_sd/tcm_sd__README.md)。

## IMCS-21

来源：[发布方](https://github.com/lemuria-wchen/imcs21)。

状态：仅引用，未收录题目。未发现明确数据许可

## MeDAL

来源：[发布方](https://github.com/McGill-NLP/medal)。

状态：仅引用，未收录题目。Zenodo v4 与原 README 明确指向 NLM 条款，部分 PubMed 摘要仍可能受第三方版权保护。不能将模型/代码 MIT 或 Apache 许可当作全部摘要数据开放许可；本轮留空。

核验日期：2026-10-10；结论：原文授权未闭合。

[发布证据](https://zenodo.org/records/4482922)；许可：NLM 使用条款；部分原摘要可能另有版权。

材料性质：医学摘要经缩写替换形成的消歧材料，不是标准术语临床映射金标。

答案依据：缩写与原展开词对应；需要独立固定词表及上游版权核验。

## CMedCalc-Bench

来源：[发布方](https://github.com/Zhihong-Zhu/CMedCalc-Bench)。

状态：仅引用，未收录题目。公开仓库未见明确数据许可；原文与合成混合

## MedJourney

来源：[发布方](https://github.com/Medical-AI-Learning/MedJourney)。

状态：仅引用，未收录题目。未见明确数据许可；部分任务共用 CMB/CMExam 上游

## CDrugRed

来源：[发布方](https://arxiv.org/abs/2511.06230)。

状态：仅引用，未收录题目。下载入口与官方数据包许可链待核验

## TRIAGE

来源：[发布方](https://github.com/NLie2/Triage)。

状态：仅引用，未收录题目。公开数据未见明确许可，87病例的提示变体不当作独立病例

## THYME

来源：[发布方](https://github.com/stylerw/thymedata)。

状态：仅引用，未收录题目。标注公开不等于临床原文开放，原文需数据协议

## n2c2/i2b2

来源：[发布方](https://n2c2.dbmi.hms.harvard.edu/data-sets)。

状态：仅引用，未收录题目。需要相应数据使用协议，不纳入公开题目

## openFDA drug labels

来源：[发布方](https://open.fda.gov/apis/drug/label/)。

状态：仅引用，未收录题目。可作规则材料，尚无对应患者判断题与金标

## MedMCQA

来源：[发布方](https://github.com/medmcqa/medmcqa)。

状态：仅引用，未收录题目。需要逐题筛选临床情境与任务类型，核对数据卡与仓库划分数量差异；不混入纯知识记忆题。

核验日期：2026-10-10；结论：需任务筛选。

[发布证据](https://huggingface.co/datasets/openlifescienceai/medmcqa)；许可：Apache-2.0（发布数据卡）；GitHub 代码 MIT。

材料性质：考试题与原选项答案；不是真实临床结局。

答案依据：已有单选金标，但按科目划分，不直接提供诊断/检查/治疗决策标签。

## PMR-Bench Reddit Test Pairs

来源：[发布方](https://arxiv.org/abs/2601.13178)。

状态：仅引用，未收录题目。论文 §3.2.1 明确：Reddit 等级由 GPT-5 根据医生回复推导，再配对；并非逐对医生直接标注。本轮保留研究引用，不作为人工金标补入。

核验日期：2026-10-10；结论：弱标签，暂未纳入。

[发布证据](https://arxiv.org/html/2601.13178v1)；许可：CC-BY-NC-4.0。

材料性质：患者自述消息的比较；不能称为医院急诊真实分诊记录。

答案依据：1,502 个官方测试对；chosen/rejected 来自模型推导等级。医生直接配对标注属于另一个 PMR-Synth 子集，不能混称。

## TriageBench（Wong，一致性探针）

来源：[发布方](https://github.com/wongqihan/triagebench)。

状态：仅引用，未收录题目。仅作另行设计的一致性附加实验，不填分诊正确性主任务。

核验日期：2026-10-10；结论：不纳入主集。

[发布证据](https://huggingface.co/datasets/wongqihan/triagebench)；许可：MIT。

材料性质：同一神经症状题设的属性/语言变体。

答案依据：发布方明确只测一致性、不声称临床正确；不能当正确性金标。

## PhysioNet Challenge 2019

来源：[发布方](https://physionet.org/content/challenge-2019/1.0.0/)。

引用：Reyna et al. (2019), Early Prediction of Sepsis From Clinical Data: The PhysioNet/Computing in Cardiology Challenge 2019; PhysioNet v1.0.0, doi:10.13026/v64v-d857.，[论文/项目](https://doi.org/10.1097/CCM.0000000000004145)。

数据许可：[CC-BY-4.0](https://physionet.org/content/challenge-2019/view-license/1.0.0/)；分发类别：`open`。

材料性质：真实 ICU 小时记录；只使用公开训练医院 A 中按固定哈希预选的 1,000 个来源记录，非官方隐藏测试。

答案依据：原 SepsisLabel 提前 6 小时。首次 1 所在小时加 6 得到挑战定义起病小时。要求完整 ICU 第 1–12 小时，随访至起病或第 24 小时；排除起始即阳性、12 小时内起病、非法序列及随访不足。只给前 12 小时，预测 (12,24] 小时起病。

许可与来源快照：[LICENSE.txt](sources/sepsis2019/LICENSE.txt)、[source-page.html](sources/sepsis2019/source-page.html)、[preselection.json](sources/sepsis2019/preselection.json)、[selection_frame.json](sources/sepsis2019/selection_frame.json)。

评测范围：本子集仅有 11 个阳性、89 个阴性；恒答阴性准确率为 89%，应同时报告两类召回。来源是公开训练医院 A，不能对训练过该库的模型声称盲测。选择框为 1,000 例，合格 528 例（11 阳性/517 阴性）；分层抽样改变了类别比例，不用于风险校准、临床患病率或 PPV 估计。推算起病和原挑战逐小时 utility 不等价。

## CLIP 出院行动标注

来源：[发布方](https://physionet.org/content/mimic-iii-clinical-action/1.0.0/)。

状态：仅引用，未收录题目。需凭证、培训及 DUA；只能在获准环境适配，不公开转发原文。

核验日期：2026-10-10；结论：受控访问。

[发布证据](https://doi.org/10.13026/kw00-z903)；许可：PhysioNet Credentialed Health Data License 1.5.0。

材料性质：MIMIC-III 出院记录，部分脱敏占位替换为合成信息。

答案依据：医生标注的行动片段与类别；Patient Instructions 部分依章节规则标注。

## MIMIC-IV-ED

来源：[发布方](https://physionet.org/content/mimic-iv-ed/2.2/)。

状态：仅引用，未收录题目。需凭证与 DUA；构建入院分诊任务时必须排除出院诊断、去向等未来信息。

核验日期：2026-10-10；结论：受控访问。

[发布证据](https://physionet.org/content/mimic-iv-ed/2.2/)；许可：PhysioNet Credentialed Health Data License。

材料性质：真实急诊就诊资料，含分诊、生命体征及出院诊断等表。

答案依据：分诊 acuity 可作为原记录标签；出院诊断是后验信息。

## MedNLI

来源：[发布方](https://physionet.org/content/mednli/1.0.0/)。

状态：仅引用，未收录题目。需凭证及 DUA；不从公开镜像绕过原始访问条件。

核验日期：2026-10-10；结论：受控访问。

[发布证据](https://doi.org/10.13026/C2RS98)；许可：PhysioNet Credentialed Health Data License 1.5.0。

材料性质：MIMIC-III 病历前提配临床医生撰写的推论。

答案依据：entailment/contradiction/neutral 三分类医生标签。

## CT-ADE-SOC / CT-ADE-PT

来源：[发布方](https://github.com/ds4dh/CT-ADE)。

状态：仅引用，未收录题目。核对数据版本和外部术语条件，按 NCT/试验组隔离；不良事件频率与标签不能作为输入。

核验日期：2026-10-10；结论：需预测协议。

[发布证据](https://huggingface.co/datasets/anthonyyazdaniml/CT-ADE-SOC)；许可：MIT（SOC 数据卡）；第三方术语与补充源需单独核验。

材料性质：临床试验组层面的单药与不良事件数据。

答案依据：ClinicalTrials.gov 结果派生的多标签结局；不是个体药物因果或禁忌标签。

## MACCROBAT2020

来源：[发布方](https://doi.org/10.6084/m9.figshare.9764942.v2)。

引用：Caufield et al., MACCROBAT (2019/2020)，[论文/项目](https://doi.org/10.6084/m9.figshare.c.4652765.v1)。

数据许可：[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)；分发类别：`open`。

材料性质：公开发表的临床病例报告；原病例被编辑整理，不等同医院原始 EHR。

答案依据：原始 BRAT MODIFY 关系；把事件引用解析为文本实体，只保留目标检查/药物唯一的关联。

许可与来源快照：[figshare-metadata.json](sources/maccrobat/figshare-metadata.json)。

## CMB-Exam（中文病例单选子集）

来源：[发布方](https://github.com/FreedomIntelligence/CMB)。

引用：Wang et al., CMB (NAACL 2024)，[论文/项目](https://arxiv.org/abs/2308.08833)。

数据许可：[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0)；分发类别：`open`。

材料性质：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。

答案依据：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 v0.4.0 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

许可与来源快照：[LICENSE](sources/cmb/LICENSE)、[README.md](sources/cmb/README.md)、[HF_DATA_CARD.md](sources/cmb/HF_DATA_CARD.md)。

## CNMLEQA-10k（中文案例分析子集）

来源：[发布方](https://doi.org/10.5281/zenodo.18951465)。

引用：Zong et al., Scientific Data (2026)，[论文/项目](https://doi.org/10.1038/s41597-026-07261-9)。

数据许可：[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)；分发类别：`open`。

材料性质：中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。

答案依据：只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 v0.4.0 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

许可与来源快照：[zenodo-metadata.json](sources/cnmleqa/zenodo-metadata.json)、[README.md](sources/cnmleqa/README.md)。

## CMExam

来源：[发布方](https://github.com/williamliujl/CMExam)。

状态：仅引用，未收录题目。Apache 标识与 README 学术/研究限制并存，先澄清数据授权范围；病例题也需筛选。

核验日期：2026-10-10；结论：许可范围待澄清。

[发布证据](https://github.com/williamliujl/CMExam)；许可：Apache-2.0（仓库）；README 另限学术/研究使用。

材料性质：中文医考题，不是病历。

答案依据：测试 CSV 有原答案及疾病、科室、能力等标注。

## CBLUE（KUAKE-QIC / CHIP-CTC / CHIP-CDN）

来源：[发布方](https://github.com/CBLUEbenchmark/CBLUE)。

状态：仅引用，未收录题目。不能用代码许可替代数据许可；需取得官方数据包及其协议，核验开发集答案，CDN 候选术语表还需核对许可。

核验日期：2026-10-10；结论：需官方数据条款。

[发布证据](https://github.com/CBLUEbenchmark/CBLUE)；许可：Apache-2.0（代码）；天池数据包协议待核验。

材料性质：医疗搜索问题、试验标准及诊断术语，材料性质分任务。

答案依据：QIC 为意图分类，CTC 为 44 类标准；CDN 为诊断归一化。公开测试通常不带答案，可研究开发集。

## PromptCBLUE

来源：[发布方](https://github.com/michael-wzhu/PromptCBLUE)。

状态：仅引用，未收录题目。优先回到 CBLUE 原任务核验许可和划分；不把模板改写当独立来源或独立病例，不纳入生成子任务。

核验日期：2026-10-10；结论：衍生来源待核验。

[发布证据](https://github.com/michael-wzhu/PromptCBLUE)；许可：未核验到覆盖全部上游数据的独立分发许可。

材料性质：CBLUE 等任务的指令化衍生集合。

答案依据：部分分类任务可恢复有限标签；其余为抽取/生成。

## MLEC-QA

来源：[发布方](https://github.com/Judenpech/MLEC-QA)。

状态：仅引用，未收录题目。需下载官方包核对独立数据许可、测试划分和共享题干；仅收病例决策单选。

核验日期：2026-10-10；结论：下载包待核验。

[发布证据](https://github.com/Judenpech/MLEC-QA)；许可：MIT（代码）；下载包数据许可待核验。

材料性质：中文执业医师考试题，包含共享病例题干。

答案依据：公开说明含题型、选项和答案；官方入口为 Google Drive。

## RJUA-MedDQA

来源：[发布方](https://github.com/AQ-MedAI/medDQA_benchmark)。

状态：仅引用，未收录题目。仓库目前给示例、README 仍称完整集将发布；需核验完整下载、OCR 对齐和单选金标，若采用只入非商业附加集。

核验日期：2026-10-10；结论：完整数据入口待核验。

[发布证据](https://github.com/AQ-MedAI/medDQA_benchmark)；许可：CC-BY-NC-SA-4.0（数据）；AGPL（代码）。

材料性质：泌尿科真实报告影像及专家标注，发布方声明。

答案依据：含报告数值推理及临床推理单选，也有自由回答。

## MedXpertQA

来源：[发布方](https://github.com/TsinghuaC3I/MedXpertQA)。

状态：仅引用，未收录题目。论文附录提出不在线分享题例；在与 MIT 数据卡的适用范围澄清前仅引用，不在本仓库再分发题目。

核验日期：2026-10-10；结论：发布条件待澄清。

[发布证据](https://proceedings.mlr.press/v267/zuo25a.html)；许可：MIT（数据卡）；论文另要求不在线分享题例。

材料性质：专家复核的医学考试改写题；分 Text 与 MM。

答案依据：原选项、label、medical_task、question_type 可用；Diagnosis 标签也含检查选择，需再细分。

## MedHallu

来源：[发布方](https://github.com/MedHallu/MedHallu)。

状态：仅引用，未收录题目。官方代码与论文已定位；完整数据下载及上游摘要许可待核验，只考虑错误判别，不收生成任务。

核验日期：2026-10-10；结论：数据与标签质量待核验。

[发布证据](https://github.com/MedHallu/MedHallu)；许可：MIT（项目）；PubMedQA 等上游材料需核验。

材料性质：论文问答上自动构造的正确/幻觉答案；不是真实临床错误。

答案依据：二分类适配可能可行，但生成标签不等于逐条医生审核。

## MedEthicEval

来源：[发布方](https://github.com/X-LANCE/MedEthicEval)。

状态：仅引用，未收录题目。需明确数据再分发许可和违规类别答案，只考虑有明确标签的违规识别；不收开放伦理解释。

核验日期：2026-10-10；结论：数据许可待明确。

[发布证据](https://github.com/X-LANCE/MedEthicEval)；许可：公开仓库未见明确数据许可证。

材料性质：中文医疗伦理知识、违规场景与伦理两难。

答案依据：违规识别可作分类；平衡两难不应强行产生唯一答案。

## RD-Triage

来源：[发布方](https://github.com/zhelishisongjie/RD-Triage)。

状态：仅引用，未收录题目。优先核对上游来源许可与 PMID、单标签数量和诊断泄露；论文尚在审稿，适用范围为罕见病。

核验日期：2026-10-10；结论：优先核验分诊候选。

[发布证据](https://github.com/zhelishisongjie/RD-Triage)；许可：MIT（仓库）；RareBench 等上游条款待核验。

材料性质：罕见病病例报告/表型改编的初诊科室分流。

答案依据：629 条、固定 30 科室；部分题有多个可接受科室，不能只保留其中一个。

## ClinicalMC / ClinicalMPD

来源：[发布方](https://github.com/hzyuezh/ClinicalMPD)。

状态：仅引用，未收录题目。只研究可封闭计分的子任务，需核验发布数据、许可及逐时点信息边界，不能把完整住院信息泄漏给早期决策。

核验日期：2026-10-10；结论：工作流候选待核验。

[发布证据](https://arxiv.org/abs/2606.03157)；许可：仓库未见明确数据许可证；上游 MedEureka / PMC-Patients 需核验。

材料性质：发布论文称 1,275 中文、5,804 英文多病程样本。

答案依据：科室分流可作有限选择；检查、诊断、治疗等多为开放生成和评判。

## CARE-MI

来源：[发布方](https://github.com/Meetyou-AI-Lab/CARE-MI)。

状态：仅引用，未收录题目。仅研究真假判别子集及人工标签；代码样例不足以认定完整可用，不收自由生成部分。

核验日期：2026-10-10；结论：完整数据及许可待核验。

[发布证据](https://github.com/Meetyou-AI-Lab/CARE-MI)；许可：Apache-2.0（代码）；完整数据及上游许可待核验。

材料性质：母婴领域知识与题库衍生，包含自动生成的真假陈述。

答案依据：论文有专家审核与真假题，但主要评价长回答；README 仍称完整集后续发布。

## CT-EBM-SP v3

来源：[发布方](https://github.com/lcampillos/ct-ebm-sp-v3)。

引用：Campillos-Llanos et al.; CSIC，[论文/项目](https://github.com/lcampillos/ct-ebm-sp-v3)。

数据许可：[CC-BY-NC-SA-4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)；分发类别：`research_noncommercial`。

材料性质：西班牙语试验注册文本与期刊摘要；不是患者就诊记录。

答案依据：使用 brat/test 原始人工属性和关系；频次与剂型关联另外使用 brat/dev，逐题保留划分。实体片段或关联目标有限选择；不导出 UMLS 术语库，不构造未标注负例。

许可与来源快照：[README.md](sources/ct_ebm_sp/README.md)、[LICENSE](sources/ct_ebm_sp/LICENSE)、[annotation.conf](sources/ct_ebm_sp/annotation.conf)。

## E3C English Layer 1

来源：[发布方](https://github.com/hltfbk/E3C-Corpus)。

引用：Magnini et al.; Fondazione Bruno Kessler，[论文/项目](https://e3c.fbk.eu/home)。

数据许可：[CC-BY-NC (publisher does not specify version)](https://github.com/hltfbk/E3C-Corpus/blob/8196181eacd5d65828d324dcc63970c503aff5e9/README.md)；分发类别：`research_noncommercial`。

材料性质：公开病例报道；Layer 1 人工事件与时间标注。保留各文献原作者、DOI、原文许可。

答案依据：仅官方英文测试文档；原 docTimeRel、permanence、TIMEX3 类型及 timexLink 唯一目标机械适配，不使用自动标注层。

许可与来源快照：[README.md](sources/e3c/README.md)、[train_test_split.txt](sources/e3c/train_test_split.txt)。

## CARE-Bench

来源：[发布方](https://github.com/ningkko/CARE-bench)。

引用：CARE-Bench authors / ningkko，[论文/项目](https://arxiv.org/abs/2608.03731)。

数据许可：[CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/)；分发类别：`research_noncommercial`。

材料性质：来源约束的重构咨询轨迹；GPT-5.5 辅助构建后人工审核（发布方说明），不是原始真实分诊记录。

答案依据：只用 public_test_1 的四类 gold_label；只给当前已披露患者消息，不给后续轮次、参考回复、信息充分性和构造标签。

许可与来源快照：[README.md](sources/care_bench/README.md)。

## Diabetes 130-US Hospitals for Years 1999-2008

来源：[发布方](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)。

引用：John Clore, Krzysztof Cios, Jon DeShazo, Beata Strack，[论文/项目](https://doi.org/10.24432/C5230J)。

数据许可：[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)；分发类别：`open`。

材料性质：The dataset represents ten years (1999-2008) of clinical care at 130 US hospitals and integrated delivery networks. Each row concerns hospital records of patients diagnosed with diabetes, who underwent laboratory, medications, and stayed up to 14 days. The goal is to determine the early readmission of the patient within 30 days of discharge.
The problem is important for the following reasons. Despite high-quality evidence showing improved clinical outcomes for diabetic patients who receive various preventive and therapeutic interventions, many patients do not receive them. This can be partially attributed to arbitrary diabetes management in hospital environments, which fail to attend to glycemic control. Failure to provide proper diabetes care not only increases the managing costs for the hospitals (as the patients are readmitted) but also impacts the morbidity and mortality of the patients, who may face complications associated with diabetes.


答案依据：按患者取首个合格住院；出院去向只保留回家 (1)；readmitted <30 为阳性，其他为未观察到 30 日内再入院。输入移除患者 ID、住院 ID 和再入院标签。

许可与来源快照：[metadata.json](sources/uci_diabetes/metadata.json)、[source-page.html](sources/uci_diabetes/source-page.html)。

## Post-Operative Patient

来源：[发布方](https://archive.ics.uci.edu/dataset/82/post+operative+patient)。

引用：Sharon Summers, Linda Woolery，[论文/项目](https://doi.org/10.24432/C5DG6Q)。

数据许可：[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)；分发类别：`open`。

材料性质：Dataset of patient features

答案依据：ADM-DECS 原术后去向标签；相同输入冲突全部排除，无患者 ID，不冒称患者独立。

许可与来源快照：[metadata.json](sources/uci_postoperative/metadata.json)、[source-page.html](sources/uci_postoperative/source-page.html)。

## Heart Failure Clinical Records

来源：[发布方](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records)。

引用：Ahmad et al.; Chicco and Jurman; UCI，[论文/项目](https://doi.org/10.24432/C5Z89R)。

数据许可：[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)；分发类别：`open`。

材料性质：This dataset contains the medical records of 299 patients who had heart failure, collected during their follow-up period, where each patient profile has 13 clinical features.

答案依据：90 日死亡：time<=90 且 DEATH_EVENT=1 为阳性；time>=90 且无此前死亡为阴性；90 日前删失排除。time 与死亡标签不输入。

许可与来源快照：[metadata.json](sources/uci_heart_failure/metadata.json)、[source-page.html](sources/uci_heart_failure/source-page.html)。

## Maternal Health Risk

来源：[发布方](https://archive.ics.uci.edu/dataset/863/maternal+health+risk)。

引用：Marzia Ahmed，[论文/项目](https://doi.org/10.24432/C5DP5D)。

数据许可：[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)；分发类别：`open`。

材料性质：Data has been collected from different hospitals, community clinics, maternal health cares from the rural areas of Bangladesh through the IoT based risk monitoring system.

答案依据：沿用原 RiskLevel，不能当成独立结局随访；完全相同特征冲突全部排除，无患者 ID。

许可与来源快照：[metadata.json](sources/uci_maternal/metadata.json)、[source-page.html](sources/uci_maternal/source-page.html)。

## MTCMB

来源：[发布方](https://github.com/Wayyuanyuan/MTCMB)。

状态：仅引用，未收录题目。主体包含病历/处方/解释生成和实体抽取；不把这些任务计入决策任务数。考试选择题与已有任务同型；病例来源和原始分发条款待进一步核对。

核验日期：2026-10-10；结论：scope_and_upstream_terms_pending。

[发布证据](https://github.com/Wayyuanyuan/MTCMB/blob/faffd813c67fe012cef74277a23270d5dd6db9b8/ReadMe_cn.md)；许可：CC-BY-4.0（发布方 Zenodo 数据声明）；各上游来源仍需核对。

材料性质：教材、医考题库、古籍、专家医案及 CCL/Tianchi 衍生；不能统称自然发生的临床记录。

答案依据：部分为选择题、部分为自由文本或多字段答案；未转换为本次评测题。

## MEDDOCAN / SPACCC

来源：[发布方](https://github.com/PlanTL-GOB-ES/SPACCC_MEDDOCAN)。

引用：Marimon et al. (2019), Automatic De-identification of Medical Texts in Spanish: the MEDDOCAN Track, Corpus, Guidelines, Methods and Evaluation of Results; SEAD / BSC / CNIO.，[论文/项目](https://ceur-ws.org/Vol-2421/MEDDOCAN_overview.pdf)。

数据许可：[CC-BY-4.0](https://raw.githubusercontent.com/PlanTL-GOB-ES/SPACCC_MEDDOCAN/783a6df385c975b328c99bcffb54196a9ba4078a/LICENSE)；分发类别：`open`。

材料性质：西班牙语公开病例报告经筛选、补入合成个人信息；不能视为原始患者身份记录。

答案依据：官方 test BRAT 人工 PHI 片段标注。目标词完全落在标注片段内映射为 yes，完全不重叠映射为 no（闭世界 O 标签）；跨边界目标排除，不生成隐私标识。

许可与来源快照：[README.md](sources/meddocan/README.md)、[LICENSE](sources/meddocan/LICENSE)。

评测范围：仅评估给定词是否落入原 PHI 片段，不是整份文档脱敏召回率。负例沿用完整标注语料的闭世界假设，仍可能受到上游漏标影响。

## CMED / n2c2 2022 Track 1

来源：[发布方](https://n2c2.dbmi.hms.harvard.edu/2022-track-1)。

状态：仅引用，未收录题目。具有启停、变更、时态等原标注，但不具备公开转发临床原文的授权。

核验日期：2026-10-10；结论：本轮核验后留空。

[发布证据](https://n2c2.dbmi.hms.harvard.edu/2022-track-1)；许可：受数据访问与使用协议约束。

材料性质：临床病历中的药物事件。

答案依据：原始药物事件上下文标注；并非开放再分发语料。

## FEBRL record linkage datasets

来源：[发布方](https://recordlinkage.readthedocs.io/en/latest/ref-datasets.html)。

状态：仅引用，未收录题目。公开合成身份匹配基准，不是医疗材料的患者身份核实；缺信息时的不确定标签也未覆盖。

核验日期：2026-10-10；结论：本轮核验后留空。

[发布证据](https://recordlinkage.readthedocs.io/en/latest/ref-datasets.html)；许可：需按原数据条款单独核验；本轮未再分发。

材料性质：生成并扰动的人口学记录。

答案依据：原身份分组可支持同人匹配，不能代表医疗上下文中的可确定性。

## LabQAR

来源：[发布方](https://doi.org/10.6084/m9.figshare.29189894)。

引用：Bhasuran, Jin, Deville et al., A Curated Dataset for Question Answering on Laboratory Test Reference Ranges and Interpretation. Scientific Data (2026); Figshare 29189894 v1.，[论文/项目](https://doi.org/10.1038/s41597-026-07554-z)。

数据许可：[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)；分发类别：`open`。

材料性质：根据专家医学参考资料整理的区间与条件，不是患者记录。仅采用 Set 1 可解析且无冲突的原始范围答案。

答案依据：原 Set 1 范围答案机械映射为同检验、单位、类别的固定候选；输入附上同组原参考条目，考查条件匹配。排除同条件答案冲突、裸数值及无替代范围条目；不生成范围或不确定答案。

许可与来源快照：[LabQAR_README.md](sources/labqar/LabQAR_README.md)、[figshare-metadata.json](sources/labqar/figshare-metadata.json)。

评测范围：仅评估给定参考条目的人群、标本和条件匹配；不是独立诊疗知识或所有实验室范围的正确性。本版 72 题，未覆盖不确定和检验方法差异。

## NLI4CT

来源：[发布方](https://github.com/ai-systems/nli4ct)。

状态：仅引用，未收录题目。数据为试验报告论断的支持/矛盾二分类，缺少患者病历的无法确定类别；不替代当前病历三分类任务。

核验日期：2026-10-10；结论：本轮核验后留空。

[发布证据](https://github.com/ai-systems/nli4ct)；许可：原发布仓库未明确数据再分发许可；不以参与团队代码 MIT 替代。

材料性质：ClinicalTrials.gov 试验材料配专家撰写论断。

答案依据：专家标注二分类，与 MedNLI 的患者病历三分类不同。

## Chinese-medical-dialogue-data

来源：[发布方](https://github.com/Toyhom/Chinese-medical-dialogue-data)。

状态：仅引用，未收录题目。科室字段是采集来源的分类，未证明为临床审核的最佳首诊科室；不能直接作分流金标。

核验日期：2026-10-10；结论：本轮核验后留空。

[发布证据](https://github.com/Toyhom/Chinese-medical-dialogue-data)；许可：仓库 MIT；原问诊内容授权链未核实。

材料性质：中文在线医疗问答汇编，原平台逐条溯源不足。

答案依据：含 department/title/question/answer；没有独立首诊分流正确性审核。

## FHIR R4 clinical workflow definitions

来源：[发布方](https://hl7.org/fhir/R4/)。

状态：仅引用，未收录题目。可定义诊断核实、标本链、操作及报告状态；标准示例不等于独立临床金标数据集。

核验日期：2026-10-10；结论：本轮核验后留空。

[发布证据](https://hl7.org/fhir/R4/)；许可：标准文档许可；不是病例标注集。

材料性质：互操作标准及示例。

答案依据：字段与枚举定义，无本项目目标的独立题目答案集。

## UCUM unit specification

来源：[发布方](https://ucum.org/ucum)。

状态：仅引用，未收录题目。提供单位语义与换算标准；本轮未找到符合医疗数值等价判断的独立标注题集。

核验日期：2026-10-10；结论：本轮核验后留空。

[发布证据](https://ucum.org/ucum)；许可：UCUM 原使用条款；非临床病例数据许可。

材料性质：单位编码标准及规则。

答案依据：标准公式可用于将来自建规则测试，不能冒称已有临床评测金标。

## MIMIC-IV Clinical Database Demo v2.2

来源：[发布方](https://physionet.org/content/mimic-iv-demo/2.2/)。

状态：仅引用，未收录题目。开放结构化演示数据可作开发材料；本轮未建立覆盖开单、配药、给入、未执行的独立证据与金标协议。不能把已有状态字段原样放进输入再要求选择同一字段。

核验日期：2026-10-10；结论：本轮核验后留空。

[发布证据](https://physionet.org/content/mimic-iv-demo/2.2/)；许可：Open Data Commons Open Database License v1.0（以发布页为准）。

材料性质：真实去标识临床数据库演示子集。

答案依据：原事件记录字段不自动构成完整临床流程判断题。
