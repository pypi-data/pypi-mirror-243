import pytest

from eveparse import exceptions
from eveparse.parsers import compare


def test_dynamic_columns():
    string = "'full duplex' ballistic control system	storyline	58,884,220.91 isk	10.50 %"
    expected = {21484: 1}
    actual = compare.dynamic_columns(string=string)
    assert actual == expected


def test_dynamic_columns_name_only():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "'full duplex' ballistic control system"
        assert compare.dynamic_columns(string=string)


def test_dynamic_columns_two():
    string = "'full duplex' ballistic control system	storyline"
    expected = {21484: 1}
    actual = compare.dynamic_columns(string=string)
    assert actual == expected


def test_dynamic_columns_two_invalid_meta_group():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "'full duplex' ballistic control system	invalid meta group"
        assert compare.dynamic_columns(string=string)


def test_dynamic_columns_three_invalid_meta_group():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "'full duplex' ballistic control system	invalid meta group	58,884,220.91 isk"
        assert compare.dynamic_columns(string=string)


def test_dynamic_columns_with_quantity():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "'full duplex' ballistic control system	storyline	58,884,220.91 isk	100"
        assert compare.dynamic_columns(string=string)
