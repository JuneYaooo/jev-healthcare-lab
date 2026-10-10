
LabQAR Dataset for Reference Range Prediction and Lab Result Classification

 Overview

This dataset, LabQAR (Laboratory Question Answering with Reference Ranges), is designed to evaluate the performance of large language models (LLMs) in two crucial clinical reasoning tasks:

1. Reference Range Prediction – Given a lab test, predict the correct SI reference range.
2. Lab Result Classification – Classify a given numeric value as High, Normal, or Low based on contextual factors like specimen type, unit, gender, and age.

The dataset is structured in JSON format and consists of two main sets, each aligned with different types of question-answering tasks to assess LLMs' capabilities in clinical decision support.

---

Dataset Structure

 📁 Set 1: Reference Range Prediction

Task: Predict the correct lower and upper bound SI reference range values.

```json
[
  {
    "ID": 1,
    "Question": "For the lab test 'Acetaminophen' measuring in 'μmol/L' in Specimen 'Serum, plasma' for 'any gender' and 'any age group', what is the correct lower and upper bound range values in SI reference range?",
    "Answer": "70–200"
  }
]
```

 📁 Set 2: Lab Result Classification

Task: Classify a numeric lab test result as `High`, `Normal`, or `Low`.

```json
[  {
    "ID": 1,
    "Question": "For the lab test 'Acetaminophen' measuring in 'μmol/L' in Specimen 'Serum, plasma' for 'any gender' and 'any age group', a value in 'SI reference range' is 341.62. Is the lab test result?",
    "Choices": "\nA: High\nB: Normal\nC: Low",
    "Answer": "A",
    "reference_range": {
      "lower_bound": 70.0,
      "upper_bound": 200.0,
      "unit": "μmol/L"
    }
  }
]
```

---


 📂 Files Included

| Filename                  | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| `set1_reference_range.json` | JSON data for reference range prediction questions                        |
| `set2_classification.json`  | JSON data for lab value classification questions                         |
| `annotation_guidelines.pdf`| Detailed instructions followed by annotators during data curation       |


---
