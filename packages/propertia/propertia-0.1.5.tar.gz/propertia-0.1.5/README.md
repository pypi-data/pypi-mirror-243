# Propertia SDK

![PyPI version](https://badge.fury.io/py/propertia.svg) [![Python support](https://img.shields.io/badge/python-3.8+-blue.svg)](https://img.shields.io/badge/python-3.8+-blue)

The Propertia SDK helps users integrate easily with the SmartScore services
## Installation

Install Propertia SDK using `pip`

```
pip install propertia
```

### SDK set up

In order to authenticate with Propertia, you will have to supply the API Key.

```python
from propertia.client import PropertiaClient

with PropertiaClient(api_key="your_api_key") as client:
    ...
```

## Usage


### Get Scores

Given coordinates and needs, return the scores

#### Takes:

* properties
* needs

#### Returns:

* List of properties sorted by descending scores

#### Example:

```python
from propertia.client import PropertiaClient

properties = [
    {
        "id": "Property A",
        "latitude": "43.70558",
        "longitude": "-79.530985"
    },
    {
        "id": "Property B",
        "latitude": "43.640971",
        "longitude": "-79.579119"
    },
    {
        "id": "Property C",
        "latitude": "43.704711",
        "longitude": "-79.287965"
    }
]

needs = {
    "food-and-drink": {
        "importance": 5,
        "categories": [
            "fast-food"
        ]
    }
}

with PropertiaClient(api_key="your_api_key") as client:
    scores = client.get_scores(properties, needs)
    # Do something with your scores
```

