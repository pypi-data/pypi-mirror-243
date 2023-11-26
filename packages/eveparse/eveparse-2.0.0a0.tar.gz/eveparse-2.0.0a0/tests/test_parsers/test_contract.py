import pytest

from eveparse import exceptions
from eveparse.parsers import contract


def test_multiple_items():
    string = " ice harvester ii	1	strip miner	module	high slot"
    expected = {22229: 1}
    actual = contract.multiple_items(string=string)
    assert actual == expected


def test_multiple_items_columns():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = " ice harvester ii	1	strip miner	module"
        assert contract.multiple_items(string=string)
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = " ice harvester ii	1	strip miner	module	high slot	1"
        assert contract.multiple_items(string=string)


def test_multiple_items_market_group():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = " ice harvester ii	1	invalid market group	module	high slot"
        assert contract.multiple_items(string=string)


def test_multiple_items_no_details():
    string = "mackinaw	1	exhumer	ship"
    expected = {22548: 1}
    actual = contract.multiple_items_no_details(string=string)
    assert actual == expected


def test_multiple_items_no_details_columns():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "mackinaw	1	exhumer	ship	"
        assert contract.multiple_items_no_details(string=string)
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "mackinaw	1	exhumer"
        assert contract.multiple_items_no_details(string=string)


def test_multiple_items_no_details_market_group():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "mackinaw	1	invalid market group	ship"
        assert contract.multiple_items_no_details(string=string)
