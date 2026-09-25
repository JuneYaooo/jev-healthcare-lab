# 科学论断与给定摘要一致性：逐案例结果

100 个案例，共 118 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| 48 | {"abstract": ["OBJECTIVES To carry out a further survey of archived appendix samples to understand better the … | 1 | 100.0% | 0.0% |
| 141 | {"abstract": ["Integrating information across sensory domains to construct a unified representation of multi-s… | 2 | 100.0% | 50.0% |
| 314 | {"abstract": ["Viral replication usually requires that innate intracellular lines of defence be overcome, a ta… | 1 | 100.0% | 100.0% |
| 1216 | {"abstract": ["The signals and molecular mechanisms that regulate the replication of terminally differentiated… | 1 | 0.0% | 100.0% |
| 598 | {"abstract": ["With respect to cervical cancer management, Finland and the Netherlands are comparable in relev… | 1 | 100.0% | 100.0% |
| 660 | {"abstract": ["Over the past two decades there have been significant achievements in the control of a handful … | 1 | 100.0% | 100.0% |
| 756 | {"abstract": ["Lysine acetylation is a reversible posttranslational modifcation, an epigenetic phenomenon, ref… | 1 | 100.0% | 100.0% |
| 142 | {"abstract": ["CONTEXT Antibody-based induction therapy plus calcineurin inhibitors (CNIs) reduce acute reject… | 1 | 100.0% | 100.0% |
| 70 | {"abstract": ["Gliomas arising in the brainstem and thalamus are devastating tumors that are difficult to surg… | 2 | 100.0% | 100.0% |
| 49 | {"abstract": ["Adenosine deaminases acting on RNA (ADARs) are involved in RNA editing that converts adenosine … | 1 | 100.0% | 100.0% |
| 1019 | {"abstract": ["Two-component signal transduction pathways comprising histidine protein kinases (HPKs) and thei… | 1 | 100.0% | 100.0% |
| 516 | {"abstract": ["IMPORTANCE Exacerbations of respiratory symptoms in chronic obstructive pulmonary disease (COPD… | 1 | 100.0% | 100.0% |
| 613 | {"abstract": ["Leucine-rich repeat kinase 2 (LRRK2) mutations are the most common genetic cause of Parkinson's… | 1 | 100.0% | 100.0% |
| 54 | {"abstract": ["Fibrosis is a pathological result of a dysfunctional repair response to tissue injury and occur… | 1 | 100.0% | 100.0% |
| 985 | {"abstract": ["The canonical role of messenger RNA (mRNA) is to deliver protein-coding information to sites of… | 1 | 100.0% | 100.0% |
| 960 | {"abstract": ["OBJECTIVE Although the Polypill concept (proposed in 2003) is promising in terms of benefits fo… | 1 | 100.0% | 100.0% |
| 508 | {"abstract": ["Heterogeneity within the self-renewal durability of adult hematopoietic stem cells (HSCs) chall… | 1 | 100.0% | 100.0% |
| 821 | {"abstract": ["Protein modifications play a major role for most biological processes in living organisms.", "A… | 1 | 100.0% | 100.0% |
| 249 | {"abstract": ["The interest in brown adipose tissue (BAT) as a target to combat metabolic disease has recently… | 1 | 100.0% | 100.0% |
| 690 | {"abstract": ["Background The degree of volume depletion in severe malaria is currently unknown, although know… | 1 | 100.0% | 100.0% |
| 577 | {"abstract": ["Immune clearance and resource limitation (via red blood cell depletion) shape the peaks and tro… | 1 | 0.0% | 0.0% |
| 823 | {"abstract": ["Background The catalytically active 66-kDa subunit of the human immunodeficiency virus type 1 (… | 1 | 100.0% | 100.0% |
| 1014 | {"abstract": ["The target of rapamycin (TOR) pathway is a major nutrient-sensing pathway that, when geneticall… | 1 | 100.0% | 100.0% |
| 692 | {"abstract": ["CONTEXT A number of countries have implemented a policy of universal leukoreduction of their bl… | 1 | 100.0% | 0.0% |
| 100 | {"abstract": ["Stem cells are proposed to segregate chromosomes asymmetrically during self-renewing divisions … | 1 | 100.0% | 100.0% |
| 517 | {"abstract": ["BACKGROUND Genetic and epidemiological evidence suggests an inverse association between B-type … | 1 | 100.0% | 100.0% |
| 637 | {"abstract": ["OBJECTIVE To establish the mental health needs of homeless children and families before and aft… | 1 | 100.0% | 100.0% |
| 551 | {"abstract": ["T cell receptor (TCR-CD3) triggering involves both receptor clustering and conformational chang… | 1 | 100.0% | 100.0% |
| 1110 | {"abstract": ["BACKGROUND The Global Burden of Diseases, Injuries, and Risk Factors Study 2015 provides an up-… | 1 | 100.0% | 100.0% |
| 1292 | {"abstract": ["Background Macrosomia is associated with considerable neonatal and maternal morbidity.", "Facto… | 1 | 0.0% | 100.0% |
| 589 | {"abstract": ["CONTEXT More than 1.5 million US adults use stimulants and other medications labeled for treatm… | 1 | 100.0% | 100.0% |
| 384 | {"abstract": ["BACKGROUND The Global Burden of Diseases, Injuries, and Risk Factors Study 2015 provides an up-… | 1 | 0.0% | 100.0% |
| 911 | {"abstract": ["Synaptic long-term potentiation (LTP) at spinal neurons directly communicating pain-specific in… | 1 | 100.0% | 100.0% |
| 993 | {"abstract": ["G-quadruplex (G4)-forming genomic sequences, including telomeres, represent natural replication… | 1 | 100.0% | 100.0% |
| 723 | {"abstract": ["Neutrophils rapidly undergo polarization and directional movement to infiltrate the sites of in… | 1 | 100.0% | 100.0% |
| 729 | {"abstract": ["We generated a series of knockin mouse lines, in which the cytokine receptor gp130-dependent ST… | 1 | 100.0% | 100.0% |
| 1137 | {"abstract": ["Glioblastomas are deadly cancers that display a functional cellular hierarchy maintained by sel… | 1 | 100.0% | 100.0% |
| 859 | {"abstract": ["The TLX1 and TLX3 transcription factor oncogenes have a key role in the pathogenesis of T cell … | 1 | 100.0% | 100.0% |
| 1280 | {"abstract": ["Half the world's population is chronically infected with Helicobacter pylori, causing gastritis… | 1 | 100.0% | 100.0% |
| 1337 | {"abstract": ["DNA damage tolerance during eukaryotic replication is orchestrated by PCNA ubiquitination.", "W… | 1 | 0.0% | 100.0% |
| 386 | {"abstract": ["OBJECTIVES To determine the incidence and clinical importance of errors in the preparation and … | 1 | 100.0% | 100.0% |
| 236 | {"abstract": ["In the mammalian model of sex determination, embryos are considered to be sexually indifferent … | 1 | 0.0% | 0.0% |
| 1175 | {"abstract": ["The RIG-I-like receptors (RLRs) RIG-I, MDA5, and LGP2 play a major role in pathogen sensing of … | 1 | 100.0% | 100.0% |
| 133 | {"abstract": ["Tks5/Fish is a scaffolding protein with five SH3 domains and one PX domain.", "In Src-transform… | 5 | 100.0% | 100.0% |
| 385 | {"abstract": ["Combining DNA-demethylating agents (DNA methyltransferase inhibitors [DNMTis]) with histone dea… | 2 | 50.0% | 50.0% |
| 1266 | {"abstract": ["CONTEXT During pregnancy, serum levels of estrogen, progesterone, and other hormones are marked… | 1 | 100.0% | 100.0% |
| 793 | {"abstract": ["Mitochondria are the primary energy-generating system in most eukaryotic cells.", "Additionally… | 1 | 100.0% | 100.0% |
| 343 | {"abstract": ["BACKGROUND Diabetes mellitus is a major risk factor for adverse outcomes after acute coronary s… | 2 | 50.0% | 50.0% |
| 230 | {"abstract": ["BACKGROUND Alcohol has been reported to be a common and modifiable risk factor for hypertension… | 1 | 100.0% | 100.0% |
| 956 | {"abstract": ["Ligand-directed signal bias offers opportunities for sculpting molecular events, with the promi… | 1 | 0.0% | 100.0% |
| 1197 | {"abstract": ["OBJECTIVE To establish the mental health needs of homeless children and families before and aft… | 1 | 100.0% | 100.0% |
| 212 | {"abstract": ["In mammals, caloric restriction consistently results in extended lifespan.", "Epigenetic inform… | 1 | 100.0% | 100.0% |
| 312 | {"abstract": ["IMPORTANCE Identification of the bacterium responsible for an outbreak can aid in disease manag… | 1 | 100.0% | 100.0% |
| 527 | {"abstract": ["Mesenchymal niche cells may drive tissue failure and malignant transformation in the hematopoie… | 1 | 0.0% | 0.0% |
| 163 | {"abstract": ["IMPORTANCE Bariatric surgery is associated with sustained weight loss and improved physical hea… | 1 | 100.0% | 100.0% |
| 659 | {"abstract": ["Over the past two decades there have been significant achievements in the control of a handful … | 1 | 100.0% | 100.0% |
| 213 | {"abstract": ["OBJECTIVE To determine the effectiveness and cost effectiveness of using information from circu… | 1 | 100.0% | 100.0% |
| 1271 | {"abstract": ["BACKGROUND The prognosis and treatment of the 2 main types of cardiac amyloidosis, immunoglobul… | 1 | 100.0% | 100.0% |
| 1319 | {"abstract": ["Human astrocytes are larger and more complex than those of infraprimate mammals, suggesting tha… | 1 | 100.0% | 100.0% |
| 279 | {"abstract": ["The non-enveloped bacilliform viruses are the second group of plant viruses known to possess a … | 1 | 100.0% | 100.0% |
| 554 | {"abstract": ["Neutrophil extracellular traps (NETs) are implicated in autoimmunity, but how they are generate… | 1 | 100.0% | 100.0% |
| 1146 | {"abstract": ["Background Extensive debate exists in the healthcare community over whether outcomes of medical… | 1 | 100.0% | 100.0% |
| 820 | {"abstract": ["Protein modifications play a major role for most biological processes in living organisms.", "A… | 1 | 100.0% | 100.0% |
| 51 | {"abstract": ["Application of stem cell biology to breast cancer research has been limited by the lack of simp… | 1 | 100.0% | 100.0% |
| 623 | {"abstract": ["OBJECTIVE To examine whether past high sun exposure is associated with a reduced risk of multip… | 1 | 100.0% | 100.0% |
| 1221 | {"abstract": ["Human tumors show a high level of genetic heterogeneity, but the processes that influence the t… | 1 | 0.0% | 0.0% |
| 1241 | {"abstract": ["The functional heart is comprised of distinct mesoderm-derived lineages including cardiomyocyte… | 1 | 100.0% | 100.0% |
| 452 | {"abstract": ["Gene expression is a fundamentally stochastic process, with randomness in transcription and tra… | 2 | 100.0% | 100.0% |
| 1298 | {"abstract": ["BACKGROUND Deep vein thrombosis (DVT) and pulmonary embolism are common after stroke.", "In sma… | 1 | 100.0% | 100.0% |
| 36 | {"abstract": ["BACKGROUND Homocysteine is a risk factor for coronary artery disease (CAD), although a causal r… | 2 | 100.0% | 100.0% |
| 1259 | {"abstract": ["CONTEXT The growth inhibitory effect of tamoxifen, which is used for the treatment of hormone r… | 1 | 100.0% | 100.0% |
| 971 | {"abstract": ["BACKGROUND Screening for cervical cancer based on testing for human papillomavirus (HPV) increa… | 4 | 100.0% | 100.0% |
| 1049 | {"abstract": ["Historically, the ribosome has been viewed as a complex ribozyme with constitutive rather than … | 1 | 100.0% | 100.0% |
| 179 | {"abstract": ["BACKGROUND Birth size, perhaps a proxy for prenatal environment, might be a correlate of subseq… | 4 | 100.0% | 100.0% |
| 261 | {"abstract": ["BACKGROUND Endothelium-dependent modulation of coronary tone is impaired in the collateral-depe… | 2 | 100.0% | 100.0% |
| 501 | {"abstract": ["OBJECTIVE To evaluate the association of overall and specific headaches with volume of white ma… | 1 | 100.0% | 100.0% |
| 1335 | {"abstract": ["Delayed T cell recovery and restricted T cell receptor (TCR) diversity after allogeneic hematop… | 1 | 100.0% | 100.0% |
| 1303 | {"abstract": ["Limited neural input results in muscle weakness in neuromuscular disease because of a reduction… | 1 | 100.0% | 100.0% |
| 560 | {"abstract": ["Mice lacking junctional adhesion molecule A (JAM-A, encoded by F11r) exhibit enhanced intestina… | 1 | 100.0% | 100.0% |
| 421 | {"abstract": ["A solid tumor is an organ composed of cancer and host cells embedded in an extracellular matrix… | 1 | 100.0% | 100.0% |
| 1262 | {"abstract": ["The RNA-guided DNA endonuclease Cas9 is a powerful tool for genome editing.", "Little is known … | 1 | 100.0% | 100.0% |
| 1100 | {"abstract": ["One-fourth of all deaths in industrialized countries result from coronary heart disease.", "A c… | 1 | 0.0% | 0.0% |
| 1225 | {"abstract": ["To identify new genetic factors for colorectal cancer (CRC), we conducted a genome-wide associa… | 1 | 100.0% | 100.0% |
| 1281 | {"abstract": ["Half the world's population is chronically infected with Helicobacter pylori, causing gastritis… | 1 | 100.0% | 100.0% |
| 1359 | {"abstract": ["IMPORTANCE Combining pharmacotherapies for tobacco-dependence treatment may increase smoking ab… | 1 | 100.0% | 100.0% |
| 491 | {"abstract": ["Background Macrosomia is associated with considerable neonatal and maternal morbidity.", "Facto… | 1 | 100.0% | 100.0% |
| 146 | {"abstract": ["CONTEXT Antibody-based induction therapy plus calcineurin inhibitors (CNIs) reduce acute reject… | 1 | 100.0% | 100.0% |
| 770 | {"abstract": ["BACKGROUND Elderly and frail patients with cancer, although often treated with chemotherapy, ar… | 1 | 0.0% | 100.0% |
| 1336 | {"abstract": ["Delayed T cell recovery and restricted T cell receptor (TCR) diversity after allogeneic hematop… | 1 | 100.0% | 100.0% |
| 300 | {"abstract": ["Chronic obstructive pulmonary disease (COPD) is linked to both cigarette smoking and genetic de… | 1 | 100.0% | 100.0% |
| 716 | {"abstract": ["Recent studies have reported that competitive endogenous RNAs (ceRNAs) can act as sponges for a… | 1 | 100.0% | 100.0% |
| 721 | {"abstract": ["Research on the human microbiome has established that commensal and pathogenic bacteria can inf… | 1 | 100.0% | 100.0% |
| 700 | {"abstract": ["Dynamically polarized membrane proteins define different cell boundaries and have an important … | 1 | 100.0% | 100.0% |
| 269 | {"abstract": ["Molecular mechanisms underlying the cold-associated high cardiovascular risk remain unknown.", … | 1 | 0.0% | 100.0% |
| 814 | {"abstract": ["Activating mutations in genes encoding G protein α (Gα) subunits occur in 4-5% of all human can… | 1 | 0.0% | 0.0% |
| 127 | {"abstract": ["Plus-end tracking proteins, such as EB1 and the dynein/dynactin complex, regulate microtubule d… | 1 | 100.0% | 100.0% |
| 1132 | {"abstract": ["T cell receptor (TCR-CD3) triggering involves both receptor clustering and conformational chang… | 2 | 50.0% | 50.0% |
| 903 | {"abstract": ["Viral replication and microbial translocation from the gut to the blood during HIV infection le… | 1 | 100.0% | 100.0% |
| 514 | {"abstract": ["CONTEXT Adequate vitamin D status for optimum bone health has received increased recognition in… | 1 | 0.0% | 0.0% |
| 536 | {"abstract": ["Panic disorder is a severe anxiety disorder with recurrent, debilitating panic attacks.", "In i… | 1 | 100.0% | 100.0% |
