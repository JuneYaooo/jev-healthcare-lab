"""Build and score the decision-only medical benchmark. Standard library, no API calls.

The source lock, taxonomy, and adapters are versioned separately from old results.
Labels are copied or mechanically mapped from upstream annotations, never generated.
"""
from __future__ import annotations

import argparse
import ast
import collections
import csv
import hashlib
import io
import json
import re
import tarfile
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "benchmarks/medical_decision_v1"
CACHE = ROOT / "work/decision-benchmark-v1/raw"
SEED = 20261010


def dumps(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(dumps(value).encode()).hexdigest()


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(dumps(row) + "\n" for row in rows))


def read_jsonl(path):
    with path.open() as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def norm(text):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", text)).casefold()


def strings(value):
    if isinstance(value, str):
        yield value
        # SFT user messages often wrap the material in serialized JSON.
        if value.lstrip().startswith(("{", "[")):
            try:
                yield from strings(json.loads(value))
            except (ValueError, RecursionError):
                pass
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def signatures(value):
    """Exact material (including short questions) plus three 160-character windows."""
    result = set()
    for text in strings(value):
        text = norm(text)
        if len(text) < 24:
            continue
        result.add(digest(text))
        if len(text) >= 160:
            for start in {0, (len(text) - 160) // 2, len(text) - 160}:
                result.add(digest(text[start:start + 160]))
    return result


def chinese_exam_task(question):
    """Conservative question-intent filter, not a clinical answer generator."""
    if len(question) < 60 or not re.search(r"患者|患儿|病人|\d+\s*岁", question):
        return None
    if re.search(r"如图|见图|图示|上图|下图|附图|见表|如下表|如下图|(?:CT|心电图|胸片|影像|图像).{0,6}如下", question):
        return None
    end = question.rstrip("。！？?\n（）() ")
    tail = re.split(r"[。；;！？?\n]", end)[-1][-35:]
    if re.search(r"不正确|错误|不宜|不适宜|不适合|不应|不能|不包括|不支持|不考虑|不可能|不是|不属于|最不|除外|表现|机制|疗程|时间|不良反应|原则|剂量|途径|频次|频率|治疗目标|治疗目的|多长|多少", tail):
        return None
    if re.search(r"药物|用药|抗生素|方剂", tail) and re.search(r"首选|选用|宜用|选择|最适宜|最合适|最佳", tail):
        return "medication_choice"
    if ("检查" in tail and re.search(r"首选|进一步|确诊|明确诊断|最有价值|最有助|最重要", tail)
            and not re.search(r"检查结果|检查发现|检查示", tail)):
        return "examination_choice"
    if (not re.search(r"护理|依据|根据", tail)
            and re.search(r"(?:最可能|最有可能|初步|首先考虑|应考虑|可能的).{0,8}诊断|诊断(?:是|为|应为|可能为|首先考虑)", tail)):
        return "diagnosis_choice"
    if (not re.search(r"护理|心理|宣教|沟通", tail) and re.search(r"治疗|处理|措施|手术", tail)
            and re.search(r"首选|最佳|最有效|最合适|最适宜|首先|选择|采取|立即", tail)):
        return "treatment_choice"
    return None


def join_cmb_answers(questions, answers):
    """Join on original ID and verify metadata; never rely on row order."""
    index = {}
    for position, answer in enumerate(answers):
        if answer["id"] in index:
            raise ValueError("Duplicate CMB answer ID")
        index[answer["id"]] = (position, answer)
    seen = set()
    for position, question in enumerate(questions):
        uid = question["id"]
        if uid in seen or uid not in index:
            raise ValueError("Duplicate or unmatched CMB question ID")
        seen.add(uid)
        answer_position, answer = index[uid]
        if any(question[key] != answer[key] for key in ["exam_type", "exam_class", "exam_subject", "question_type"]):
            raise ValueError("CMB question/answer metadata mismatch")
        yield position, answer_position, question, answer
    if seen != set(index):
        raise ValueError("Unmatched CMB answer ID")


def fetch(config, cache):
    cache.mkdir(parents=True, exist_ok=True)
    lock = json.loads((config / "sources.lock.json").read_text())
    for entry in lock["files"]:
        path = cache / entry["name"]
        if path.exists() and file_sha(path) == entry["sha256"]:
            continue
        request = urllib.request.Request(entry["url"], headers={"User-Agent": "Jev-Medical-Decision-Benchmark"})
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
        if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
            raise ValueError("Source hash changed; refusing replacement: " + entry["name"])
        path.write_bytes(raw)
    print("Verified", len(lock["files"]), "source files")


class Builder:
    def __init__(self, config, cache):
        self.config, self.cache = config, cache
        self.taxonomy = json.loads((config / "taxonomy.json").read_text())
        self.tasks = {x["id"]: x for x in self.taxonomy["tasks"]}
        self.sources = {x["id"]: x for x in json.loads((config / "sources.json").read_text())["sources"]}
        self.lock = {x["name"]: x for x in json.loads((config / "sources.lock.json").read_text())["files"]}
        self.pools = collections.defaultdict(list)
        self.exclusions = collections.Counter()

    def path(self, name):
        path = self.cache / name
        if file_sha(path) != self.lock[name]["sha256"]:
            raise ValueError("Unverified source: " + name)
        return path

    def csv(self, name):
        return list(csv.DictReader(io.StringIO(self.path(name).read_text(encoding="utf-8-sig"))))

    def add(self, task, source, uid, group, state, criteria, gold, file, locator,
            split, language="en", stratum=None, **metadata):
        criteria = {str(k): str(v) for k, v in criteria.items()}
        gold = str(gold)
        if gold not in criteria or len(criteria) < 2:
            raise ValueError((task, uid, "invalid target or vocabulary"))
        request = {"state": state, "questions": {"decision": {
            "type": "choice", "instructions": self.tasks[task]["definition"], "criteria": criteria}}}
        card, resource = self.sources[source], self.lock[file]
        self.pools[task].append({
            "id": task + ":" + source + ":" + str(uid), "task": task,
            "dimension": self.tasks[task]["dimension"], "decision_mode": self.tasks[task]["decision_mode"],
            "primary_scenario": self.tasks[task]["primary_scenario"],
            "ability_tags": self.tasks[task]["ability_tags"],
            "decision_stage": self.tasks[task]["decision_stage"],
            "language": language, "group_id": source + ":" + str(group),
            "request": request, "gold": gold, "request_sha256": digest(request),
            "provenance": {"source_id": source, "source_url": card["url"],
                "upstream_id": str(uid), "upstream_group": str(group), "split": split,
                "resource": file, "resource_url": resource["url"], "resource_sha256": resource["sha256"],
                "version": resource["version"], "locator": locator,
                "data_license": card["data_license"], "distribution": card["distribution"],
                "material_kind": card["material_kind"], "gold_origin": "upstream_annotation",
                "independent_clinical_review": False},
            "metadata": metadata, "sampling_stratum": str(stratum if stratum is not None else gold)})

    def errors(self):
        for sid, name, language in [
            ("medec", "medec__MEDEC-MS_MEDEC-MS-TestSet-with-GroundTruth-and-ErrorType.csv", "en"),
            ("mederr", "mederr__datasets_test_reviewed_data_CN_test.csv", "zh")]:
            for i, row in enumerate(self.csv(name)):
                if row["Error Flag"] not in {"0", "1"}:
                    self.exclusions[sid + ":missing_error_gold"] += 1
                    continue
                uid = row["Text ID"]
                common = dict(file=name, locator={"csv_row": i + 2, "text_id": uid}, split="official_test", language=language)
                self.add("clinical_error_detection", sid, uid, uid, {"clinical_text": row["Text"]},
                         {"0": "No annotated medical error", "1": "Contains an annotated medical error"},
                         row["Error Flag"], stratum=sid + ":" + row["Error Flag"], **common)
                if row["Error Flag"] != "1":
                    continue
                sentences = {}
                for line in row["Sentences"].splitlines():
                    match = re.fullmatch(r"\s*(\d+)\s+(.+)", line)
                    if match:
                        sentences[match[1]] = match[2]
                target = row["Error Sentence ID"].strip()
                if target not in sentences or len(sentences) < 2:
                    self.exclusions[sid + ":unparseable_sentence_id"] += 1
                    continue
                self.add("clinical_error_location", sid, uid, uid,
                         {"clinical_text": row["Text"], "sentences": sentences},
                         {key: "Sentence " + key for key in sentences}, target,
                         stratum=sid, **common)

    def sections(self):
        # Fixed semantic groups, based on upstream section headings, not the correct option.
        groups = {
            "history": ["CHIEF COMPLAINT", "HISTORY OF PRESENT ILLNESS", "PAST MEDICAL HISTORY", "PAST SURGICAL HISTORY", "SOCIAL HISTORY", "FAMILY HISTORY", "REVIEW OF SYSTEMS", "MEDICATIONS", "ALLERGIES"],
            "exam": ["PHYSICAL EXAMINATION", "PHYSICAL EXAM", "VITALS", "VITAL SIGNS"],
            "results": ["RESULTS", "LABORATORY RESULTS", "LABORATORY DATA", "IMAGING", "LABS"],
            "assessment_plan": ["ASSESSMENT", "PLAN", "ASSESSMENT AND PLAN", "ASSESSMENT/PLAN"]}
        mapping = {name: group for group, names in groups.items() for name in names}
        criteria = {"history": "History, symptoms, medications or allergies", "exam": "Physical examination or vital signs",
                    "results": "Laboratory, imaging or diagnostic results", "assessment_plan": "Assessment or plan"}
        for file in sorted(self.lock):
            if not file.startswith("aci_bench__data_") or not file.endswith(".csv"):
                continue
            for i, row in enumerate(self.csv(file)):
                note = row["note"]
                headings = list(re.finditer(r"(?m)^([A-Z][A-Z /&-]{2,}):?\s*$", note))
                for j, heading in enumerate(headings):
                    name = heading[1].strip()
                    end = headings[j + 1].start() if j + 1 < len(headings) else len(note)
                    text = note[heading.end():end].strip()
                    if name not in mapping or len(norm(text)) < 30:
                        self.exclusions["aci:unmapped_or_short_section"] += 1
                        continue
                    uid = row["encounter_id"] + ":" + str(j)
                    self.add("note_section", "aci_bench", uid, row["encounter_id"], {"section_text": text},
                             criteria, mapping[name], file, {"csv_row": i + 2, "encounter_id": row["encounter_id"], "heading": name},
                             "official_test_1_2_3", adaptation="Removed original heading; mapped section titles into four fixed categories.")

    def medquad(self):
        file = "medquad.zip"
        # Same twelve-category intent vocabulary for all examples; no reference answer sent.
        labels = ["information", "symptoms", "treatment", "prevention", "causes", "exams and tests", "susceptibility", "outlook", "complications", "inheritance", "frequency", "research"]
        criteria = {x: x for x in labels}
        with zipfile.ZipFile(self.path(file)) as archive:
            for member in sorted(archive.namelist()):
                if not member.endswith(".xml"):
                    continue
                root = ET.fromstring(archive.read(member))
                source_url = root.attrib.get("url", "")
                for qa in root.findall(".//QAPair"):
                    question = qa.find("Question")
                    if question is None or not question.text:
                        continue
                    label = question.attrib.get("qtype", "")
                    if label not in criteria:
                        self.exclusions["medquad:outside_fixed_intent_vocabulary"] += 1
                        continue
                    uid = member + ":" + qa.attrib.get("pid", "")
                    self.add("query_intent", "medquad", uid, source_url or member,
                             {"question": question.text}, criteria, label, file,
                             {"zip_member": member, "qa_pid": qa.attrib.get("pid"), "original_page": source_url},
                             "published_corpus_no_official_split")

    def longhealth(self):
        file = "longhealth__data_benchmark_v5.json"
        for pid, patient in json.loads(self.path(file).read_text()).items():
            for q in patient["questions"]:
                criteria = {key: q["answer_" + key] for key in "abcde"}
                matches = [key for key, value in criteria.items() if value == q["correct"]]
                if len(matches) != 1:
                    self.exclusions["longhealth:nonunique_correct_option"] += 1
                    continue
                self.add("long_record_evidence", "longhealth", pid + ":" + str(q["No"]), pid,
                         {"documents": patient["texts"], "question": q["question"]}, criteria, matches[0],
                         file, {"patient_key": pid, "question_No": q["No"]}, "published_benchmark",
                         stratum=pid, fictional_patient=True)

    def medcalc(self):
        file = "medcalc__datasets_test_data.csv"
        ranges = {"21": (3, 15), "45": (0, 5), "51": (0, 4), "4": (0, 9), "33": (0, 5)}
        for i, row in enumerate(self.csv(file)):
            cid = row["Calculator ID"]
            if cid not in ranges:
                continue
            low, high = ranges[cid]
            try:
                value = float(row["Ground Truth Answer"])
                if value != int(value) or not low <= value <= high:
                    raise ValueError()
            except ValueError:
                self.exclusions["medcalc:out_of_range_gold"] += 1
                continue
            criteria = {str(j): str(j) for j in range(low, high + 1)}
            self.add("bounded_score", "medcalc", row["Row Number"], row["Note ID"],
                     {"patient_note": row["Patient Note"], "question": row["Question"]}, criteria, str(int(value)),
                     file, {"csv_row": i + 2, "row_number": row["Row Number"], "note_id": row["Note ID"]},
                     "official_github_test", stratum=cid, calculator=row["Calculator Name"],
                     note_type=row["Note Type"], note="Uses original GitHub release, not the inaccessible HF Verified file.")

    def trialgpt(self):
        file = "trialgpt__dataset_sigir_retrieved_trials.json"
        criteria = {"0": "Irrelevant: would not refer", "1": "Potential: consider referral after further investigation", "2": "Eligible: highly likely to refer"}
        for patient in json.loads(self.path(file).read_text()):
            for label in criteria:
                for trial in patient[label]:
                    uid = patient["patient_id"] + ":" + trial["NCTID"]
                    state = {"patient": patient["patient"], "trial": {k: trial[k] for k in ["brief_title", "brief_summary", "inclusion_criteria", "exclusion_criteria"]}}
                    self.add("trial_referral", "trialgpt", uid, patient["patient_id"], state, criteria, label,
                             file, {"patient_id": patient["patient_id"], "nct_id": trial["NCTID"], "relevance": label},
                             "sigir_judged_pool", trial_id=trial["NCTID"], grouping_unit="synthetic_patient")

    def ddi(self):
        file = "ddi__DDICorpus-2013.zip"
        criteria = {"none": "No annotated interaction", "mechanism": "Pharmacokinetic mechanism", "effect": "Pharmacodynamic effect", "advise": "Advice or recommendation about joint use", "int": "Interaction without specified mechanism or effect"}
        with zipfile.ZipFile(self.path(file)) as archive:
            for member in sorted(archive.namelist()):
                if "Test for DDI Extraction task" not in member or not member.endswith(".xml"):
                    continue
                doc = ET.fromstring(archive.read(member))
                for sentence in doc.findall("sentence"):
                    entities = {x.attrib["id"]: x.attrib for x in sentence.findall("entity")}
                    for pair in sentence.findall("pair"):
                        p = pair.attrib
                        label = p.get("type") if p.get("ddi") == "true" else "none"
                        if label not in criteria:
                            self.exclusions["ddi:unknown_label"] += 1
                            continue
                        state = {"sentence": sentence.attrib["text"], "drug_1": entities[p["e1"]]["text"], "drug_2": entities[p["e2"]]["text"]}
                        self.add("drug_interaction", "ddi", p["id"], doc.attrib["id"], state, criteria, label,
                                 file, {"zip_member": member, "pair_id": p["id"]}, "official_test")

    def nubes(self):
        criteria = {"negative": "Negated or absent", "uncertain": "Possible or uncertain"}
        for file in sorted(self.lock):
            if not file.startswith("nubes__NUBes_") or not file.endswith(".ann"):
                continue
            text_file = file[:-4] + ".txt"
            text = self.path(text_file).read_text()
            ents, relations = brat(self.path(file).read_text())
            for rid, kind, left, right in relations:
                if kind != "Scope" or left not in ents or right not in ents:
                    continue
                cue, target = ents[left], ents[right]
                label = "negative" if cue["type"].startswith("Neg") else "uncertain" if cue["type"].startswith("Uncert") else None
                if label is None:
                    continue
                low = min(cue["start"], target["start"])
                high = max(cue["end"], target["end"])
                start = text.rfind("\n", 0, low) + 1
                end = text.find("\n", high)
                end = len(text) if end == -1 else end
                excerpt = text[start:end]
                if "\n" in excerpt or not valid_span(text, target) or not valid_span(text, cue):
                    self.exclusions["nubes:discontinuous_or_cross_sentence"] += 1
                    continue
                self.add("assertion_scope", "nubes", file + ":" + rid, digest([file, start]),
                         {"excerpt": excerpt, "target": target["text"]}, criteria, label,
                         file, {"relation_id": rid, "target_id": right, "text_resource": text_file, "sentence_start": start},
                         "SAMPLE-001_no_official_patient_split", language="es", grouping_unit="shuffled_sentence_not_patient")

    def chia(self):
        file = "chia_without_scope.zip"
        entity_types = ["Condition", "Drug", "Procedure", "Measurement", "Observation", "Device", "Person", "Temporal", "Value", "Qualifier", "Negation", "Reference_point", "Multiplier", "Mood", "Visit"]
        relation_types = ["Has_value", "Has_temporal", "Has_qualifier", "Has_context", "Has_negation", "Has_index", "Has_multiplier", "Has_mood", "Subsumes"]
        with zipfile.ZipFile(self.path(file)) as archive:
            for member in sorted(archive.namelist()):
                if not member.endswith(".ann"):
                    continue
                text = archive.read(member[:-4] + ".txt").decode("utf-8-sig")
                raw_ann = archive.read(member).decode("utf-8-sig")
                ents, relations = brat(raw_ann)
                group = Path(member).name.split("_")[0]
                common = dict(file=file, split="published_corpus_no_official_split")
                for eid, entity in ents.items():
                    if entity["type"] not in entity_types or not valid_span(text, entity):
                        continue
                    self.add("criterion_entity_type", "chia", member + ":" + eid, group,
                             {"criteria_text": text, "target": entity["text"], "start": entity["start"], "end_exclusive": entity["end"]},
                             {x: x for x in entity_types}, entity["type"], locator={"zip_member": member, "entity_id": eid}, **common)
                # BRAT equivalence-style OR groups contain two or more arguments.
                for line_no, line in enumerate(raw_ann.splitlines()):
                    parts = line.split()
                    if len(parts) >= 4 and parts[:2] == ["*", "OR"]:
                        args = parts[2:]
                        for i, left in enumerate(args):
                            for right in args[i + 1:]:
                                relations.append(("OR-" + str(line_no) + "-" + left + "-" + right, "OR", left, right))
                pair_labels = collections.defaultdict(set)
                for _, kind, left, right in relations:
                    pair_labels[(left, right)].add(kind)
                for rid, kind, left, right in relations:
                    if left not in ents or right not in ents or len(pair_labels[(left, right)]) != 1:
                        continue
                    a, b = ents[left], ents[right]
                    if not valid_span(text, a) or not valid_span(text, b):
                        continue
                    task = "criterion_boolean" if kind in {"AND", "OR"} else "criterion_relation"
                    vocabulary = ["AND", "OR"] if task == "criterion_boolean" else relation_types
                    if kind not in vocabulary:
                        continue
                    state = {"criteria_text": text, "entity_1": {k: a[k] for k in ["text", "start", "end"]}, "entity_2": {k: b[k] for k in ["text", "start", "end"]}}
                    self.add(task, "chia", member + ":" + rid, group, state, {x: x for x in vocabulary}, kind,
                             locator={"zip_member": member, "relation_id": rid, "entity_ids": [left, right]},
                             annotation_scope="Only upstream annotated positive relations; no synthetic no-relation negatives.", **common)

    def frd(self):
        file = "frd__data_ner_test_processed_medical_ner.tsv"
        for i, line in enumerate(self.path(file).read_text().splitlines()):
            annotations, text = line.split("\t", 1)
            for j, annotation in enumerate(annotations.split(",")):
                start, end, kind = annotation.split(":")
                if kind not in {"upper_bound", "lower_bound"}:
                    continue
                start, end = int(start) - 1, int(end) - 1
                if not 0 <= start < end <= len(text):
                    self.exclusions["frd:invalid_span"] += 1
                    continue
                self.add("criterion_bound", "frd", str(i + 1) + ":" + str(j), digest(norm(text)),
                         {"criterion": text, "target": text[start:end], "start": start, "end_exclusive": end},
                         {"upper_bound": "Upper bound / maximum", "lower_bound": "Lower bound / minimum"}, kind,
                         file, {"line": i + 1, "annotation_index": j, "original_annotation": annotation},
                         "official_test", grouping_unit="criterion_NCT_not_in_processed_release", normalized_numbers=True)

    def scifact(self):
        file = "scifact__data.tar.gz"
        with tarfile.open(self.path(file)) as archive:
            def rows(suffix):
                member = next(x for x in archive.getnames() if x.endswith(suffix))
                return [json.loads(line) for line in archive.extractfile(member) if line.strip()]
            corpus = {str(x["doc_id"]): x for x in rows("corpus.jsonl")}
            train = rows("claims_train.jsonl")
            train_docs = {str(doc) for claim in train for doc in claim["cited_doc_ids"]}
            for claim in rows("claims_dev.jsonl"):
                for doc_id in claim["cited_doc_ids"]:
                    doc_id = str(doc_id)
                    if doc_id in train_docs:
                        self.exclusions["scifact:document_shared_with_upstream_train"] += 1
                        continue
                    evidence = claim["evidence"].get(doc_id, [])
                    labels = {item["label"] for item in evidence}
                    if len(labels) > 1:
                        self.exclusions["scifact:ambiguous_label"] += 1
                        continue
                    gold = next(iter(labels)) if labels else "NOT_ENOUGH_INFO"
                    doc = corpus[doc_id]
                    self.add("claim_support", "scifact", str(claim["id"]) + ":" + doc_id, doc_id,
                             {"claim": claim["claim"], "title": doc["title"], "abstract": " ".join(doc["abstract"])},
                             {"SUPPORT": "Supports the claim", "CONTRADICT": "Contradicts the claim", "NOT_ENOUGH_INFO": "No annotated support or contradiction in this abstract"},
                             gold, file, {"claim_id": claim["id"], "doc_id": doc_id}, "official_dev_document_disjoint_from_upstream_train")

    def ddxplus(self):
        file = "ddxplus__release_test_patients.zip"
        evidences = json.loads(self.path("ddxplus__release_evidences.json").read_text())
        conditions = json.loads(self.path("ddxplus__release_conditions.json").read_text())
        labels = sorted({v["cond-name-eng"] for v in conditions.values()})
        criteria = {"d" + str(i): label for i, label in enumerate(labels)}
        reverse = {v: k for k, v in criteria.items()}
        # Hash sample from the complete released test CSV, not a downloaded prefix.
        with zipfile.ZipFile(self.path(file)) as archive:
            member = archive.namelist()[0]
            raw_pool = []
            for i, row in enumerate(csv.DictReader(io.TextIOWrapper(archive.open(member)))):
                raw_pool.append((digest([SEED, "ddxplus", i]), i, row))
            for _, i, row in sorted(raw_pool)[:1000]:
                observed = []
                for encoded in ast.literal_eval(row["EVIDENCES"]):
                    key, _, value = encoded.partition("_@_")
                    evidence = evidences[key]
                    meanings = evidence.get("value_meaning", {})
                    meaning = meanings.get(value, value)
                    if isinstance(meaning, dict):
                        meaning = meaning.get("en", meaning.get("english", value))
                    observed.append({"question": evidence["question_en"], "value": meaning if value else "present"})
                self.add("synthetic_diagnosis", "ddxplus", str(i + 1), str(i + 1),
                         {"age": int(row["AGE"]), "sex": row["SEX"], "observed_evidence": observed}, criteria,
                         reverse[row["PATHOLOGY"]], file, {"zip_member": member, "csv_row": i + 2}, "official_test",
                         raw_test_rows=len(raw_pool), candidate_pool_note="Seeded hash preselection of 1000 from the complete official test CSV.")

    def tcm(self):
        file = "tcm_sd__test.json"
        rows = list(read_jsonl(self.path(file)))
        # Vocabulary comes from all released test labels, never individual target-based distractors.
        labels = sorted({r["norm_syndrome"] for r in rows})
        for i, row in enumerate(rows):
            state = {k: row[k] for k in ["chief_complaint", "description", "detection"]}
            # Remove literal answer mentions conservatively; retain original wording otherwise.
            if row["norm_syndrome"] in dumps(state):
                self.exclusions["tcm:literal_gold_in_material"] += 1
                continue
            self.add("tcm_syndrome", "tcm_sd", str(i + 1), digest(str(row["user_id"])), state,
                     {label: label for label in labels}, row["norm_syndrome"], file,
                     {"jsonl_line": i + 1, "patient_key_sha256": digest(str(row["user_id"]))}, "official_test", language="zh",
                     stratum="natural_test_distribution")

    def maccrobat(self):
        file = "maccrobat__MACCROBAT2020.zip"
        with zipfile.ZipFile(self.path(file)) as archive:
            for member in sorted(archive.namelist()):
                if not member.endswith(".ann") or member.startswith("__MACOSX"):
                    continue
                text = archive.read(member[:-4] + ".txt").decode("utf-8-sig")
                annotation = archive.read(member).decode("utf-8-sig")
                entities, relations = brat(annotation)
                events = {}
                for line in annotation.splitlines():
                    if line.startswith("E"):
                        eid, body = line.split("\t", 1)
                        events[eid] = body.split()[0].split(":", 1)[1]
                links = collections.defaultdict(set)
                for rid, kind, a, b in relations:
                    a, b = events.get(a, a), events.get(b, b)
                    if kind == "MODIFY" and a in entities and b in entities:
                        links[a].add((b, rid))
                for task, modifier_type, target_type in [
                    ("lab_link", "Lab_value", "Diagnostic_procedure"),
                    ("dose_link", "Dosage", "Medication")]:
                    candidates = {eid: ent for eid, ent in entities.items()
                                  if ent["type"] == target_type and valid_span(text, ent)}
                    if len(candidates) < 2:
                        continue
                    options = {eid: f"{ent['text']} [characters {ent['start']}:{ent['end']}]"
                               for eid, ent in sorted(candidates.items())}
                    for eid, targets in links.items():
                        ent = entities[eid]
                        if ent["type"] != modifier_type or not valid_span(text, ent):
                            continue
                        if task == "lab_link" and not re.search(r"\d", ent["text"]):
                            self.exclusions["maccrobat:non_numeric_result"] += 1
                            continue
                        matches = {target for target, _ in targets if target in candidates}
                        if len(matches) != 1:
                            self.exclusions["maccrobat:ambiguous_or_unusable_" + task] += 1
                            continue
                        gold = next(iter(matches))
                        self.add(task, "maccrobat", member + ":" + eid, Path(member).stem,
                                 {"case_report": text, "target": {k: ent[k] for k in ["text", "start", "end"]}},
                                 options, gold, file,
                                 {"zip_member": member, "modifier_id": eid, "linked_entity_id": gold,
                                  "relation_ids": sorted(rid for target, rid in targets if target == gold)},
                                 "published_corpus_no_official_split", stratum="natural_distribution",
                                 adaptation="Resolve event IDs to text anchors; unique original MODIFY link; all valid same-type entities are options.")

    def chinese_exams(self):
        file, answers_file = "cmb__CMB.zip", "cmb__CMB-test-choice-answer.json"
        member = "CMB/CMB-Exam/CMB-test/CMB-test-choice-question-merge.json"
        with zipfile.ZipFile(self.path(file)) as archive:
            questions = json.loads(archive.read(member))
        answers = json.loads(self.path(answers_file).read_text())
        # The archive includes C-type and multiple-answer items. Some C-type
        # metadata was relabeled in the answer release; these are out of scope.
        question_positions = {row["id"]: i for i, row in enumerate(questions)}
        answer_positions = {row["id"]: i for i, row in enumerate(answers)}
        if len(question_positions) != len(questions) or len(answer_positions) != len(answers):
            raise ValueError("Duplicate CMB source IDs")
        eligible_ids = {row["id"] for row in questions if row["question_type"] == "单项选择题"}
        self.exclusions["cmb:out_of_scope_question_type"] += len(questions) - len(eligible_ids)
        questions = [row for row in questions if row["id"] in eligible_ids]
        answers = [row for row in answers if row["id"] in eligible_ids]
        candidates = []
        for i, j, row, answer in join_cmb_answers(questions, answers):
            i, j = question_positions[row["id"]], answer_positions[row["id"]]
            if row["question_type"] != "单项选择题" or answer["answer"] not in row["option"]:
                self.exclusions["cmb:non_single_choice"] += 1
                continue
            candidates.append(("cmb", row["id"], row["question"], row["option"], answer["answer"], file,
                {"zip_member": member, "json_index": i, "question_id": row["id"],
                 "supporting_resources": [answers_file], "answer_json_index": j, "answer_field": "answer"},
                "official_test", {"exam_type": row["exam_type"], "exam_class": row["exam_class"], "exam_subject": row["exam_subject"]}))
        file = "cnmleqa__CNMLEQA-10k.json"
        for i, row in enumerate(json.loads(self.path(file).read_text())):
            if row["question_type"] != "案例分析":
                self.exclusions["cnmleqa:knowledge_question"] += 1
                continue
            options = {key: row[key] for key in ["opa", "opb", "opc", "opd", "ope"]}
            candidates.append(("cnmleqa", row["id"], row["question"], options, row["answer"], file,
                {"json_index": i, "question_id": row["id"], "answer_field": "answer", "original_source": row["source"]},
                "published_benchmark_no_official_split", {"original_source": row["source"], "exam_year": row.get("year"),
                 "original_question_type": row["question_type"]}))
        identities = collections.defaultdict(set)
        for source, uid, question, options, gold, *rest in candidates:
            key = digest([norm(question), sorted(norm(v) for v in options.values())])
            identities[key].add(norm(options[gold]))
        seen = set()
        for source, uid, question, options, gold, file, locator, split, metadata in candidates:
            task = chinese_exam_task(question)
            if task is None or len(options) != 5 or len(set(options.values())) != 5 or any(not str(v).strip() for v in options.values()):
                self.exclusions[source + ":incomplete_or_outside_decision_filter"] += 1
                continue
            key = digest([norm(question), sorted(norm(v) for v in options.values())])
            if len(identities[key]) != 1 or key in seen:
                self.exclusions[source + ":duplicate_or_conflicting_exam_item"] += 1
                continue
            seen.add(key)
            # Keep one vocabulary per source; preserve original option order and labels.
            self.add(task, source, uid, uid, {"clinical_question": question}, options, gold, file, locator,
                     split, language="zh", stratum=source + ":" + gold,
                     eligibility="case_vignette_and_explicit_decision_query_v1", **metadata)
            # Shared case prefixes across the two exam collections are one conservative group.
            prefix = re.sub(r"[^\w]", "", norm(question))[:60]
            self.pools[task][-1]["group_id"] = "zh_exam_case:" + digest(prefix)[:24]

    def run(self):
        for name in ["nubes", "ddi", "sections", "medquad", "errors", "longhealth", "medcalc", "trialgpt", "chia", "frd", "scifact", "ddxplus", "tcm", "maccrobat", "chinese_exams"]:
            getattr(self, name)()
            print("Prepared", name, flush=True)
        return self.pools


def brat(text):
    entities, relations = {}, []
    for line in text.splitlines():
        fields = line.split("\t")
        if line.startswith("T") and len(fields) >= 3:
            match = re.fullmatch(r"(\S+) (\d+) (\d+)", fields[1])
            if match:
                entities[fields[0]] = dict(type=match[1], start=int(match[2]), end=int(match[3]), text=fields[2])
        elif line.startswith("R") and len(fields) >= 2:
            match = re.fullmatch(r"(\S+) Arg1:(\S+) Arg2:(\S+)", fields[1].strip())
            if match:
                relations.append((fields[0], match[1], match[2], match[3]))
    return entities, relations


def valid_span(text, entity):
    return 0 <= entity["start"] < entity["end"] <= len(text) and text[entity["start"]:entity["end"]] == entity["text"]


def make_exposure_index(config, repo):
    index = {"method": "NFKC, whitespace removal, casefold; exact strings >=24 chars and start/middle/end 160-character windows",
             "limitations": "Exact/window screening only; no claim of semantic, translated, patient-level or foundation-model contamination freedom.",
             "training_files": [], "historical_files": []}
    train, history = set(), set()
    for path in sorted((repo / "training").rglob("train.jsonl")):
        if any(part in {"jev", "sft", "inputs", "grounded_sft"} for part in path.parts):
            continue
        index["training_files"].append({"path": str(path.relative_to(repo)), "sha256": file_sha(path)})
        for row in read_jsonl(path):
            train.update(signatures(row))
    for path in sorted((repo / "scenarios").glob("*/*/samples.jsonl")):
        index["historical_files"].append({"path": str(path.relative_to(repo)), "sha256": file_sha(path)})
        for row in read_jsonl(path):
            history.update(signatures(row["request"]["state"]))
    index["training_signatures"] = sorted(train)
    index["historical_signatures"] = sorted(history)
    write_json(config / "exposure_index.json", index)
    print("Indexed", len(index["training_files"]), "training files and", len(index["historical_files"]), "historical tasks")


def select_rows(rows, n=100, max_per_group=5):
    """Balanced deterministic strata, initially one question per source group.

    A scarce stratum is exhausted before its remaining quota goes elsewhere. The
    group cap increases from one to five only if necessary. No duplicates/padding.
    """
    by_request = collections.defaultdict(list)
    for row in rows:
        by_request[row["request_sha256"]].append(row)
    clean, conflicts = [], 0
    for candidates in by_request.values():
        if len({r["gold"] for r in candidates}) != 1:
            conflicts += len(candidates)
            continue
        clean.append(min(candidates, key=lambda r: digest([SEED, r["id"]])))
    clean.sort(key=lambda r: digest([SEED, r["task"], r["id"]]))
    pools = collections.defaultdict(list)
    for row in clean:
        pools[row["sampling_stratum"]].append(row)
    selected, chosen = [], set()
    groups, strata = collections.Counter(), collections.Counter()
    for cap in range(1, max_per_group + 1):
        while len(selected) < n:
            progress = False
            for key in sorted(pools, key=lambda k: (strata[k], digest([SEED, k]))):
                candidate = next((r for r in pools[key] if r["id"] not in chosen and groups[r["group_id"]] < cap), None)
                if candidate is None:
                    continue
                selected.append(candidate)
                chosen.add(candidate["id"])
                groups[candidate["group_id"]] += 1
                strata[key] += 1
                progress = True
                if len(selected) == n:
                    break
            if not progress:
                break
        if len(selected) == n:
            break
    return sorted(selected, key=lambda r: digest([SEED, "output", r["id"]])), {
        "raw_pool": len(rows), "unique_consistent_pool": len(clean), "conflicting_rows_removed": conflicts,
        "duplicate_requests_removed": len(rows) - len(clean) - conflicts, "group_cap": max_per_group}


def build(config, cache, output):
    builder = Builder(config, cache)
    pools = builder.run()
    exposure = json.loads((config / "exposure_index.json").read_text())
    train, history = set(exposure["training_signatures"]), set(exposure["historical_signatures"])
    all_rows, task_reports = [], []
    for task in builder.taxonomy["tasks"]:
        raw = pools.get(task["id"], [])
        clean = []
        blocked = 0
        for row in raw:
            sig = signatures(row["request"]["state"])
            if sig & train:
                blocked += 1
                continue
            row["exposure"] = {"local_training_signature_match": False,
                               "historical_material_signature_match": bool(sig & history),
                               "screening": "frozen_exposure_index"}
            clean.append(row)
        selected, sampling = select_rows(clean, task["target_count"])
        report = {**task, "count": len(selected), "groups": len({r["group_id"] for r in selected}),
                  "status": "ready" if len(selected) == task["target_count"] else "partial" if selected else "empty",
                  "sampling": {**sampling, "upstream_adapter_pool": len(raw), "local_training_matches_excluded": blocked},
                  "label_counts": dict(collections.Counter(r["gold"] for r in selected)),
                  "language_counts": dict(collections.Counter(r["language"] for r in selected)),
                  "source_counts": dict(collections.Counter(r["provenance"]["source_id"] for r in selected)),
                  "historical_material_matches": sum(r["exposure"]["historical_material_signature_match"] for r in selected)}
        if raw and len(selected) < task["target_count"]:
            report["missing_reason"] = "去重、训练重合筛查和来源分组限制后不足目标数量；保留实际数量。"
        if task["source_ids"] and not raw:
            raise ValueError("Adapter yielded no records for configured source task: " + task["id"])
        task_reports.append(report)
        all_rows.extend(selected)
        write_jsonl(output / "tasks" / task["id"] / "samples.jsonl", selected)
        write_json(output / "tasks" / task["id"] / "task.json", report)
    write_jsonl(output / "samples.jsonl", all_rows)
    write_jsonl(output / "requests.jsonl", ({"id": r["id"], "task": r["task"], "request": r["request"]} for r in all_rows))
    write_jsonl(output / "answers.jsonl", ({"id": r["id"], "gold": r["gold"], "group_id": r["group_id"]} for r in all_rows))
    # Source sharing across tasks is recorded, rather than counted as independent patients.
    membership = collections.defaultdict(set)
    for row in all_rows:
        membership[row["group_id"]].add(row["task"])
    summary = {"version": builder.taxonomy["version"], "seed": SEED, "total_tasks": len(task_reports),
               "ready_tasks": sum(t["status"] == "ready" for t in task_reports),
               "partial_tasks": sum(t["status"] == "partial" for t in task_reports),
               "empty_tasks": sum(t["status"] == "empty" for t in task_reports),
               "records": len(all_rows), "unique_source_groups": len(membership),
               "languages": dict(collections.Counter(r["language"] for r in all_rows)),
               "distribution_counts": dict(collections.Counter(r["provenance"]["distribution"] for r in all_rows)),
               "historical_material_matches": sum(r["exposure"]["historical_material_signature_match"] for r in all_rows),
               "adapter_exclusions": dict(builder.exclusions),
               "shared_source_groups": {g: sorted(tasks) for g, tasks in membership.items() if len(tasks) > 1},
               "tasks": task_reports}
    summary["scenarios"] = [{**scene,
        "defined_tasks": sum(t["primary_scenario"] == scene["id"] for t in task_reports),
        "populated_tasks": sum(t["primary_scenario"] == scene["id"] and t["count"] > 0 for t in task_reports),
        "records": sum(t["count"] for t in task_reports if t["primary_scenario"] == scene["id"])}
        for scene in builder.taxonomy["scenarios"]]
    write_json(output / "summary.json", summary)
    generate_docs(output, builder, summary)
    files = [p for p in output.rglob("*") if p.is_file() and p.name not in {"manifest.json", "validation.json"}]
    write_json(output / "manifest.json", {"version": builder.taxonomy["version"], "builder_sha256": file_sha(Path(__file__)), "files": {
        str(p.relative_to(output)): {"sha256": file_sha(p), "bytes": p.stat().st_size} for p in sorted(files)}})
    return summary


def generate_docs(output, builder, summary):
    source_lines = ["# 数据来源与引用\n", "各来源分别保留其数据许可；本仓库代码的 MIT 许可不改变题目材料的许可。`research_noncommercial` 为研究/非商业附加部分，不计入默认开放许可核心分数。\n"]
    for sid, source in builder.sources.items():
        source_lines += ["## " + source["name"] + "\n", "来源：[发布方](" + source["url"] + ")。\n"]
        if source["distribution"] == "reference_only":
            source_lines += ["状态：仅引用，未收录题目。" + source["reason"] + "\n"]
            if source.get("evidence_url"):
                source_lines += [f"核验日期：{source['checked_on']}；结论：{source['review_status']}。\n",
                                 f"[发布证据]({source['evidence_url']})；许可：{source['data_license']}。\n",
                                 "材料性质：" + source["authenticity"] + "\n",
                                 "答案依据：" + source["gold_provenance"] + "\n"]
            continue
        source_lines += [f"引用：{source['attribution']}，[论文/项目]({source['citation_url']})。\n",
                         f"数据许可：[{source['data_license']}]({source['license_url']})；分发类别：`{source['distribution']}`。\n",
                         "材料性质：" + source["authenticity"] + "\n", "答案依据：" + source["gold_provenance"] + "\n",
                         "许可与来源快照：" + "、".join(f"[{Path(p).name}]({p})" for p in source["license_evidence"]) + "。\n"]
    (output / "SOURCES.md").write_text("\n".join(source_lines))
    lines = [f"# Jev 医疗决策评测集 v{summary['version']}\n",
             "给定医疗材料、规则或候选项，评估可明确计分的分类、状态、关系、证据和方案选择。每题只有一个决策输出，使用 Jev `choice` 请求格式；不要求生成病历、建议或解释。\n",
             f"**{len(builder.taxonomy['scenarios'])} 个医疗场景 · {summary['total_tasks']} 个任务定义 · {summary['ready_tasks']} 个任务各 100 题 · {summary['partial_tasks']} 个不足 100 题 · {summary['empty_tasks']} 个留空 · 共 {summary['records']:,} 题。**\n",
             f"开放许可核心部分 {summary['distribution_counts'].get('open', 0):,} 题；非商业研究附加部分 {summary['distribution_counts'].get('research_noncommercial', 0):,} 题。当前 {sum(s['records'] > 0 for s in summary['scenarios'])} 个场景有题目，不代表场景工作流完整覆盖；语言分布为 " + "、".join(f"{lang} {count:,} 题" for lang, count in sorted(summary['languages'].items())) + "。\n",
             "[全部题目](samples.jsonl) · [无答案请求](requests.jsonl) · [答案](answers.jsonl) · [来源与许可](SOURCES.md) · [场景任务定义](taxonomy.json) · [按场景寻找数据](SCENARIO_RESEARCH.md) · [构建统计](summary.json)\n",
             "**[下载独立数据包](../../releases/README.md)**：开放核心包和非商业研究附加包分别交付，内含题目、答案、逐题溯源索引、原许可、格式说明及校验/评分工具。每道题可通过 `id → 原始资源版本与哈希 → 标注位置 → 转换代码` 回查。\n",
             "主目录按医疗场景 → 决策任务组织。每个任务只有一个 `primary_scenario`；原九个能力维度作为 `ability_tags`，允许多标签但不重复计算题目。`dimension` 保留为主要能力，兼容旧分析。材料判断、临床候选选择和结局预测分别报告；当前预测任务尚未收题。\n",
             "## 场景覆盖\n", "| 场景 | 有题任务 / 定义任务 | 题数 |", "| --- | ---: | ---: |"]
    for scene in summary["scenarios"]:
        lines.append(f"| {scene['title']} | {scene['populated_tasks']} / {scene['defined_tasks']} | {scene['records']} |")
    lines += ["", "## 任务目录\n", "题数是决策问题数，来源组可能是文档、句子、模拟病例或患者，不能一律解读为患者数。语种和输入条件不另计为任务。\n"]
    for scene in builder.taxonomy["scenarios"]:
        lines += ["### " + scene["title"] + "\n", scene["scope"] + "\n", "| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |", "| --- | ---: | --- | --- |"]
        for task in summary["tasks"]:
            if task["primary_scenario"] != scene["id"]:
                continue
            sources = task["source_ids"] or task["candidate_source_ids"]
            names = "、".join(f"[{builder.sources[s]['name']}]({builder.sources[s]['url']})" for s in sources) or "待补"
            note = task["definition"] if task["status"] == "ready" else task["missing_reason"]
            lines.append(f"| [{task['title']}](tasks/{task['id']}/task.json) | {task['count']} / {task['groups']} | {names} | {note} |")
        lines.append("")
    lines += ["## 版本、抽样和答案\n",
              "固定种子 20261010；从锁定版本的原文件解析，以标签/量表/来源等已声明分层轮流取样。先尽量每来源组一题，必要时逐步放宽至每组最多五题。去掉重复请求、冲突答案、不能解析的标注和本地训练指纹命中；不复制或改写题目补足数量。DDXPlus 先从完整官方测试 CSV 按哈希取 1,000 条候选。\n",
              "LongHealth 对 20 个虚构患者各取五题；这些问题共享整份病历。TCM-SD 按原测试分布哈希抽样，不将 148 个证型强行压成每类一题。CHIA 关系题只分类原始已标注关系，不包含自动构造的负例。NUBes 只测否定/不确定。FRD 的数值已由上游替换为 @NUMBER，仅测上下界方向。MedCalc 使用固定 GitHub 测试版本，不能报告为 HF Verified 版本。\n",
              "答案来自原始发布标注及可重现的机械映射。记录经过格式、定位、映射与去重检查，尚未做本项目独立医生逐题审核。本版本属于可审计初版，不是临床验证金标准。原始训练/开发/测试划分逐题保留；没有官方测试划分的来源不冒称官方测试集。\n",
              "v0.2.0 新增 MACCROBAT 的检查数值关联、药物剂量关联；检查题仅保留含数字的原始结果片段。候选项为病例中所有有效的对应类型实体，带原文位置以区分重复名称。只收原始 MODIFY 关系可唯一定位目标的题，不构造负关系、不判断处方适宜性。旧版 1,600 题的 ID、请求及金标保留，迁移基线见 [历史身份索引](history/v0.1.0_sample_identity.json)。\n",
              "v0.3.0 从 CMB-Exam 和 CNMLEQA-10k 补入中文病例的诊断、检查、治疗、用药四类选择题，原有 1,800 题的 ID、请求与答案保持不变，见 [v0.2.0 身份索引](history/v0.2.0_sample_identity.json)。按病例特征和问题意图规则筛选，排除纯知识题、缺图题、反向提问及不符合任务定义的题；保留原选项与金标，不生成新答案。CMB 原题与独立答案按 ID 连接，原 C 型及多选题不纳入。CNMLEQA 没有官方测试划分，使用发布语料的固定自留子集。\n",
              "两套中文题库按标准化题干与完整选项集合去重，答案文本冲突时全部排除；来源组由去标点后题干前 60 字的指纹近似确定，可能合并相似病例，也不能排除所有改写重复。题目中的旧术语或原始拼写按原文保留。中文新增题经过程序化适配与抽查，未独立复核其临床金标。[本轮新增来源核验](../../docs/DATASET_EXPANSION.md) 记录其他中文及英文候选。\n",
              "## 训练隔离与历史使用\n",
              f"[筛查索引](exposure_index.json) 固定列出本地训练文件及哈希。选中题目没有命中该索引的精确/窗口指纹；{summary['historical_material_matches']} 道题的材料或片段命中过往主评测指纹（通用片段可能误报）。新抽样不等于从未见过的新病例，不能把这部分称为全新盲测。SciFact 额外排除与官方训练声明共用的文档。\n",
              "该筛查不证明不存在改写、翻译、患者级关联或基础模型预训练暴露。`summary.json` 记录任务间共享来源组；跨任务统计应按组处理，不把共享文档的不同题当作独立患者。后续训练材料应反向检查本评测集，版本冻结后不根据成绩挑换题。\n",
              "## 运行\n", "在仓库根目录执行（Python 标准库，无自动模型调用）：\n", "```bash",
              "python3 scripts/medical_decision_dataset.py validate",
              "python3 scripts/medical_decision_dataset.py fetch",
              "python3 scripts/medical_decision_dataset.py build",
              "python3 scripts/medical_decision_dataset.py export --output work/decision-requests.jsonl",
              "python3 scripts/medical_decision_dataset.py score --predictions work/predictions.jsonl --output work/decision-scores.json",
              "```\n",
              "`fetch` 按 sources.lock.json 下载并核验源文件，`build` 使用已冻结的训练筛查索引复建；不重新生成答案。刷新本地筛查使用 `index` 子命令，刷新后重建将形成不同内容的版本，需复核并更新版本号。\n",
              "默认导出及计分只包含 `open` 部分。研究用途需要显式加 `--include-research`，才纳入 DDI 和 TCM-SD；相应题目仍受非商业及相同方式共享等原许可约束。\n",
              "模型只接收 `request`（按 API 需要另加 model）；不要发送 gold、provenance、metadata 或来源定位。预测文件每行格式：\n", "```json",
              '{"id":"样本完整 ID","choice":"选项键"}', "```\n",
              "也接受 `{\"id\":\"样本完整 ID\",\"response\":{\"answers\":{\"decision\":{\"choice\":\"选项键\"}}}}`。缺失、格式错误和不在选项内的回答按错计；重复或未知 ID 会使计分失败。\n",
              "计分先报告逐任务结果，再对同一场景内任务准确率等权平均；`scenario_macro_accuracy` 对有题场景等权，避免试验筛选任务较多而主导总分。场景表同时显示已计分任务数和定义任务数；空场景分数为 null，不计零分也不算已覆盖。旧 `task_macro_accuracy` 仍保留。能力标签统计可重叠，不累加成主分母。不同版本和不同题目覆盖的总分不可直接作训练前后比较。\n",
              "逐任务输出准确率、宏 F1、逐类召回和来源组全对率；另按决策模式、来源性质、语种及历史匹配状态分层。宏 F1 使用实际有金标的类别，未出现的候选类别单列。公开论文、考试改编、模拟病例和真实临床材料分别报告。\n",
              "每任务 100 题适合固定的小规模模型与训练对照，不能据此确认细小提升或临床效果。比较训练前后应使用相同题目、候选项、提示和计分范围，并按来源组做配对分析；LongHealth 的有效来源组只有 20 个。这里的汇总分数仅为描述性统计。\n",
              "## 评测状态\n",
              "本版本尚未运行模型评测。逐题历史材料重合标记及冻结筛查索引属于数据来源记录，不能解释为本版本模型成绩。\n"]
    (output / "README.md").write_text("\n".join(lines))
    research = ["# 按医疗场景寻找任务与数据\n", "核验日期：2026-10-10。仅有数据可下载，不表示已满足当前任务的题目、答案、许可与隔离要求。以下为新增来源的采用状态和剩余步骤；已采用来源也可只覆盖某个场景的局部任务。\n"]
    for scene in builder.taxonomy["scenarios"]:
        relevant = [t for t in summary["tasks"] if t["primary_scenario"] == scene["id"]]
        research += ["## " + scene["title"] + "\n", scene["scope"] + "\n",
                     "任务：" + "、".join(t["title"] for t in relevant) + "。\n"]
        adopted = sorted({sid for t in relevant if t["count"] for sid in t["source_ids"]})
        research += ["已有题目来源：" + ("、".join(f"[{builder.sources[sid]['name']}]({builder.sources[sid]['url']})" for sid in adopted) or "暂无") + "。\n"]
        for source in builder.sources.values():
            if scene["id"] not in source.get("scenario_ids", []):
                continue
            research += [f"### [{source['name']}]({source['url']})\n",
                         "材料：" + source["authenticity"] + "\n", "金标：" + source["gold_provenance"] + "\n",
                         "许可：" + source["data_license"] + "。\n"]
            if source["distribution"] == "reference_only":
                research += [f"状态：{source['review_status']}。{source['reason']}\n", f"[核验依据]({source['evidence_url']})。\n"]
            else:
                research += ["状态：已采用。抽样和转换见任务目录及逐题来源定位。\n"]
    (output / "SCENARIO_RESEARCH.md").write_text("\n".join(research))


def validate(dataset):
    manifest = json.loads((dataset / "manifest.json").read_text())
    for name, record in manifest["files"].items():
        if file_sha(dataset / name) != record["sha256"]:
            raise ValueError("Manifest mismatch: " + name)
    taxonomy = json.loads((dataset / "taxonomy.json").read_text())
    definitions = {x["id"]: x for x in taxonomy["tasks"]}
    scenarios = {x["id"] for x in taxonomy["scenarios"]}
    abilities = {x["id"] for x in taxonomy["dimensions"]}
    assert len(scenarios) == 8 and len(definitions) == len(taxonomy["tasks"])
    sources = {x["id"]: x for x in json.loads((dataset / "sources.json").read_text())["sources"]}
    resources = {x["name"]: x for x in json.loads((dataset / "sources.lock.json").read_text())["files"]}
    for task in definitions.values():
        assert task["primary_scenario"] in scenarios
        assert task["dimension"] in task["ability_tags"] and set(task["ability_tags"]) <= abilities
        assert set(task["source_ids"] + task["candidate_source_ids"]) <= set(sources)
    for card in sources.values():
        if card["distribution"] != "reference_only":
            assert card["license_evidence"] and all((dataset / p).is_file() for p in card["license_evidence"])
    rows = list(read_jsonl(dataset / "samples.jsonl"))
    ids = set()
    by_task = collections.defaultdict(list)
    exposure = json.loads((dataset / "exposure_index.json").read_text())
    train = set(exposure["training_signatures"])
    for row in rows:
        if row["id"] in ids:
            raise ValueError("Duplicate ID: " + row["id"])
        ids.add(row["id"])
        by_task[row["task"]].append(row)
        assert row["task"] in definitions
        assert row["dimension"] == definitions[row["task"]]["dimension"]
        assert row["primary_scenario"] == definitions[row["task"]]["primary_scenario"]
        assert row["ability_tags"] == definitions[row["task"]]["ability_tags"]
        assert row["decision_stage"] == definitions[row["task"]]["decision_stage"]
        assert set(row["request"]) == {"state", "questions"}
        assert set(row["request"]["questions"]) == {"decision"}
        question = row["request"]["questions"]["decision"]
        assert question["type"] == "choice" and row["gold"] in question["criteria"]
        assert row["request_sha256"] == digest(row["request"])
        assert not signatures(row["request"]["state"]) & train
        card = sources[row["provenance"]["source_id"]]
        assert card["distribution"] != "reference_only"
        assert card["data_license"] == row["provenance"]["data_license"]
        assert card["distribution"] == row["provenance"]["distribution"]
        assert row["provenance"]["resource_sha256"] == resources[row["provenance"]["resource"]]["sha256"]
        forbidden = {"gold", "correct", "corrected_text", "ground_truth_answer", "error_flag", "error_sentence_id"}
        def keys(value):
            if isinstance(value, dict):
                for key, val in value.items():
                    yield str(key).lower()
                    yield from keys(val)
            elif isinstance(value, list):
                for item in value:
                    yield from keys(item)
        assert not set(keys(row["request"]["state"])) & forbidden
    for task in definitions:
        part = list(read_jsonl(dataset / "tasks" / task / "samples.jsonl"))
        report = json.loads((dataset / "tasks" / task / "task.json").read_text())
        assert part == by_task[task]
        assert len(part) == report["count"] <= definitions[task]["target_count"]
        assert len({r["request_sha256"] for r in part}) == len(part)
        assert max(collections.Counter(r["group_id"] for r in part).values(), default=0) <= 5
        assert bool(part) == (report["status"] != "empty")
    requests = list(read_jsonl(dataset / "requests.jsonl"))
    assert requests == [{"id": r["id"], "task": r["task"], "request": r["request"]} for r in rows]
    assert list(read_jsonl(dataset / "answers.jsonl")) == [{"id": r["id"], "gold": r["gold"], "group_id": r["group_id"]} for r in rows]
    now = {r["id"]: {"request_sha256": r["request_sha256"], "gold": r["gold"]} for r in rows}
    for baseline in sorted((dataset / "history").glob("*_sample_identity.json")):
        previous = json.loads(baseline.read_text())
        assert all(now.get(uid) == identity for uid, identity in previous.items()), "Existing frozen questions changed: " + baseline.name
    result = {"passed": True, "records": len(rows), "task_definitions": len(definitions),
              "checks": ["manifest hashes", "unique IDs", "per-task counts", "label membership", "request-only export", "answer separation", "source licenses", "no training fingerprint matches", "group cap", "empty-task representation", "primary scenario and ability tags", "all frozen question identities preserved"]}
    write_json(dataset / "validation.json", result)
    return result


def metrics(rows, predictions):
    tp, fp, fn = collections.Counter(), collections.Counter(), collections.Counter()
    groups = collections.defaultdict(list)
    correct = missing = invalid = 0
    labels = sorted({r["gold"] for r in rows})
    candidates = {k for r in rows for k in r["request"]["questions"]["decision"]["criteria"]}
    for row in rows:
        pred = predictions.get(row["id"])
        if row["id"] not in predictions:
            missing += 1
        elif pred not in row["request"]["questions"]["decision"]["criteria"]:
            invalid += 1
        good = pred == row["gold"]
        groups[row["group_id"]].append(good)
        correct += good
        if good:
            tp[row["gold"]] += 1
        else:
            fp[pred] += 1
            fn[row["gold"]] += 1
    per_class = {label: {"support": tp[label] + fn[label], "recall": tp[label] / (tp[label] + fn[label]),
                         "f1": 2 * tp[label] / (2 * tp[label] + fp[label] + fn[label])} for label in labels}
    return {"n": len(rows), "correct": correct, "accuracy": correct / len(rows),
            "macro_f1": sum(x["f1"] for x in per_class.values()) / len(per_class),
            "missing": missing, "invalid": invalid, "per_class": per_class,
            "candidate_labels_without_gold": sorted(candidates - set(labels)),
            "groups": len(groups), "groups_all_correct": sum(all(x) for x in groups.values()),
            "group_all_correct_rate": sum(all(x) for x in groups.values()) / len(groups)}


def score(dataset, prediction_path, include_research=False):
    all_rows = list(read_jsonl(dataset / "samples.jsonl"))
    known = {r["id"] for r in all_rows}
    rows = [r for r in all_rows if include_research or r["provenance"]["distribution"] == "open"]
    predictions = {}
    for record in read_jsonl(prediction_path):
        if not isinstance(record, dict) or not isinstance(record.get("id"), str):
            raise ValueError("Prediction must be an object with a string ID")
        uid = record.get("id")
        if uid not in known or uid in predictions:
            raise ValueError("Unknown or duplicate prediction ID: " + str(uid))
        value = record.get("choice")
        if value is None:
            try:
                value = record["response"]["answers"]["decision"]["choice"]
            except (KeyError, TypeError):
                value = None
        # A numeric value, explanation, list or malformed response is not a valid option key.
        predictions[uid] = value if isinstance(value, str) else None
    tasks = collections.defaultdict(list)
    for row in rows:
        tasks[row["task"]].append(row)
    results = {task: metrics(items, predictions) for task, items in sorted(tasks.items())}
    aggregate = {}
    for name, key in [("primary_scenario", lambda r: r["primary_scenario"]),
                      ("decision_stage", lambda r: r["decision_stage"]),
                      ("dimension", lambda r: r["dimension"]), ("decision_mode", lambda r: r["decision_mode"]),
                      ("material_kind", lambda r: r["provenance"]["material_kind"]), ("language", lambda r: r["language"]),
                      ("distribution", lambda r: r["provenance"]["distribution"]),
                      ("historical_material_match", lambda r: str(r["exposure"]["historical_material_signature_match"]).lower())]:
        parts = collections.defaultdict(lambda: collections.defaultdict(list))
        for row in rows:
            parts[key(row)][row["task"]].append(row)
        aggregate[name] = {value: {"n": sum(len(x) for x in groups.values()), "tasks": len(groups),
                                   "task_macro_accuracy": sum(metrics(items, predictions)["accuracy"] for items in groups.values()) / len(groups)}
                           for value, groups in parts.items()}
    taxonomy = json.loads((dataset / "taxonomy.json").read_text())
    scene_scores = scenario_scores(taxonomy, results, tasks)
    covered = [s["task_macro_accuracy"] for s in scene_scores.values() if s["task_macro_accuracy"] is not None]
    ability_parts = collections.defaultdict(lambda: collections.defaultdict(list))
    for row in rows:
        for tag in row["ability_tags"]:
            ability_parts[tag][row["task"]].append(row)
    aggregate["ability_tags_overlapping"] = {tag: {"tasks": len(parts), "n": sum(len(items) for items in parts.values()),
        "task_macro_accuracy": sum(metrics(items, predictions)["accuracy"] for items in parts.values()) / len(parts)}
        for tag, parts in ability_parts.items()}
    return {"dataset_version": taxonomy["version"],
            "dataset_manifest_sha256": file_sha(dataset / "manifest.json"),
            "predictions_sha256": file_sha(prediction_path),
            "include_research": include_research, "records": len(rows),
            "scored_tasks": len(results), "task_macro_accuracy": sum(r["accuracy"] for r in results.values()) / len(results),
            "scenario_macro_accuracy": sum(covered) / len(covered) if covered else None,
            "covered_scenarios": len(covered), "defined_scenarios": len(taxonomy["scenarios"]), "scenarios": scene_scores,
            "tasks": results, "stratified": aggregate,
            "note": "Descriptive macro scores; empty tasks excluded. No claim of independent patients or clinical effectiveness."}


def scenario_scores(taxonomy, results, tasks):
    output = {}
    for scene in taxonomy["scenarios"]:
        defined = [t["id"] for t in taxonomy["tasks"] if t["primary_scenario"] == scene["id"]]
        present = [tid for tid in defined if tid in results]
        output[scene["id"]] = {"title": scene["title"], "defined_tasks": len(defined), "scored_tasks": len(present),
            "records": sum(len(tasks[tid]) for tid in present),
            "task_macro_accuracy": sum(results[tid]["accuracy"] for tid in present) / len(present) if present else None}
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["fetch", "index", "build", "validate", "export", "score"])
    parser.add_argument("--dataset", type=Path, default=DEFAULT)
    parser.add_argument("--cache", type=Path, default=CACHE)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--predictions", type=Path)
    parser.add_argument("--include-research", action="store_true")
    args = parser.parse_args()
    if args.command == "fetch":
        fetch(args.dataset, args.cache)
    elif args.command == "index":
        make_exposure_index(args.dataset, ROOT)
    elif args.command == "build":
        if args.output and args.output != args.dataset:
            raise SystemExit("Build in a copied dataset directory using --dataset; config and output must stay together.")
        summary = build(args.dataset, args.cache, args.dataset)
        print(dumps({k: v for k, v in summary.items() if k not in {"tasks", "shared_source_groups", "adapter_exclusions"}}))
        print(dumps(validate(args.dataset)))
    elif args.command == "validate":
        print(dumps(validate(args.dataset)))
    elif args.command == "export":
        if not args.output:
            parser.error("export requires --output")
        validate(args.dataset)
        rows = [r for r in read_jsonl(args.dataset / "samples.jsonl") if args.include_research or r["provenance"]["distribution"] == "open"]
        write_jsonl(args.output, ({"id": r["id"], "task": r["task"], "request": r["request"]} for r in rows))
        print("Exported", len(rows), "requests")
    elif args.command == "score":
        if not args.predictions or not args.output:
            parser.error("score requires --predictions and --output")
        validate(args.dataset)
        result = score(args.dataset, args.predictions, args.include_research)
        write_json(args.output, result)
        print(dumps({k: v for k, v in result.items() if k not in {"tasks", "stratified"}}))


if __name__ == "__main__":
    main()
