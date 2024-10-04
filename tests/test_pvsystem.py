import json
import math
import os
import unittest

from requests import HTTPError

from steadysun.pvsystem import PVSystem, get_pvsystem_uuids
from steadysun.steadysun_api import SteadysunAPI
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

    @classmethod
    def setUpClass(cls) -> None:
        with open(os.path.join(DATA_DIR, "pvsystem_config.json"), encoding="utf-8") as f:
            cls.basic_config = json.load(f)
        cls.test_pvsystem_uuid = SteadysunAPI().post("pvsystem/", data=cls.basic_config)["uuid"]
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        SteadysunAPI().delete(f"pvsystem/{cls.test_pvsystem_uuid}/")
        return super().tearDownClass()

    @unittest.skip("Really long request if the token have access to all systems")
    def test_get_pvsystem_uuids(self):
        """Test the get_pvsystem_uuids request"""
        pv_list = get_pvsystem_uuids()
        self.assertIsInstance(pv_list, dict)

    def test_pvsystem_model_from_uuid(self):
        """Test the basic get forecast request"""
        pvsystem = PVSystem.from_uuid(self.test_pvsystem_uuid)
        self.assertEqual(str(pvsystem.uuid), self.test_pvsystem_uuid)
        self.assertEqual(pvsystem.name, self.basic_config["name"])
        # self.assertEqual(pvsystem.location.model_dump(), self.basic_config["location"]) # FIXME Tuple vs List
        self.assertEqual(pvsystem.altitude, self.basic_config["altitude"])
        self.assertEqual(pvsystem.pv_type.value, self.basic_config["pv_type"])
        self.assertEqual(pvsystem.expert_params.tracker_config.model_dump(), self.basic_config["tracker_config"])
        self.assertEqual(pvsystem.expert_params.bifacial_config.model_dump(), self.basic_config["bifacial_config"])
        self.assertEqual(pvsystem.expert_params.bifacial_config.model_dump(), self.basic_config["bifacial_config"])
        # inverter_parameters

    def test_pvsystem_model_update(self):
        """Test the basic get forecast request"""
        pvsystem = PVSystem.from_uuid(self.test_pvsystem_uuid)
        pvsystem.name = "changed_name"
        pvsystem.save_changes()
        same_pvsystem = PVSystem.from_uuid(self.test_pvsystem_uuid)
        self.assertEqual(same_pvsystem.name, pvsystem.name)

    def test_create_get_delete_with_pvsystem_class(self):
        """Test the full PVsystem create/get/delete process using the class"""
        base_required_args = {
            "name": "ci_pypi_test",
            "location": (5.8756, 45.6403),
            "pdc0": 10,
        }
        # Create
        pvsystem = PVSystem.create_new(**base_required_args)
        self.assertEqual(pvsystem.name, base_required_args["name"])
        self.assertEqual(pvsystem.location.coordinates, base_required_args["location"])
        self.assertEqual(pvsystem.expert_params.arrays[0].pvmodules_pdc0, base_required_args["pdc0"])

        # Get
        same_pvsystem = PVSystem.from_uuid(pvsystem.uuid)
        self.assertEqual(pvsystem, same_pvsystem)

        # Delete
        same_pvsystem.delete()
        with self.assertRaises(HTTPError):
            PVSystem.from_uuid(pvsystem.uuid)
