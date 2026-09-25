# 给定药物对相互作用分类：逐案例结果

77 个案例，共 150 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| DDI-DrugBank.d766 | {"sentence": "Agents that might be coadministered with trimetrexate in AIDS patients for other indications tha… | 3 | 66.7% | 66.7% |
| DDI-DrugBank.d735 | {"sentence": "Patients receiving sirolimus or nifedipine in combination with MYCAMINE should be monitored for … | 3 | 33.3% | 66.7% |
| DDI-DrugBank.d639 | {"sentence": "Co-administration of SUTENT with strong inhibitors of the CYP3A4 family (e.g., ketoconazole, itr… | 4 | 100.0% | 100.0% |
| DDI-DrugBank.d643 | {"sentence": "Melatonin may interact with the following drugs: aspirin and other NSAIDs (may lower melatonin l… | 7 | 28.6% | 14.3% |
| DDI-DrugBank.d776 | {"sentence": "Careful monitoring of cyclosporine concentrations and serum creatinine is recommended in patient… | 11 | 90.9% | 81.8% |
| DDI-DrugBank.d675 | {"sentence": "Examples of some of the more potent CYP 3A4 inhibitors include macrolide antibiotics (e.g., eryt… | 2 | 100.0% | 100.0% |
| DDI-MedLine.d216 | {"sentence": "In this randomized, blinded, crossover study, 11 healthy volunteers ingested 0.2 mg/kg S-ketamin… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d628 | {"sentence": "The concurrent administration of potent inhalational agents (eg, isoflurane, enflurane, and halo… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d603 | {"sentence": "ProAmatine. Alpha-adrenergic blocking agents, such as prazosin, terazosin, and doxazosin, can an… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d780 | {"sentence": "Sulfonamides: Concurrent use of procaine hydrochloride and sulfonamides may result in a reductio… | 2 | 50.0% | 50.0% |
| DDI-DrugBank.d773 | {"sentence": "Patients studied in clinical trials of TNKase were routinely treated with heparin and aspirin. "… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d709 | {"sentence": "Although such a reaction has not been demonstrated with roxithromycin, concomitant administratio… | 1 | 0.0% | 0.0% |
| DDI-DrugBank.d668 | {"sentence": "John s Wort, and certain anticonvulsants (phenytoin, phenobarbital, carbamazepine) may induce mi… | 1 | 0.0% | 0.0% |
| DDI-DrugBank.d715 | {"sentence": "Concurrent use of DEMSER with alcohol or other CNS depressants can increase their sedative effec… | 1 | 0.0% | 0.0% |
| DDI-DrugBank.d765 | {"sentence": "For patients receiving ketoconazole or other potent CYP3A4 inhibitors such as other azole antifu… | 2 | 100.0% | 50.0% |
| DDI-DrugBank.d716 | {"sentence": "Before taking this medication, tell your doctor if you are taking a tricyclic antidepressant suc… | 2 | 50.0% | 50.0% |
| DDI-DrugBank.d585 | {"sentence": "The following agents may increase certain actions or side effects of anticholinergic drugs: aman… | 1 | 100.0% | 0.0% |
| DDI-DrugBank.d737 | {"sentence": "Dopamine antagonists: Since pramipexole is a dopamine agonist, it is possible that dopamine anta… | 3 | 66.7% | 66.7% |
| DDI-DrugBank.d680 | {"sentence": "Based on studies evaluating possible interactions of pantoprazole with other drugs, no dosage ad… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d775 | {"sentence": "Some drug interactions are: - birth control pills - corticosteroids - medicines for angina or hi… | 11 | 18.2% | 18.2% |
| DDI-DrugBank.d752 | {"sentence": "Drugs such as erythromycin, diltiazem, verapamil, ketoconazole, fluconazole and itraconazole wer… | 5 | 100.0% | 100.0% |
| DDI-DrugBank.d627 | {"sentence": "While no formal drug interaction studies have been performed, the following concomitant drugs we… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d756 | {"sentence": "Additive sedative effects and confusional states may emerge if levomepromazine is given with ben… | 4 | 100.0% | 100.0% |
| DDI-DrugBank.d615 | {"sentence": "Triprolidine may enhance the sedative effects of central nervous system depressants including al… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d604 | {"sentence": "Thalidomide has been reported to enhance the sedative activity of barbiturates, alcohol, chlorpr… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d777 | {"sentence": "Use of Anticoagulants and Antiplatelet Agents -- Streptase, Streptokinase, alone or in combinati… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d689 | {"sentence": "MAO Inhibitors - The pressor effect of sympathomimetic pressor amines is markedly potentiated in… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d624 | {"sentence": "In clinical studies of TOBI, patients taking TOBI concomitantly with dornase alfa (PULMOZYME , G… | 2 | 100.0% | 50.0% |
| DDI-DrugBank.d640 | {"sentence": "Use of potassium-sparing diuretics (spironolactone, triamterene, amiloride) or potassium supplem… | 1 | 100.0% | 100.0% |
| DDI-MedLine.d200 | {"sentence": "We have demonstrated appropriateness of inhospital administration of fixed amlodipine/valsartan … | 2 | 50.0% | 0.0% |
| DDI-MedLine.d154 | {"sentence": "In experiment 2, the same regimen of GSLS was administered to chickens inoculated with inactivat… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d637 | {"sentence": "Use with Other Central Nervous System Depressants: The depressant effects of morphine are potent… | 2 | 100.0% | 100.0% |
| DDI-DrugBank.d742 | {"sentence": "However, the impairment of motor skills produced by REMERON has been shown to be additive with t… | 2 | 100.0% | 100.0% |
| DDI-DrugBank.d649 | {"sentence": "Sulfamethizole may increase the effects of barbiturates, tolbutamide, and uricosurics. ", "targe… | 1 | 100.0% | 100.0% |
| DDI-MedLine.d180 | {"sentence": "We also found that Bcl-2 was overexpressed in DZNep insensitive cells, and cotreatment with DZNe… | 1 | 100.0% | 100.0% |
| DDI-MedLine.d194 | {"sentence": "Studies with forced expression and siRNA knockdown of Bcl-2 and Cdk1 suggest that dasatinib-medi… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d690 | {"sentence": "The CNS-depressant effect of propoxyphene is additive with that of other CNS depressants, includ… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d725 | {"sentence": "The pressor response of adrenergic agents may also be potentiated by tricyclic antidepressants."… | 1 | 100.0% | 100.0% |
| DDI-MedLine.d161 | {"sentence": "Our data demonstrate that chronic treatment with the metabotropic glutamate receptor 5 antagonis… | 1 | 100.0% | 100.0% |
| DDI-MedLine.d218 | {"sentence": "Also mirtazapine, which is not believed to interact with warfarin, increased the risk of GI blee… | 1 | 0.0% | 0.0% |
| DDI-MedLine.d190 | {"sentence": "AAV2-mediated retinal transduction is improved by co-injection of heparinase III or chondroitin … | 1 | 100.0% | 100.0% |
| DDI-MedLine.d217 | {"sentence": "We found antagonism between celecoxib and the four drugs in the breast cancer cells MCF7 followi… | 1 | 100.0% | 100.0% |
| DDI-MedLine.d179 | {"sentence": "Synergistic interaction between sunitinib and docetaxel is sequence dependent in human non-small… | 1 | 0.0% | 0.0% |
| DDI-DrugBank.d655 | {"sentence": "Methscopolamine may interact with antidepressants (tricyclic type), MAO inhibitors (e.g., phenel… | 11 | 100.0% | 100.0% |
| DDI-DrugBank.d697 | {"sentence": "Interactions for Vitamin B1 (Thiamine): Loop Diuretics, Oral Contraceptives, Stavudine, Tricycli… | 1 | 100.0% | 0.0% |
| DDI-DrugBank.d781 | {"sentence": "Gentamicin: Animal data have suggested the possibility of interaction between perindopril and ge… | 2 | 100.0% | 50.0% |
| DDI-MedLine.d181 | {"sentence": "The authors report the case of an infant with confirmed congenital hypothyroidism on levothyroxi… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d636 | {"sentence": "Some anticonvulsants may interact with Mephenytoin. ", "target_1": {"charOffset": "5-19", "text"… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d601 | {"sentence": "Barbiturates may decrease the effectiveness of oral contraceptives, certain antibiotics, quinidi… | 1 | 0.0% | 0.0% |
| DDI-DrugBank.d784 | {"sentence": "Other inhibitors of the cytochrome P450 3A4 enzyme system, such as antimycotic agents (e.g., itr… | 3 | 100.0% | 100.0% |
| DDI-DrugBank.d599 | {"sentence": "These data suggest that GH administration may alter the clearance of compounds known to be metab… | 1 | 100.0% | 100.0% |
| DDI-MedLine.d213 | {"sentence": "Systemic and apparent oral midazolam clearance were 24% (269 73 vs. 354 102 ml/min, P = 0.022) a… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d653 | {"sentence": "Drugs that induce hepatic enzymes such as phenobarbital, phenytoin and rifampin may increase the… | 3 | 100.0% | 100.0% |
| DDI-DrugBank.d638 | {"sentence": "Human pharmacologic studies have shown that Ritalin may inhibit the metabolism of coumarin antic… | 4 | 100.0% | 100.0% |
| DDI-DrugBank.d598 | {"sentence": "Trimethoprim, given at a common clinical dosage, increased the phenytoin half-life by 51% and de… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d591 | {"sentence": "In vivo, the plasma clearance of ropivacaine was reduced by 70% during coadministration of fluvo… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d783 | {"sentence": "Posicor inhibits some of the liver's ability to metabolize some other drugs - terfenadine, astem… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d577 | {"sentence": "Sulfonamides can also displace methotrexate from plasma protein-binding sites, thus increasing f… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d645 | {"sentence": "Terbinafine decreases the clearance of caffeine by 19%. ", "target_1": {"charOffset": "0-10", "t… | 1 | 100.0% | 100.0% |
| DDI-MedLine.d231 | {"sentence": "Moxifloxacin and Lomefloxacin reacts faster with sucralfate and gelusil in acidic media whereas … | 1 | 0.0% | 0.0% |
| DDI-DrugBank.d695 | {"sentence": "While co-administration of ZAVESCA appeared to increase the clearance of Cerezyme by 70%, these … | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d632 | {"sentence": "Mixing SYMLIN and Insulin The pharmacokinetic parameters of SYMLIN were altered when mixed with … | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d702 | {"sentence": "However, the co administration of SPIRIVA with other anticholinergic containing drugs (e.g., ipr… | 2 | 100.0% | 100.0% |
| DDI-DrugBank.d743 | {"sentence": "Concomitant administration of terfenadine with clarithromycin, erythromycin, or troleandomycin i… | 2 | 100.0% | 100.0% |
| DDI-DrugBank.d703 | {"sentence": "Interaction with Other Central Nervous System Depressants: MEPERIDINE SHOULD BE USED WITH GREAT … | 2 | 100.0% | 100.0% |
| DDI-DrugBank.d579 | {"sentence": "Patients receiving antibiotics and sulfonamides generally should not be treated with ganglion bl… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d739 | {"sentence": "It is reasonable to employ appropriate clinical monitoring when potent cytochrome P450 enzyme in… | 2 | 100.0% | 100.0% |
| DDI-DrugBank.d641 | {"sentence": "Although ibuprofen (400 mg qid) can be administered with ALIMTA in patients with normal renal fu… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d726 | {"sentence": "A multiple dose drug-drug interaction study demonstrated that ketoconazole approximately doubled… | 2 | 100.0% | 100.0% |
| DDI-DrugBank.d652 | {"sentence": "Because the action of metoclopramide will influence the delivery of food to the intestines and t… | 1 | 0.0% | 0.0% |
| DDI-DrugBank.d727 | {"sentence": "Therefore, use of zidovudine in combination with ZERIT should be avoided. ", "target_1": {"charO… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d633 | {"sentence": "This increase was observed at the first test point which was the second day after starting Mexit… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d700 | {"sentence": "Azathioprine/Mycophenolate Mofetil: Given that azathioprine and mycophenolate mofetil inhibit pu… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d578 | {"sentence": "Drugs that induce hepatic enzymes such as phenobarbital, phenytoin, and rifampin may increase th… | 1 | 0.0% | 0.0% |
| DDI-DrugBank.d597 | {"sentence": "Caution should be used when administering MOBIC with warfarin since patients on warfarin may exp… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d642 | {"sentence": "Prothrombin time or other suitable anticoagulation test should be monitored if tigecycline is ad… | 1 | 100.0% | 100.0% |
| DDI-DrugBank.d779 | {"sentence": "Coadministration of methyldopa with ferrous sulfate or ferrous gluconate is not recommended. ", … | 1 | 100.0% | 100.0% |
