from eveparse import converters
from eveparse import exceptions
from eveparse import translations


def icons(string: str) -> dict:
    parts = string.split("\t")
    if len(parts) != 2:
        raise exceptions.ParserException(string)
    type_name, quantity_string = parts
    if not quantity_string.strip():
        quantity = 1
    else:
        quantity = converters.quantity_string_to_int(string=quantity_string)
    type_id = converters.type_name_to_type_id(type_name=type_name)
    return {type_id: quantity}


def details(string: str) -> dict:
    parts = string.split("\t")
    if len(parts) != 7:
        raise exceptions.ParserException(string)
    if not any([unit in parts[5] for unit in translations.VOLUME_UNITS]):
        raise exceptions.ParserException(string)
    if not any([unit in parts[6] for unit in translations.ISK_UNITS]):
        raise exceptions.ParserException(string)
    type_name, quantity_string, *_ = parts
    if quantity_string.strip():
        quantity = converters.quantity_string_to_int(string=quantity_string)
    else:
        quantity = 1
    type_id = converters.type_name_to_type_id(type_name=type_name)
    return {type_id: quantity}
