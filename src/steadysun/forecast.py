from typing import Any, Dict, List, Optional, Union

import pandas as pd
from pydantic import BaseModel, field_validator

from .steadysun_api import SteadysunAPI


class _ForecastParameters(BaseModel):
    """Available parameters for the get_forecast API call.

    See default values and more information about each parameters at:
    https://www.steady-sun.com/api-documentation/#section__parameters
    """

    time_step: Optional[int] = None
    horizon: Optional[int] = None
    precision: Optional[int] = None
    fields: Optional[Union[List[str], str]] = None
    date_time_format: Optional[str] = None
    time_stamp_unit: Optional[str] = None
    # data_format have specifics functions (use Forecast functions : as_json, as_csv)

    class Config:
        validate_assignment = True

    @field_validator("fields")
    @classmethod
    def handle_fields(cls, fields: Optional[Union[List[str], str]]):
        if fields is None:
            return None
        if len(fields) == 0:
            raise ValueError("Fields can't be an empty list (You can set it to None to get all available fields)")
        if isinstance(fields, list):
            fields = ",".join(map(str, fields))
        if isinstance(fields, str):
            fields = fields.replace("[", "").replace("]", "")

        return fields if len(fields) else None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the attributes to a dictionary adapted to api_requests (excluding None values)
        """
        return super().model_dump(exclude_none=True)


# pylint: disable=too-many-arguments, unused-argument
def get_forecast(
    site_uuid: str,
    time_step: Optional[int] = None,
    horizon: Optional[int] = None,
    precision: Optional[int] = None,
    fields: Optional[List[str]] = None,
    date_time_format: Optional[str] = None,
    time_stamp_unit: Optional[str] = None,
    raw_api_response: Optional[bool] = False,
) -> pd.DataFrame:
    """Fetch forecast data for a specific site."""

    forecast_parameters = _ForecastParameters(**{k: v for k, v in locals().items() if k != "site_uuid"})

    endpoint = f"forecast/pvsystem/{site_uuid}/"
    params = forecast_parameters.to_dict()

    # Make the GET call
    api_data = SteadysunAPI().get(endpoint, params=params)

    # Convert the response to a pandas DataFrame
    forecast_df = pd.DataFrame(data=api_data["data"], index=api_data["index"], columns=api_data["columns"])

    return forecast_df
