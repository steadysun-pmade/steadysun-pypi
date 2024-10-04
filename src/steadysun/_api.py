import logging

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
        """Handle error responses (4xx and 5xx status codes)"""
        error_message = ERROR_MESSAGE_MAP.get(self.status_code, self.text or "An unexpected error occurred.")
        raise requests.exceptions.HTTPError(f"{self.status_code} {error_message}", response=self.response) from http_err

    def _parse_json(self):
        """Attempt to parse the JSON response."""
        try:
            return self.response.json()
        except ValueError:
            logger.warning("Failed to parse JSON from response.")
            return None
