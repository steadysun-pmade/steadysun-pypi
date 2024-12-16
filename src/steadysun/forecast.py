"""This module is here to help fetching forecast data from the Steadysun API

It includes the `_ForecastParameters` class to model the parameters for the forecast API request, and
the `get_forecast` function to retrieve forecast data as a pandas DataFrame.
"""

from typing import Any, Dict, List, Literal, Optional, Union

import pandas as pd
from pydantic import BaseModel, field_validator

from .steadysun_api import SteadysunAPI


class _ForecastParameters(BaseModel):
    """Available parameters for the get_forecast API call.

    See default values and more information about each parameters at:
    https://steadyweb.steady-sun.com/rapidoc/#get-/forecast/-object_type-/-component_uuid-/

    Attributes:
        time_step (Optional[int]): The time step of the forecast (in minutes).
        horizon (Optional[int]): The horizon of the forecast (in minutes).
        precision (Optional[int]): Maximal number of decimal places.
        fields (Optional[Union[List[str], str]]): The fields to retrieve.
        date_time_format (Optional[Literal["time_stamp", "iso_8601"]]): Set the date format.
        time_stamp_unit (Optional[Literal["ms", "s"]]): The unit of the timestamp (if used in date_time_format).
    """

    time_step: Optional[int] = None
    horizon: Optional[int] = None
    precision: Optional[int] = None
    fields: Optional[Union[List[str], str]] = None
    date_time_format: Optional[Literal["time_stamp", "iso_8601"]] = None
    time_stamp_unit: Optional[Literal["ms", "s"]] = None

    class Config:
        """Pydantic config"""

        validate_assignment = True

    @field_validator("fields")
    @classmethod
    def handle_fields(cls, fields: Optional[Union[List[str], str]]) -> Optional[str]:
        """Validator for the 'fields' parameter (also converting List to str).

        Args:
            fields (Optional[Union[List[str], str]]): The fields to include in the forecast.

        Returns:
            Optional[str]: The processed fields parameter.

        Raises:
            ValueError: If the fields parameter is an empty list.
        """
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
        """Convert the attributes to a dictionary adapted to api_requests (excluding None values).

        Returns:
            Dict[str, Any]: The dictionary representation of the forecast parameters.
        """
        return super().model_dump(exclude_none=True)


# pylint: disable=too-many-arguments
def get_forecast(
    site_uuid: str,
    time_step: Optional[int] = None,
    horizon: Optional[int] = None,
    precision: Optional[int] = None,
    fields: Optional[List[str]] = None,
    use_timestamp_format: bool = False,
    time_stamp_unit: Optional[Literal["ms", "s"]] = None,
) -> pd.DataFrame:
    """
    Fetch forecast data for a specific site with given parameters.

    See default values and more information about each parameters at:
    https://steadyweb.steady-sun.com/rapidoc/#get-/forecast/-object_type-/-component_uuid-/

    Args:
        site_uuid (str): The UUID of the site.
        time_step (Optional[int], optional): The time step of the forecast (in minutes).
        horizon (Optional[int], optional): The horizon of the forecast (in minutes).
        precision (Optional[int], optional): Maximal number of decimal places.
        fields (Optional[List[str]], optional): The fields to include in the forecast.
        use_timestamp_format (bool, optional): Should the timestamp format be used instead of iso_8601 for date.
        time_stamp_unit (Optional[Literal["ms", "s"]], optional): The unit of the time stamp (if use_timestamp_format).

    Returns:
        pd.DataFrame: The forecast data for the specified site.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.

    Example:
        Fetch forecast data for a specific site with a time step of 30 minutes, a horizon of 2440 minutes,
        a precision of 4 decimal places, and including the "all_sky_global_horizontal_irradiance" and "2m_temperature"::

            forecast_df = get_forecast(
                site_uuid="SITE_UUID",
                time_step=30,
                horizon=2440,
                precision=4,
                fields=["all_sky_global_horizontal_irradiance", "2m_temperature"],
            )
    """
    forecast_parameters = _ForecastParameters(
        time_step=time_step,
        horizon=horizon,
        precision=precision,
        fields=fields,
        date_time_format="time_stamp" if use_timestamp_format else None,
        time_stamp_unit=time_stamp_unit,
    )

    endpoint = f"forecast/pvsystem/{site_uuid}/"
    params = forecast_parameters.to_dict()

    # Make the GET call
    api_data = SteadysunAPI().get(endpoint, params=params)

    # Convert the response to a pandas DataFrame
    forecast_df = pd.DataFrame(data=api_data["data"], index=api_data["index"], columns=api_data["columns"])

    return forecast_df
