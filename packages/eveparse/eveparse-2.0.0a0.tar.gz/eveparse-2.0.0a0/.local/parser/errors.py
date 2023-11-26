class ConverterError(Exception):
    """Raised if a converter is unable to transform a string"""
    pass


class ParserError(Exception):
    """Raised if a parser is unable to extract data from a string"""
    pass


class ValidatorError(Exception):
    """Raised if a validator finds invalid characters in a string"""
    pass
