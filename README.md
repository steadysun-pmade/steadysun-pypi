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
from steadysun.client import SteadysunClient
from steadysun import forecast

# You can either set your token in your env at "STEADYSUN_API_TOKEN"
# OR use the following line :
SteadysunClient.set_api_token("YOUR_TOKEN")

get_solar_forecast(
    site_uuid="testts",
    forecast_parameters={
        "time_step": 30,
        "horizon": 2440,
        "precision": 4,
        "fields": ["ghi", "dni"],
    },
)
```

## API Documentation

For detailed information about the API endpoints, parameters, and available data, please refer to the [Steadysun API Documentation](https://www.steady-sun.com/api-documentation/).

## Contact

For questions, issues, or support, feel free to reach out via email at <email@example.com>.

You can also submit ideas or report issues on the [GitLab Issues page](https://gitlab.com/steadysun/business-applications/steadysun_pipy/-/issues).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.