"""Exercise standalone distribution, license separation and tamper detection."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import medical_decision_release as release


class ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.meta = release.package_files(release.data.DEFAULT, "open")
        cls.nc_files, cls.nc_meta = release.package_files(release.data.DEFAULT, "research_noncommercial")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name, raw in self.files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)

    def replace_and_rehash(self, name, value):
        path = self.root / name
        path.write_text(json.dumps(value, ensure_ascii=False) + "\n")
        manifest_path = self.root / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["files"][name] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}
        manifest_path.write_text(json.dumps(manifest))

    def test_license_slices_are_disjoint_and_cover_canonical_samples(self):
        core = [json.loads(line) for line in self.files["samples.jsonl"].splitlines()]
        nc = [json.loads(line) for line in self.nc_files["samples.jsonl"].splitlines()]
        self.assertEqual({r["provenance"]["distribution"] for r in core}, {"open"})
        self.assertEqual({r["provenance"]["source_id"] for r in nc}, {"ddi", "tcm_sd"})
        self.assertFalse({r["id"] for r in core} & {r["id"] for r in nc})
        original = {r["id"]: r for r in release.data.read_jsonl(release.data.DEFAULT / "samples.jsonl")}
        self.assertEqual({r["id"]: r for r in core + nc}, original)
        self.assertFalse(any(name.startswith(("work/", "training/", ".env", "history/")) for name in self.files))
        self.assertNotIn("ddi", {s["id"] for s in json.loads(self.files["sources.json"])["sources"]})

    def test_standalone_cli_runs_without_repository_imports(self):
        proc = subprocess.run([sys.executable, "tools/medical_decision_release.py", "verify", "--dataset", "."],
                              cwd=self.root, text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(proc.stdout)["records"], self.meta["records"])

    def test_changed_data_fails_integrity_check(self):
        with (self.root / "samples.jsonl").open("a") as f:
            f.write("{}\n")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            release.verify(self.root)

    def test_trace_cannot_silently_drift_even_with_updated_file_hash(self):
        values = list(release.data.read_jsonl(self.root / "provenance.jsonl"))
        values[0]["gold"] = "corrupt"
        path = self.root / "provenance.jsonl"
        release.data.write_jsonl(path, values)
        manifest_path = self.root / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["files"]["provenance.jsonl"]["sha256"] = release.data.file_sha(path)
        manifest["files"]["provenance.jsonl"]["bytes"] = path.stat().st_size
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "Broken source trace"):
            release.verify(self.root)

    def test_declared_core_cannot_be_relabeled_noncommercial(self):
        self.replace_and_rehash("release.json", {**self.meta, "distribution": "research_noncommercial"})
        with self.assertRaisesRegex(ValueError, "Mixed license"):
            release.verify(self.root)

    def test_unknown_id_and_unsafe_manifest_paths_fail(self):
        with self.assertRaisesRegex(ValueError, "Unknown sample"):
            release.trace(self.root, "does-not-exist")
        for name in ["../secret", "/absolute", "a\\b"]:
            with self.assertRaisesRegex(ValueError, "Unsafe"):
                release.checked_path(self.root, name)

    def test_cmb_trace_includes_separate_official_answer_resource(self):
        rows = [json.loads(line) for line in self.files["samples.jsonl"].splitlines()]
        row = next(r for r in rows if r["provenance"]["source_id"] == "cmb")
        traced = release.trace(self.root, row["id"])
        self.assertEqual({r["name"] for r in traced["resources"]},
                         {"cmb__CMB.zip", "cmb__CMB-test-choice-answer.json"})
        self.assertIn("answer_json_index", traced["provenance"]["locator"])

    def test_source_fetch_rejects_wrong_upstream_bytes(self):
        uid = json.loads(self.files["provenance.jsonl"].splitlines()[0])["id"]
        with patch.object(release.urllib.request, "urlopen") as fetch:
            fetch.return_value.__enter__.return_value.read.return_value = b"changed upstream"
            with self.assertRaisesRegex(ValueError, "Upstream changed"):
                release.trace(self.root, uid, True, self.root / "cache")
        self.assertEqual(list((self.root / "cache").iterdir()), [])


if __name__ == "__main__":
    unittest.main()
