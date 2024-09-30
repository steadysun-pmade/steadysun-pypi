import logging

import requests

from .exceptions import ERROR_MAP, APIError, BadRequestError, NotFoundError

logger = logging.getLogger(__name__)


class APIResponseHandler:
    """Handles API responses and raises exceptions for error status codes."""

    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        self.text = response.text

    def handle(self):
        """Process the response, raise errors for non-success status codes"""
        try:
            self.response.raise_for_status()
            return self._handle_success()
        except requests.exceptions.HTTPError as http_err:
            self._handle_error(http_err)
            return None

    def _handle_success(self):
        """Handle successful responses (2xx status codes)"""

        if self.status_code in [200, 201]:
            logger.info(f"Request succeeded with status {self.status_code}: {self.text}")
            return self._parse_json()
        if self.status_code == 204:
            logger.info("Resource successfully deleted.")
            return {"message": "Resource successfully deleted."}
        return {"message": "Unknown success response."}

    def _handle_error(self, http_err):
        """Handle error responses (4xx and 5xx status codes)."""
        error_class = ERROR_MAP.get(self.status_code, None)
        if error_class is None:
            raise APIError(self.status_code, "Request error", f"Response: {self.text}") from http_err
        if error_class is NotFoundError:
            raise error_class(self.response.url) from http_err
        if error_class is BadRequestError:
            raise error_class(self._parse_json()) from http_err
        raise error_class() from http_err

    def _parse_json(self):
        """Attempt to parse the JSON response."""
        try:
            return self.response.json()
        except ValueError:
            logger.warning("Failed to parse JSON from response.")
            return {"error": "Response body is not valid JSON", "text": self.text}
