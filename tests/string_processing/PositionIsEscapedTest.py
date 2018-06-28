
from coala_utils.string_processing import position_is_escaped
from tests.string_processing.StringProcessingTestBase import (
    StringProcessingTestBase)


class PositionIsEscapedTest(StringProcessingTestBase):
    # Test the position_is_escaped() function.

    def test_basic(self):
        expected_results = [
            30 * [False] + [True] + 7 * [False],
            30 * [False] + [True] + 7 * [False],
            30 * [False] + [True] + 7 * [False],
            28 * [False] + [True, False, True] + 7 * [False],
            31 * [False] + [True] + 6 * [False],
            31 * [False] + [True] + 6 * [False],
            38 * [False],
            6 * [False] + [True] + 31 * [False],
            6 * [False] + [True, False, True] + 29 * [False],
            6 * [False] + [True] + 31 * [False],
            6 * [False] + [True, False, True] + 29 * [False],
            14 * [False] + [True] + 23 * [False],
            12 * [False] + [True, False, True] + 23 * [False],
            38 * [False],
            [],
            14 * [False],
            [False],
            [False, True]]

        self.assertResultsEqual(
            position_is_escaped,
            {(test_string, position): result
             for test_string, string_result in zip(self.test_strings,
                                                   expected_results)
             for position, result in zip(range(len(test_string)),
                                         string_result)})

    # Test position_is_escaped() with a more special test string.
    def test_extended(self):
        test_string = r"\\\\\abcabccba###\\13q4ujsabbc\+'**'ac###.#.####-ba"
        result_dict = {
            0: False,
            1: True,
            2: False,
            3: True,
            4: False,
            5: True,
            6: False,
            7: False,
            17: False,
            18: True,
            19: False,
            30: False,
            31: True,
            50: False,
            51: False,
            6666666: False,
            -1: False,
            -20: True,
            -21: False}

        self.assertResultsEqual(
            position_is_escaped,
            {(test_string, position): result
             for position, result in result_dict.items()})

    # Test position_is_escaped() for a PowerShell script
    def test_powershell(self):
        expected_results = [
            7 * [False] + [True] + 11 * [False] + [True] + 9 * [False],
            12 * [False] + [True] + 5 * [False] + [True] + 7 * [False],
            11 * [False] + [True, False, True] + 7 * [False] + [True, False],
            20 * [False] + [True] + 9 * [False] + [True] + 4 * [False] + [True],
            4 * [False] + [True] + 3 * [False] + [True] + 11 * [False],
            24 * [False] + [True] + 12 * [False],
        ]

        self.assertResultsEqual(
            position_is_escaped,
            {(test_string, position, '`'): result
             for test_string, string_result in zip(self.powershell_test_script,
                                                   expected_results)
             for position, result in zip(range(len(test_string)),
                                         string_result)})
