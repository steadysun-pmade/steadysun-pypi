# Steadysun Package

A Python package designed to facilitate interaction with the **Steadysun** API.

## Features

- **Easy API Interaction**: Simplified methods to authenticate and query the Steadysun API.
- **Data Retrieval**: Fetch solar forecast data in various formats (JSON, CSV, etc.).
- **Error Handling**: Graceful error handling for common API errors such as authentication failure, bad requests, and more.
- **Customizable**: Flexible configuration options to tailor API requests to your needs.

## Installation

You can install the package using pip:

```bash
pip install steadysun
```

## Quick Start

Here's an example of how to use `steadysun`:

```python
from steadysun.steadysun_api import SteadysunAPI
from steadysun.forecast import get_forecast

# You can either set your token in your env at "STEADYSUN_API_TOKEN"
# OR use the following line :
SteadysunAPI.set_api_token("YOUR_TOKEN")

forecast_df = get_forecast("SITE_UUID")

forecast_df = get_forecast(
    site_uuid="SITE_UUID",
    time_step=30,
    horizon=2440,
    precision=4,
    fields=["all_sky_global_horizontal_irradiance", "2m_temperature"],
)
```

## API Documentation

For detailed information about the API endpoints, parameters, and available data, please refer to the [Steadysun API Documentation](https://www.steady-sun.com/api-documentation/).

## Package history (CHANGELOG)

For detailed information on version updates of this package, please refer to the [CHANGELOG](./CHANGELOG.md).

## Contact

For questions, issues, or support, feel free to reach out via email at <email@example.com>.

You can also submit ideas or report issues on the [GitLab Issues page](https://gitlab.com/steadysun/business-applications/steadysun_pipy/-/issues).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
