from django.test import TestCase
from parser.errors import ParserError
from parser.industry import BuyMissingMaterials, InputOutputMaterials


class BuyMissingMaterialsTestCase(TestCase):
    def test_expected_passes(self):
        string = "Siege Module II"
        expected = "Siege Module II", 1
        result = BuyMissingMaterials.parse(string)
        self.assertEqual(expected, result)

    def test_tab_fails(self):
        string = "Siege Module II	1"
        self.assertRaises(ParserError, BuyMissingMaterials.parse, string)


class InputOutputMaterialsTestCase(TestCase):
    def test_expected_passes(self):
        string = "Siege Module II"
        expected = "Siege Module II", 1
        result = InputOutputMaterials.parse(string)
        self.assertEqual(expected, result)

    def test_tab_fails(self):
        string = "Siege Module II	1"
        self.assertRaises(ParserError, InputOutputMaterials.parse, string)
