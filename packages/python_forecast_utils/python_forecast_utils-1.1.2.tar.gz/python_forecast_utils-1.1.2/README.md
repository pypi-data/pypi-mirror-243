# Forecast utils

Forecast utils expose custom features for `python-forecast` projects

## Installation
```bash
pip install python_forecast_utils
```

## Usage
```
from python_forecast_utils import sqrt_transformer

sqrt_transformer.SqrtTransformer()
```

## Development
In order to add a new feature, add the feature into `forecast_utils` folder in its own file.
If the feature uses packages add/check if the package is listed inside the `pyproject.toml`

To add a new package:
`poetry add <PACKAGE>`

Then install all the dependencies:
`poetry install`

To add tests to anew feature, add a file to `tests` folder prefixed with `test_`.

To run the tests:
`poetry run pytest`

## Package deployment
To deploy on pypi, make sure to update the version inside `pyproject.toml`, then :
`poetry build`
`poetry publish`

PS: curretly link to bgeffrault@outlook.fr account, but an organization creation is in progress

### Documentation
Additional documentation https://python-poetry.org/
