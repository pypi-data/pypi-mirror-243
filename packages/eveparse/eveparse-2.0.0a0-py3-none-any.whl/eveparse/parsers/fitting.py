import re

from eveparse import converters
from eveparse import exceptions

X_QUANTITY_RE = re.compile(r" x[\d,\.]+$")
QUANTITY_X_RE = re.compile(r"^[\d,\.]+x ")


def hull_name(string: str) -> dict:
    if not (string.startswith("[") and "," in string and string.endswith("]")):
        raise exceptions.ParserException(string)
    string = string.lstrip("[")
    type_name, *_ = string.split(", ")
    type_id = converters.type_name_to_type_id(type_name=type_name)
    return {type_id: 1}


def type_name_only(string: str) -> dict:
    type_id = converters.type_name_to_type_id(type_name=string)
    return {type_id: 1}


def x_quantity(string: str) -> dict:
    match = X_QUANTITY_RE.search(string)
    if not match:
        raise exceptions.ParserException(string)
    quantity_string = match.group()
    type_name = string.removesuffix(quantity_string)
    quantity_string = quantity_string.removeprefix(" x")
    quantity = converters.quantity_string_to_int(string=quantity_string)
    type_id = converters.type_name_to_type_id(type_name=type_name)
    return {type_id: quantity}


def quantity_x(string: str) -> dict:
    match = QUANTITY_X_RE.search(string)
    if not match:
        raise exceptions.ParserException(string)
    quantity_string = match.group()
    type_name = string.removeprefix(quantity_string)
    quantity_string = quantity_string.removesuffix("x ")
    quantity = converters.quantity_string_to_int(string=quantity_string)
    type_id = converters.type_name_to_type_id(type_name=type_name)
    return {type_id: quantity}


def module_with_ammo(string: str) -> dict:
    if "," not in string:
        raise exceptions.ParserException(string)

    # Raise an exception if the type_name exists
    # There are a few items with commas in the
    # type name, such as Hull Tanking, Elite
    # This parser is not meant to extract those
    try:
        converters.type_name_to_type_id(string)
    except exceptions.ConverterException:
        pass
    else:
        raise exceptions.ParserException

    items = {}
    parts = string.split(",")
    for part in parts:
        try:
            type_id = converters.type_name_to_type_id(part)
        except exceptions.ConverterException:
            continue
        else:
            if type_id in items:
                items[type_id] += 1
            else:
                items[type_id] = 1
    return items
