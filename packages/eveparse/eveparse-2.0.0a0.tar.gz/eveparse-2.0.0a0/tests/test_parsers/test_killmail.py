import pytest

from eveparse import exceptions
from eveparse.parsers import killmail


def test_content():
    string = "fleeting compact stasis webifier	1		destroyed"
    expected = {4027: 1}
    actual = killmail.content(string=string)
    assert actual == expected


def test_content_columns():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "fleeting compact stasis webifier	1	destroyed"
        assert killmail.content(string=string)
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "fleeting compact stasis webifier	1			destroyed"
        assert killmail.content(string=string)


def test_content_drop_destroy():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "fleeting compact stasis webifier	1	invalid string"
        assert killmail.content(string=string)
