# 医学回答幻觉识别：有证据：逐案例结果

100 个案例，共 200 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| 203 | {"answer_to_check": "Our data showed no difference in 25(OH) D levels between normal children and those with C… | 2 | 100.0% | 100.0% |
| 366 | {"answer_to_check": "Our study suggests that there is great reliability between PRO data captured between FTE-… | 2 | 100.0% | 100.0% |
| 162 | {"answer_to_check": "In our population, ART conception was not significantly associated with the probability o… | 2 | 100.0% | 100.0% |
| 757 | {"answer_to_check": "Pelvic CT does not offer additional information in the vast majority of cases with RCC an… | 2 | 100.0% | 100.0% |
| 977 | {"answer_to_check": "The Internet would be a practical and accessible way of delivering sexual health educatio… | 2 | 100.0% | 100.0% |
| 262 | {"answer_to_check": "The employees believe the merger has neither generated economy of scale advantages nor su… | 2 | 50.0% | 100.0% |
| 961 | {"answer_to_check": "Over 14 years, a higher BMI predicts knee pain at Y15 in women, independently of radiogra… | 2 | 100.0% | 50.0% |
| 492 | {"answer_to_check": "Most of the prognostic value of tumor depth in soft tissue sarcomas of the extremity or t… | 2 | 100.0% | 100.0% |
| 887 | {"answer_to_check": "Our findings reveal a significant decrease in ADMA levels of ex-ELBW subjects compared to… | 2 | 50.0% | 100.0% |
| 968 | {"answer_to_check": "E2+antag pretreatment does not appear to improve IVF outcomes in ML protocol when compare… | 2 | 100.0% | 100.0% |
| 709 | {"answer_to_check": "The results showed no overall first night effect on severity of RMMA frequency in young a… | 2 | 50.0% | 100.0% |
| 823 | {"answer_to_check": "In our study; sex is not a significant predictor of recanalization rate, time to recanali… | 2 | 100.0% | 100.0% |
| 176 | {"answer_to_check": "Most children undergoing congenital heart surgery can be extubated in the operating room.… | 2 | 100.0% | 100.0% |
| 626 | {"answer_to_check": "To uphold the notion for radiation exposure to be as low as reasonably achievable, ureter… | 2 | 100.0% | 100.0% |
| 610 | {"answer_to_check": "Expander deflation immediately prior to radiotherapy, may augment the adverse effects, es… | 2 | 100.0% | 50.0% |
| 868 | {"answer_to_check": "There is a knowledge deficit regarding the SU treatment goal among gout patients receivin… | 2 | 50.0% | 50.0% |
| 487 | {"answer_to_check": "This study suggests that CA72-4 determination can be useful to confirm the benign nature … | 2 | 50.0% | 50.0% |
| 398 | {"answer_to_check": "These results do not support the view that AA women are at greater risk for obesity becau… | 2 | 100.0% | 100.0% |
| 652 | {"answer_to_check": "Exclusive CRT approach is not safe to treat patients with low infiltrative rectal carcino… | 2 | 100.0% | 100.0% |
| 407 | {"answer_to_check": "Education by pharmacists, combined with access to counter samples, may or may not have an… | 2 | 100.0% | 100.0% |
| 136 | {"answer_to_check": "a-tDCS could be useful in identifying residual connectivity markers in clinically-defined… | 2 | 100.0% | 50.0% |
| 944 | {"answer_to_check": "We have thus provided compelling evidence that there is a mossy fiber GABAergic signal. T… | 2 | 50.0% | 100.0% |
| 786 | {"answer_to_check": "A possible decreased transformation of procarcinogens by CYP2D6*4 poor metabolisers could… | 2 | 100.0% | 100.0% |
| 324 | {"answer_to_check": "Findings depict wandering and PNA as overlapping, but nonequivalent phenomena. Evidence s… | 2 | 50.0% | 50.0% |
| 367 | {"answer_to_check": "Barrett's cytokeratin 7/20 pattern can be a useful marker for the diagnosis of short-segm… | 2 | 100.0% | 100.0% |
| 34 | {"answer_to_check": "Better prognosis was obtained when ruptured aneurysm was repaired in the elderly than it … | 2 | 100.0% | 100.0% |
| 210 | {"answer_to_check": "The results of this study suggest that the safest areas for the placement of miniscrews a… | 2 | 50.0% | 50.0% |
| 785 | {"answer_to_check": "Just over half the patients in this present cohort may be physically able to undertake so… | 2 | 100.0% | 100.0% |
| 295 | {"answer_to_check": "The fMRI paradigm mental imagery displays a high concordance with the further clinical co… | 2 | 50.0% | 50.0% |
| 315 | {"answer_to_check": "In Southern Italy, hepatitis G virus infection is widespread among patients with chronic … | 2 | 0.0% | 50.0% |
| 259 | {"answer_to_check": "Despite advances in early diagnosis and surgical technique, 5-year survival of stage I no… | 2 | 50.0% | 100.0% |
| 497 | {"answer_to_check": "Puberty and family factors were strong predictors of adolescent alcohol use, but family f… | 2 | 100.0% | 100.0% |
| 788 | {"answer_to_check": "Increased private health care activity does not reduce the demand for NHS care: NHS and p… | 2 | 100.0% | 100.0% |
| 881 | {"answer_to_check": "Roux-en-Y gastric bypass is a promising option for lifelong treatment of type 2 diabetes.… | 2 | 100.0% | 50.0% |
| 53 | {"answer_to_check": "Font influenced pregnant women's ratings of intervention complexity.", "evidence": ["To a… | 2 | 100.0% | 100.0% |
| 9 | {"answer_to_check": "This data demonstrates the robust nature of the short stay ward. At these two very differ… | 2 | 100.0% | 100.0% |
| 317 | {"answer_to_check": "Our prospective study confirmed the leading role of EUS and MDCT in the staging of gastri… | 2 | 100.0% | 100.0% |
| 571 | {"answer_to_check": "The presently used intervention programme provides a good starting point for adults with … | 2 | 100.0% | 100.0% |
| 174 | {"answer_to_check": "At baseline assessment patients of lower socioeconomic status showed lower health related… | 2 | 100.0% | 100.0% |
| 556 | {"answer_to_check": "TEE allowed a diagnosis of site involvement that did correlate with the anatomic diagnosi… | 2 | 100.0% | 50.0% |
| 797 | {"answer_to_check": "Golytely was more efficacious than MiraLAX in bowel cleansing, and was independently asso… | 2 | 50.0% | 100.0% |
| 330 | {"answer_to_check": "Income support policy may be a significant new lever for improving population health, esp… | 2 | 100.0% | 100.0% |
| 871 | {"answer_to_check": "The call for boycott did not affect the campaign significantly. However, if the call for … | 2 | 100.0% | 100.0% |
| 702 | {"answer_to_check": "Age ≤ 45 years, DFI＞1 year, and the combined therapy were good prognostic factors for NPC… | 2 | 100.0% | 50.0% |
| 899 | {"answer_to_check": "Compared with patients without hypothyroidism, patients with treated hypothyroidism are n… | 2 | 100.0% | 100.0% |
| 208 | {"answer_to_check": "Due to a relatively good reproducibility, fast and easy application, we found the linear … | 2 | 50.0% | 100.0% |
| 611 | {"answer_to_check": "The new storage can affords more stable temperature levels when compared to the formerly … | 2 | 50.0% | 50.0% |
| 96 | {"answer_to_check": "Histology usually demonstrated moderate to severe inflammation when VLEM were present. VL… | 2 | 100.0% | 100.0% |
| 674 | {"answer_to_check": "Biochemical analysis of injured cervical intervertebral disks reveals the presence of inf… | 2 | 100.0% | 100.0% |
| 132 | {"answer_to_check": "Although the cost-effectiveness of a single-pill strategy was within the acceptable willi… | 2 | 50.0% | 50.0% |
| 430 | {"answer_to_check": "In the present study we found a significant increase in the incidence of GBS colonization… | 2 | 50.0% | 50.0% |
| 39 | {"answer_to_check": "In comparison with its accuracy in non-DM patients, the accuracy of PET in cervical cance… | 2 | 100.0% | 100.0% |
| 651 | {"answer_to_check": "Serum PON 1 level is not correlated with the epicardial fat tissue thickness. But PON 1 l… | 2 | 50.0% | 50.0% |
| 599 | {"answer_to_check": "Important differences about the clinical relevance of certain RBC-M terms exist between c… | 2 | 50.0% | 50.0% |
| 855 | {"answer_to_check": "Our findings demonstrate that OTC pharmacy syringe sales were not associated with increas… | 2 | 100.0% | 100.0% |
| 198 | {"answer_to_check": "TEE is useful to assess left ventricular function in potential brain-dead donors. An FAC … | 2 | 100.0% | 50.0% |
| 518 | {"answer_to_check": "Our results demonstrate that kidney damage occurs during LPN when warm ischemia is＞30 min… | 2 | 0.0% | 0.0% |
| 804 | {"answer_to_check": "There was considerable impact at many levels; graduates were perceived to be able to cont… | 2 | 100.0% | 100.0% |
| 196 | {"answer_to_check": "These data suggest that CIN and VAIN may have some common features in certain cases, i.e.… | 2 | 100.0% | 100.0% |
| 720 | {"answer_to_check": "C-kit positivity was observed in the mitotic, proliferating and also dysplastic hepatic c… | 2 | 50.0% | 100.0% |
| 771 | {"answer_to_check": "These findings provide evidence for the existence of a high-IQ variant of schizophrenia t… | 2 | 100.0% | 100.0% |
| 441 | {"answer_to_check": "Discordant observations due to interobserver variability make histological sub-classifica… | 2 | 100.0% | 100.0% |
| 178 | {"answer_to_check": "Little is known about the mechanisms underlying irregular bleeding in HT users. This is t… | 2 | 100.0% | 100.0% |
| 76 | {"answer_to_check": "Alcohol and drug use are important contributory factors to injury and poisoning deaths. M… | 2 | 100.0% | 50.0% |
| 119 | {"answer_to_check": "Conveyance of emotions or movements through music may be decoded differently by persons w… | 2 | 100.0% | 100.0% |
| 389 | {"answer_to_check": "This paper discusses the cultural appropriateness of the RAQ in Australian settings, and … | 2 | 100.0% | 100.0% |
| 322 | {"answer_to_check": "Leaving out the period of intake of meals and beverages from the raw pH data might be the… | 2 | 100.0% | 50.0% |
| 975 | {"answer_to_check": "In our study, we suggest that glomerular hyperfiltration due to pregnancy does not have a… | 2 | 50.0% | 100.0% |
| 780 | {"answer_to_check": "The researchers studied a defined skin care protocol using a cleanser with aloe vera and … | 2 | 50.0% | 50.0% |
| 179 | {"answer_to_check": "Percutaneous ethanol injection without aspiration of ethanol-mixed fluid seems to be the … | 2 | 100.0% | 100.0% |
| 667 | {"answer_to_check": "Urinary biomarkers allow a non-invasive, sensitive, early assessment of the tubular lesio… | 2 | 50.0% | 50.0% |
| 827 | {"answer_to_check": "BV/TV assessed by micro-CT correlates with the percentage of bone assessed by conventiona… | 2 | 100.0% | 50.0% |
| 846 | {"answer_to_check": "Family physicians provide sensitive, timely, and accurate community influenza morbidity d… | 2 | 50.0% | 50.0% |
| 952 | {"answer_to_check": "Solitary kidney in a canine model is more resistant to ischemia than paired kidneys based… | 2 | 100.0% | 100.0% |
| 533 | {"answer_to_check": "The cost-effectiveness of DMOADs for OA prevention for persons at high risk for incident … | 2 | 100.0% | 100.0% |
| 390 | {"answer_to_check": "This study has shown that mailing out a summary of current evidence to surgeons concernin… | 2 | 100.0% | 100.0% |
| 986 | {"answer_to_check": "Patient coaching offers promise as a means of reducing racial/ethnic disparities in pain … | 2 | 100.0% | 50.0% |
| 326 | {"answer_to_check": "New depression diagnosis and antidepressant use was shown to be less likely in areas of h… | 2 | 100.0% | 100.0% |
| 842 | {"answer_to_check": "The tendency to clear one's plate when eating is associated with increased body weight an… | 2 | 100.0% | 100.0% |
| 435 | {"answer_to_check": "Our data suggest that hearing loss caused by GM otic drops may be reduced by the inclusio… | 2 | 100.0% | 100.0% |
| 863 | {"answer_to_check": "Tuberculous enterocolitis can be managed by 9-month chemotherapy without disease recurren… | 2 | 50.0% | 100.0% |
| 878 | {"answer_to_check": "Vitamin C reduces the prevalence of complex regional pain syndrome after wrist fractures.… | 2 | 100.0% | 100.0% |
| 884 | {"answer_to_check": "In breast cancer patients having SLN biopsy, the failure of routine intraoperative FS is … | 2 | 100.0% | 100.0% |
| 43 | {"answer_to_check": "GM of CRC and SLM was associated with fewer procedures but did not influence overall surv… | 2 | 100.0% | 100.0% |
| 297 | {"answer_to_check": "Pretreatment ECG is of limited value for patients with an unremarkable cardiovascular his… | 2 | 100.0% | 100.0% |
| 101 | {"answer_to_check": "ECL assays improved the ability to predict time to diabetes in these autoantibody-positiv… | 2 | 100.0% | 100.0% |
| 601 | {"answer_to_check": "Ultrasound not only has comparable sensitivity to that of X-ray for the identification of… | 2 | 50.0% | 50.0% |
| 90 | {"answer_to_check": "HIV/STD control measures appear to have slowed the HIV/AIDS epidemic in Jamaica, however … | 2 | 50.0% | 50.0% |
| 639 | {"answer_to_check": "An elevated homocysteine level may be a precipitating factor for vitiligo in predisposed … | 2 | 100.0% | 50.0% |
| 250 | {"answer_to_check": "High-quality training, strict compliance with evidence-based guidelines, and thorough doc… | 2 | 50.0% | 50.0% |
| 35 | {"answer_to_check": "The analyses show that structural characteristics of a practice are not associated with u… | 2 | 50.0% | 100.0% |
| 460 | {"answer_to_check": "It is important to ensure that new mothers are adequately informed about topics important… | 2 | 100.0% | 50.0% |
| 940 | {"answer_to_check": "The results show that fatigue in patients with pSS and sSS is not due to the coexistence … | 2 | 50.0% | 50.0% |
| 268 | {"answer_to_check": "Consistent with prior studies, we found an inverse relationship between obesity and serum… | 2 | 50.0% | 100.0% |
| 135 | {"answer_to_check": "The leukocyte count at presentation can be used as an adjunct in the evaluation of the se… | 2 | 100.0% | 100.0% |
| 200 | {"answer_to_check": "For a given NIHSS score, the median volume of right hemisphere strokes is consistently la… | 2 | 50.0% | 100.0% |
| 47 | {"answer_to_check": "We conclude that patient and graft survival on transplanting kidneys from elderly donors … | 2 | 100.0% | 50.0% |
| 462 | {"answer_to_check": "Patients with CSM due to either degenerative disease or segmental OPLL have similar perio… | 2 | 100.0% | 100.0% |
| 241 | {"answer_to_check": "The prevalence of cognitive impairment in MND in this population based study of an unsele… | 2 | 100.0% | 100.0% |
| 814 | {"answer_to_check": "Collectively, results suggest that behavioral adaptation to ESC is likely in certain driv… | 2 | 0.0% | 50.0% |
