from django.test import TestCase
from parser.validators import is_int, is_legal


class IsIntTestCase(TestCase):
    def test_single_digit(self):
        string = "1"
        expected = True
        result = is_int(string)
        self.assertEqual(expected, result)

    def test_double_digit(self):
        string = "12"
        expected = True
        result = is_int(string)
        self.assertEqual(expected, result)

    def test_comma_delineated(self):
        string = "1,234"
        expected = True
        result = is_int(string)
        self.assertEqual(expected, result)

    def test_period_delineated(self):
        string = "1.234"
        expected = True
        result = is_int(string)
        self.assertEqual(expected, result)

    def test_dual_delineated(self):
        string = "1,234.00"
        result = is_int(string)
        self.assertFalse(result)

    def test_x_int(self):
        string = "x1"
        expected = False
        result = is_int(string)
        self.assertEqual(expected, result)

    def test_int_x(self):
        string = "1x"
        expected = False
        result = is_int(string)
        self.assertEqual(expected, result)


class IsLegalTestCase(TestCase):
    def test_expected_pass(self):
        self.assertTrue(is_legal("Rifter"))

    def test_empty_fails(self):
        self.assertFalse(is_legal(""))
