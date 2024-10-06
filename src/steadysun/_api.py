"""API response handling module. Used to create more user-friendly error messages."""

import logging
from typing import NoReturn

import requests

logger = logging.getLogger(__name__)

ERROR_MESSAGE_MAP = {
    400: "BadRequestError: Please check your request format.",
    401: "UnauthorizedError: You need to authenticate first.",
    403: "ForbiddenError: You don't have permission to access this resource.",
    404: "NotFoundError: The requested resource was not found.",
    429: "TooManyRequestsError: You have exceeded your request quota.",
    500: "InternalServerError: An unexpected server error occurred.",
    502: "BadGatewayError: Server timeout, please try again after 30 seconds.",
}


class APIResponseHandler:
    """Handles API responses and raises exceptions for error status codes"""

    def __init__(self, response: requests.Response):
        """Initializes the API response handler.

        Args:
            response (requests.Response): The API response object.
        """
        self.response = response
        self.status_code = response.status_code
        self.text = response.text

    def handle(self) -> dict:
        """Process the response, raise errors for non-success status codes.

        Returns:
            dict: The parsed response data (or raise if an error occurred).

        Raises:
            requests.exceptions.HTTPError: If the response status code indicates an error.
        """
        try:
            self.response.raise_for_status()
            return self._handle_success()
        except requests.exceptions.HTTPError as http_err:
            self._handle_error(http_err)

    def _handle_success(self) -> dict:
        """Handle successful responses (2xx status codes).

        Returns:
            dict: The parsed response data.
        """
        if self.status_code in [200, 201]:
            logger.info(f"Request succeeded with status {self.status_code}: {self.text}")
            return self._parse_json()
        if self.status_code == 204:
            logger.info("Resource successfully deleted.")
            return {"message": "Resource successfully deleted."}
        return {"message": "Unknown success response."}

    def _handle_error(self, http_err: requests.exceptions.HTTPError) -> NoReturn:
        """Handle error responses (4xx and 5xx status codes).

        Args:
            http_err (requests.exceptions.HTTPError): The HTTP error exception.

        Raises:
            requests.exceptions.HTTPError: The original HTTP error exception with an added error message.
        """
        error_message = ERROR_MESSAGE_MAP.get(self.status_code, self.text or "An unexpected error occurred.")
        raise requests.exceptions.HTTPError(f"{self.status_code} {error_message}", response=self.response) from http_err

    def _parse_json(self) -> dict:
        """Attempt to parse the JSON response.

        Returns:
            dict: The parsed JSON data (or a dict with an error message if parsing failed).
        """
        try:
            return self.response.json()
        except ValueError as e:
            return {"message": f"Failed to parse JSON from response : {e}"}
