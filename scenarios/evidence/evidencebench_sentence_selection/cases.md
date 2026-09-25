# 全文证据句筛选：逐案例结果

37 个案例，共 37 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| pmc_1280405 | {"hypothesis": "Critically ill neonates have higher DEHP exposure than neonates receiving routine care, mediat… | 1 | 45.8 分 F1 | 41.2 分 F1 |
| pmc_2009453 | {"hypothesis": "Co-administration of benzo[a]pyrene and cigarette smoke synergistically increases the incidenc… | 1 | 32.4 分 F1 | 16.0 分 F1 |
| pmc_2374298 | {"hypothesis": "Residential exposure to radon does not elevate the risk of developing leukemia in children.", … | 1 | 20.7 分 F1 | 24.6 分 F1 |
| pmc_9141260 | {"hypothesis": "Occupational firefighter exposure alters receptor signaling in the female reproductive system,… | 1 | 40.5 分 F1 | 24.7 分 F1 |
| pubmed_9000312 | {"hypothesis": "Occupational exposure to poorly soluble cobalt-aluminate spinel increases the incidence of lun… | 1 | 26.5 分 F1 | 19.9 分 F1 |
| pmc_2702396 | {"hypothesis": "Polychlorinated biphenyls and their hydroxylated metabolites disrupt thyroid hormone homeostas… | 1 | 16.5 分 F1 | 15.4 分 F1 |
| pmc_1567786 | {"hypothesis": "Inorganic lead and organic lead cause distinct neurotoxic effects and clinical syndromes, desp… | 1 | 41.4 分 F1 | 36.8 分 F1 |
| pubmed_9476804 | {"hypothesis": "Urinary 1-naphthol and 2-naphthol concentrations are quantitative biomarkers of occupational n… | 1 | 28.1 分 F1 | 18.0 分 F1 |
| pmc_2397408 | {"hypothesis": "DEHP, an environmental contaminant, is present in soil samples, including those from waste dis… | 1 | 14.8 分 F1 | 30.3 分 F1 |
| pmc_3565452 | {"hypothesis": "The fast acetylator phenotype of NAT2 increases the risk of colorectal cancer in individuals w… | 1 | 24.4 分 F1 | 16.7 分 F1 |
| pmc_1568860 | {"hypothesis": "Exposure to industrial chemicals used in the manufacture of synthetic chemicals increases the … | 1 | 20.3 分 F1 | 23.3 分 F1 |
| pmc_1568845 | {"hypothesis": "Co-exposure to ethanol and vinyl chloride synergistically increases the risk of hepatic angios… | 1 | 49.2 分 F1 | 40.0 分 F1 |
| pmc_1314915 | {"hypothesis": "Ambient particulate matter exposure increases pulmonary inflammation in individuals with pre-e… | 1 | 20.6 分 F1 | 28.6 分 F1 |
| pubmed_6612267 | {"hypothesis": "Exposure to stainless steel welding fumes containing chromium and nickel does not increase the… | 1 | 40.7 分 F1 | 54.5 分 F1 |
| pmc_2073824 | {"hypothesis": "4-aminobiphenyl is not a significant carcinogen.", "sentences": {"0": "A FURTHER STUDY OF THE … | 1 | 17.9 分 F1 | 30.8 分 F1 |
| pmc_1469770 | {"hypothesis": "1,4-benzoquinone is the causative agent of phenol's toxicity at high doses.", "sentences": {"0… | 1 | 16.1 分 F1 | 18.0 分 F1 |
| pmc_2579688 | {"hypothesis": "BK virus infection causes urothelial carcinoma in immunosuppressed individuals.", "sentences":… | 1 | 16.9 分 F1 | 22.9 分 F1 |
| pmc_2033722 | {"hypothesis": "Chronic 1,2-dimethylhydrazine exposure causes preneoplastic alterations in colonic mucosa.", "… | 1 | 20.0 分 F1 | 17.5 分 F1 |
| pubmed_3353696 | {"hypothesis": "Short-term exposure to high concentrations of toluene causes persistent central nervous system… | 1 | 23.3 分 F1 | 24.5 分 F1 |
| pmc_2734180 | {"hypothesis": "Merkel cell polyomavirus causes Merkel cell carcinoma.", "sentences": {"0": "Merkel cell carci… | 1 | 26.0 分 F1 | 36.0 分 F1 |
| pmc_1555602 | {"hypothesis": "Estrogen-progestogen menopausal therapy improves disease-free survival in postmenopausal ER+ b… | 1 | 37.1 分 F1 | 33.0 分 F1 |
| pmc_3903646 | {"hypothesis": "Chronic inflammation caused by long-term welding fume exposure accelerates genomic instability… | 1 | 40.8 分 F1 | 28.6 分 F1 |
| pmc_2974688 | {"hypothesis": "The presence of dibromoacetonitrile in chlorinated or brominated swimming pools may result in … | 1 | 33.3 分 F1 | 25.6 分 F1 |
| pmc_1566609 | {"hypothesis": "Exposure to polychlorinated biphenyls disrupts the thyroid hormone system.", "sentences": {"0"… | 1 | 26.9 分 F1 | 28.0 分 F1 |
| pmc_1638185 | {"hypothesis": "Exposure to high levels of arsenic in drinking water during pregnancy increases the risk of ne… | 1 | 61.7 分 F1 | 47.6 分 F1 |
| pubmed_6725010 | {"hypothesis": "Occupational styrene exposure increases chromosomal aberrations in human lymphocytes.", "sente… | 1 | 29.8 分 F1 | 26.3 分 F1 |
| pmc_3120675 | {"hypothesis": "Multi-walled carbon nanotube exposure causes macrophages to develop a mixed pro-inflammatory a… | 1 | 44.8 分 F1 | 46.5 分 F1 |
| pubmed_2772581 | {"hypothesis": "Occupational exposure to crystalline silica dust increases the risk of lung cancer in stone wo… | 1 | 20.0 分 F1 | 16.9 分 F1 |
| pubmed_8597119 | {"hypothesis": "Polymorphic variants in the NAT1 gene that increase N-acetyltransferase activity cause elevate… | 1 | 22.9 分 F1 | 16.0 分 F1 |
| pmc_2363982 | {"hypothesis": "The consumption of very hot beverages, compared to beverages at lower temperatures, increases … | 1 | 30.8 分 F1 | 27.8 分 F1 |
| pmc_1241347 | {"hypothesis": "Lindane exposure increases the risk of non-Hodgkin lymphoma.", "sentences": {"0": "Risk of non… | 1 | 21.1 分 F1 | 21.9 分 F1 |
| pmc_2074189 | {"hypothesis": "Topical areca nut and tobacco extract exposure induces local squamous neoplasia.", "sentences"… | 1 | 3.8 分 F1 | 4.3 分 F1 |
| pmc_2831966 | {"hypothesis": "Occupational exposure to airborne carbon nanotube agglomerates is higher when CNTs are dispers… | 1 | 51.7 分 F1 | 53.3 分 F1 |
| pmc_3164654 | {"hypothesis": "The cord blood CD34+ transplant mouse model can be adapted to study the interactions between P… | 1 | 21.1 分 F1 | 0.0 分 F1 |
| pubmed_24434723 | {"hypothesis": "Glyphosate-based formulations are more potent than glyphosate alone at inducing apoptosis in h… | 1 | 16.7 分 F1 | 23.7 分 F1 |
| pmc_2008583 | {"hypothesis": "Higher tea consumption leads to increased mortality from multiple cancers.", "sentences": {"0"… | 1 | 16.0 分 F1 | 20.2 分 F1 |
| pubmed_3787220 | {"hypothesis": "Occupational exposure to polycyclic aromatic hydrocarbons and tar volatiles in the aluminum sm… | 1 | 38.0 分 F1 | 34.8 分 F1 |
