import pytest

from eveparse import exceptions
from eveparse.parsers import inventory


def test_icons():
    string = "isogen	542383"
    expected = {37: 542383}
    actual = inventory.icons(string=string)
    assert actual == expected


def test_icons_no_quantity():
    string = "isogen	"
    expected = {37: 1}
    actual = inventory.icons(string=string)
    assert actual == expected


def test_icons_columns():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "isogen	542383	1"
        assert inventory.icons(string=string)
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "isogen"
        assert inventory.icons(string=string)


def test_details_item():
    string = "mobile depot	1	mobile depot			50 m3	2,082,587.93 isk"
    expected = {33474: 1}
    actual = inventory.details(string=string)
    assert actual == expected


def test_details_ship():
    string = "charon		freighter			16,250,000 m3	2,250,133,333.33 isk"
    expected = {20185: 1}
    actual = inventory.details(string=string)
    assert actual == expected


def test_details_columns():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "charon		freighter		16,250,000 m3	2,250,133,333.33 isk"
        assert inventory.details(string=string)
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "charon		freighter				16,250,000 m3	2,250,133,333.33 isk"
        assert inventory.details(string=string)


def test_details_volume():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "charon		freighter			16,250,000	2,250,133,333.33 isk"
        assert inventory.icons(string=string)


def test_details_isk():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "charon		freighter			16,250,000 m3	2,250,133,333.33"
        assert inventory.icons(string=string)


def test_details_quantity():
    string = "charon	2	freighter			16,250,000 m3	2,250,133,333.33 isk"
    expected = {20185: 2}
    actual = inventory.details(string=string)
    assert actual == expected
