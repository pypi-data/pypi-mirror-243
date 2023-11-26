from django.test import TestCase
from parser import parse
from parser.errors import ParserError


class ParserTestCase(TestCase):
    def test_expected_pass(self):
        self.assertEqual(parse("25000mm Steel Plates II"), ("25000mm Steel Plates II", 1))
        self.assertEqual(parse("Prototype Cloaking Device I x1"), ("Prototype Cloaking Device I", 1))

    def test_expected_fail(self):
        self.assertRaises(ParserError, parse, "")
