"""Reproduce scope-review counts and simple dataset shortcut baselines.

Read-only: no model calls, benchmark edits, or changes to the official scorer.
"""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "benchmarks/medical_decision_v1"


def audit():
    review = json.loads((ROOT / "docs/task_scope_review.json").read_text())
    for name, expected in review["reviewed_file_sha256"].items():
        actual = hashlib.sha256((DATA / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Scope review is outdated for {name}; review the changed data first.")
    tasks = json.loads((DATA / "taxonomy.json").read_text())["tasks"]
    assessments = {x["task_id"]: x for x in review["tasks"]}
    if (len(assessments) != len(review["tasks"]) or len(assessments) != len(tasks)
            or set(assessments) != {t["id"] for t in tasks}):
        raise ValueError("Scope review must cover every task exactly once.")
    by_task = defaultdict(list)
    for line in (DATA / "samples.jsonl").read_text().splitlines():
        row = json.loads(line)
        by_task[row["task"]].append(row)
    groups = {}
    for task in tasks:
        tid = task["id"]
        group = assessments[tid]["proposed_group"]
        count = groups.setdefault(group, {"defined_tasks": 0, "populated_tasks": 0, "records": 0})
        count["defined_tasks"] += 1
        count["populated_tasks"] += bool(by_task[tid])
        count["records"] += len(by_task[tid])

    rows = by_task["input_sufficiency"]
    if not rows:
        raise ValueError("No input_sufficiency records to audit.")
    errors = []
    confusion = Counter()
    structure_matches = 0
    for row in rows:
        state = row["request"]["state"]
        # The prediction uses only model-visible input, never gold or provenance.
        documents = "\n".join(d["text"] for d in state["documents"]).casefold()
        prediction = "yes" if state["target_patient"].casefold() in documents else "no"
        confusion[f"gold={row['gold']},prediction={prediction}"] += 1
        if prediction != row["gold"]:
            errors.append(row["id"])
        # Separately inspect construction metadata; this is not a prediction.
        locator = row["provenance"]["locator"]
        target_present = any(k.startswith(locator["patient_key"] + "/") for k in locator["display_document_keys"])
        structure_matches += target_present == (row["gold"] == "yes")
    shortcut = {
        "method": "case-insensitive exact target_patient substring in input documents",
        "records": len(rows),
        "correct": len(rows) - len(errors),
        "accuracy": (len(rows) - len(errors)) / len(rows),
        "confusion": dict(confusion),
        "error_ids": errors,
        "construction_target_document_presence_matches_gold": structure_matches,
    }
    majorities = {}
    for task in tasks:
        tid = task["id"]
        if assessments[tid]["proposed_group"] != "risk" or not by_task[tid]:
            continue
        counts = Counter(row["gold"] for row in by_task[tid])
        label, n = counts.most_common(1)[0]
        majorities[tid] = {
            "records": len(by_task[tid]), "label_counts": dict(counts),
            "sample_majority_label": label,
            "sample_majority_accuracy": n / len(by_task[tid]),
        }
    return {"proposed_groups": groups, "input_sufficiency_shortcut": shortcut,
            "risk_sample_majority_baselines": majorities}


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
