import errors
import validators


def quantity_to_int(string: str) -> int:
    if not validators.is_quantity(string=string):
        raise errors.ParserError
    if "," in string and "." in string:
        if not string[-3] in ".," and string[-2] == "0" and string[-1] == "0":
            raise errors.ParserError(string)
        trimmed_string = string[:-3]
        cleaned_string = trimmed_string.replace(",", "").replace(".", "")
        try:
            return int(cleaned_string)
        except ValueError:
            raise errors.ParserError(string)
    elif "," in string or "." in string:
        cleaned_string = string.replace(",", "").replace(".", "")
        try:
            return int(cleaned_string)
        except ValueError:
            raise errors.ParserError(string)
    else:
        try:
            return int(string)
        except ValueError:
            raise errors.ParserError(string)


def type_name_to_type_id(string: str) -> int:
    pass
