import unittest
import tympy as TO


class TestTympy(unittest.TestCase):
    def setUp(self):
        self.t = TO

    def test_compare_with_multiple_files_and_functions(self):
        self.t.compare(["example_1.py", "example_2.py", "example_3.py"],
                       ["sum", "SuM", "SuMIT"],
                       [(5, 9), (9, 5), (5, 9)])

    def test_compare_with_mismatched_length(self):
        with self.assertRaises(Exception):
            self.t.compare(["example_1.py", "example_2.py"],
                           ["sum", "SuM", "SuMIT"],
                           [(5, 9), (9, 5), (5, 9)])

    def test_compare_with_single_string_function(self):
        self.t.compare(["example_1.py", "example_2.py"],
                       "subtract",
                       [(5, 9), (9, 5)])

    def test_compare_with_single_tuple_argument(self):
        self.t.compare(["example_1.py", "example_3.py"],
                       ["sum", "SuMIT"],
                       (5, 9))

    def test_compare_with_single_string_argument(self):
        self.t.compare(["example_1.py", "example_2.py"],
                       ["printNOW", "printNoW"],
                       "Hello World!")


if __name__ == '__main__':
    unittest.main()
