import errors

type_names_set = set()


def is_type_name(string: str) -> bool:
    string = string.rstrip("*")
    return string in type_names_set


def is_quantity(string: str) -> bool:
    if not all([char in "1234567890,." for char in string]):
        raise errors.ValidatorError
