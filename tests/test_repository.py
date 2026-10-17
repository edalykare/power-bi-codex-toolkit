import importlib.util
import json
import re
import tomllib
import unittest

from tests.helpers import ROOT


class RepositoryTests(unittest.TestCase):
    def test_repository_contracts(self):
        spec = importlib.util.spec_from_file_location(
            "repo_check", ROOT / "scripts" / "check_repo.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.check(), [])

    def test_version_consistency(self):
        metadata = tomllib.loads((ROOT / "pyproject.toml").read_text())
        source = (ROOT / "src" / "pbi_codex" / "__init__.py").read_text()
        version = re.search(r'__version__ = "([^"]+)"', source).group(1)
        self.assertEqual(version, metadata["project"]["version"])

    def test_reference_inventory_covers_all_domains(self):
        inventory = json.loads((ROOT / "docs" / "reference-inventory.json").read_text())
        self.assertEqual(len(inventory["plugins"]), 13)
        self.assertEqual(sum(len(p["skills"]) for p in inventory["plugins"]), 33)
        self.assertEqual(sum(len(p["agents"]) for p in inventory["plugins"]), 8)

    @unittest.skipUnless(importlib.util.find_spec("yaml"), "Install dev extras for YAML checks")
    def test_yaml_and_skill_frontmatter_parse(self):
        import yaml

        for path in [*ROOT.glob(".github/**/*.yml"), ROOT / ".pre-commit-config.yaml"]:
            with self.subTest(path=path):
                self.assertIsInstance(yaml.safe_load(path.read_text()), dict)
        for path in ROOT.glob(".agents/skills/*/SKILL.md"):
            with self.subTest(path=path):
                metadata = yaml.safe_load(path.read_text().split("---", 2)[1])
                self.assertEqual(metadata["name"], path.parent.name)
                self.assertIsInstance(metadata["description"], str)
