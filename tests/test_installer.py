import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import DEMO, ROOT

spec = importlib.util.spec_from_file_location("installer", ROOT / "scripts" / "install_skills.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.destination = Path(self.temp.name).resolve() / "project skills"

    def test_single_skill_is_independent(self):
        installed = installer.install(["dax-expert"], self.destination)
        self.assertEqual([p.name for p in self.destination.iterdir()], ["dax-expert"])
        skill = installed[0]
        self.assertTrue((skill / "LICENSE").exists())
        # Isolated mode suppresses PYTHONPATH and user site-package leakage.
        environment = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
        result = subprocess.run(
            [
                sys.executable,
                "-I",
                str(skill / "scripts" / "pbi.py"),
                "check",
                str(DEMO),
                "--strict",
                "--format",
                "json",
            ],
            cwd=self.destination,
            env=environment,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["diagnostics"], [])

    def test_existing_skill_is_never_overwritten(self):
        installer.install(["dax-expert"], self.destination)
        sentinel = self.destination / "dax-expert" / "my-notes.txt"
        sentinel.write_text("keep")
        with self.assertRaises(FileExistsError):
            installer.install(["dax-expert"], self.destination)
        self.assertEqual(sentinel.read_text(), "keep")

    def test_selection_preflight_prevents_partial_installs(self):
        installer.install(["semantic-model"], self.destination)
        with self.assertRaises(FileExistsError):
            installer.install(["dax-expert", "semantic-model"], self.destination)
        self.assertFalse((self.destination / "dax-expert").exists())

    def test_invalid_or_duplicate_names(self):
        for names in (["../outside"], ["dax-expert", "dax-expert"], []):
            with self.subTest(names=names), self.assertRaises(ValueError):
                installer.install(names, self.destination)

    def test_all_skills_install_and_run(self):
        names = sorted(p.name for p in (ROOT / ".agents" / "skills").iterdir())
        for skill in installer.install(names, self.destination):
            result = subprocess.run(
                [sys.executable, "-I", str(skill / "scripts" / "pbi.py"), "--version"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "0.1.0")

    def test_project_scope_option(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "install_skills.py"),
                "semantic-model",
                "--project",
                str(self.destination),
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            (self.destination / ".agents" / "skills" / "semantic-model" / "SKILL.md").exists()
        )
