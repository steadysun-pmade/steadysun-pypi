from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ValidationError


class ParameterModel(BaseModel):
    """
    A base class that extends Pydantic's BaseModel with custom functionality.

    Methods:
        to_param_dict(): Converts the model to a dictionary used for api parameters.
    """

    @staticmethod
    def _obj_to_api_format(value: Any) -> Union[int, str, dict]:
        """Convert object to api format (list, df, ...)"""
        if isinstance(value, list):
            # Convert list to comma-separated string
            return ",".join(map(str, value))
        return value

    @staticmethod
    def _api_format_to_obj(value: Any, expected_type: Any) -> Any:
        """Convert object to api format (list, df, ...)"""
        if expected_type in [Optional[List[str]], List[str]] and isinstance(value, str):
            return value.split(",")
        return value

    def to_param_dict(self) -> Dict[str, Any]:
        """
        Convert the attributes to a dictionary adapted to api_requests
        This will exclude None values and converting objects to api format
        """
        data = super().model_dump(exclude_none=True)
        data = {k: ParameterModel._obj_to_api_format(v) for k, v in data.items()}
        return data

    @classmethod
    def from_param_dict(cls, data: Dict[str, Any]):
        """
        Load attributes from a dictionary, converting any API format strings back to objects.
        This will validate the data according to the model's fields.

        Args:
            data (Dict[str, Any]): The input data to load.

        Returns:
            ParameterModel: An instance of the model populated with the provided data.
        """
        # Prepare data by converting API format back to object format
        processed_data = {}
        for key, value in data.items():
            if key not in cls.model_fields:
                raise ValueError(f"Invalid key: {key}")
            expected_type = cls.__annotations__.get(key)
            try:
                processed_data[key] = cls._api_format_to_obj(value, expected_type)
            except Exception as e:
                raise ValueError(f"Error processing key '{key}'") from e

        # Create an instance of the model using the processed data
        try:
            return cls(**processed_data)
        except ValidationError as e:
            raise ValueError(e) from e
