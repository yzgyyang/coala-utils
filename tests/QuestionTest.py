import unittest

from pyprint.ConsolePrinter import ConsolePrinter
from coala_utils.ContextManagers import (
    simulate_console_inputs, suppress_stdout, retrieve_stdout)
from coala_utils.Question import ask_question


class TestQuestion(unittest.TestCase):

    def setUp(self):
        self.printer = ConsolePrinter()
        self.simulated_input = "42"
        self.question_text = "What is the answer?"
        self.caption = "TestCaption"

    def test_ask_question(self):
        with simulate_console_inputs(self.simulated_input),\
                retrieve_stdout() as custom_stdout:
            response = ask_question(
                self.question_text,
                default=None,
                printer=self.printer)
            self.assertIn(
                self.question_text,
                custom_stdout.getvalue())
            self.assertEqual(response, self.simulated_input)

    def test_question_caption(self):
        with simulate_console_inputs(""), retrieve_stdout() as custom_stdout:
            response = ask_question(
                self.question_text,
                default=self.caption)
            self.assertIn(
                self.question_text + " \x1b[0m[" + self.caption + "]",
                custom_stdout.getvalue())
            self.assertEqual(response, self.caption)

    def test_question_typecast(self):
        with simulate_console_inputs("apples, mangoes"), suppress_stdout():
            response = ask_question(
                self.question_text,
                typecast=list)
            self.assertEqual(response, ["apples", "mangoes"])

    def test_invalid_answer_type(self):
        with simulate_console_inputs("test", "42"), \
                retrieve_stdout() as custom_stdout:
            response = ask_question(
                self.question_text,
                typecast=int)

            self.assertIn("Please enter a", custom_stdout.getvalue())
            self.assertEqual(response, 42)
