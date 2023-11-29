import unittest
import tympy as TO


class TestTympy(unittest.TestCase):
    def setUp(self):
        self.t = TO

    def test_compare(self):
        result = self.t.compare(["example_1.py", "example_2.py", "example_3.py"],
                                ["sum", "SuM", "SuMIT"],
                                [(5, 9), (9, 5), (5, 9)])
        print(result)
        # self.assertEqual(result, [14, 14])


if __name__ == '__main__':
    unittest.main()
