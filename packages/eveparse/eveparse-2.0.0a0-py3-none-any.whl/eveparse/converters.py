from eveparse import exceptions
from eveparse import translations


def type_name_to_type_id(type_name: str) -> int:
    type_name = type_name.rstrip("*").strip()
    if type_name not in translations.TYPE_NAMES:
        raise exceptions.ConverterException(type_name)
    return translations.TYPE_DICT[type_name]


def quantity_string_to_int(string: str) -> int:
    string = string.strip()
    if not all([char in "1234567890,." for char in string]):
        raise exceptions.ConverterException(string)
    if "," in string and "." in string:  # confirmed float
        if not (string.endswith(".00") or string.endswith(",00")):  # mixed separators are only valid in floats
            raise exceptions.ConverterException(string)
        trimmed_string = string[:-3]  # remove float ending
        cleaned_string = trimmed_string.replace(",", "").replace(".", "")
        try:
            return int(cleaned_string)
        except ValueError as e:
            raise exceptions.ConverterException(string) from e
    elif "," in string or "." in string:
        if string.endswith(".00") or string.endswith(",00"):  # is a float
            string = string[:-3]
        cleaned_string = string.replace(",", "").replace(".", "")
        try:
            return int(cleaned_string)
        except ValueError as e:
            raise exceptions.ConverterException(string) from e
    else:
        try:
            return int(string)
        except ValueError as e:
            raise exceptions.ConverterException(string) from e
