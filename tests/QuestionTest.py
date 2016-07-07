import unittest
from unittest.mock import patch
from pygments.token import Token
from pygments.styles.tango import TangoStyle
from prompt_toolkit.styles import style_from_pygments

from coala_utils.Question import ask_question


class QuestionTest(unittest.TestCase):

    def setUp(self):
        self.question = "What's the answer to life, universe and everything?"
        self.default = "42"

    @patch("prompt_toolkit.prompt")
    def test_ask_question(self, patched_prompt):
        patched_prompt.return_value = self.default
        self.assertEqual(
            ask_question(self.question, self.default, prefill=True),
            self.default)

    @patch("prompt_toolkit.prompt")
    def test_ask_question_typecast(self, patched_prompt):
        patched_prompt.return_value = "life, universe, everything"
        self.assertEqual(
            ask_question(self.question, self.default, typecast=list),
            ["life", "universe", "everything"])

    @patch("prompt_toolkit.prompt")
    def test_ask_question_newline(self, patched_prompt):
        patched_prompt.return_value = ""
        self.assertEqual(
            ask_question(self.question, self.default, no_newline=True),
            self.default)

    @patch("prompt_toolkit.prompt")
    def test_ask_question_style(self, patched_prompt):
        patched_prompt.return_value = self.default
        red = style_from_pygments(TangoStyle, {Token.Prompt: "#ff0000"})
        self.assertEqual(
            ask_question(self.question, self.default, style=red),
            self.default)
