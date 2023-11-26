from .base import EveParser
from .converters import to_int
from .errors import ParserError
from .validators import is_int


class BuyMissingMaterials(EveParser):
    """Mexallon	156	0	52.17	36"""

    @classmethod
    def parse(cls, string: str) -> tuple[str, int]:
        if "\t" not in string:
            raise ParserError("Required tab not found")
        parts = string.split("\t")
        if len(parts) != 5:
            raise ParserError("Parts length not 5")
        name, quantity_str, *_ = parts
        if not is_int(quantity_str):
            raise ParserError("Quantity not an int")
        quantity = to_int(quantity_str)
        return name, quantity


class InputOutputMaterials(EveParser):
    """1 x Rifter"""

    @classmethod
    def parse(cls, string: str) -> tuple[str, int]:
        if "\t" in string:
            raise ParserError("Prohibited tab found")
        if " x " not in string:
            raise ParserError("Required space x space not found")
        parts = string.split(" x ")
        if len(parts) != 2:
            raise ParserError("Parts length not 2")
        quantity_str, name = parts
        if not is_int(quantity_str):
            raise ParserError("Quantity not an int")
        quantity = to_int(quantity_str)
        return name, quantity
