import re

from .base import EveParser
from .converters import to_int
from .errors import ParserError
from .validators import is_int

NAME_QUANTITY = re.compile(r".+\s+[\d+\.,]+$", re.IGNORECASE)
QUANTITY_NAME = re.compile(r"[\d+\.,]+\s+\S+", re.IGNORECASE)


class NameOnly(EveParser):
    """No tabs, no quantity, no delineators, no formatting.
    Last-ditch effort to extract a name from a string.
    Returns a default quantity of 1.
    Returned name must be checked for membership in known item names.
    """

    @classmethod
    def parse(cls, string):
        if "\t" in string:
            raise ParserError("Prohibited tab found")
        return string, 1


class NameQuantity(EveParser):
    @classmethod
    def parse(cls, string: str) -> tuple[str, int]:
        if "\t" in string:
            raise ParserError("Prohibited tab found")
        match = NAME_QUANTITY.match(string)
        if not match:
            raise ParserError("Regex pattern not found")
        parts = string.split()
        if len(parts) < 2:
            raise ParserError("Parts length less than 2")
        quantity_str = parts[-1]
        if not is_int(quantity_str):
            raise ParserError("Quantity not int")
        quantity = to_int(quantity_str)
        name = " ".join(parts[:-1])
        return name, quantity


class NameXQuantity(EveParser):
    """Capacitor Flux Coil II x3"""

    @classmethod
    def parse(cls, string):
        if "\t" in string:
            raise ParserError("Prohibited tab found")
        if " x" not in string:
            raise ParserError("Required space followed by x not found")
        parts = string.split(" x")
        if len(parts) != 2:
            raise ParserError("Not 2 parts")
        name, quantity_str = parts
        if not is_int(quantity_str):
            raise ParserError("Quantity not int")
        quantity = to_int(quantity_str)
        return name, quantity


class QuantityName(EveParser):
    @classmethod
    def parse(cls, string: str) -> tuple[str, int]:
        if "\t" in string:
            raise ParserError("Prohibited tab found")
        match = QUANTITY_NAME.match(string)
        if not match:
            raise ParserError("Regex pattern not found")
        parts = string.split()
        if len(parts) < 2:
            raise ParserError("Parts length less than 2")
        quantity_str = parts[0]
        if not is_int(quantity_str):
            raise ParserError("Quantity not int")
        quantity = to_int(quantity_str)
        name = " ".join(parts[1:])
        return name, quantity


class QuantityXName(EveParser):
    """3x Capacitor Flux Coil II"""

    @classmethod
    def parse(cls, string):
        if "\t" in string:
            raise ParserError("Prohibited tab found")
        if "x " not in string:
            raise ParserError("Required x followed by space not found")
        parts = string.split("x ")
        if len(parts) != 2:
            # 3x Capacitor Flux Coil II has to instances of this
            quantity_str, *rest = parts
            name = "x ".join(rest)
        else:
            quantity_str, name = parts
        if not is_int(quantity_str):
            raise ParserError("Quantity not int")
        quantity = to_int(quantity_str)
        return name, quantity
