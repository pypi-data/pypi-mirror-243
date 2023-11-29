class BaseError(Exception):
    """
    Base class for all errors
    """


class QuantityError(BaseError):
    """
    Base class for all quantity-related errors
    """


# ToDo @Paul: should the error be renamed as "value" was replaced by "quantity"?
class QuantityValueError(QuantityError):
    """
    Class for errors related to quantity values
    """


class QuantityUnitsError(QuantityError):
    """
    Class for errors related to quantity units
    """


class ParameterError(BaseError):
    """
    Base class for all parameter-related errors
    """


class ParameterValueError(BaseError):
    """
    Class for errors related to (user-given) parameter values
    """


class ParameterConversionError(BaseError):
    """
    Class for errors related to parameter conversion
    """
