from os import environ, getenv

import requests

from ._api import APIResponseHandler

ENV_STEADYSUN_API_TOKEN = "STEADYSUN_API_TOKEN"
DEFAULT_STEADYSUN_API_URL = "https://steadyweb.steady-sun.com/api/v1/"


class BadRequestException(Exception):
    """Raised when the sent request have issues."""

    def __init__(self, message):
        super().__init__(message)


class SteadysunAPI:
    """
    A class to interact with the Steadysun API.

    This class provides methods for making HTTP requests (GET, POST, PUT, PATCH, DELETE)
    to the Steadysun API, handling authorization and response validation automatically.
    """

    def __init__(self, timeout: int = 30, base_url: str = None):
        self.token = self.retrieve_token_from_env()
        self.timeout = timeout
        self.base_url = base_url or DEFAULT_STEADYSUN_API_URL
        self.headers = {
            "Authorization": f"Token {self.token}",
        }

    @staticmethod
    def retrieve_token_from_env():
        """Get the steadysun api token defined in your environment and check it"""
        token = getenv(ENV_STEADYSUN_API_TOKEN, None)
        if token is None:
            raise ValueError(f"{ENV_STEADYSUN_API_TOKEN} was not found in your environment.")
        if len(token) == 0:
            raise ValueError(f"{ENV_STEADYSUN_API_TOKEN} was found but is empty.")
        if len(token) != 40:
            raise ValueError(f"{ENV_STEADYSUN_API_TOKEN} was found but does not seem valid ({token}).")
        return token

    @staticmethod
    def set_api_token(token: str):
        """Set the steadysun api token in your environment"""
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
    ):
        """Generalized method for making API requests."""
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

    def get(self, endpoint: str, params: dict = None):
        """GET request."""
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: dict = None):
        """POST request."""
        return self._make_request("POST", endpoint, data=data)

    def patch(self, endpoint: str, data: dict = None):
        """PATCH request."""
        return self._make_request("PATCH", endpoint, data=data)

    def put(self, endpoint: str, data: dict = None):
        """PUT request."""
        return self._make_request("PUT", endpoint, data=data)

    def delete(self, endpoint: str, params: dict = None):
        """DELETE request."""
        return self._make_request("DELETE", endpoint, params=params)

    def get_list(self, endpoint: str, params: dict = None, page_limit: int = 10, get_all_pages: bool = False):
        """GET request for list on multiple pages"""
        params = dict(params or {}, **{"limit": page_limit, "offset": 0})
        response = self.get(endpoint, params)
        if get_all_pages:
            while response["next"] is not None:
                params["offset"] += params["limit"]
                response["results"] = response["results"] + self.get(endpoint, params)["results"]
            del response["next"]
            del response["previous"]
        return response
