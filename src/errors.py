class ParserError(BaseException):
    """Error raise when parsing is impossible."""
    pass

class UndeclaredVariableError(BaseException):
    """Error raise when variable is undeclared."""
    pass