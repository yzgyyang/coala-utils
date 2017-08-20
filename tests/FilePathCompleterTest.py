import os
import shutil
import unittest

from coala_utils.FilePathCompleter import (
    path_completer, FilePathCompleter)
from coala_utils.ContextManagers import (
    retrieve_stdout, simulate_console_inputs)

try:
    import readline
except ImportError:
    import pyreadline as readline


class FilePathCompleterTest(unittest.TestCase):

    def setUp(self):
        os.makedirs("test_dir", exist_ok=True)

        touch(os.path.join("test_dir", "a_file"))
        touch(os.path.join("test_dir", "b_file"))
        touch("c_file")

        self.fpc = FilePathCompleter()

        self.directory = os.getcwd()

    def assert_expected_output(self, user_input, expected_output):
        state = 0
        try:
            while True:
                self.assertEqual(expected_output[state],
                                 path_completer(user_input, state))
                state += 1
        except IndexError:
            self.assertEqual(state, len(expected_output))

    def test_path_completer(self):
        self.fpc.activate()
        self.assertEqual(readline.get_completer(), path_completer)
        self.assert_expected_output("test_d", ['test_dir' + os.sep])
        self.assert_expected_output(
            "test_dir" + os.sep, [os.path.join("test_dir", "a_file"),
                                  os.path.join("test_dir", "b_file")])
        self.assert_expected_output(
            os.path.join("test_dir", "a"), [os.path.join("test_dir", "a_file")])
        self.assert_expected_output("c_fi", ["c_file"])
        self.fpc.deactivate()
        self.assertEqual(readline.get_completer(), None)

    def tearDown(self):
        shutil.rmtree("test_dir")
        os.remove("c_file")


def touch(fpath):
    try:
        os.utime(fpath, None)
    except OSError:
        open(fpath, 'a').close()
