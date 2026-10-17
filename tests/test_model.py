import tempfile
import unittest
from pathlib import Path

from tests.helpers import DEMO, minimal_model, write

# isort: split

from pbi_codex.model import endpoint, validate_model
from pbi_codex.tmdl import parse_file


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = minimal_model(Path(self.temp.name))

    def codes(self):
        return [d.code for d in validate_model(self.root)[1]]

    def test_valid_model(self):
        self.assertEqual(self.codes(), [])

    def test_demo_counts(self):
        nodes, issues = validate_model(DEMO)
        self.assertFalse(issues)
        self.assertEqual(sum(o.kind == "measure" for o in nodes), 4)
        self.assertEqual(sum(o.kind == "table" for o in nodes), 2)

    def test_missing_endpoint(self):
        write(
            self.root / "relationships.tmdl",
            "relationship broken\n\tfromColumn: Sales.NoSuchKey\n\ttoColumn: Product.Key\n",
        )
        self.assertIn("REL002", self.codes())

    def test_case_insensitive_endpoint_and_quotes(self):
        self.assertEqual(endpoint("'Bob''s Sales'.'Product Key'"), ("bob's sales", "product key"))
        write(
            self.root / "relationships.tmdl",
            "relationship r\n\tfromColumn: sales.productkey\n\ttoColumn: PRODUCT.KEY\n",
        )
        self.assertNotIn("REL002", self.codes())

    def test_type_and_filter_warnings(self):
        write(self.root / "Product.tmdl", "table Product\n\tcolumn Key\n\t\tdataType: string\n")
        with (self.root / "relationships.tmdl").open("a") as f:
            f.write("\tcrossFilteringBehavior: bothDirections\n")
        self.assertIn("REL003", self.codes())
        self.assertIn("REL101", self.codes())

    def test_duplicate_names_case_insensitive(self):
        write(self.root / "duplicate.tmdl", "table product\n")
        self.assertIn("MODEL001", self.codes())

    def test_measure_names_are_global(self):
        with (self.root / "Product.tmdl").open("a") as f:
            f.write("\tmeasure rows = 1\n")
        self.assertIn("MODEL001", self.codes())

    def test_missing_measure_metadata(self):
        write(self.root / "new.tmdl", "table New\n\tmeasure X = 1\n")
        self.assertIn("META101", self.codes())
        self.assertIn("META102", self.codes())

    def test_qualified_member_validation(self):
        write(self.root / "new.tmdl", "table New\n\tmeasure X = SUM(Sales[Typo])\n")
        self.assertIn("DAX201", self.codes())

    def test_multiline_and_consecutive_descriptions(self):
        path = write(
            self.root / "fenced.tmdl",
            "table New\n\t/// First line\n\t/// Second line\n\tmeasure X = ```\n\t\tVAR x = [Rows]\n\t\tRETURN x\n\t\t```\n\t\tformatString: 0\n\t\tdisplayFolder: Counts\n",
        )
        nodes, issues = parse_file(path)
        measure = next(o for o in nodes if o.kind == "measure")
        self.assertEqual(measure.description, "First line\nSecond line")
        self.assertIn("RETURN x", measure.expression)
        self.assertEqual(measure.properties["formatString"], "0")
        self.assertFalse(issues)

    def test_unclosed_fence(self):
        write(self.root / "broken.tmdl", "table New\n\tmeasure X = ```\n\t\t1\n")
        self.assertIn("TMDL002", self.codes())

    def test_multiline_expression_preserves_source_lines(self):
        write(
            self.root / "multiline.tmdl",
            "table New\n\t/// Multiline\n\tmeasure X =\n"
            "\t\t\tVAR x = 1\n\n\t\t\t// explanation\n\t\t\tRETURN (x\n"
            "\t\tformatString: 0\n\t\tdisplayFolder: Counts\n",
        )
        diagnostics = validate_model(self.root)[1]
        errors = [d for d in diagnostics if d.code == "DAX001"]
        self.assertEqual([d.line for d in errors], [7])

    def test_orphan_measure(self):
        write(self.root / "broken.tmdl", "measure X = 1\n")
        self.assertIn("TMDL001", self.codes())

    def test_mixed_indentation(self):
        write(self.root / "mixed.tmdl", "table New\n\tcolumn Key\n        dataType: int64\n")
        self.assertIn("TMDL101", self.codes())

    def test_no_tmdl_does_not_pass(self):
        with tempfile.TemporaryDirectory() as empty:
            self.assertEqual(validate_model(Path(empty))[1][0].code, "TMDL000")
