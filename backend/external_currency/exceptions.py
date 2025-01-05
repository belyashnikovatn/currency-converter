"""Exceptions storage."""


class NotOKStatusCodeException(Exception):
    """Raise when api status-code != 200."""
    pass


class NoResponse(Exception):
    """Raise when cannot get the api-answer."""
    pass


class NoCurrency(Exception):
    """Raise when there's no that currency."""
    pass


class NoJSON(Exception):
    """Raise when there's not a json-format."""
    pass


class DividedValueIsNull(Exception):
    """We cannot divide into 0."""
    pass
