import errors
from parsers import assets
from parsers import blueprint
from parsers import compare
from parsers import contracts
from parsers import dscan
from parsers import fitting
from parsers import fitting_management
from parsers import fleet
from parsers import industry
from parsers import insurance
from parsers import inventory
from parsers import killmail
from parsers import market
from parsers import mining_ledger
from parsers import multibuy
from parsers import pi
from parsers import pyfa
from parsers import showinfo
from parsers import structure_browser
from parsers import uncontrolled

parsers = [
    # assets.station,
    # assets.view_contents,
    # inventory.details,
    inventory.icons,
]


def parse(text: str) -> dict:
    parsed_items = {}
    error_lines = []
    for line in text.splitlines():
        normalized_line = line.casefold()
        for parser in parsers:
            try:
                line_items = parser(string=normalized_line)
            except errors.ParserError:
                continue
            else:
                for type_id, quantity in line_items.items():
                    if type_id in parsed_items:
                        parsed_items[type_id] += quantity
                    else:
                        parsed_items[type_id] = quantity
                break
        else:
            error_lines.append(line)
    return dict(items=parsed_items, errors=error_lines)
