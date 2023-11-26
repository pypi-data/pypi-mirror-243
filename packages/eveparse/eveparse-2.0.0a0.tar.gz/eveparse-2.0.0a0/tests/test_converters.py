import pytest

from eveparse import converters
from eveparse import exceptions


def test_type_name_empty():
    with pytest.raises(expected_exception=exceptions.ConverterException):
        assert converters.type_name_to_type_id("")


def test_type_name_space():
    with pytest.raises(expected_exception=exceptions.ConverterException):
        assert converters.type_name_to_type_id(" ")


def test_type_name_tab():
    with pytest.raises(expected_exception=exceptions.ConverterException):
        assert converters.type_name_to_type_id("	")


def test_type_name_de():
    assert converters.type_name_to_type_id("rifter") == 587


def test_type_name_en():
    assert converters.type_name_to_type_id("rifter") == 587


def test_type_name_es():
    assert converters.type_name_to_type_id("planetología") == 2406


def test_type_name_fr():
    assert converters.type_name_to_type_id("planétologie") == 2406


def test_type_name_ja():
    assert converters.type_name_to_type_id("惑星学") == 2406


def test_type_name_ru():
    assert converters.type_name_to_type_id("планетология") == 2406


def test_type_name_zh():
    assert converters.type_name_to_type_id("行星学") == 2406


def test_type_name_asterisk():
    assert converters.type_name_to_type_id("rifter*") == 587


def test_type_name_invalid():
    with pytest.raises(expected_exception=exceptions.ConverterException):
        assert converters.type_name_to_type_id("invalid string")


def test_quantity_empty():
    with pytest.raises(expected_exception=exceptions.ConverterException):
        assert converters.quantity_string_to_int("")
    with pytest.raises(expected_exception=exceptions.ConverterException):
        assert converters.quantity_string_to_int(" ")
    with pytest.raises(expected_exception=exceptions.ConverterException):
        assert converters.quantity_string_to_int("	")


def test_quantity_padded():
    assert converters.quantity_string_to_int("1 ") == 1
    assert converters.quantity_string_to_int(" 1") == 1
    assert converters.quantity_string_to_int("1	") == 1
    assert converters.quantity_string_to_int("	1") == 1


def test_quantity_invalid_chars():
    with pytest.raises(expected_exception=exceptions.ConverterException):
        assert converters.quantity_string_to_int("1 isk")
    with pytest.raises(expected_exception=exceptions.ConverterException):
        assert converters.quantity_string_to_int("1 m3")


def test_quantity_good_ints():
    assert converters.quantity_string_to_int("1234") == 1234
    assert converters.quantity_string_to_int("1,234") == 1234
    assert converters.quantity_string_to_int("1.234") == 1234
    assert converters.quantity_string_to_int("1,234,567") == 1234567
    assert converters.quantity_string_to_int("1.234.567") == 1234567


def test_quantity_good_floats():
    assert converters.quantity_string_to_int("1,000.00") == 1000
    assert converters.quantity_string_to_int("1.000,00") == 1000
    assert converters.quantity_string_to_int("1000.00") == 1000
    assert converters.quantity_string_to_int("1000,00") == 1000


def test_quantity_bad_ints():
    with pytest.raises(expected_exception=exceptions.ConverterException):
        assert converters.quantity_string_to_int("1,2.3")
    with pytest.raises(expected_exception=exceptions.ConverterException):
        assert converters.quantity_string_to_int("1,000.000")


def test_quantity_bad_floats():
    with pytest.raises(expected_exception=exceptions.ConverterException):
        assert converters.quantity_string_to_int("1,000.0")
    with pytest.raises(expected_exception=exceptions.ConverterException):
        assert converters.quantity_string_to_int("1,000.000")
