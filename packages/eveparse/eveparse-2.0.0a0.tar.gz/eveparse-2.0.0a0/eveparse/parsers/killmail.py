from eveparse import converters
from eveparse import exceptions
from eveparse import translations


def content(string: str) -> dict:
    parts = string.split("\t")
    if len(parts) != 4:
        raise exceptions.ParserException(string)
    type_name, quantity_string, _, drop_destroy = parts
    if drop_destroy not in translations.DROP_DESTROY:
        raise exceptions.ParserException(string)
    quantity = converters.quantity_string_to_int(string=quantity_string)
    type_id = converters.type_name_to_type_id(type_name=type_name)
    return {type_id: quantity}
