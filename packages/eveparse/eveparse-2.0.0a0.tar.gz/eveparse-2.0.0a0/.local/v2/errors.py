class ParserError(Exception):
    pass


class ConverterError(ParserError):
    pass


class ValidatorError(ParserError):
    pass
