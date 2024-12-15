"""Steadysun package to help with API interactions.

This package provides tools and utilities for interacting with the Steadysun API,
which facilitates operations such as retrieving forecasts and managing photovoltaic systems.
The package consists of the following submodules:
- `forecast`: Fetches forecast data for specific systems.
- `pvsystem`: Handles the creation, updating, and deletion of PV systems via the API.
- `steadysun_api`: Provides low-level utilities for making authenticated API requests.

Attributes:
    __version__ (str): The current version of the steadysun package
"""

from importlib.metadata import PackageNotFoundError, version

from . import forecast, pvsystem, steadysun_api

try:
    __version__ = version("steadysun")
except PackageNotFoundError:
    __version__ = "unknown version"

__all__ = ["forecast", "pvsystem", "steadysun_api"]
