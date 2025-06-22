class AntisniperUnknownException(Exception):
    """Raised when an unknown error occurs."""
    pass

class AntisniperForbiddenException(Exception):
    """Raised when your API-Key is invalid or banned."""
    pass

class AntisniperUnprocessableException(Exception):
    """Raised when Unprocessable Entity error occurs."""

class AntisniperRatelimitException(Exception):
    """Caused by exceeding the request limit of your API-Key."""
    pass

class AntisniperConnectionException(Exception):
    """Raised when a network error occurs."""
    pass