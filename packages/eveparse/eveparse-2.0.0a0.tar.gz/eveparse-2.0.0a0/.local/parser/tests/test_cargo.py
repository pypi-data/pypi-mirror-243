from django.test import TestCase
from parser.cargo import Icons, ListDetail
from parser.errors import ParserError


class IconsTestCase(TestCase):
    def test_valid_example(self):
        string = "Enhanced Ward Console	31"
        expected = "Enhanced Ward Console", 31
        result = Icons.parse(string)
        self.assertEqual(expected, result)

    def test_no_tab(self):
        string = "Enhanced Ward Console 31"
        self.assertRaises(ParserError, Icons.parse, string)

    def test_extra_tab(self):
        string = "Enhanced Ward Console	31	1000"
        self.assertRaises(ParserError, Icons.parse, string)

    def test_no_quantity(self):
        string = "Enhanced Ward Console	string"
        self.assertRaises(ParserError, Icons.parse, string)

    def test_quantity_first(self):
        string = "31	Enhanced Ward Console"
        self.assertRaises(ParserError, Icons.parse, string)


class ListTestCase(TestCase):
    def test_valid_example(self):
        string = "Enhanced Ward Console	31	Salvaged Materials"
        expected = "Enhanced Ward Console", 31
        result = ListDetail.parse(string)
        self.assertEqual(expected, result)

    def test_no_tab(self):
        string = "Enhanced Ward Console 31 Salvaged Materials"
        self.assertRaises(ParserError, ListDetail.parse, string)

    def test_extra_tab(self):
        string = "Enhanced Ward Console	31	Salvaged Materials	string"
        self.assertRaises(ParserError, ListDetail.parse, string)

    def test_no_quantity(self):
        string = "Enhanced Ward Console	string	Salvaged Materials"
        self.assertRaises(ParserError, ListDetail.parse, string)
