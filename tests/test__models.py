import unittest
from typing import List, Optional

from steadysun._models import ParameterModel


class TestModel(ParameterModel):
    name: str
    id: int
    fields: Optional[List[str]] = None


class TestParameterModel(unittest.TestCase):
    def test_to_param_dict_with_valid_data(self):
        """Test converting model attributes to API parameter dictionary."""
        model = TestModel(name="site_1", id=1, fields=["ghi", "t2m"])
        expected_output = {"name": "site_1", "id": 1, "fields": "ghi,t2m"}
        self.assertEqual(model.to_param_dict(), expected_output)

    def test_to_param_dict_with_optionals(self):
        """Test converting model with None values to API parameter dictionary."""
        model = TestModel(name="site_2", id=2)
        expected_output = {"name": "site_2", "id": 2}
        self.assertEqual(model.to_param_dict(), expected_output)

    def test_from_param_dict_with_valid_data(self):
        """Test creating a model instance from a valid parameter dictionary."""
        dict_with_str_lit = {"name": "site_3", "id": 3, "fields": "ghi,t2m"}
        dict_with_lit = {"name": "site_3", "id": 3, "fields": ["ghi", "t2m"]}

        for data in [dict_with_str_lit, dict_with_lit]:
            model = TestModel.from_param_dict(data)
            expected_model = TestModel(name="site_3", id=3, fields=["ghi", "t2m"])
            self.assertEqual(model.name, "site_3")
            self.assertEqual(model.id, 3)
            self.assertEqual(model.fields, ["ghi", "t2m"])
            self.assertEqual(expected_model, model)

    def test_from_to_param_dict(self):
        dict_with_str_lit = {"name": "site_3", "id": 3, "fields": "ghi,t2m"}
        self.assertEqual(dict_with_str_lit, TestModel.from_param_dict(dict_with_str_lit).to_param_dict())

        model = TestModel(name="site_3", id=3, fields=["ghi", "t2m"])
        self.assertEqual(model, TestModel.from_param_dict(model.to_param_dict()))

    def test_from_param_dict_with_invalid_key(self):
        """Test raising ValueError for invalid keys in input data."""
        data = {"name": "bad_site", "id": 99, "invalid_key": "value"}
        with self.assertRaises(ValueError) as context:
            TestModel.from_param_dict(data)
        self.assertEqual(str(context.exception), "Invalid key: invalid_key")

    def test_from_param_dict_with_validation_error(self):
        """Test raising ValueError for invalid value types in input data."""
        data = {"name": "bad_site", "id": "not_a_number", "fields": "ghi,t2m"}
        with self.assertRaises(ValueError):
            TestModel.from_param_dict(data)

        data = {"name": "bad_site", "id": "not_a_number", "fields": [123]}
        with self.assertRaises(ValueError):
            TestModel.from_param_dict(data)

    def test_api_format_to_obj_conversion(self):
        """Test the internal conversion from API format to object format."""
        api_format_to_obj = TestModel._api_format_to_obj  # pylint: disable=protected-access
        self.assertEqual(api_format_to_obj("a,b,c", List[str]), ["a", "b", "c"])
        self.assertEqual(api_format_to_obj(42, int), 42)

    def test_obj_to_api_format_conversion(self):
        """Test the internal conversion from object format to API format."""
        obj_to_api_format = TestModel._obj_to_api_format  # pylint: disable=protected-access
        self.assertEqual(obj_to_api_format(["a", "b", "c"]), "a,b,c")
        self.assertEqual(obj_to_api_format(100), 100)
