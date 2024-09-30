import os
import unittest

from steadysun._steadysun_api import ENV_STEADYSUN_API_TOKEN
from steadysun.exceptions import APIError, NotFoundError, UnauthorizedError
from steadysun.forecast import ForecastParameters, get_solar_forecast


class TestForecast(unittest.TestCase):
    """Test for the forecast.py file"""

    TEST_SITE_PV_UUID = "be64cdf1-22e5-4072-85d8-d6c1502c4460"

    def test_get_forecast_basic(self):
        """Test the basic get forecast request"""
        forecast_df = get_solar_forecast(site_uuid=self.TEST_SITE_PV_UUID)
        self.assertIn("2m_temperature", forecast_df.columns)

    def test_get_forecast_bad_uuid(self):
        """Test the basic get forecast request with a bad pv"""
        with self.assertRaises(NotFoundError) as context:
            get_solar_forecast(site_uuid="bad_uuid")
        self.assertIsInstance(context.exception, APIError)

    def test_get_forecast_bad_token(self):
        """Test the basic get forecast request with a bad token"""
        token_tmp = os.environ[ENV_STEADYSUN_API_TOKEN]
        os.environ[ENV_STEADYSUN_API_TOKEN] = "a" * 40
        with self.assertRaises(UnauthorizedError):
            get_solar_forecast(site_uuid=self.TEST_SITE_PV_UUID)
        os.environ[ENV_STEADYSUN_API_TOKEN] = token_tmp

    def test_get_forecast_with_dict(self):
        """Test the basic get forecast request with a dict"""
        forecast_parameters = {
            "time_step": 30,
            "horizon": 2440,
            "precision": 4,
            "fields": "all_sky_global_horizontal_irradiance,2m_temperature",
        }
        forecast_df = get_solar_forecast(
            site_uuid=self.TEST_SITE_PV_UUID,
            forecast_parameters=forecast_parameters,
        )
        self.assertEqual(len(forecast_df.columns), 2)
        self.assertIn("all_sky_global_horizontal_irradiance", forecast_df.columns)
        self.assertIn("2m_temperature", forecast_df.columns)

    def test_get_forecast_with_param_obj(self):
        """Test the basic get forecast request with a ForecastParameters object"""
        forecast_parameters = ForecastParameters(
            time_step=30,
            horizon=2440,
            precision=4,
            fields=["all_sky_global_horizontal_irradiance", "2m_temperature"],
        )
        forecast_df = get_solar_forecast(
            site_uuid=self.TEST_SITE_PV_UUID,
            forecast_parameters=forecast_parameters,
        )
        self.assertEqual(len(forecast_df.columns), 2)
        self.assertIn("all_sky_global_horizontal_irradiance", forecast_df.columns)
        self.assertIn("2m_temperature", forecast_df.columns)
