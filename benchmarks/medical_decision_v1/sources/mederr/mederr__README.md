# MedErrBench_dataset


## 📁 Dataset Structure

The dataset is organized as follows:

```

datasets/
├── train/
│   ├── reviewed_ARA_train.csv
│   ├── reviewed_EN_train.csv
│   └── reviewed_CN_train.csv
├── validation/
│   ├── reviewed_ARA_validation.csv
│   ├── reviewed_EN_validation.csv
│   └── reviewed_CN_validation.csv
└── test/
│   ├── reviewed_ARA_test.csv
│   │── reviewed_EN_test.csv
└   │── reviewed_CN_test.csv

```

Each file corresponds to one language and one data split.

## 📄 Data Description

Each CSV file contains annotated clinical or medically themed texts with rich metadata for linguistic and reasoning analysis. The standard format of the datasets contain the following columns:

- `Text ID`: Unique identifier for each entry (e.g., ara-test-0, ara-test-1)
- `Text`: A complete clinical notes, which may or may not contain an error
- `Sentences`: The text split into sentences, each with an index (e.g., 0,1,2…)
- `Error Flag`: Indicates if an error is present: 1 = error present, 0 = no error
- `Error Sentence ID`: Index of the sentence containing the error (corresponding to Sentences); -1 if no error
- `Error Sentence`: The sentence containing the error
- `Error Type`: Type of error (e.g., diagnosis, treatment); NA if no error
- `Corrected Sentence`: The medically correct version of the erroneous sentence
- `Corrected Text`: The full corrected paragraph including the revised sentence
- `Important Words`: Key medical terms or clues that determine the presence of the error
- `Difficulty`: Level of complexity or challenge (Easy, Medium, or Hard)
- `Reasoning Type`: Type of reasoning required  (Factual recall, Multi-hop, or Single-hop)

**Note:**  
The Arabic dataset (`reviewed_ARA.csv` in each split) includes one additional column:

- `Question Type`: Specifies the nature of the question (Knowledge-based question or Scenario-based question)

## 🌐 Languages

- **Arabic**: Standard format, plus Question Type
- **English**: Standard format 
- **Chinese**: Standard format 



