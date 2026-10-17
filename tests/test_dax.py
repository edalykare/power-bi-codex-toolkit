import unittest

from tests import helpers  # noqa: F401

# isort: split

from pbi_codex.dax import lint_dax, qualified_references, tokenize


class DaxTests(unittest.TestCase):
    def test_valid_expression(self):
        self.assertEqual(lint_dax("DIVIDE([Profit], [Revenue])"), [])

    def test_comments_and_strings_do_not_change_structure(self):
        self.assertEqual(lint_dax('ROW("text", "a / ( ) FORMAT(""x"")") // ( /\n/* } */'), [])

    def test_all_comment_styles(self):
        self.assertEqual(lint_dax("1 -- (\n + 2 // }\n/* ( */"), [])

    def test_escaped_names(self):
        self.assertEqual(
            qualified_references("SUM('Bob''s Sales'[A]]B])"), [("Bob's Sales", "A]B", 1)]
        )

    def test_return_is_not_a_table_reference(self):
        self.assertEqual(qualified_references("VAR x = [Revenue] RETURN [Profit]"), [])

    def test_unknown_qualified_reference_is_extracted(self):
        self.assertEqual(qualified_references("SUM(Sales[Wrong])"), [("Sales", "Wrong", 1)])

    def test_delimiter_errors(self):
        for text in ("SUM([Sales]", "{1, 2)", ")", "{"):
            with self.subTest(text=text):
                self.assertTrue(any(d.code == "DAX001" for d in lint_dax(text)))

    def test_unclosed_quotes_comments(self):
        for text in ('"abc', "'abc", "[abc", "/* abc"):
            with self.subTest(text=text):
                self.assertTrue(any(d.code == "DAX002" for d in lint_dax(text)))

    def test_division_warning_and_line_offset(self):
        result = lint_dax("\n[A] / [B]", "measure.tmdl", 10)
        self.assertEqual(
            (result[0].code, result[0].line, result[0].severity), ("DAX101", 12, "warning")
        )

    def test_format_is_advisory_only(self):
        self.assertEqual(lint_dax('FORMAT([X], "0")')[0].severity, "info")

    def test_empty_input(self):
        self.assertTrue(any(d.code == "DAX000" for d in lint_dax("// just a comment")))

    def test_lexer_preserves_name_case(self):
        tokens, errors = tokenize("SUM('sAles'[Key])")
        self.assertFalse(errors)
        self.assertIn("sAles", [t.value for t in tokens])
