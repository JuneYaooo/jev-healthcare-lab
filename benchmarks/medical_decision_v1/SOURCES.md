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

状态：仅引用，未收录题目。旧用例只有演示数据，尚未构建独立公开测试子集

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

状态：仅引用，未收录题目。固定消息级隔离和配对位置平衡，核对判定者及意见分歧后抽样；只进非商业附加部分。

核验日期：2026-10-10；结论：需抽样协议。

[发布证据](https://huggingface.co/datasets/PortalPal-AI/PMR-Reddit-Test-Pairs)；许可：CC-BY-NC-4.0。

材料性质：患者自述消息的比较；不能称为医院急诊真实分诊记录。

答案依据：官方测试文件含 1,502 对 chosen/rejected 及等级字段；不采用合成训练对作测试。

## TriageBench（Wong，一致性探针）

来源：[发布方](https://github.com/wongqihan/triagebench)。

状态：仅引用，未收录题目。仅作另行设计的一致性附加实验，不填分诊正确性主任务。

核验日期：2026-10-10；结论：不纳入主集。

[发布证据](https://huggingface.co/datasets/wongqihan/triagebench)；许可：MIT。

材料性质：同一神经症状题设的属性/语言变体。

答案依据：发布方明确只测一致性、不声称临床正确；不能当正确性金标。

## PhysioNet Challenge 2019

来源：[发布方](https://physionet.org/content/challenge-2019/1.0.0/)。

状态：仅引用，未收录题目。先固定预测时点/提前窗口、患者划分与基线；公开训练材料构建的自留评测应明确标注，不能直接代表是否应转 ICU。

核验日期：2026-10-10；结论：需预测协议。

[发布证据](https://physionet.org/content/challenge-2019/1.0.0/)；许可：CC-BY-4.0。

材料性质：真实 ICU 的生命体征与检验时序，公开训练部分。

答案依据：基于挑战定义的 SepsisLabel；官方隐藏测试不能假称已取得。

## UCI Diabetes 130-US Hospitals

来源：[发布方](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)。

状态：仅引用，未收录题目。按 patient_nbr 隔离；排除不适用出院情况；仅使用出院时已知特征，报告人群和年代限制。

核验日期：2026-10-10；结论：需预测协议。

[发布证据](https://doi.org/10.24432/C5230J)；许可：CC-BY-4.0。

材料性质：1999—2008 年美国医院糖尿病住院结构化记录。

答案依据：readmitted 表示实际再入院结果，不是最优随访行动标签。

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
