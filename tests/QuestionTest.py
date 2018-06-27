import unittest

from pyprint.ConsolePrinter import ConsolePrinter
from coala_utils.ContextManagers import (
    simulate_console_inputs, suppress_stdout, retrieve_stdout)
from coala_utils.Question import ask_question, ask_yes_no


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


class TestYesNo(unittest.TestCase):

    def setUp(self):
        self.printer = ConsolePrinter()
        self.question_text = 'Are you sure?'

    def test_ask_yes_no(self):
        with simulate_console_inputs('yes'), retrieve_stdout() as custom_stdout:
            response = ask_yes_no(
                self.question_text,
                printer=self.printer)
            self.assertIn(
                self.question_text,
                custom_stdout.getvalue())
            self.assertIn(
                ' [y/n] ',
                custom_stdout.getvalue())
            self.assertTrue(response)

    def test_yes_no_default(self):
        with simulate_console_inputs(''), retrieve_stdout() as custom_stdout:
            response = ask_yes_no(
                self.question_text,
                default='no')
            self.assertIn(
                self.question_text,
                custom_stdout.getvalue())
            self.assertIn(
                ' [y/N] ',
                custom_stdout.getvalue())
            self.assertFalse(response)

    def test_yes_no_change_default(self):
        with simulate_console_inputs('No'), retrieve_stdout() as custom_stdout:
            response = ask_yes_no(
                self.question_text,
                default='yes',
                printer=self.printer)
            self.assertIn(
                self.question_text,
                custom_stdout.getvalue())
            self.assertIn(
                ' [Y/n] ',
                custom_stdout.getvalue())
            self.assertFalse(response)

    def test_yes_no_loop(self):
        with simulate_console_inputs('', 'Noo', 'q', 'y'), \
                retrieve_stdout() as custom_stdout:
            response = ask_yes_no(
                self.question_text,
                default=None,
                printer=self.printer)
            self.assertEqual(
                3,
                custom_stdout.getvalue().count('Invalid'))
            self.assertEqual(
                4,
                custom_stdout.getvalue().count(self.question_text))
            self.assertEqual(
                4,
                custom_stdout.getvalue().count(' [y/n] '))
            self.assertTrue(response)

    def test_yes_no_invalid_default(self):
        with simulate_console_inputs('y'):
            with self.assertRaises(ValueError):
                ask_yes_no(
                    self.question_text,
                    default='nahh',
                    printer=self.printer)
