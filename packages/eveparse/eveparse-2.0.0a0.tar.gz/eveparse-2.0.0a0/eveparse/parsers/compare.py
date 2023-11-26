from eveparse import converters
from eveparse import exceptions
from eveparse import translations


def dynamic_columns(string: str) -> dict:
    parts = string.split("\t")
    if len(parts) < 2:
        raise exceptions.ParserException(string)
    if len(parts) == 2:
        type_name, meta_group = parts
        if meta_group not in translations.META_GROUPS:
            raise exceptions.ParserException(string)
        type_id = converters.type_name_to_type_id(type_name=type_name)
        return {type_id: 1}
    elif len(parts) > 2:
        type_name, meta_group, *columns = parts
        if meta_group not in translations.META_GROUPS:
            raise exceptions.ParserException(string)
        # test remaining columns for valid quantity string
        # if a valid quantity is found, this string is not
        # from the compare window so an exception is raised
        for column in columns:
            try:
                converters.quantity_string_to_int(column)
            except exceptions.ConverterException:
                continue
            else:
                raise exceptions.ParserException(string)
        type_id = converters.type_name_to_type_id(type_name=type_name)
        return {type_id: 1}
