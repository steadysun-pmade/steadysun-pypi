import os
import unittest

from steadysun.steadysun_api import ENV_STEADYSUN_API_TOKEN, SteadysunAPI


class TestSteadysunApi(unittest.TestCase):
    def setUp(self) -> None:
        self.real_token = os.environ[ENV_STEADYSUN_API_TOKEN]
        return super().setUp()

    def tearDown(self) -> None:
        os.environ[ENV_STEADYSUN_API_TOKEN] = self.real_token
        return super().tearDown()

    def test_init_with_token(self):
        """Basic test init with token in your env (the token is in the CI)"""
        self.assertEqual(len(os.getenv(ENV_STEADYSUN_API_TOKEN, "")), 40)
        SteadysunAPI()

    def test_init_with_bad_token(self):
        """Basic test init without token"""
        del os.environ[ENV_STEADYSUN_API_TOKEN]
        with self.assertRaises(ValueError):
            SteadysunAPI()
        os.environ[ENV_STEADYSUN_API_TOKEN] = ""
        with self.assertRaises(ValueError):
            SteadysunAPI()
        os.environ[ENV_STEADYSUN_API_TOKEN] = "12345"
        with self.assertRaises(ValueError):
            SteadysunAPI()
        tmp_token = os.environ[ENV_STEADYSUN_API_TOKEN]
        os.environ[ENV_STEADYSUN_API_TOKEN] = tmp_token

    def test_set_api_token(self):
        """Test set_api_token"""
        os.environ[ENV_STEADYSUN_API_TOKEN] = "unset"

        with self.assertRaises(ValueError):
            SteadysunAPI.set_api_token(None)
        self.assertEqual(os.getenv(ENV_STEADYSUN_API_TOKEN), "unset")

        with self.assertRaises(ValueError):
            SteadysunAPI.set_api_token("")
        self.assertEqual(os.getenv(ENV_STEADYSUN_API_TOKEN), "unset")

        with self.assertRaises(ValueError):
            SteadysunAPI.set_api_token("bad length ...")
        self.assertEqual(os.getenv(ENV_STEADYSUN_API_TOKEN), "unset")

        SteadysunAPI.set_api_token("a" * 40)
        self.assertEqual(os.getenv(ENV_STEADYSUN_API_TOKEN), "a" * 40)
