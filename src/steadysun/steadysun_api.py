"""This module defines the `SteadysunAPI` class for interacting with the Steadysun API.

It provides a convenient wrapper around common HTTP methods (GET, POST, PATCH, PUT, DELETE) and handles
authorization and response validation. The `SteadysunAPI` class abstracts API interactions for different endpoints
and supports making paginated requests.

Classes:
    SteadysunAPI: A class that handles HTTP requests to the Steadysun API, with authorization and response handling.
"""

from os import environ, getenv
from typing import NoReturn

import requests

from ._api import APIResponseHandler

ENV_STEADYSUN_API_TOKEN = "STEADYSUN_API_TOKEN"
ENV_STEADYSUN_API_URL = "STEADYSUN_API_URL"
DEFAULT_STEADYSUN_API_URL = "https://steadyweb.steady-sun.com/api/v1/"


class SteadysunAPI:
    """A class to interact with the Steadysun API.

    This class provides methods for making HTTP requests (GET, POST, PUT, PATCH, DELETE)
    to the Steadysun API, handling authorization and response validation automatically.

    Attributes:
        timeout (int): Timeout for API requests in seconds (default is 30).
        token (str): API token retrieved from environment variables.
        base_url (str): Base URL for Steadysun API requests.
        headers (dict): Authorization headers with API token.
    """

    def __init__(self, timeout: int = 30):
        """Initializes a SteadysunAPI instance, setting up the API token, base URL, and headers required for requests.

        Args:
            timeout (int): Timeout for API requests in seconds (default is 30 seconds).

        Raises:
            ValueError: If the API token is not found or is invalid.
        """
        self.token = self.retrieve_token_from_env()
        self.timeout = timeout
        self.base_url = getenv(ENV_STEADYSUN_API_URL, DEFAULT_STEADYSUN_API_URL)
        self.headers = {
            "Authorization": f"Token {self.token}",
        }

    @staticmethod
    def retrieve_token_from_env() -> str:
        """Retrieves the Steadysun API token from environment variables and quick-check it.

        Returns:
            str: The API token.

        Raises:
            ValueError: If the token is not found, empty, or not the good size.
        """
        token = getenv(ENV_STEADYSUN_API_TOKEN, None)
        if token is None:
            raise ValueError(f"{ENV_STEADYSUN_API_TOKEN} was not found in your environment.")
        if len(token) == 0:
            raise ValueError(f"{ENV_STEADYSUN_API_TOKEN} was found but is empty.")
        if len(token) != 40:
            raise ValueError(f"{ENV_STEADYSUN_API_TOKEN} was found but does not seem valid ({token}).")
        return token

    @staticmethod
    def set_api_token(token: str) -> NoReturn:
        """Sets the Steadysun API token in the environment.

        Args:
            token (str): The API token to set.

        Raises:
            ValueError: If the token is empty or does not seem valid.
        """
        if token is None or token == "":
            raise ValueError("The given token is empty")
        if len(token) != 40:
            raise ValueError(f"The given token does not seem valid (expected 40 characters, but got {len(token)}).")
        environ[ENV_STEADYSUN_API_TOKEN] = token

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        data: dict = None,
    ) -> dict:
        """Makes an HTTP request to the Steadysun API.

        Args:
            method (str): The HTTP method (e.g., GET, POST, PATCH, PUT, DELETE).
            endpoint (str): The API endpoint to call.
            params (dict, optional): URL parameters for GET requests (default is None).
            data (dict, optional): JSON payload for POST, PUT, PATCH requests (default is None).

        Returns:
            dict: The parsed response from the API.

        Raises:
            HTTPError: If the API response indicates an error.
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            params=params,
            json=data,
            headers=self.headers,
            timeout=self.timeout,
        )
        return APIResponseHandler(response).handle()

    def get(self, endpoint: str, params: dict = None) -> dict:
        """Makes a GET request to the Steadysun API.

        Args:
            endpoint (str): The API endpoint to call.
            params (dict, optional): URL parameters for the GET request (default is None).

        Returns:
            dict: The parsed response from the API.
        """
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: dict = None) -> dict:
        """Makes a POST request to the Steadysun API.

        Args:
            endpoint (str): The API endpoint to call.
            data (dict, optional): The JSON payload to send (default is None).

        Returns:
            dict: The parsed response from the API.
        """
        return self._make_request("POST", endpoint, data=data)

    def patch(self, endpoint: str, data: dict = None) -> dict:
        """Makes a PATCH request to the Steadysun API.

        Args:
            endpoint (str): The API endpoint to call.
            data (dict, optional): The JSON payload to send (default is None).

        Returns:
            dict: The parsed response from the API.
        """
        return self._make_request("PATCH", endpoint, data=data)

    def put(self, endpoint: str, data: dict = None) -> dict:
        """Makes a PUT request to the Steadysun API.

        Args:
            endpoint (str): The API endpoint to call.
            data (dict, optional): The JSON payload to send (default is None).

        Returns:
            dict: The parsed response from the API.
        """
        return self._make_request("PUT", endpoint, data=data)

    def delete(self, endpoint: str, params: dict = None) -> dict:
        """Makes a DELETE request to the Steadysun API.

        Args:
            endpoint (str): The API endpoint to call.
            params (dict, optional): URL parameters for the DELETE request (default is None).

        Returns:
            dict: The parsed response from the API.
        """
        return self._make_request("DELETE", endpoint, params=params)

    def get_list(self, endpoint: str, params: dict = None, page_limit: int = 10, get_all_pages: bool = False):
        """Makes a paginated GET request to retrieve a list of results from the Steadysun API.

        Args:
            endpoint (str): The API endpoint to call.
            params (dict, optional): URL parameters for the GET request (default is None).
            page_limit (int): The number of items to request per page (default is 10).
            get_all_pages (bool): Whether to retrieve all pages of results (default is False).

        Returns:
            dict: The combined results from all pages (if get_all_pages is True).
        """
        params = dict(params or {}, **{"limit": page_limit, "offset": 0})
        response = self.get(endpoint, params)
        if get_all_pages:
            while response["next"] is not None:
                params["offset"] += params["limit"]
                response["results"] = response["results"] + self.get(endpoint, params)["results"]
            del response["next"]
            del response["previous"]
        return response
