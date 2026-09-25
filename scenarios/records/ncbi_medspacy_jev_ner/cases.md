# medspaCy 候选与 Jev 疾病实体筛选：逐案例结果

100 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| 9585605 | Mutation analysis of UBE3A in Angelman syndrome patients. Angelman syndrome (AS) is caused by chromosome 15q11… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9792860 | Determination of the genomic structure of the COL4A4 gene and of novel mutations causing autosomal recessive A… | 1 | 0.0 分 F1 | 0.0 分 F1 |
| 9867744 | Diagnosis of hemochromatosis. If untreated, hemochromatosis can cause serious illness and early death, but the… | 1 | 75.0 分 F1 | 75.0 分 F1 |
| 9521421 | Molecular heterogeneity in mucopolysaccharidosis IVA in Australia and Northern Ireland: nine novel mutations i… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9590178 | Wilms' tumor 1 and Dax-1 modulate the orphan nuclear receptor SF-1 in sex-specific gene expression. Products o… | 1 | 57.1 分 F1 | 75.0 分 F1 |
| 9973276 | Inherited colorectal polyposis and cancer risk of the APC I1307K polymorphism. Germ-line and somatic truncatin… | 1 | 45.0 分 F1 | 46.2 分 F1 |
| 9618166 | Two frequent missense mutations in Pendred syndrome. Pendred syndrome is an autosomal recessive disorder chara… | 1 | 84.2 分 F1 | 84.2 分 F1 |
| 9674906 | Schwartz-Jampel syndrome type 2 and Stuve-Wiedemann syndrome: a case for "lumping". Recent studies demonstrate… | 1 | 14.3 分 F1 | 14.3 分 F1 |
| 9674903 | Maternal disomy and Prader-Willi syndrome consistent with gamete complementation in a case of familial translo… | 1 | 77.4 分 F1 | 77.4 分 F1 |
| 9733027 | Sperm DNA analysis in a Friedreich ataxia premutation carrier suggests both meiotic and mitotic expansion in t… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9950360 | Molecular analysis of the APC gene in 205 families: extended genotype-phenotype correlations in FAP and eviden… | 1 | 88.9 分 F1 | 70.3 分 F1 |
| 9457914 | A deletion mutation in COL17A1 in five Austrian families with generalized atrophic benign epidermolysis bullos… | 1 | 0.0 分 F1 | 0.0 分 F1 |
| 9603435 | W474C amino acid substitution affects early processing of the alpha-subunit of beta-hexosaminidase A and is as… | 1 | 50.0 分 F1 | 50.0 分 F1 |
| 9800909 | Are Dp71 and Dp140 brain dystrophin isoforms related to cognitive impairment in Duchenne muscular dystrophy? M… | 1 | 73.7 分 F1 | 73.7 分 F1 |
| 9931324 | Missense mutations in the most ancient residues of the PAX6 paired domain underlie a spectrum of human congeni… | 1 | 55.6 分 F1 | 55.6 分 F1 |
| 9580132 | Identification of a novel nonsense mutation and a missense substitution in the vasopressin-neurophysin II gene… | 1 | 90.9 分 F1 | 90.9 分 F1 |
| 9888390 | Coincidence of two novel arylsulfatase A alleles and mutation 459+1G＞A within a family with metachromatic leuk… | 1 | 100.0 分 F1 | 73.7 分 F1 |
| 9497246 | Genetic heterogeneity and penetrance analysis of the BRCA1 and BRCA2 genes in breast cancer families. The Brea… | 1 | 83.3 分 F1 | 83.3 分 F1 |
| 9546397 | Crystal structure of the hemochromatosis protein HFE and characterization of its interaction with transferrin … | 1 | 85.7 分 F1 | 85.7 分 F1 |
| 9949209 | Genetic mapping of the copper toxicosis locus in Bedlington terriers to dog chromosome 10, in a region synteni… | 1 | 50.0 分 F1 | 43.5 分 F1 |
| 9843038 | Identification of a novel mutation of the CPO gene in a Japanese hereditary coproporphyria family. Hereditary … | 1 | 0.0 分 F1 | 0.0 分 F1 |
| 9450866 | Piebaldism with deafness: molecular evidence for an expanded syndrome. In a South African girl of Xhosa stock … | 1 | 90.0 分 F1 | 90.0 分 F1 |
| 9472666 | Molecular defects leading to human complement component C6 deficiency in an African-American family. Complemen… | 1 | 33.3 分 F1 | 33.3 分 F1 |
| 9888388 | Systematic analysis of coproporphyrinogen oxidase gene defects in hereditary coproporphyria and mutation updat… | 1 | 18.2 分 F1 | 18.2 分 F1 |
| 9336417 | Susceptibility to ankylosing spondylitis in twins: the role of genes, HLA, and the environment. OBJECTIVE To d… | 1 | 93.3 分 F1 | 93.3 分 F1 |
| 9288106 | Clustering of missense mutations in the ataxia-telangiectasia gene in a sporadic T-cell leukaemia. Ataxia-tela… | 1 | 60.5 分 F1 | 60.5 分 F1 |
| 9731533 | The APCI1307K allele and cancer risk in a community-based study of Ashkenazi Jews. Mutations in APC are classi… | 1 | 69.2 分 F1 | 72.7 分 F1 |
| 9792861 | Founder BRCA1 and BRCA2 mutations in French Canadian breast and ovarian cancer families. We have identified fo… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9467011 | Mutation spectrum and genotype-phenotype analyses in Cowden disease and Bannayan-Zonana syndrome, two hamartom… | 1 | 17.6 分 F1 | 17.6 分 F1 |
| 9420335 | The tumor suppressor gene Smad4/Dpc4 is required for gastrulation and later for anterior development of the mo… | 1 | 44.4 分 F1 | 60.0 分 F1 |
| 9342365 | Cell cycle-dependent colocalization of BARD1 and BRCA1 proteins in discrete nuclear domains. Germ-line mutatio… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9371490 | Frequent inactivation of PTEN/MMAC1 in primary prostate cancer. Sporadic prostate carcinoma is the most common… | 1 | 50.0 分 F1 | 50.0 分 F1 |
| 9294109 | Myotonic dystrophy protein kinase is involved in the modulation of the Ca2+ homeostasis in skeletal muscle cel… | 1 | 88.9 分 F1 | 88.9 分 F1 |
| 9600235 | Mutations of the ATM gene detected in Japanese ataxia-telangiectasia patients: possible preponderance of the t… | 1 | 76.9 分 F1 | 83.3 分 F1 |
| 9856498 | The molecular basis of C6 deficiency in the western Cape, South Africa. Deficiency of the sixth component of h… | 1 | 66.7 分 F1 | 66.7 分 F1 |
| 9585606 | The hemochromatosis 845 G--＞A and 187 C--＞G mutations: prevalence in non-Caucasian populations. Hemochromatosi… | 1 | 66.7 分 F1 | 72.7 分 F1 |
| 9382108 | Risk reversals in predictive testing for Huntington disease. The first predictive testing for Huntington disea… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9457913 | Cycloheximide facilitates the identification of aberrant transcripts resulting from a novel splice-site mutati… | 1 | 0.0 分 F1 | 0.0 分 F1 |
| 9482572 | PAX6 mutations reviewed. Mutations in PAX6 are responsible for human aniridia and have also been found in pati… | 1 | 72.7 分 F1 | 72.7 分 F1 |
| 9703501 | BRCA1 required for transcription-coupled repair of oxidative DNA damage. The breast and ovarian cancer suscept… | 1 | 66.7 分 F1 | 66.7 分 F1 |
| 9792409 | ATM germline mutations in classical ataxia-telangiectasia patients in the Dutch population. Germline mutations… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9848786 | Human complement factor H deficiency associated with hemolytic uremic syndrome. This study reports on six case… | 1 | 11.8 分 F1 | 16.7 分 F1 |
| 9770531 | Down-regulation of transmembrane carbonic anhydrases in renal cell carcinoma cell lines by wild-type von Hippe… | 1 | 95.2 分 F1 | 95.2 分 F1 |
| 9634518 | A European multicenter study of phenylalanine hydroxylase deficiency: classification of 105 mutations and a ge… | 1 | 87.5 分 F1 | 87.5 分 F1 |
| 9358014 | Ethnic differences in the HFE codon 282 (Cys/Tyr) polymorphism. Recent studies have shown that hereditary hemo… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9620771 | Severe early-onset obesity, adrenal insufficiency and red hair pigmentation caused by POMC mutations in humans… | 1 | 84.2 分 F1 | 84.2 分 F1 |
| 9668171 | Somatic instability of the CTG repeat in mice transgenic for the myotonic dystrophy region is age dependent bu… | 1 | 93.3 分 F1 | 93.3 分 F1 |
| 9869602 | Prevalence of the I1307K APC gene variant in Israeli Jews of differing ethnic origin and risk for colorectal c… | 1 | 71.4 分 F1 | 64.0 分 F1 |
| 9689113 | A mouse model of severe von Willebrand disease: defects in hemostasis and thrombosis. von Willebrand factor (v… | 1 | 50.0 分 F1 | 50.0 分 F1 |
| 9585611 | Genotype-phenotype correlations in attenuated adenomatous polyposis coli. Germ-line mutations of the tumor sup… | 1 | 87.0 分 F1 | 78.0 分 F1 |
| 9927033 | Human MLH1 deficiency predisposes to hematological malignancy and neurofibromatosis type 1. Heterozygous germ-… | 1 | 57.1 分 F1 | 57.1 分 F1 |
| 9590284 | A mouse model for Prader-Willi syndrome imprinting-centre mutations. Imprinting in the 15q11-q13 region involv… | 1 | 92.3 分 F1 | 92.3 分 F1 |
| 941901 | Low levels of beta hexosaminidase A in healthy individuals with apparent deficiency of this enzyme. Appreciabl… | 1 | 85.7 分 F1 | 85.7 分 F1 |
| 9425239 | Progression of somatic CTG repeat length heterogeneity in the blood cells of myotonic dystrophy patients. The … | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9703418 | Nonsense mutation in exon 4 of human complement C9 gene is the major cause of Japanese complement C9 deficienc… | 1 | 71.4 分 F1 | 71.4 分 F1 |
| 9744473 | The R496H mutation of arylsulfatase A does not cause metachromatic leukodystrophy. Deficiency of arylsulfatase… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9529364 | Identification of constitutional WT1 mutations, in patients with isolated diffuse mesangial sclerosis, and ana… | 1 | 60.6 分 F1 | 60.6 分 F1 |
| 9536083 | The 185delAG BRCA1 mutation originated before the dispersion of Jews in the diaspora and is not limited to Ash… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9400934 | The RB1 gene mutation in a child with ectopic intracranial retinoblastoma. The RB1 gene mutation was investiga… | 1 | 20.0 分 F1 | 20.0 分 F1 |
| 9463309 | The haptoglobin-gene deletion responsible for anhaptoglobinemia. We have found an allelic deletion of the hapt… | 1 | 0.0 分 F1 | 0.0 分 F1 |
| 9448273 | The von Hippel-Lindau tumor suppressor gene is required for cell cycle exit upon serum withdrawal. The inactiv… | 1 | 57.8 分 F1 | 57.8 分 F1 |
| 9852676 | Further evidence for a major ancient mutation underlying myotonic dystrophy from linkage disequilibrium studie… | 1 | 94.7 分 F1 | 94.7 分 F1 |
| 9618170 | Insertional mutation by transposable element, L1, in the DMD gene results in X-linked dilated cardiomyopathy. … | 1 | 28.6 分 F1 | 28.6 分 F1 |
| 9425228 | Prevalence of p16 and CDK4 germline mutations in 48 melanoma-prone families in France. The French Familial Mel… | 1 | 66.7 分 F1 | 66.7 分 F1 |
| 9385378 | A novel common missense mutation G301C in the N-acetylgalactosamine-6-sulfate sulfatase gene in mucopolysaccha… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9311732 | Constitutional RB1-gene mutations in patients with isolated unilateral retinoblastoma. In most patients with i… | 1 | 62.1 分 F1 | 71.0 分 F1 |
| 9702690 | A Japanese family with adrenoleukodystrophy with a codon 291 deletion: a clinical, biochemical, pathological, … | 1 | 69.6 分 F1 | 69.6 分 F1 |
| 9790667 | A novel Arg362Ser mutation in the sterol 27-hydroxylase gene (CYP27): its effects on pre-mRNA splicing and enz… | 1 | 80.0 分 F1 | 80.0 分 F1 |
| 9705283 | Truncation mutations in the transactivation region of PAX6 result in dominant-negative mutants. PAX6 is a tran… | 1 | 83.3 分 F1 | 83.3 分 F1 |
| 9391889 | Paternal transmission of congenital myotonic dystrophy. We report a rare case of paternally transmitted congen… | 1 | 44.4 分 F1 | 42.9 分 F1 |
| 9988281 | Localization of human BRCA1 and its loss in high-grade, non-inherited breast carcinomas. Although the link bet… | 1 | 28.6 分 F1 | 28.6 分 F1 |
| 932197 | Hereditary deficiency of the fifth component of complement in man. I. Clinical, immunochemical, and family stu… | 1 | 96.3 分 F1 | 96.3 分 F1 |
| 9463314 | ATM mutations and phenotypes in ataxia-telangiectasia families in the British Isles: expression of mutant ATM … | 1 | 93.8 分 F1 | 93.8 分 F1 |
| 993342 | The chromosomal order of genes controlling the major histocompatibility complex, properdin factor B, and defic… | 1 | 88.9 分 F1 | 88.9 分 F1 |
| 9585583 | Genetic heterogeneity of Saethre-Chotzen syndrome, due to TWIST and FGFR mutations. Thirty-two unrelated patie… | 1 | 11.8 分 F1 | 11.8 分 F1 |
| 9724771 | The APC variants I1307K and E1317Q are associated with colorectal tumors, but not always with a family history… | 1 | 75.5 分 F1 | 57.8 分 F1 |
| 9563950 | Disruption of splicing regulated by a CUG-binding protein in myotonic dystrophy. Myotonic dystrophy (DM) is ca… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9831355 | I1307K APC and hMLH1 mutations in a non-Jewish family with hereditary non-polyposis colorectal cancer. We desc… | 1 | 42.9 分 F1 | 50.0 分 F1 |
| 9709714 | Reversal of severe hypertrophic cardiomyopathy and excellent neuropsychologic outcome in very-long-chain acyl-… | 1 | 84.2 分 F1 | 84.2 分 F1 |
| 9671401 | A novel missense mutation in patients from a retinoblastoma pedigree showing only mild expression of the tumor… | 1 | 80.0 分 F1 | 80.0 分 F1 |
| 9465301 | Genomic organization of the UBE3A/E6-AP gene and related pseudogenes. The UBE3A gene encodes the E6-AP ubiquit… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9774970 | Stable interaction between the products of the BRCA1 and BRCA2 tumor suppressor genes in mitotic and meiotic c… | 1 | 66.7 分 F1 | 66.7 分 F1 |
| 9439660 | Detection of heterozygous carriers of the ataxia-telangiectasia (ATM) gene by G2 phase chromosomal radiosensit… | 1 | 84.6 分 F1 | 88.0 分 F1 |
| 9427148 | Aspartylglucosaminuria among Palestinian Arabs. Aspartylglucosaminuria (AGU) is a rare disorder of glycoprotei… | 1 | 80.0 分 F1 | 85.7 分 F1 |
| 9949197 | Distribution of emerin and lamins in the heart and implications for Emery-Dreifuss muscular dystrophy. Emerin … | 1 | 92.3 分 F1 | 92.3 分 F1 |
| 9443866 | Ataxia-telangiectasia: identification and detection of founder-effect mutations in the ATM gene in ethnic popu… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9856499 | Complement C7 deficiency: seven further molecular defects and their associated marker haplotypes. Seven furthe… | 1 | 40.0 分 F1 | 40.0 分 F1 |
| 9700175 | Oral contraceptives and the risk of hereditary ovarian cancer. Hereditary Ovarian Cancer Clinical Study Group.… | 1 | 55.6 分 F1 | 55.6 分 F1 |
| 9360520 | Autosomal dominant neurohypophyseal diabetes insipidus associated with a missense mutation encoding Gly23--＞Va… | 1 | 66.7 分 F1 | 66.7 分 F1 |
| 9554743 | Identification of three novel mutations and a high frequency of the Arg778Leu mutation in Korean patients with… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9771706 | A gene encoding a transmembrane protein is mutated in patients with diabetes mellitus and optic atrophy (Wolfr… | 1 | 70.6 分 F1 | 70.6 分 F1 |
| 9863607 | Segregation distortion in myotonic dystrophy. Myotonic dystrophy (DM) is an autosomal dominant disease which, … | 1 | 82.8 分 F1 | 82.8 分 F1 |
| 9714764 | Cloning of a novel member of the low-density lipoprotein receptor family. A gene encoding a novel transmembran… | 1 | 40.0 分 F1 | 40.0 分 F1 |
| 9521325 | Genetic basis and molecular mechanism for idiopathic ventricular fibrillation. Ventricular fibrillation causes… | 1 | 94.7 分 F1 | 94.7 分 F1 |
| 9861003 | A genome-wide search for chromosomal loci linked to mental health wellness in relatives at high risk for bipol… | 1 | 75.0 分 F1 | 75.0 分 F1 |
| 9463318 | The DMPK gene of severely affected myotonic dystrophy patients is hypermethylated proximal to the largely expa… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9729124 | Genomic structure of the human congenital chloride diarrhea (CLD) gene. Congenital chloride diarrhea (CLD) is … | 1 | 30.8 分 F1 | 30.8 分 F1 |
| 9465039 | The hemochromatosis gene product complexes with the transferrin receptor and lowers its affinity for ligand bi… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| 9506545 | Eye movement abnormalities correlate with genotype in autosomal dominant cerebellar ataxia type I. We compared… | 1 | 44.4 分 F1 | 44.4 分 F1 |
| 9391879 | Low frequency of BRCA1 germline mutations in 45 German breast/ovarian cancer families. In this study we invest… | 1 | 100.0 分 F1 | 100.0 分 F1 |
