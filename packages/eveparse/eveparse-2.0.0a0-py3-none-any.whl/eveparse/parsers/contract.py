from eveparse import converters
from eveparse import exceptions
from eveparse import translations


def multiple_items(string: str) -> dict:
    parts = string.split("\t")
    if len(parts) != 5:
        raise exceptions.ParserException(string)
    type_name, quantity_string, market_group, category, details = parts
    if market_group not in translations.MARKET_GROUPS:
        raise exceptions.ParserException(string)
    type_id = converters.type_name_to_type_id(type_name=type_name)
    quantity = converters.quantity_string_to_int(string=quantity_string)
    return {type_id: quantity}


def multiple_items_no_details(string: str) -> dict:
    parts = string.split("\t")
    if len(parts) != 4:
        raise exceptions.ParserException(string)
    type_name, quantity_string, market_group, category = parts
    if market_group not in translations.MARKET_GROUPS:
        raise exceptions.ParserException(string)
    type_id = converters.type_name_to_type_id(type_name=type_name)
    quantity = converters.quantity_string_to_int(string=quantity_string)
    return {type_id: quantity}
