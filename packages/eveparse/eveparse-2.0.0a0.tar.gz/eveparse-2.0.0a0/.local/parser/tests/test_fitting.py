from django.test import TestCase
from parser.errors import ParserError
from parser.fitting import FittingShipTypeName


class FittingShipTypeNameTestCase(TestCase):
    def test_expected_pass(self):
        string = "[Venture, Alpha Miner]"
        expected = "Venture", 1
        result = FittingShipTypeName.parse(string)
        self.assertEqual(result, expected)

    def test_bracket_missing_fail(self):
        string = "Venture, Alpha Miner]"
        self.assertRaises(ParserError, FittingShipTypeName.parse, string)

    def test_missing_comma_fail(self):
        string = "[Venture Alpha Miner]"
        self.assertRaises(ParserError, FittingShipTypeName.parse, string)

