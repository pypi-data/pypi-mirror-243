from parser.errors import ConverterError


def to_int(string: str) -> int:
    if "," in string and "." in string:
        # Indicates it is a float value
        raise ConverterError
    normalized = string.replace(",", "").replace(".", "")
    return int(normalized)
