# PrinciplismQA

<p align="center">
  <a href="https://aclanthology.org/2026.findings-acl.1806/">
    <img src="https://img.shields.io/badge/ACL%20Anthology-2026.findings--acl.1806-blue.svg" alt="ACL Anthology: 2026.findings-acl.1806" />
  </a>
  <a href="https://arxiv.org/abs/2508.05132">
    <img src="https://img.shields.io/badge/arXiv-2508.05132-b31b1b.svg" alt="arXiv:2508.05132" />
  </a>
</p>

This repository hosts the full **PrinciplismQA** dataset, introduced in [*“PrinciplismQA: A Philosophy-Grounded Approach to Assessing LLM-Human Clinical Medical Ethics Alignment”*](https://aclanthology.org/2026.findings-acl.1806/) at Findings of ACL 2026. The original [arXiv preprint](https://arxiv.org/abs/2508.05132) remains available for work-in-progress updates. PrinciplismQA supports assessment of medical ethics knowledge and clinical ethical reasoning through the four principles of biomedical ethics: autonomy, beneficence, non-maleficence, and justice.

---

## 📂 Repository Contents

| File / Folder | Description |
|---|---|
| `data/knowledge-mcqa.json` | 2,182 multiple-choice medical ethics questions, each with four options, an answer, explanation, and principlism annotations. |
| `data/open-ended-qa.json` | 677 clinical cases containing 1,466 open-ended questions and their rubric keypoints. |
| `data/open-ended-rubric-principles.json` | Principlism and ACGME competency annotations for the 1,466 open-ended-question rubrics. |
| `scripts/open_ended_eval.py` | Generates and rubric-scores open-ended responses through an OpenAI-compatible API. |
| `scripts/mcqa_eval.py` | Evaluates MCQA responses, preserves raw model output, handles refusals, and summarizes results. |
| `scripts/evaluation_config.env.example` | Credential-free template with separate MCQA, open-ended answer, and open-ended judge endpoint profiles. |
| `requirements.txt` | Minimal runtime dependencies for the evaluation scripts. |
| `README.md` | This file, describing the complete dataset, usage, and license. |
| `LICENSE` | MIT license (covering the repository and scripts). |

## JSON Schemas

### Knowledge MCQA

`knowledge-mcqa.json` contains multiple-choice questions. Each item uses the following schema:

```json
{
    "id": 37652,
    "question_id": 1,
    "question": "Question title contents",
    "options": {
        "A": "Option A Contents",
        "B": "Option B Contents",
        "C": "Option C Contents",
        "D": "Option D Contents"
    },
    "correct_answer": "A",
    "explanation": "Explanation to the correct answer...",
    "principlism": {
        "autonomy": true,
        "nonmaleficience": false,
        "beneficience": false,
        "justice": false
    }
}
```

`id` is the item identifier and `question_id` is the sequential question identifier. `correct_answer` is one of `"A"`, `"B"`, `"C"`, or `"D"`. The `principlism` object uses the field names present in the released data.

### Open-Ended Questions

`open-ended-qa.json` is organized by clinical case. `id` is the stable case/group identifier. Each individual question under `ethical_issues` has a globally unique `qid`, which joins it to the corresponding record in `open-ended-rubric-principles.json`.

```json
{
    "id": 1,
    "tags": ["Ethics topic defined by JAMA"],
    "title": "Case Title",
    "case": "Case context descriptions...",
    "case_rewrite": "Expanded case context...",
    "ethical_issues": [
      {
        "qid": 1,
        "question": "Question title contents...",
        "keypoints": ["Rubric keypoint..."]
      }
    ]
}
```

### Open-Ended Rubrics

`open-ended-rubric-principles.json` stores the principles and ACGME competencies associated with each open-ended question. Its `id` is the same case/group ID, and its `qid` is the unique question ID shared with the question file.

```json
{
    "id": 1,
    "qid": 1,
    "question": "question title",
    "principles": ["autonomy"],
    "keypoint_competencies": [
        {
            "keypoint": "rubric content",
            "competency": "corresponding ACGME competency"
        }
    ]
}
```

The `qid` values are contiguous from 1 through 1,466. Use `qid` to join an open-ended question to its rubric; do not use the case-level `id` alone because a case can contain multiple questions.

---

## 🎯 Purpose & Use Cases

* **Benchmarking medical ethics knowledge:** assess multiple-choice performance with answers, explanations, and annotations for the four principles of biomedical ethics.
* **Evaluating clinical ethical reasoning:** generate and score open-ended responses against question-specific rubric keypoints, principles, and ACGME competencies.
* **Studying principle-level behavior:** filter items by autonomy, beneficence, non-maleficence, or justice to analyze model strengths, trade-offs, and failure modes.
* **Reproducible research and baselines:** use the full release to establish, compare, and report medical-ethics evaluation results.

The dataset is intended for research, education, and evaluation of clinical AI systems. It is not clinical guidance and should not be used as the sole basis for patient-care decisions.

---

## Usage Instructions

1. Clone or download this repository.
2. Load the JSON files using your preferred JSON library (e.g. Python’s `json`, `orjson`, etc.).
3. For MCQ items, present the four `options` to a model or human annotator and compare the prediction with `correct_answer`.
4. For open-ended items, generate a response for each question and score it against its `keypoints`. Join `open-ended-qa.json` and `open-ended-rubric-principles.json` using `qid` to retrieve its principles and keypoint competencies.
5. Optionally filter knowledge MCQAs by their `principlism` annotations, or filter open-ended rubrics by `principles`, to study principle-specific behavior.

### Recommended Evaluation Scripts

The evaluation scripts require Python 3.10+ and the minimal dependencies listed in `requirements.txt`. They use OpenAI-compatible chat-completions endpoints and read credentials from an environment variable rather than from source code.

```bash
python -m pip install -r requirements.txt
```

Start with `scripts/evaluation_config.env.example` and keep the populated configuration outside version control. It defines separate `MCQA_*`, `OPEN_ENDED_ANSWER_*`, and `OPEN_ENDED_JUDGE_*` values, so MCQA evaluation, open-ended answer generation, and open-ended rubric judging can use different credentials, base URLs, and models.

```bash
source /path/to/evaluation_config.env
```

The examples below pass each profile explicitly. The scripts use the bundled data files by default.

### Open-Ended Evaluation

`scripts/open_ended_eval.py` validates the `qid` join between the question and rubric files before calling a model. The default `both` stage generates an answer and scores it against the corresponding keypoints. Results are checkpointed atomically and the same command resumes completed compatible records. A `tqdm` progress bar reports completed questions, including failed requests.

```bash
# Validate the first three joined questions without API calls.
python scripts/open_ended_eval.py --dry-run --limit 3

# Generate and score ten questions with one model for answers and another for judging.
python scripts/open_ended_eval.py \
  --answer-model "$OPEN_ENDED_ANSWER_MODEL" \
  --answer-base-url "$OPEN_ENDED_ANSWER_BASE_URL" \
  --answer-api-key-env OPEN_ENDED_ANSWER_API_KEY \
  --judge-model "$OPEN_ENDED_JUDGE_MODEL" \
  --judge-base-url "$OPEN_ENDED_JUDGE_BASE_URL" \
  --judge-api-key-env OPEN_ENDED_JUDGE_API_KEY \
  --output results/open_ended_eval.json \
  --limit 10
```

Use `--stage generate` to create answers only, or `--stage score` to score answers already stored in an output file. Use `--qid` repeatedly to select specific questions, `--workers` to control concurrency, and `--force` to rerun records that would otherwise be resumed.

Analyze a completed open-ended result without calling a model:

```bash
python scripts/open_ended_eval.py \
  --analyze results/open_ended_eval.json \
  --summary-output results/open_ended_eval_summary.json
```

The open-ended analyzer reports answer and scoring coverage separately from performance, score totals and normalized scores, the distribution of 0.0/0.5/1.0 keypoint judgments, and breakdowns by principlism principle, ACGME competency, and answer/judge model pair.

### MCQA Evaluation

`scripts/mcqa_eval.py` asks the model for one of `A`, `B`, `C`, or `D` and compares the extracted answer with `correct_answer`. Each completed result always includes `original_response`. When no unambiguous option can be extracted, `model_answer` and `is_correct` are `null`; `response_status` distinguishes `refusal` from `unparseable` responses. A `tqdm` progress bar reports completed questions, including failed requests.

```bash
# Validate the first three MCQA items without API calls.
python scripts/mcqa_eval.py --dry-run --limit 3

# Evaluate five questions and checkpoint each result.
python scripts/mcqa_eval.py \
  --model "$MCQA_MODEL" \
  --base-url "$MCQA_BASE_URL" \
  --api-key-env MCQA_API_KEY \
  --output results/mcqa_eval.json \
  --limit 5 \
  --save-interval 1

# Analyze a completed result without calling a model.
python scripts/mcqa_eval.py \
  --analyze results/mcqa_eval.json \
  --summary-output results/mcqa_eval_summary.json
```

The MCQA analyzer reports overall answer, correctness, refusal, and unparseable-response counts; answer and refusal rates; and accuracy by the principlism annotations stored in the result file.

Do not commit API keys or generated model responses unless their disclosure has been reviewed for your intended use.

For reproducible results, report the data-file version or commit SHA used in an evaluation and cite the accompanying ACL Anthology paper.

---

## 📜 Licensing & Attribution

PrinciplismQA is released under the **MIT License**, a permissive license that allows use, modification, and distribution provided that the copyright and license notices are retained.
For background: the MIT License allows reuse, modification, and distribution with minimal restrictions (so long as you retain copyright and license notices).

Please cite the accompanying paper when you use the dataset in research or derivative work.

## 🙋 Contributions & Issues

* If you find a typo, answer error, question-rubric mismatch, or annotation issue, please open an **issue** in this repository.
* Please describe the affected file and, for open-ended data, include both `id` and `qid` in the issue report.
* Contributions that correct data or improve documentation are welcome through issues and pull requests.

---

If you use this dataset in work, we acknowledge (but do not require) a citation:

```bibtex
@inproceedings{hong-etal-2026-principlismqa,
    title = "{P}rinciplism{QA}: A Philosophy-Grounded Approach to Assessing {LLM}-Human Clinical Medical Ethics Alignment",
    author = "Hong, Chang  and
      Wu, Minghao  and
      Xiao, Qingying  and
      Wang, Yuchi  and
      Wan, Xiang  and
      Yu, Guangjun  and
      Wang, Benyou  and
      Hu, Yan",
    editor = "Liakata, Maria  and
      Moreira, Viviane P.  and
      Zhang, Jiajun  and
      Jurgens, David",
    booktitle = "Findings of the {A}ssociation for {C}omputational {L}inguistics: {ACL} 2026",
    month = jul,
    year = "2026",
    address = "San Diego, California, United States",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.findings-acl.1806/",
    doi = "10.18653/v1/2026.findings-acl.1806",
    pages = "36229--36245",
    ISBN = "979-8-89176-395-1",
    abstract = "As medical LLMs transition to clinical deployment, assessing their ethical reasoning capability becomes critical. While achieving high accuracy on knowledge benchmarks, LLMs lack validated assessment for navigating ethical trade-offs in clinical decision-making where multiple valid solutions exist. Existing benchmarks lack systematic approaches to incorporate recognized philosophical frameworks and expert validation for ethical reasoning assessment. We introduce PrinciplismQA, a philosophy-grounded approach to assessing LLM clinical medical ethics alignment. Grounded in Principlism, our approach provides a systematic methodology for incorporating clinical ethics philosophy into LLM assessment design. PrinciplismQA comprises 3,648 expert-validated questions spanning knowledge assessment and clinical reasoning. Our expert-calibrated pipeline enables reproducible evaluation and models ethical biases. Evaluating recent models reveals significant ethical reasoning gaps despite high knowledge accuracy, demonstrating that knowledge-oriented training does not ensure clinical ethical alignment. PrinciplismQA provides a validated tool for assessing clinical AI deployment readiness."
}
```
