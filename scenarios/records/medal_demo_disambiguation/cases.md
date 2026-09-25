# 医学缩写消歧：逐案例结果

34 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| 1 | {"abstract": "a report is given on the recent discovery of outstanding immunological properties in ba ncyanoet… | 5 | 80.0% | 60.0% |
| 2 | {"abstract": "the CSD of blood flow to the subendocardial medium and subepicardial layers of the left VVI free… | 6 | 83.3% | 33.3% |
| 3 | {"abstract": "the virostatic compound nndiethyloxotetradecylimidazolidinylethylpiperazinecarboxamidehydrochlor… | 1 | 100.0% | 100.0% |
| 4 | {"abstract": "rmi rmi and rmi are newly synthetized nrdibenzobfoxepinylnmethylpiperazinemaleates which show in… | 2 | 100.0% | 0.0% |
| 5 | {"abstract": "a doubleblind study with intraindividual comparisons was carried out to investigate the effects … | 1 | 0.0% | 0.0% |
| 6 | {"abstract": "a serum agglutinin reactive with CRC in the presence of polycarboxyl groups is reported it is li… | 2 | 100.0% | 0.0% |
| 7 | {"abstract": "stroma from either normal or pnhlike CRC is capable of inhibiting to some extent lysis in the su… | 4 | 50.0% | 0.0% |
| 8 | {"abstract": "the effect of the L1 metabolite of aspirin namely salicylic acid upon the PPP ppp of normal and … | 4 | 75.0% | 50.0% |
| 9 | {"abstract": "in one experiment the effect on rumen ph of feeding with restricted amounts of whole or pelleted… | 3 | 66.7% | 66.7% |
| 10 | {"abstract": "the presence of at least two ionizable AS center groups has been detected by a study of the effe… | 2 | 100.0% | 50.0% |
| 11 | {"abstract": "the reaction of glutamate dehydrogenase and glu gl with nad and nadp has been studied with stopp… | 5 | 80.0% | 0.0% |
| 12 | {"abstract": "choline AT ec catalyzes the biosynthesis of acetylcholine according to the following chemical eq… | 6 | 66.7% | 50.0% |
| 13 | {"abstract": "increasing concentrations of chloride were found to increase the resolution between two visible … | 2 | 100.0% | 0.0% |
| 14 | {"abstract": "the properties of the functional groups in a protein can be used as builtinprobes of the structu… | 1 | 0.0% | 0.0% |
| 15 | {"abstract": "primary amines react with pentanedione at ph to form enamines nalkylaminopentenones the latter c… | 1 | 100.0% | 100.0% |
| 16 | {"abstract": "a purification procedure is reported for obtaining bovine CL dihydrofolate reductase in high yie… | 5 | 60.0% | 40.0% |
| 17 | {"abstract": "dihydrofolate reductase has been purified fold to apparent homogeneity from a trimethoprimresist… | 8 | 37.5% | 25.0% |
| 18 | {"abstract": "ionization effects on the IB of the potential TS analogues phosphoglycolate and phosphoglycolohy… | 3 | 100.0% | 33.3% |
| 19 | {"abstract": "bovine erythrocyte superoxide dismutase was slowly and irreversibly inactivated by hydrogen pero… | 1 | 100.0% | 100.0% |
| 20 | {"abstract": "kinetic analyses of monoanion inhibition and cl nuclear magnetic resonance at mhz were employed … | 2 | 50.0% | 0.0% |
| 21 | {"abstract": "the circular polarization of luminescence cpl emitted by tryptophan residues was used as a sensi… | 1 | 100.0% | 0.0% |
| 22 | {"abstract": "the functional role of the bacillus stearothermophilus s ribosomal protein bl probably homologou… | 3 | 33.3% | 0.0% |
| 23 | {"abstract": "the localization of the previously postulated interface recognition site irs in porcine pancreat… | 2 | 100.0% | 100.0% |
| 24 | {"abstract": "the action of snake venom phospholipases a in intact human erythrocytes was investigated in deta… | 3 | 100.0% | 33.3% |
| 25 | {"abstract": "the spontaneous inactivation of yeast glyceraldehydephosphate dehydrogenase was found to fit a s… | 2 | 0.0% | 0.0% |
| 26 | {"abstract": "the kinetics of the phinduced dissociation of the x mol wt hemoglobin from lumbricus terrestris … | 3 | 100.0% | 33.3% |
| 27 | {"abstract": "the purification of axonal membranes of crustaceans was followed by measuring enrichment in htet… | 7 | 85.7% | 85.7% |
| 28 | {"abstract": "a new procedure is described for selecting nitrogenasederepressed mutants based on the method of… | 1 | 100.0% | 0.0% |
| 29 | {"abstract": "the superoxide anion radical o reacts with ferricytochrome c to form ferrocytochrome c no interm… | 1 | 0.0% | 0.0% |
| 30 | {"abstract": "T3 a mus laser flash a mus phase in the decay of delayed fluorescence is visible under a variety… | 4 | 50.0% | 25.0% |
| 31 | {"abstract": "crude extracts and partially purified enzyme S9 from potato tubers catalyse at ph the conversion… | 2 | 0.0% | 0.0% |
| 32 | {"abstract": "microsomal phosphatidate phosphohydrolase phosphatidate phosphatase ec was solubilized and fract… | 1 | 0.0% | 0.0% |
| 33 | {"abstract": "rabbit CL microsomal S9 fortified with mm nadph effectively promote hydroxylation of betah or ca… | 4 | 75.0% | 75.0% |
| 34 | {"abstract": "properties of the phenobarbital induced cytoplasmic aldehyde dehydrogenase ec have been studied … | 2 | 0.0% | 0.0% |
