import json
import math
import os
import unittest

from steadysun.pvsystem import (
    create_pvsystem,
    delete_pvsystem,
    get_pvsystem_config,
    get_pvsystem_list,
    get_pvsystem_uuids,
)
from tests import DATA_DIR


def _compare_config(a, b):
    """Checking that all keys and values in a are present in b (with custom handling for config)"""
    if isinstance(a, dict) and isinstance(b, dict):
        return all(k in b and _compare_config(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_compare_config(i, j) for i, j in zip(sorted(a), sorted(b)))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=1e-9)
    return a == b


class TestPvsystem(unittest.TestCase):
    """Test for the pvsystem.py file"""

    TEST_SITE_PV_UUID = "be64cdf1-22e5-4072-85d8-d6c1502c4460"

    def setUp(self) -> None:
        with open(os.path.join(DATA_DIR, "pvsystem_config.json"), encoding="utf-8") as f:
            self.basic_config = json.load(f)
        return super().setUp()

    def test_get_pvsystem_list_first_page(self):
        """Test the get_pvsystem_list request but only first page and limit"""
        pv_list = get_pvsystem_list(page_limit=3)
        self.assertIn("results", pv_list)
        self.assertEqual(len(pv_list["results"]), 3)

    @unittest.skip("Really long request if the token have access to all systems")
    def test_get_pvsystem_list_all_pages(self):
        """Test the get_pvsystem_list request with all pages"""
        pv_list = get_pvsystem_list(page_limit=100, get_all_pages=True)
        self.assertIn("count", pv_list)
        self.assertIn("results", pv_list)
        self.assertEqual(len(pv_list["results"]), pv_list["count"])

    @unittest.skip("Really long request if the token have access to all systems")
    def test_get_pvsystem_uuids(self):
        """Test the get_pvsystem_uuids request"""
        pv_list = get_pvsystem_uuids()
        self.assertIsInstance(pv_list, list)

    def test_create_get_delete_pvsystem(self):
        """Test the basic get forecast request"""
        pvsystem_config = create_pvsystem(config=self.basic_config)
        self.assertIn("uuid", pvsystem_config)
        del self.basic_config["inverter_parameters"]
        self.assertTrue(_compare_config(self.basic_config, pvsystem_config))

        pvsystem_config = get_pvsystem_config(site_uuid=pvsystem_config["uuid"])
        del self.basic_config["arrays"]
        del self.basic_config["pv_type"]
        self.assertTrue(_compare_config(self.basic_config, pvsystem_config))

        delete_pvsystem(site_uuid=pvsystem_config["uuid"])
