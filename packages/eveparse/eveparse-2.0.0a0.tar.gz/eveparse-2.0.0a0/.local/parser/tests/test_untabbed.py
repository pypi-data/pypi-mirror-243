from django.test import TestCase
from parser.errors import ParserError
from parser.untabbed import NameOnly, NameQuantity, NameXQuantity, QuantityName, QuantityXName


class NameOnlyTestCase(TestCase):
    def test_expected_passes(self):
        string = "Siege Module II"
        expected = "Siege Module II", 1
        result = NameOnly.parse(string)
        self.assertEqual(expected, result)

    def test_tab_fails(self):
        string = "Siege Module II	1"
        self.assertRaises(ParserError, NameOnly.parse, string)


class NameQuantityTestCase(TestCase):
    def test_expected_pass(self):
        string = "Rifter 2"
        expected = "Rifter", 2
        result = NameQuantity.parse(string)
        self.assertEqual(result, expected)

    def test_tab_fail(self):
        string = "Rifter	1"
        self.assertRaises(ParserError, NameQuantity.parse, string)

    def test_bad_regex_fail(self):
        string = "Rifter string"
        self.assertRaises(ParserError, NameQuantity.parse, string)

    def test_no_space_fail(self):
        string = "Rifter"
        self.assertRaises(ParserError, NameQuantity.parse, string)


class NameXQuantityTestCase(TestCase):
    def test_expected_passes(self):
        string = "Siege Module II x1"
        expected = "Siege Module II", 1
        result = NameXQuantity.parse(string)
        self.assertEqual(expected, result)

    def test_tab_fails(self):
        string = "Siege Module II	x1"
        self.assertRaises(ParserError, NameXQuantity.parse, string)

    def test_no_x_fails(self):
        string = "Siege Module II 1"
        self.assertRaises(ParserError, NameXQuantity.parse, string)

    def test_extra_x_fails(self):
        string = "Siege Module II x1 x2"
        self.assertRaises(ParserError, NameXQuantity.parse, string)

    def test_string_quantity_fails(self):
        string = "Siege Module II xstring"
        self.assertRaises(ParserError, NameXQuantity.parse, string)


class QuantityNameTestCase(TestCase):
    def test_expected_pass(self):
        string = "21 Thanatos"
        expected = "Thanatos", 21
        result = QuantityName.parse(string)
        self.assertEqual(result, expected)

    def test_tab_fails(self):
        string = "2	Siege Module II"
        self.assertRaises(ParserError, QuantityName.parse, string)

    def test_bad_regex_fail(self):
        string = "string Rifter"
        self.assertRaises(ParserError, QuantityName.parse, string)

    def test_no_space_fail(self):
        string = "Rifter"
        self.assertRaises(ParserError, QuantityName.parse, string)


class QuantityXNameTestCase(TestCase):
    def test_expected_passes(self):
        string = "3x Hobgoblin I"
        expected = "Hobgoblin I", 3
        result = QuantityXName.parse(string)
        self.assertEqual(expected, result)

    def test_multi_x_passes(self):
        string = "3x Capacitor Flux Coil II"
        expected = "Capacitor Flux Coil II", 3
        result = QuantityXName.parse(string)
        self.assertEqual(expected, result)

    def test_tab_fails(self):
        string = "3x	Capacitor Flux Coil II"
        self.assertRaises(ParserError, QuantityXName.parse, string)

    def test_missing_x_space_fails(self):
        string = "3 Capacitor Flux Coil II"
        self.assertRaises(ParserError, QuantityXName.parse, string)
