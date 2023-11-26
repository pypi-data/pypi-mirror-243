from django.test import TestCase
from parser.converters import to_int
from parser.errors import ConverterError


class ToIntTestCase(TestCase):
    def test_single_digit(self):
        string = "1"
        expected = 1
        result = to_int(string)
        self.assertEqual(expected, result)

    def test_double_digit(self):
        string = "12"
        expected = 12
        result = to_int(string)
        self.assertEqual(expected, result)

    def test_comma_delineated(self):
        string = "1,234"
        expected = 1234
        result = to_int(string)
        self.assertEqual(expected, result)

    def test_period_delineated(self):
        string = "1.234"
        expected = 1234
        result = to_int(string)
        self.assertEqual(expected, result)

    def test_dual_delineated(self):
        string = "1,234.00"
        self.assertRaises(ConverterError, to_int, string)
