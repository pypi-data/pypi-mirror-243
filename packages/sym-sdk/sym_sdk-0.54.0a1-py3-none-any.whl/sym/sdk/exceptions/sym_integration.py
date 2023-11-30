from sym.sdk.exceptions import SymException


class SymIntegrationError(SymException):
    """This is the base class for all ``SymIntegrationError``\\ s; that is, for errors that occur in functions that
    integrate internally with the Sym platform.

    Not to be confused with :class:`~sym.sdk.exceptions.sym_exception.SymException`, which is the base class of this
    exception and is used for _all_ exceptions that occur in the Sym Runtime.

    Args:
        name: The name of the exception (used as the second part of the error code, e.g. ``INVALID_RESPONSE_DATA``)
        message: The exception message to display
    """

    def __init__(self, name: str, message: str, error_type: str = "SymIntegration"):
        super().__init__(error_type=error_type, name=name, message=message)
