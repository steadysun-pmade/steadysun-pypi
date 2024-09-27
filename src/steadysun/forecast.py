from functools import partial
from typing import List, Optional, Union

import pandas as pd

from ._api import SteadysunAPI
from ._models import ParameterModel


class ForecastParameters(ParameterModel):
    """Available parameters for the get_forecast API call.

    See default values and more information about each parameters at:
    https://www.steady-sun.com/api-documentation/#section__parameters
    """

    time_step: Optional[int] = None
    horizon: Optional[int] = None
    precision: Optional[int] = None
    fields: Optional[List[str]] = None
    date_time_format: Optional[str] = None
    time_stamp_unit: Optional[str] = None
    # TODO add data_format (add also df / csv / json ?)


def get_forecast(
    site_type: str,
    site_uuid: str,
    forecast_parameters: Union[ForecastParameters, dict] = None,
):
    """Fetch forecast data for a specific site."""

    if isinstance(forecast_parameters, dict):
        forecast_parameters = ForecastParameters.from_param_dict(forecast_parameters)

    endpoint = f"forecast/{site_type}/{site_uuid}/"
    params = forecast_parameters.to_param_dict() if forecast_parameters else None

    # Make the GET call
    api_data = SteadysunAPI().get(endpoint, params=params)

    # Convert the response to a pandas DataFrame
    forecast_df = pd.DataFrame(
        data=api_data["data"], index=api_data["index"], columns=api_data["columns"]
    )

    return forecast_df


get_solar_forecast = partial(get_forecast, site_type="pvsystem")
get_group_forecast = partial(get_forecast, site_type="group")
get_windfarm_forecast = partial(get_forecast, site_type="windfarm")
get_windturbine_forecast = partial(get_forecast, site_type="windturbine")
