from os import environ, getenv

import requests

ENV_STEADYSUN_API_TOKEN = "STEADYSUN_API_TOKEN"
STEADYSUN_API_URL = "https://steadyweb.steady-sun.com/api/v1/"


class SteadysunAPI:
    """
    A class to interact with the Steadysun API.

    This class provides methods for making HTTP requests (GET, POST, PUT, PATCH, DELETE)
    to the Steadysun API, handling authorization and response validation automatically.
    """

    def __init__(self):
        self.token = getenv(ENV_STEADYSUN_API_TOKEN, None)
        if self.token is None:
            raise PermissionError(f"{ENV_STEADYSUN_API_TOKEN} was not found in your environment.")
        self.timeout = 30
        self.base_url = STEADYSUN_API_URL
        self.headers = {
            "Authorization": f"Token {self.token}",
        }

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
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()

    @staticmethod
    def set_api_token(token: str):
        """Set the steadysun api token in your environment"""
        environ[ENV_STEADYSUN_API_TOKEN] = token

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
