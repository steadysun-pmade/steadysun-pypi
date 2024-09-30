from importlib.metadata import PackageNotFoundError, version

from . import exceptions, forecast, pvsystem

try:
    __version__ = version("steadysun")
except PackageNotFoundError:
    __version__ = "unknown version"

__all__ = ["exceptions", "forecast", "pvsystem"]
