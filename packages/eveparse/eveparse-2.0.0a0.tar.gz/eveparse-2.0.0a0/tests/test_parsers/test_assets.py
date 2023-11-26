import pytest

from eveparse import exceptions
from eveparse.parsers import assets


def test_contents_container():
    string = "mystic s	advanced exotic plasma charge	16174"
    expected = {47927: 16174}
    actual = assets.view_contents_container(string=string)
    assert actual == expected


def test_contents_container_columns():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "mystic s	16174"
        assert assets.view_contents_container(string=string)
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "mystic s	advanced exotic plasma charge	16174	"
        assert assets.view_contents_container(string=string)


def test_contents_container_market_group():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "mystic s	invalid market group	16174"
        assert assets.view_contents_container(string=string)


def test_contents_ship():
    string = "caldari navy nova torpedo	torpedo	cargo hold	500"
    expected = {27359: 500}
    actual = assets.view_contents_ship(string=string)
    assert actual == expected


def test_contents_ship_columns():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "caldari navy nova torpedo	torpedo	500"
        assert assets.view_contents_ship(string=string)
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "caldari navy nova torpedo	torpedo	cargo hold	500	"
        assert assets.view_contents_ship(string=string)


def test_contents_ship_market_group():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "caldari navy nova torpedo	invalid market group	cargo hold	500"
        assert assets.view_contents_ship(string=string)
