import unittest
from unittest.mock import Mock

import requests

from steadysun._api import APIResponseHandler
from steadysun.exceptions import (
    APIError,
    BadGatewayError,
    BadRequestError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    TooManyRequestsError,
    UnauthorizedError,
)


class TestAPIResponseHandler(unittest.TestCase):
    def setUp(self):
        self.mock_response = Mock(spec=requests.Response)

    def test_success_responses(self):
        """Test handling successful 2xx responses."""
        success_cases = [
            (200, '{"message": "success"}', {"message": "success"}),
            (201, '{"id": "created"}', {"id": "created"}),
            (204, "", {"message": "Resource successfully deleted."}),
        ]

        for status_code, text, expected_output in success_cases:
            with self.subTest(status_code=status_code):
                self.mock_response.status_code = status_code
                self.mock_response.text = text
                self.mock_response.json.return_value = expected_output if status_code != 204 else None
                self.mock_response.raise_for_status = Mock()

                result = APIResponseHandler(self.mock_response).handle()
                self.assertEqual(result, expected_output)

    def test_error_responses(self):
        """Test handling various 4xx and 5xx error responses."""
        error_cases = [
            (400, '{"message": "Bad Request"}', BadRequestError),
            (401, "", UnauthorizedError),
            (403, "", ForbiddenError),
            (404, '{"message": "Not Found"}', NotFoundError),
            (429, "", TooManyRequestsError),
            (500, "", InternalServerError),
            (502, "", BadGatewayError),
        ]

        for status_code, text, error_class in error_cases:
            self.mock_response.status_code = status_code
            self.mock_response.text = text
            self.mock_response.url = "example_url"
            self.mock_response.json.return_value = {"message": text} if text else None
            self.mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

            with self.assertRaises(error_class):
                APIResponseHandler(self.mock_response).handle()

    def test_unknown_error(self):
        """Test handling an unknown error (unmapped status code)."""
        self.mock_response.status_code = 418
        self.mock_response.text = "Unknown error"
        self.mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

        with self.assertRaises(APIError):
            APIResponseHandler(self.mock_response).handle()
