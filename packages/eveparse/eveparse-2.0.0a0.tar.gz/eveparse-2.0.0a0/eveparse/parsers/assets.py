from eveparse import converters
from eveparse import exceptions
from eveparse import translations


def station(string: str) -> dict:
    """Station assets are formatted the same as inventory.details
    and are currently handled by that parser.
    """

    raise NotImplemented(string)


def view_contents_container(string: str) -> dict:
    parts = string.split("\t")
    if len(parts) != 3:
        raise exceptions.ParserException(string)
    type_name, market_group, quantity_string = parts
    if market_group not in translations.MARKET_GROUPS:
        raise exceptions.ParserException(string)
    type_id = converters.type_name_to_type_id(type_name=type_name)
    quantity = converters.quantity_string_to_int(string=quantity_string)
    return {type_id: quantity}


def view_contents_ship(string: str) -> dict:
    parts = string.split("\t")
    if len(parts) != 4:
        raise exceptions.ParserException(string)
    type_name, market_group, _, quantity_string = parts
    if market_group not in translations.MARKET_GROUPS:
        raise exceptions.ParserException(string)
    type_id = converters.type_name_to_type_id(type_name=type_name)
    quantity = converters.quantity_string_to_int(string=quantity_string)
    return {type_id: quantity}
