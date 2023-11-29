"""GM error classes."""

__all__ = [
    "GMError",
    "DataOverflowError",
    "IncorrectLengthError",
    "InfinitePointError",
    "PointNotOnCurve",
]


class GMError(Exception):
    """Base class of all errors in GM algorithms."""


class DataOverflowError(GMError):
    """Over maximum length limit."""


class IncorrectLengthError(GMError):
    """Incorrect data length given."""


class InfinitePointError(GMError):
    """Encountered a point at infinity."""


class PointNotOnCurve(GMError):
    """Point not on elliptic curve."""
