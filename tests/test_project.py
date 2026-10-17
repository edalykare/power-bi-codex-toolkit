import tempfile
import unittest
from pathlib import Path

from tests.helpers import DEMO, write, write_json

# isort: split

from pbi_codex.project import load_json, local_target, validate_project


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def test_demo_is_structurally_clean(self):
        self.assertEqual(validate_project(DEMO), [])

    def test_duplicate_json_keys(self):
        path = write(self.root / "bad.json", '{"name":"a","name":"b"}')
        with self.assertRaises(ValueError):
            load_json(path)
        self.assertEqual(validate_project(self.root)[0].code, "JSON001")

    def test_nonfinite_json(self):
        write(self.root / "bad.json", '{"duration":NaN}')
        self.assertEqual(validate_project(self.root)[0].code, "JSON001")

    def test_malformed_json(self):
        write(self.root / "bad.json", "{")
        self.assertEqual(validate_project(self.root)[0].code, "JSON001")

    def test_absolute_and_escaping_paths(self):
        for value in (
            "../../outside",
            "/tmp/a",
            "C:\\data\\Report",
            "\\\\server\\share",
            "C:relative",
            "",
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                local_target(self.root, value, self.root)

    def test_windows_relative_reference(self):
        target = self.root / "Model"
        target.mkdir()
        report = self.root / "Report"
        report.mkdir()
        self.assertEqual(local_target(report, "..\\Model", self.root), target)

    def test_pbip_missing_report(self):
        write_json(self.root / "Test.pbip", {"artifacts": [{"report": {"path": "Missing.Report"}}]})
        self.assertEqual(validate_project(self.root)[0].code, "PATH001")

    def test_invalid_pbip_artifacts(self):
        for value in ({"artifacts": {}}, {"artifacts": [None]}, []):
            write_json(self.root / "Test.pbip", value)
            self.assertTrue(any(d.severity == "error" for d in validate_project(self.root)))

    def test_ambiguous_binding_is_error(self):
        write_json(
            self.root / "definition.pbir", {"datasetReference": {"byPath": {}, "byConnection": {}}}
        )
        self.assertIn("PBIR001", [d.code for d in validate_project(self.root)])

    def test_remote_binding_is_explicitly_unresolved(self):
        write_json(self.root / "definition.pbir", {"datasetReference": {"byConnection": {}}})
        self.assertIn("PBIR900", [d.code for d in validate_project(self.root)])

    def test_page_order_and_active_name(self):
        write_json(
            self.root / "pages" / "pages.json",
            {"pageOrder": ["Missing"], "activePageName": "Other"},
        )
        self.assertEqual({d.code for d in validate_project(self.root)}, {"PBIR004", "PBIR005"})

    def test_duplicate_page_order(self):
        write_json(self.root / "pages" / "pages.json", {"pageOrder": ["A", "A"]})
        self.assertIn("PBIR003", [d.code for d in validate_project(self.root)])

    def test_invalid_visual_dimensions(self):
        write_json(
            self.root / "Visual1" / "visual.json",
            {"name": "Wrong", "position": {"x": 0, "y": 0, "z": 0, "width": -1, "height": 10}},
        )
        self.assertEqual({d.code for d in validate_project(self.root)}, {"PBIR006", "PBIR009"})

    def test_boolean_is_not_numeric_dimension(self):
        write_json(
            self.root / "Page1" / "page.json", {"name": "Page1", "width": True, "height": 10}
        )
        self.assertEqual(validate_project(self.root)[0].code, "PBIR007")

    def test_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            link = self.root / "Link"
            try:
                link.symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest("Symlinks require additional Windows privileges")
            with self.assertRaises(ValueError):
                local_target(self.root, "Link", self.root)
