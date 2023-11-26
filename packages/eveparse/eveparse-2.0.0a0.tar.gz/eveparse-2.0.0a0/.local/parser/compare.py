from .base import EveParser
from .errors import ParserError
from .validators import is_int

META_LEVELS = [
    "Tech I",
    "Tech II",
    "Tech III",
    "Storyline",
    "Deadspace",
    "Faction",
    "Officer",
]


class Compare(EveParser):
    """Caldari Navy Mjolnir Heavy Missile	Faction"""

    @classmethod
    def parse(cls, string):
        if "\t" not in string:
            raise ParserError
        parts = string.split("\t")
        if len(parts) < 2:
            raise ParserError
        name, meta_level, *_ = parts
        if meta_level not in META_LEVELS:
            raise ParserError
        if is_int(name) or is_int(meta_level):
            raise ParserError
        return name, 1
