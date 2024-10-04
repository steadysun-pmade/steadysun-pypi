import os
import unittest

from requests.exceptions import HTTPError

from steadysun.forecast import _ForecastParameters, get_forecast
from steadysun.steadysun_api import ENV_STEADYSUN_API_TOKEN


class TestForecastParameters(unittest.TestCase):
    def test_init_with_invalid_types(self):
        """Test raising ValueError for invalid types in input data."""
        with self.assertRaises(ValueError):
            _ForecastParameters(horizon="bad_value", time_step="bad_value_2")

    def test_to_api_requested_format_valid(self):
        """Test valid parameters convertion to API format."""
        params = _ForecastParameters(horizon=1, fields=["ghi", "t2m"])
        expected_output = {"horizon": 1, "fields": "ghi,t2m"}
        self.assertEqual(params.to_dict(), expected_output)

        params = _ForecastParameters(horizon=1, fields=["ghi"], time_step=None)
        expected_output = {"horizon": 1, "fields": "ghi"}
        self.assertEqual(params.to_dict(), expected_output)

    def test_field_validator_valid(self):
        """Test check_fields function during the init with valid input"""
        params = _ForecastParameters(fields=["ghi"])
        self.assertEqual(params.fields, "ghi")
        params = _ForecastParameters(fields=["ghi", "t2m"])
        self.assertEqual(params.fields, "ghi,t2m")
        params = _ForecastParameters(fields="ghi")
        self.assertEqual(params.fields, "ghi")
        params = _ForecastParameters(fields="[ghi,t2m]")
        self.assertEqual(params.fields, "ghi,t2m")

    def test_field_validator_bad(self):
        """Test check_fields function during the init with bad input"""
        with self.assertRaises(ValueError):
            _ForecastParameters(horizon=1, fields=[])
        with self.assertRaises(ValueError):
            _ForecastParameters(horizon=1, fields="")
        with self.assertRaises(ValueError):
            _ForecastParameters(horizon=1, fields=type("RandomClass", (object,), {"content": {}})())


class TestForecast(unittest.TestCase):
    """Test for the forecast.py file"""

    TEST_SITE_PV_UUID = "be64cdf1-22e5-4072-85d8-d6c1502c4460"

    def test_get_forecast_basic(self):
        """Test the basic get forecast request"""
        forecast_df = get_forecast(self.TEST_SITE_PV_UUID)
        self.assertIn("2m_temperature", forecast_df.columns)

    def test_get_forecast_bad_uuid(self):
        """Test the basic get forecast request with a bad pv"""
        with self.assertRaises(HTTPError) as context:
            get_forecast(site_uuid="bad_uuid")
        self.assertIn("404", f"{context.exception}")

    def test_get_forecast_bad_token(self):
        """Test the basic get forecast request with a bad token"""
        token_tmp = os.environ[ENV_STEADYSUN_API_TOKEN]
        os.environ[ENV_STEADYSUN_API_TOKEN] = "a" * 40
        with self.assertRaises(HTTPError) as context:
            get_forecast(site_uuid=self.TEST_SITE_PV_UUID)
        self.assertIn("401", f"{context.exception}")

        os.environ[ENV_STEADYSUN_API_TOKEN] = token_tmp

    def test_get_forecast_with_args(self):
        """Test the basic get forecast request with few params"""
        forecast_df = get_forecast(
            site_uuid=self.TEST_SITE_PV_UUID,
            time_step=30,
            horizon=2440,
            precision=4,
            fields=["all_sky_global_horizontal_irradiance", "2m_temperature"],
        )
        self.assertEqual(len(forecast_df.columns), 2)
        self.assertIn("all_sky_global_horizontal_irradiance", forecast_df.columns)
        self.assertIn("2m_temperature", forecast_df.columns)

    def test_get_forecast_with_args_fields_as_str(self):
        """Test the basic get forecast request with few params"""
        forecast_df = get_forecast(
            site_uuid=self.TEST_SITE_PV_UUID,
            time_step=30,
            horizon=2440,
            precision=4,
            fields="all_sky_global_horizontal_irradiance,2m_temperature",
        )
        self.assertEqual(len(forecast_df.columns), 2)
        self.assertIn("all_sky_global_horizontal_irradiance", forecast_df.columns)
        self.assertIn("2m_temperature", forecast_df.columns)
