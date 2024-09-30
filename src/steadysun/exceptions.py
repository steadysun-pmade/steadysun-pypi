class APIError(Exception):
    """Base class for all API-related errors."""

    def __init__(self, status_code, error_title, message):
        full_message = f"{status_code} {error_title}: {message}"
        super().__init__(full_message)


class BadRequestError(APIError):
    """Raised when the API returns a 400 Bad Request."""

    def __init__(self, message="Please check your request format."):
        super().__init__(400, "Bad Request", message)


class UnauthorizedError(APIError):
    """Raised when the API returns a 401 Unauthorized."""

    def __init__(self, message="You need to authenticate first."):
        super().__init__(401, "Unauthorized", message)


class ForbiddenError(APIError):
    """Raised when the API returns a 403 Forbidden."""

    def __init__(self, message="You don't have permission to access this resource."):
        super().__init__(403, "Forbidden", message)


class NotFoundError(APIError):
    """Raised when the API returns a 404 Not Found."""

    def __init__(self, message="The requested resource was not found."):
        super().__init__(404, "Not Found", message)


class TooManyRequestsError(APIError):
    """Raised when the API returns a 429 Too Many Requests."""

    def __init__(self, message="You have exceeded your request quota."):
        super().__init__(429, "Too Many Requests", message)


class InternalServerError(APIError):
    """Raised when the API returns a 500 Internal Server Error."""

    def __init__(self, message="An unexpected server error occurred."):
        super().__init__(500, "Internal Server Error", message)


class BadGatewayError(APIError):
    """Raised when the API returns a 502 Bad Gateway."""

    def __init__(self, message="Server timeout, please try again after 30 seconds."):
        super().__init__(502, "Bad Gateway", message)


ERROR_MAP = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    429: TooManyRequestsError,
    500: InternalServerError,
    502: BadGatewayError,
}
