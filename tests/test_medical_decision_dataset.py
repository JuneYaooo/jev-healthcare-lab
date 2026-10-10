"""Checks for sampling integrity, annotation parsing and conservative scoring."""
import collections
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("decision_dataset", ROOT / "scripts/medical_decision_dataset.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def sample(uid, gold="a", group=None, distribution="open"):
    request = {"state": {"text": uid}, "questions": {"decision": {
        "type": "choice", "criteria": {"a": "A", "b": "B", "c": "C"}}}}
    return {"id": uid, "task": "task", "group_id": group or uid, "gold": gold,
            "request": request, "request_sha256": module.digest(request),
            "sampling_stratum": gold, "dimension": "facts", "decision_mode": "material",
            "language": "en", "provenance": {"distribution": distribution, "material_kind": "synthetic"},
            "primary_scenario": "intake", "ability_tags": ["facts"], "decision_stage": "material_judgment",
            "exposure": {"historical_material_signature_match": False}}


class SamplingTests(unittest.TestCase):
    def test_order_independence_and_group_cap(self):
        rows = [sample(str(i), "a" if i % 2 else "b", group=str(i % 3)) for i in range(50)]
        selected, _ = module.select_rows(rows, n=100)
        reverse, _ = module.select_rows(list(reversed(rows)), n=100)
        self.assertEqual(selected, reverse)
        self.assertEqual(len(selected), 15)
        self.assertEqual(set(collections.Counter(r["group_id"] for r in selected).values()), {5})

    def test_duplicate_and_conflicting_requests_removed(self):
        first = sample("one")
        duplicate = {**first, "id": "two"}
        other = sample("three")
        conflict = {**other, "id": "four", "gold": "b"}
        selected, info = module.select_rows([first, duplicate, other, conflict])
        self.assertEqual(len(selected), 1)
        self.assertEqual(info["duplicate_requests_removed"], 1)
        self.assertEqual(info["conflicting_rows_removed"], 2)

    def test_no_padding_and_empty_pool(self):
        selected, _ = module.select_rows([sample("one")], n=100)
        self.assertEqual(len(selected), 1)
        self.assertEqual(module.select_rows([])[0], [])

    def test_balanced_labels_when_groups_allow(self):
        rows = [sample(str(i), "a" if i < 150 else "b") for i in range(200)]
        selected, _ = module.select_rows(rows, n=100)
        self.assertEqual(collections.Counter(r["gold"] for r in selected), {"a": 50, "b": 50})

    def test_short_material_inside_serialized_sft_is_screened(self):
        question = "What are the symptoms of asthma?"
        wrapped = {"messages": [{"content": json.dumps({"state": {"question": question}})}]}
        self.assertTrue(module.signatures(wrapped) & module.signatures({"question": question.upper()}))
        self.assertFalse(module.signatures("too short"))

    def test_window_match_for_material_embedded_in_longer_text(self):
        text = "abcdefghij" * 32
        self.assertTrue(module.signatures(text) & module.signatures(text + " further material"))


class AnnotationTests(unittest.TestCase):
    def test_chinese_exam_filter_requires_case_and_explicit_decision(self):
        case = "患者，男性，45岁，因胸痛三天就诊。既往无明确心脏疾病史，入院时测得血压正常，神志清楚，心肺听诊未见明显异常。"
        self.assertEqual(module.chinese_exam_task(case + "为明确诊断，应首选的检查是"), "examination_choice")
        self.assertEqual(module.chinese_exam_task(case + "最可能的诊断是"), "diagnosis_choice")
        self.assertEqual(module.chinese_exam_task(case + "首选的治疗药物是"), "medication_choice")
        self.assertEqual(module.chinese_exam_task(case + "最适宜的治疗措施是"), "treatment_choice")
        self.assertIsNone(module.chinese_exam_task("治疗肺炎首选的抗生素是"))
        self.assertIsNone(module.chinese_exam_task(case + "胸部CT如下。首选的检查是"))
        self.assertIsNone(module.chinese_exam_task(case + "治疗时间为多久"))
        self.assertIsNone(module.chinese_exam_task(case + "不应选用的药物是"))
        self.assertIsNone(module.chinese_exam_task(case + "以下不适宜选用的降压药物是"))
        self.assertIsNone(module.chinese_exam_task(case + "其中一项护理诊断为体温过高，请选出主要依据"))

    def test_expanded_chinese_filter_uses_question_intent_not_case_keywords(self):
        case = "患者，男性，45岁，因胸痛三天就诊。既往无明确心脏疾病史，入院时测得血压正常，神志清楚，心肺听诊未见明显异常。"
        self.assertEqual(module.expanded_chinese_task(case + "该患者临床分期为"), "clinical_grade")
        self.assertEqual(module.expanded_chinese_task(case + "该患者不宜选用的药物是"), "patient_contraindication")
        self.assertEqual(module.expanded_chinese_task(case + "症状最可能的原因是"), "case_etiology")
        self.assertEqual(module.expanded_chinese_task(case + "护士首先应采取的护理措施是"), "nursing_priority")
        for query in ["为明确病因，检査首选", "下列不属于手术禁忌证的是", "该病不常见的并发症是",
                      "经过一般补液治疗后，最可能的诊断是", "不宜使用碱性药物，其目的是", "推测致病因素发生在"]:
            self.assertIsNone(module.expanded_chinese_task(case + query), query)

    def test_mortality_horizon_excludes_early_censoring(self):
        for days, event, expected in [(89, 0, None), (90, 0, "no"), (91, 0, "no"),
                                      (89, 1, "yes"), (90, 1, "yes"), (91, 1, "no")]:
            self.assertEqual(module.mortality_at_horizon({"time": str(days), "DEATH_EVENT": str(event)}, 90), expected)

    def test_cmb_answers_join_by_id_and_preserve_original_positions(self):
        common = dict(exam_type="医师考试", exam_class="执业医师", exam_subject="内科", question_type="单项选择题")
        questions = [dict(common, id=3), dict(common, id=9)]
        answers = [dict(common, id=9, answer="A"), dict(common, id=3, answer="E")]
        joined = list(module.join_cmb_answers(questions, answers))
        self.assertEqual([(i, j, q["id"], a["answer"]) for i, j, q, a in joined], [(0, 1, 3, "E"), (1, 0, 9, "A")])
        with self.assertRaisesRegex(ValueError, "metadata mismatch"):
            list(module.join_cmb_answers(questions, [answers[0], dict(answers[1], exam_subject="外科")]))
        with self.assertRaisesRegex(ValueError, "unmatched"):
            list(module.join_cmb_answers(questions, answers[:1]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            list(module.join_cmb_answers(questions, answers + answers[:1]))

    def test_maccrobat_event_resolution_ambiguity_and_full_candidate_set(self):
        text = "aspirin 5mg; warfarin 2mg; INR 2.5; PT prolonged."
        entities = [("T1", "Medication", "aspirin"), ("T2", "Medication", "warfarin"),
                    ("T3", "Dosage", "5mg"), ("T4", "Dosage", "2mg"),
                    ("T5", "Diagnostic_procedure", "INR"), ("T6", "Diagnostic_procedure", "PT"),
                    ("T7", "Lab_value", "2.5")]
        ann = "\n".join(f"{uid}\t{typ} {text.index(value)} {text.index(value)+len(value)}\t{value}" for uid, typ, value in entities)
        ann += "\nE1\tMedication:T1 \nE2\tMedication:T2 \nE3\tDiagnostic_procedure:T5 \nR1\tMODIFY Arg1:T3 Arg2:E1 \nR2\tMODIFY Arg1:T3 Arg2:E2 \nR3\tMODIFY Arg1:T4 Arg2:E2 \nR4\tMODIFY Arg1:T7 Arg2:E3 "
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("case.ann", ann)
                archive.writestr("case.txt", text)
            builder = object.__new__(module.Builder)
            builder.path = lambda _: path
            builder.exclusions = collections.Counter()
            records = []
            builder.add = lambda *args, **kwargs: records.append((args, kwargs))
            builder.maccrobat()
        self.assertEqual(len(records), 2)
        records = {args[0]: args for args, _ in records}
        self.assertEqual(records["dose_link"][6], "T2")
        self.assertEqual(set(records["dose_link"][5]), {"T1", "T2"})
        self.assertEqual(records["lab_link"][6], "T5")
        self.assertEqual(set(records["lab_link"][5]), {"T5", "T6"})
        self.assertEqual(builder.exclusions["maccrobat:ambiguous_or_unusable_dose_link"], 1)

    def test_discontinuous_brat_span_not_silently_truncated(self):
        entities, relations = module.brat("T1\tCondition 0 6\tasthma\nT2\tCondition 0 2;4 6\tas ma\nR1\tHas_value Arg1:T1 Arg2:T2")
        self.assertEqual(list(entities), ["T1"])
        self.assertTrue(module.valid_span("asthma", entities["T1"]))
        self.assertEqual(relations[0][1], "Has_value")

    def test_negative_empty_and_inaccurate_spans_rejected(self):
        for start, end, text in [(-1, 3, ""), (0, 0, ""), (0, 99, "asthma"), (0, 6, "cancer")]:
            self.assertFalse(module.valid_span("asthma", {"start": start, "end": end, "text": text}))


class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.rows = [sample("one", group="g"), sample("two", "b", group="g"),
                     sample("research", distribution="research_noncommercial")]
        module.write_jsonl(self.folder / "samples.jsonl", self.rows)
        module.write_json(self.folder / "taxonomy.json", {"version": "fixture",
            "scenarios": [{"id": "intake", "title": "Intake"}, {"id": "followup", "title": "Follow-up"}],
            "tasks": [{"id": "task", "primary_scenario": "intake"}, {"id": "empty", "primary_scenario": "followup"}]})
        module.write_json(self.folder / "manifest.json", {})
        self.predictions = self.folder / "predictions.jsonl"

    def test_missing_and_invalid_predictions_remain_in_denominator(self):
        rows = [sample("one"), sample("two", "b"), sample("three", "b")]
        result = module.metrics(rows, {"one": "a", "two": "invalid"})
        self.assertEqual(result["accuracy"], 1 / 3)
        self.assertEqual((result["missing"], result["invalid"]), (1, 1))
        self.assertEqual(result["macro_f1"], 0.5)
        self.assertEqual(result["candidate_labels_without_gold"], ["c"])

    def test_default_core_and_explicit_research_slice(self):
        module.write_jsonl(self.predictions, [{"id": "one", "choice": "a"},
            {"id": "two", "response": {"answers": {"decision": {"choice": "b"}}}},
            {"id": "research", "choice": "a"}])
        core = module.score(self.folder, self.predictions)
        full = module.score(self.folder, self.predictions, include_research=True)
        self.assertEqual((core["records"], full["records"]), (2, 3))
        self.assertEqual(core["task_macro_accuracy"], 1)
        self.assertEqual(core["dataset_version"], "fixture")
        self.assertEqual(core["scenario_macro_accuracy"], 1)
        self.assertEqual(core["covered_scenarios"], 1)
        self.assertIsNone(core["scenarios"]["followup"]["task_macro_accuracy"])
        self.assertEqual(core["tasks"]["task"]["groups_all_correct"], 1)

    def test_group_requires_every_question_correct(self):
        result = module.metrics(self.rows[:2], {"one": "a", "two": "a"})
        self.assertEqual(result["accuracy"], 0.5)
        self.assertEqual(result["group_all_correct_rate"], 0)

    def test_scenario_score_weights_tasks_equally_and_retains_empty_coverage(self):
        taxonomy = {"scenarios": [{"id": "s", "title": "S"}, {"id": "e", "title": "E"}],
                    "tasks": [{"id": t, "primary_scenario": "s"} for t in ["a", "b", "empty"]]}
        scores = module.scenario_scores(taxonomy, {"a": {"accuracy": 1}, "b": {"accuracy": 0}},
                                        {"a": [None] * 100, "b": [None] * 10})
        self.assertEqual(scores["s"]["task_macro_accuracy"], 0.5)
        self.assertEqual((scores["s"]["defined_tasks"], scores["s"]["scored_tasks"]), (3, 2))
        self.assertIsNone(scores["e"]["task_macro_accuracy"])

    def test_numeric_and_list_choices_are_invalid(self):
        module.write_jsonl(self.predictions, [{"id": "one", "choice": 0}, {"id": "two", "choice": ["b"]}])
        result = module.score(self.folder, self.predictions)
        self.assertEqual(result["tasks"]["task"]["invalid"], 2)
        self.assertEqual(result["task_macro_accuracy"], 0)

    def test_unknown_duplicate_or_malformed_id_fails(self):
        for records in [[{"id": "unknown"}], [{"id": "one"}, {"id": "one"}],
                        [{"id": ["one"]}], [["not an object"]]]:
            with self.subTest(records=records):
                module.write_jsonl(self.predictions, records)
                with self.assertRaises(ValueError):
                    module.score(self.folder, self.predictions)


if __name__ == "__main__":
    unittest.main()
