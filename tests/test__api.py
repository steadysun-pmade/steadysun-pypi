"""Tests _api.py"""

import unittest
from unittest.mock import Mock

import requests

from steadysun._api import APIResponseHandler


class TestAPIResponseHandler(unittest.TestCase):
    """Tests for APIResponseHandler"""

    def setUp(self):
        """Set up a mock response for all tests."""
        self.mock_response = Mock(spec=requests.Response)

    def test_handle_success(self):
        """Test handling of successful responses"""
        test_cases = [
            (200, '{"message": "success"}'),
            (201, '{"message": "created"}'),
            (204, ""),
        ]
        for status_code, text in test_cases:
            with self.subTest(status_code=status_code):
                self.mock_response.status_code = status_code
                self.mock_response.text = text
                self.mock_response.json.return_value = {"json": 1} if status_code != 204 else None

                result = APIResponseHandler(self.mock_response).handle()

                if status_code != 204:
                    self.assertEqual(result, {"json": 1})
                self.mock_response.raise_for_status.assert_called_once()
                self.mock_response.raise_for_status.reset_mock()

    def test_handle_invalid_json(self):
        """Test handling of invalid JSON in successful responses."""
        self.mock_response.status_code = 200
        self.mock_response.text = "Invalid JSON"
        self.mock_response.json.side_effect = ValueError

        APIResponseHandler(self.mock_response).handle()

    def test_handle_error_responses(self):
        """Test handling of error responses (e.g., 4xx, 5xx)."""
        test_cases = [
            (400, "Bad Request"),
            (401, "Unauthorized"),
            (403, "Forbidden"),
            (404, "Not Found"),
            (429, "Too Many Requests"),
            (500, "Internal Server Error"),
            (502, "Bad Gateway"),
        ]

        for status_code, text in test_cases:
            with self.subTest(status_code=status_code):
                self.mock_response.status_code = status_code
                self.mock_response.text = text
                self.mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

                with self.assertRaises(requests.exceptions.HTTPError) as context:
                    APIResponseHandler(self.mock_response).handle()

                self.assertIn(str(status_code), str(context.exception))
                self.mock_response.raise_for_status.assert_called_once()
                self.mock_response.raise_for_status.reset_mock()
