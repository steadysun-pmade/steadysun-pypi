class APIError(Exception):
    """Base class for all API-related errors."""


class BadRequestError(APIError):
    """Raised when the API returns a 400 Bad Request."""

    def __init__(self, message):
        super().__init__(f"400 Bad Request: {message}")


class UnauthorizedError(APIError):
    """Raised when the API returns a 401 Unauthorized."""

    def __init__(self, message="You need to authenticate first."):
        super().__init__(f"401 Unauthorized: {message}")


class ForbiddenError(APIError):
    """Raised when the API returns a 403 Forbidden."""

    def __init__(self, message="You don't have permission to access this resource."):
        super().__init__(f"403 Forbidden: {message}")


class TooManyRequestsError(APIError):
    """Raised when the API returns a 429 Too Many Requests."""

    def __init__(self, message="You have exceeded your request quota."):
        super().__init__(f"429 Too Many Requests: {message}")


class InternalServerError(APIError):
    """Raised when the API returns a 500 Internal Server Error."""

    def __init__(self, message="An unexpected server error occurred."):
        super().__init__(f"500 Internal Server Error: {message}")


class BadGatewayError(APIError):
    """Raised when the API returns a 502 Bad Gateway."""

    def __init__(self, message="Server timeout, please try again after 30 seconds."):
        super().__init__(f"502 Bad Gateway: {message}")


class APIResponseHandler:
    """Handles API responses and raises exceptions for error status codes."""

    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        self.text = response.text

    def handle(self):
        """Process the response and handle errors based on the status code."""
        if 200 <= self.status_code < 300:
            return self._handle_success()

        return self._handle_error()

    def _handle_success(self):
        """Handle successful responses (2xx status codes)."""
        if self.status_code == 200:
            return self._parse_json()
        if self.status_code == 201:
            return self._parse_json()
        if self.status_code == 204:
            return {"message": "Resource deleted successfully."}  # No content for 204
        return {"message": "Unknown success response."}

    def _handle_error(self):
        """Handle error responses (4xx and 5xx status codes)."""
        if self.status_code == 400:
            raise BadRequestError(self._get_error_message())
        if self.status_code == 401:
            raise UnauthorizedError()
        if self.status_code == 403:
            raise ForbiddenError()
        if self.status_code == 429:
            raise TooManyRequestsError()
        if self.status_code == 500:
            raise InternalServerError()
        if self.status_code == 502:
            raise BadGatewayError()
        raise APIError(f"Unhandled error: {self.status_code}, Response: {self.text}")

    def _parse_json(self):
        """Attempt to parse the JSON response."""
        try:
            return self.response.json()
        except ValueError:
            return {"error": "Response body is not valid JSON", "text": self.text}

    def _get_error_message(self):
        """Extract the error message from the response body, if available."""
        try:
            error_data = self.response.json()
            return error_data.get("message", self.text)  # Return the error message if present
        except ValueError:
            return self.text
