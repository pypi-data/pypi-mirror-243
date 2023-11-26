from .base import EveParser
from .converters import to_int
from .errors import ParserError
from .validators import is_int


class Icons(EveParser):
    """Enhanced Ward Console	31"""

    @classmethod
    def parse(cls, string):
        if "\t" not in string:
            raise ParserError
        parts = string.split("\t")
        if len(parts) != 2:
            raise ParserError
        name, quantity_str = parts
        if not is_int(quantity_str):
            raise ParserError
        quantity = to_int(quantity_str)
        return name, quantity


class ListDetail(EveParser):
    """Enhanced Ward Console	31	Salvaged Materials"""

    @classmethod
    def parse(cls, string):
        if "\t" not in string:
            raise ParserError
        parts = string.split("\t")
        if len(parts) != 3:
            raise ParserError
        name, quantity_str, group = parts
        if not is_int(quantity_str):
            raise ParserError
        quantity = to_int(quantity_str)
        return name, quantity
