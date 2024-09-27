from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("steadysun")
except PackageNotFoundError:
    __version__ = "unknown version"


__all__ = [
    "forecast",
]
