import unittest
from datetime import datetime
from spotify_analysis import format_date


class TestInfo(unittest.TestCase):
    def test_typematch(self):
        self.assertEqual(
            type(format_date('15 September 2017')), datetime)

    def test_space_dayshort(self):
        self.assertEqual(
            format_date('6 January 2017'), datetime(2017, 1, 6))

    def test_space_dayfull(self):
        self.assertEqual(
            format_date('29 November 2019'), datetime(2019, 11, 29))

    def test_dot_dayshort_yearshort(self):
        self.assertEqual(
            format_date('4.May.18'), datetime(2018, 5, 4))

    def test_dot_dayfull_yearshort(self):
        self.assertEqual(
            format_date('10.April.19'), datetime(2019, 4, 10))


if __name__ == '__main__':
    unittest.main()
