# CNMLEQA

**CNMLEQA** is a large-scale benchmark dataset for evaluating large language models (LLMs) on the **Chinese National Medical Licensing Examination (CNMLE)**.

This dataset has been officially published in *Scientific Data*:

> Zong H, Cha J, Wang J, Song Y, Zhao Y, Shi M, Shen B. A Dataset for Evaluating Large Language Models on Chinese National Medical Licensing Examinations. Sci Data. 2026 Apr 17. doi: 10.1038/s41597-026-07261-9. PMID: 41998016.



## 🔍 Overview

Large language models have shown strong performance in medical QA and clinical reasoning. However, standardized evaluation benchmarks in non-English medical contexts remain limited.

CNMLEQA addresses this gap by providing a clinically grounded, expert-annotated benchmark for evaluating LLM performance in Chinese medical examinations.

### Key Features

- **Clinically grounded**: Derived from real CNMLE-style questions  
- **Multidimensional annotations**: Enables fine-grained evaluation  
- **Non-English benchmark**: Focused on Chinese medical context  
- **LLM-evaluated**: Tested on state-of-the-art models  



## 📦 Dataset Composition

| Subset         | Questions | Description |
|----------------|-----------|-------------|
| **CNMLEQA-10k** | 9,890     | Full dataset |
| **CNMLEQA-3k**  | 2,949     | Curated high-quality subset |

### Question Format

- Multiple-choice questions (MCQs)
- 5 options (A–E)
- Single correct answer
- Language: Chinese

### Question Types

- Knowledge-based questions
- Case-based clinical questions



## 🧾 Annotation Schema

Each question is annotated with multi-level clinical metadata.

### Core Fields

```json
{
  "id": "unique-id",
  "question": "Question text",
  "opa": "Option A",
  "opb": "Option B",
  "opc": "Option C",
  "opd": "Option D",
  "ope": "Option E",
  "answer": "Correct option",
  "question_type": "Knowledge-based / Case-based",
  "year": "Exam year",
  "source": "Data source"
}
```

### Extended Clinical Annotations

Each question is further annotated across five clinical dimensions:

* Disease / Diagnosis
* Surgery
* Medication
* Laboratory Examination
* Symptom / Sign

All annotations were conducted and verified by clinical experts.


## 📊 Benchmark & Evaluation

We evaluated CNMLEQA using multiple state-of-the-art LLMs, including:

* Gemini
* DeepSeek
* GPT series
* Qwen series
* LLaMA

Key Results

* Qwen2.5-32B: 90.88% (CNMLEQA-10k)
* DeepSeek-R1: 91.59% (CNMLEQA-3k)

Fine-tuning experiments (on Qwen models) further demonstrated significant performance improvements.


## 📥 Data Availability

The dataset is publicly available at:
* Zenodo:  https://zenodo.org/records/18951465
* Github: https://github.com/zonghui0228/CNMLEQA


## 📚 Citation

If you use CNMLEQA in your research, please cite:

1. Zong H, Cha J, Wang J, Song Y, Zhao Y, Shi M, Shen B. **A Dataset for Evaluating Large Language Models on Chinese National Medical Licensing Examinations**. *Scientific Data*. 2026 Apr 17. PMID: [41998016](https://pubmed.ncbi.nlm.nih.gov/41998016/). DOI: [10.1038/s41597-026-07261-9](https://doi.org/10.1038/s41597-026-07261-9).

2. Zong H, Wu R, Cha J, et al. **Large Language Models in Worldwide Medical Exams: Platform Development and Comprehensive Analysis**. *Journal of Medical Internet Research*. 2024;26:e66114. PMID: [39729356](https://pubmed.ncbi.nlm.nih.gov/39729356/) DOI: [10.2196/66114](https://doi.org/doi:10.2196/66114) 

3. Zong H, Li J, Wu E, et al. **Performance of ChatGPT on Chinese national medical licensing examinations: a five-year examination evaluation study for physicians, pharmacists and nurses**. *BMC Medical Education* 24, 143 (2024). PMID: [38355517](https://pubmed.ncbi.nlm.nih.gov/38355517/) DOI: [10.1186/s12909-024-05125-7](https://doi.org/10.1186/s12909-024-05125-7) 


