from django.test import TestCase
from parser.compare import Compare
from parser.errors import ParserError


class CompareTestCase(TestCase):
    def test_valid_example(self):
        string = "Caldari Navy Mjolnir Heavy Missile	Faction"
        expected = "Caldari Navy Mjolnir Heavy Missile", 1
        result = Compare.parse(string)
        self.assertEqual(expected, result)

    def test_no_tab(self):
        string = "Caldari Navy Mjolnir Heavy Missile    Faction"
        self.assertRaises(ParserError, Compare.parse, string)

    def test_extra_tab(self):
        string = "Caldari Navy Mjolnir Heavy Missile	Faction	string"
        expected = "Caldari Navy Mjolnir Heavy Missile", 1
        result = Compare.parse(string)
        self.assertEqual(expected, result)

    def test_not_meta(self):
        string = "Caldari Navy Mjolnir Heavy Missile	String"
        self.assertRaises(ParserError, Compare.parse, string)

    def test_name_quantity(self):
        string = "Caldari Navy Mjolnir Heavy Missile	31"
        self.assertRaises(ParserError, Compare.parse, string)

    def test_quantity_name(self):
        string = "31	Caldari Navy Mjolnir Heavy Missile"
        self.assertRaises(ParserError, Compare.parse, string)
