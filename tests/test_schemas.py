import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import DEMO, ROOT, write_json


@unittest.skipUnless(
    importlib.util.find_spec("jsonschema"), "Install dev extras for JSON Schema tests"
)
class SchemaTests(unittest.TestCase):
    def run_schema(self, path):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_schemas.py"), str(path)],
            capture_output=True,
            text=True,
        )

    def test_demo_matches_official_schemas(self):
        result = self.run_schema(DEMO)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("8 file(s)", result.stdout)

    def test_missing_required_theme_is_caught(self):
        with tempfile.TemporaryDirectory() as folder:
            copied = Path(folder) / "project"
            shutil.copytree(DEMO, copied)
            path = copied / "Retail.Report" / "definition" / "report.json"
            write_json(
                path,
                {
                    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.0.0/schema.json"
                },
            )
            result = self.run_schema(copied)
            self.assertEqual(result.returncode, 1)
            self.assertIn("themeCollection", result.stdout)

    def test_untrusted_schema_url_never_fetches(self):
        with tempfile.TemporaryDirectory() as folder:
            write_json(
                Path(folder) / "report.json", {"$schema": "https://untrusted.invalid/schema.json"}
            )
            result = self.run_schema(Path(folder))
            self.assertEqual(result.returncode, 2)
            self.assertIn("no network request made", result.stderr)
