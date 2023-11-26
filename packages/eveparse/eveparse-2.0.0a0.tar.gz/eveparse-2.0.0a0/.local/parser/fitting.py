from .base import EveParser
from .errors import ParserError


class FittingShipTypeName(EveParser):
    """[Venture, Alpha Miner]"""

    @classmethod
    def parse(cls, string):
        if not string.startswith("["):
            raise ParserError("Leading [ not found")
        if "," not in string:
            raise ParserError("Required comma not found")
        parts = string.split(", ")
        name, _ = parts
        name = name.strip("[")
        return name, 1
