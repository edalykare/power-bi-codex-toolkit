import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from tests.helpers import DEMO, ROOT, minimal_model, write, write_json

# isort: split

from pbi_codex.cli import check, main
from pbi_codex.diagnostics import files_under
from pbi_codex.operations import compare_timings, fabric_plan, model_documentation
from pbi_codex.tmdl import load_model


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def call(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            result = main(list(args))
        return result, out.getvalue(), err.getvalue()

    def test_json_summary_reports_boundaries(self):
        status, out, _ = self.call("check", str(DEMO), "--format", "json", "--strict")
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(out)["summary"]["engineValidation"], "not-run")

    def test_warning_exit_code(self):
        path = write(self.root / "example.dax", "[A] / [B]")
        self.assertEqual(self.call("dax", str(path))[0], 0)
        self.assertEqual(self.call("dax", str(path), "--strict")[0], 1)

    def test_bad_input_exit_code(self):
        self.assertEqual(self.call("check", str(self.root / "missing"))[0], 2)
        self.assertEqual(self.call("check", str(self.root))[0], 2)
        self.assertEqual(self.call("dax", str(self.root))[0], 2)

    def test_errors_fail(self):
        path = write(self.root / "bad.dax", "SUM([X]")
        self.assertEqual(self.call("dax", str(path))[0], 1)

    def test_output_not_overwritten(self):
        output = self.root / "checks.json"
        self.assertEqual(
            self.call("check", str(DEMO), "--output", str(output), "--format", "json")[0], 0
        )
        self.assertEqual(self.call("check", str(DEMO), "--output", str(output))[0], 2)
        self.assertEqual(self.call("check", str(DEMO), "--output", str(output), "--force")[0], 0)

    def test_two_models_have_independent_namespaces(self):
        minimal_model(self.root / "One.SemanticModel" / "definition")
        minimal_model(self.root / "Two.SemanticModel" / "definition")
        diagnostics, summary = check(self.root)
        self.assertFalse(diagnostics)
        self.assertEqual(summary["models"], 2)

    def test_markdown_escapes_metadata(self):
        model = minimal_model(self.root)
        nodes, _ = load_model(model)
        nodes[0].description = "<script>|a\nb"
        text = model_documentation(nodes)
        self.assertIn("&lt;script>&#124;a<br>b", text)
        self.assertNotIn("<script>", text)

    def test_doctor_never_launches_tools(self):
        from unittest.mock import patch

        with patch("subprocess.run", side_effect=AssertionError("Tool must not launch")):
            status, out, _ = self.call("doctor")
        self.assertEqual(status, 0)
        self.assertIn("tools", json.loads(out))

    def test_doctor_reports_platform_without_os_probes(self):
        from unittest.mock import patch

        for identifier, expected in (
            ("win32", "Windows"),
            ("darwin", "Darwin"),
            ("linux", "Linux"),
        ):
            # Keep shutil.which on the host OS while simulating interpreter metadata for doctor.
            with (
                self.subTest(platform=identifier),
                patch(
                    "pbi_codex.operations.sys", SimpleNamespace(platform=identifier), create=True
                ),
                patch("platform.system", side_effect=AssertionError("OS probe must not run")),
                patch("subprocess.run", side_effect=AssertionError("Process must not launch")),
            ):
                status, out, _ = self.call("doctor")
                self.assertEqual(status, 0)
                self.assertEqual(json.loads(out)["platform"], expected)

    def test_cache_directories_are_ignored(self):
        write(self.root / ".pbi" / "bad.json", "{")
        write(self.root / ".git" / "bad.json", "{")
        write(self.root / "good.json", "{}")
        self.assertEqual([p.name for p in files_under(self.root, {".json"})], ["good.json"])

    def test_large_input_fails_cleanly(self):
        path = self.root / "large.dax"
        with path.open("wb") as stream:
            stream.truncate(10 * 1024 * 1024 + 1)
        self.assertEqual(self.call("dax", str(path))[0], 2)

    def test_fabric_plan_has_hashes_and_no_execution(self):
        plan = fabric_plan(ROOT / "examples" / "fabric" / "manifest.json")
        self.assertFalse(plan["remoteOperationsExecuted"])
        self.assertTrue(plan["requiresExplicitAuthorization"])
        self.assertEqual(len(plan["actions"][0]["files"][0]["sha256"]), 64)

    def test_fabric_rejects_escape_and_unknown_type(self):
        path = self.root / "manifest.json"
        for item in (
            {"name": "x", "type": "Unknown", "source": "x.py"},
            {"name": "x", "type": "Notebook", "source": "../outside.py"},
        ):
            write_json(path, {"version": 1, "workspace": "Development", "items": [item]})
            self.assertEqual(self.call("fabric-plan", str(path))[0], 2)

    def test_timings_median(self):
        path = write_json(
            self.root / "timings.json",
            {
                "version": 1,
                "cases": [
                    {"name": "test", "baselineMs": [100, 200, 150], "candidateMs": [75, 60, 90]}
                ],
            },
        )
        result = compare_timings(path)["cases"][0]
        self.assertEqual((result["baselineMedianMs"], result["changePercent"]), (150, -50))

    def test_timings_reject_invalid_samples(self):
        for samples in ([1, 2], [0, 1, 2], [True, 2, 3], ["1", 2, 3], [float("inf"), 2, 3]):
            path = write_json(
                self.root / "timings.json",
                {
                    "version": 1,
                    "cases": [{"name": "test", "baselineMs": samples, "candidateMs": [1, 2, 3]}],
                },
            )
            self.assertEqual(self.call("compare-timings", str(path))[0], 2)

    def test_launcher_outside_checkout_and_path_with_spaces(self):
        copied = self.root / "project with spaces"
        shutil.copytree(DEMO, copied)
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "pbi.py"), "check", str(copied), "--strict"],
            cwd=self.root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
