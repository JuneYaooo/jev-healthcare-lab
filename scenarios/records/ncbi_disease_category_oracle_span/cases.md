# 给定疾病实体类别：逐案例结果

60 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| 9950360 | {"abstract": "Molecular analysis of the APC gene in 205 families: extended genotype-phenotype correlations in … | 3 | 0.0% | 0.0% |
| 9585611 | {"abstract": "Genotype-phenotype correlations in attenuated adenomatous polyposis coli. Germ-line mutations of… | 2 | 50.0% | 0.0% |
| 9288106 | {"abstract": "Clustering of missense mutations in the ataxia-telangiectasia gene in a sporadic T-cell leukaemi… | 4 | 75.0% | 100.0% |
| 9790667 | {"abstract": "A novel Arg362Ser mutation in the sterol 27-hydroxylase gene (CYP27): its effects on pre-mRNA sp… | 1 | 0.0% | 100.0% |
| 9391889 | {"abstract": "Paternal transmission of congenital myotonic dystrophy. We report a rare case of paternally tran… | 2 | 100.0% | 100.0% |
| 993342 | {"abstract": "The chromosomal order of genes controlling the major histocompatibility complex, properdin facto… | 3 | 100.0% | 100.0% |
| 9563950 | {"abstract": "Disruption of splicing regulated by a CUG-binding protein in myotonic dystrophy. Myotonic dystro… | 2 | 0.0% | 0.0% |
| 9439660 | {"abstract": "Detection of heterozygous carriers of the ataxia-telangiectasia (ATM) gene by G2 phase chromosom… | 2 | 0.0% | 0.0% |
| 9927033 | {"abstract": "Human MLH1 deficiency predisposes to hematological malignancy and neurofibromatosis type 1. Hete… | 3 | 66.7% | 66.7% |
| 9585606 | {"abstract": "The hemochromatosis 845 G--＞A and 187 C--＞G mutations: prevalence in non-Caucasian populations. … | 1 | 0.0% | 100.0% |
| 9709714 | {"abstract": "Reversal of severe hypertrophic cardiomyopathy and excellent neuropsychologic outcome in very-lo… | 3 | 66.7% | 66.7% |
| 9705283 | {"abstract": "Truncation mutations in the transactivation region of PAX6 result in dominant-negative mutants. … | 1 | 100.0% | 100.0% |
| 9450866 | {"abstract": "Piebaldism with deafness: molecular evidence for an expanded syndrome. In a South African girl o… | 1 | 100.0% | 100.0% |
| 9311732 | {"abstract": "Constitutional RB1-gene mutations in patients with isolated unilateral retinoblastoma. In most p… | 1 | 0.0% | 0.0% |
| 9843038 | {"abstract": "Identification of a novel mutation of the CPO gene in a Japanese hereditary coproporphyria famil… | 1 | 100.0% | 100.0% |
| 9888388 | {"abstract": "Systematic analysis of coproporphyrinogen oxidase gene defects in hereditary coproporphyria and … | 1 | 100.0% | 100.0% |
| 9600235 | {"abstract": "Mutations of the ATM gene detected in Japanese ataxia-telangiectasia patients: possible preponde… | 1 | 100.0% | 100.0% |
| 9689113 | {"abstract": "A mouse model of severe von Willebrand disease: defects in hemostasis and thrombosis. von Willeb… | 2 | 50.0% | 100.0% |
| 9580132 | {"abstract": "Identification of a novel nonsense mutation and a missense substitution in the vasopressin-neuro… | 1 | 0.0% | 0.0% |
| 9988281 | {"abstract": "Localization of human BRCA1 and its loss in high-grade, non-inherited breast carcinomas. Althoug… | 2 | 50.0% | 50.0% |
| 9702690 | {"abstract": "A Japanese family with adrenoleukodystrophy with a codon 291 deletion: a clinical, biochemical, … | 2 | 0.0% | 0.0% |
| 9831355 | {"abstract": "I1307K APC and hMLH1 mutations in a non-Jewish family with hereditary non-polyposis colorectal c… | 2 | 50.0% | 50.0% |
| 9294109 | {"abstract": "Myotonic dystrophy protein kinase is involved in the modulation of the Ca2+ homeostasis in skele… | 1 | 0.0% | 0.0% |
| 9497246 | {"abstract": "Genetic heterogeneity and penetrance analysis of the BRCA1 and BRCA2 genes in breast cancer fami… | 2 | 100.0% | 100.0% |
| 9448273 | {"abstract": "The von Hippel-Lindau tumor suppressor gene is required for cell cycle exit upon serum withdrawa… | 2 | 50.0% | 50.0% |
| 9443866 | {"abstract": "Ataxia-telangiectasia: identification and detection of founder-effect mutations in the ATM gene … | 2 | 50.0% | 50.0% |
| 932197 | {"abstract": "Hereditary deficiency of the fifth component of complement in man. I. Clinical, immunochemical, … | 3 | 66.7% | 66.7% |
| 9861003 | {"abstract": "A genome-wide search for chromosomal loci linked to mental health wellness in relatives at high … | 1 | 100.0% | 100.0% |
| 9792860 | {"abstract": "Determination of the genomic structure of the COL4A4 gene and of novel mutations causing autosom… | 1 | 0.0% | 0.0% |
| 9585583 | {"abstract": "Genetic heterogeneity of Saethre-Chotzen syndrome, due to TWIST and FGFR mutations. Thirty-two u… | 3 | 100.0% | 100.0% |
| 9863607 | {"abstract": "Segregation distortion in myotonic dystrophy. Myotonic dystrophy (DM) is an autosomal dominant d… | 1 | 100.0% | 100.0% |
| 9700175 | {"abstract": "Oral contraceptives and the risk of hereditary ovarian cancer. Hereditary Ovarian Cancer Clinica… | 2 | 0.0% | 50.0% |
| 9724771 | {"abstract": "The APC variants I1307K and E1317Q are associated with colorectal tumors, but not always with a … | 2 | 0.0% | 0.0% |
| 9521325 | {"abstract": "Genetic basis and molecular mechanism for idiopathic ventricular fibrillation. Ventricular fibri… | 2 | 100.0% | 100.0% |
| 9467011 | {"abstract": "Mutation spectrum and genotype-phenotype analyses in Cowden disease and Bannayan-Zonana syndrome… | 2 | 50.0% | 50.0% |
| 9603435 | {"abstract": "W474C amino acid substitution affects early processing of the alpha-subunit of beta-hexosaminida… | 1 | 100.0% | 100.0% |
| 9931324 | {"abstract": "Missense mutations in the most ancient residues of the PAX6 paired domain underlie a spectrum of… | 1 | 0.0% | 0.0% |
| 9427148 | {"abstract": "Aspartylglucosaminuria among Palestinian Arabs. Aspartylglucosaminuria (AGU) is a rare disorder … | 2 | 100.0% | 100.0% |
| 9671401 | {"abstract": "A novel missense mutation in patients from a retinoblastoma pedigree showing only mild expressio… | 3 | 0.0% | 0.0% |
| 9731533 | {"abstract": "The APCI1307K allele and cancer risk in a community-based study of Ashkenazi Jews. Mutations in … | 2 | 100.0% | 100.0% |
| 9800909 | {"abstract": "Are Dp71 and Dp140 brain dystrophin isoforms related to cognitive impairment in Duchenne muscula… | 1 | 100.0% | 100.0% |
| 9744473 | {"abstract": "The R496H mutation of arylsulfatase A does not cause metachromatic leukodystrophy. Deficiency of… | 3 | 100.0% | 100.0% |
| 9674903 | {"abstract": "Maternal disomy and Prader-Willi syndrome consistent with gamete complementation in a case of fa… | 1 | 100.0% | 100.0% |
| 9425239 | {"abstract": "Progression of somatic CTG repeat length heterogeneity in the blood cells of myotonic dystrophy … | 1 | 0.0% | 0.0% |
| 9536083 | {"abstract": "The 185delAG BRCA1 mutation originated before the dispersion of Jews in the diaspora and is not … | 1 | 100.0% | 100.0% |
| 9973276 | {"abstract": "Inherited colorectal polyposis and cancer risk of the APC I1307K polymorphism. Germ-line and som… | 2 | 50.0% | 0.0% |
| 9888390 | {"abstract": "Coincidence of two novel arylsulfatase A alleles and mutation 459+1G＞A within a family with meta… | 2 | 0.0% | 0.0% |
| 9400934 | {"abstract": "The RB1 gene mutation in a child with ectopic intracranial retinoblastoma. The RB1 gene mutation… | 1 | 100.0% | 100.0% |
| 9729124 | {"abstract": "Genomic structure of the human congenital chloride diarrhea (CLD) gene. Congenital chloride diar… | 1 | 0.0% | 0.0% |
| 9336417 | {"abstract": "Susceptibility to ankylosing spondylitis in twins: the role of genes, HLA, and the environment. … | 1 | 100.0% | 100.0% |
| 9949209 | {"abstract": "Genetic mapping of the copper toxicosis locus in Bedlington terriers to dog chromosome 10, in a … | 2 | 50.0% | 50.0% |
| 9674906 | {"abstract": "Schwartz-Jampel syndrome type 2 and Stuve-Wiedemann syndrome: a case for \"lumping\". Recent stu… | 2 | 50.0% | 50.0% |
| 9529364 | {"abstract": "Identification of constitutional WT1 mutations, in patients with isolated diffuse mesangial scle… | 1 | 100.0% | 100.0% |
| 9585605 | {"abstract": "Mutation analysis of UBE3A in Angelman syndrome patients. Angelman syndrome (AS) is caused by ch… | 1 | 0.0% | 0.0% |
| 9371490 | {"abstract": "Frequent inactivation of PTEN/MMAC1 in primary prostate cancer. Sporadic prostate carcinoma is t… | 1 | 100.0% | 100.0% |
| 9618166 | {"abstract": "Two frequent missense mutations in Pendred syndrome. Pendred syndrome is an autosomal recessive … | 1 | 100.0% | 100.0% |
| 9506545 | {"abstract": "Eye movement abnormalities correlate with genotype in autosomal dominant cerebellar ataxia type … | 1 | 100.0% | 100.0% |
| 9382108 | {"abstract": "Risk reversals in predictive testing for Huntington disease. The first predictive testing for Hu… | 1 | 100.0% | 100.0% |
| 9472666 | {"abstract": "Molecular defects leading to human complement component C6 deficiency in an African-American fam… | 1 | 100.0% | 100.0% |
| 9848786 | {"abstract": "Human complement factor H deficiency associated with hemolytic uremic syndrome. This study repor… | 1 | 100.0% | 100.0% |
