ILLEGAL_STRINGS = [
    "",
    "Components",
    "Items",
    "Minerals",  # Buy missing materials
    "Item	Required	Available	Est. Unit price	typeID",  # Buy missing materials
    "Ore",
    "Ubiquitous Ores",
    "Common Moon Ores",
    "Uncommon Moon Ores",
    "Exceptional Moon Ores",
    "Rare Moon Ores",
]

ILLEGAL_IN = [
    "Abyssal",
]

ILLEGAL_STARTSWITH = [
    "Total:"
]


def is_int(string: str) -> bool:
    if string.isdigit():
        return True
    if "," in string and "." in string:
        # Indicates it is a float value
        return False
    normalized = string.replace(",", "").replace(".", "")
    return normalized.isdigit()


def is_legal(string: str) -> bool:
    """Immediately indicate strings are not suitable for parsing"""

    if string in ILLEGAL_STRINGS:
        return False
    for s in ILLEGAL_IN:
        if s in string:
            return False
    for s in ILLEGAL_STARTSWITH:
        if string.startswith(s):
            return False
    return True
