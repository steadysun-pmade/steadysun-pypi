from importlib.metadata import PackageNotFoundError, version

from . import forecast, pvsystem, steadysun_api

try:
    __version__ = version("steadysun")
except PackageNotFoundError:
    __version__ = "unknown version"

__all__ = ["forecast", "pvsystem", "steadysun_api"]
