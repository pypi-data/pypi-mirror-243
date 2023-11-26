import pytest

from eveparse import exceptions
from eveparse.parsers import fitting


def test_hull_name():
    string = "[sabre, hyper]"
    expected = {22456: 1}
    actual = fitting.hull_name(string=string)
    assert actual == expected


def test_hull_name_bad_formats():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "sabre, hyper]"
        assert fitting.hull_name(string=string)
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "[sabre, hyper"
        assert fitting.hull_name(string=string)
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "[sabre hyper]"
        assert fitting.hull_name(string=string)
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "[sabre,hyper]"
        assert fitting.hull_name(string=string)


def test_type_name():
    string = "sabre"
    expected = {22456: 1}
    actual = fitting.type_name_only(string=string)
    assert actual == expected


def test_x_quantity():
    string = "expanded cargohold ii x3"
    expected = {1319: 3}
    actual = fitting.x_quantity(string=string)
    assert actual == expected


def test_x_quantity_tab():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "expanded cargohold ii	x3"
        assert fitting.hull_name(string=string)


def test_quantity_x():
    string = "3x expanded cargohold ii"
    expected = {1319: 3}
    actual = fitting.quantity_x(string=string)
    assert actual == expected


def test_quantity_x_tab():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "3x	expanded cargohold ii"
        assert fitting.hull_name(string=string)


def test_module_with_ammo():
    string = "concord xl cruise missile launcher,guristas mjolnir xl cruise missile"
    expected = {2188: 1, 3563: 1}
    actual = fitting.module_with_ammo(string=string)
    assert actual == expected


def test_module_with_ammo_no_comma():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "concord xl cruise missile launcher"
        assert fitting.hull_name(string=string)


def test_module_with_ammo_type_with_comma():
    with pytest.raises(expected_exception=exceptions.ParserException):
        string = "hull tanking, elite"
        assert fitting.hull_name(string=string)
