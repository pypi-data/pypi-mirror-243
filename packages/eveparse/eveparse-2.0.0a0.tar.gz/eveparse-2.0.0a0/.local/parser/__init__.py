from .cargo import Icons, ListDetail
from .compare import Compare
from .errors import ConverterError, ParserError, ValidatorError
from .fitting import FittingShipTypeName
from .industry import BuyMissingMaterials, InputOutputMaterials
from .untabbed import NameOnly, NameQuantity, NameXQuantity, QuantityName, QuantityXName
from .validators import is_legal

PARSERS = [
    Icons,
    ListDetail,
    Compare,
    NameXQuantity,
    QuantityXName,
    FittingShipTypeName,
    BuyMissingMaterials,
    InputOutputMaterials,
    NameQuantity,
    QuantityName,

    # MUST BE LAST
    NameOnly,
]


def parse(string: str) -> tuple[str, int]:
    """Attempt to parse the string. Return the first valid results.

    Raise ParserError if no parser is successful
    """

    string = string.strip()

    if not is_legal(string):
        raise ParserError("Prohibited string")

    for parser in PARSERS:
        try:
            item, quantity = parser.parse(string)
        except (ConverterError, ParserError, ValidatorError):
            continue
        else:
            return item, quantity
    else:
        raise ParserError("All parsers failed")
