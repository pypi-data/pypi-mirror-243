from typing import Dict, List

import pytest


@pytest.fixture
def properties() -> List[Dict[str, str]]:
    return [
        {
            "id": "Property A",
            "latitude": "51.0",
            "longitude": "0.0"
        },
        {
            "id": "Property B",
            "latitude": "51.1",
            "longitude": "0.1"
        },
        {
            "id": "Property C",
            "latitude": "51.2",
            "longitude": "0.2"
        }
    ]


@pytest.fixture
def needs() -> Dict[str, Dict]:
    return {
        "food-and-drink": {
            "importance": 5,
            "categories": [
                "fast-food"
            ]
        }
    }


@pytest.fixture
def destinations() -> List[Dict]:
    return [
        {
            "id": "destination",
            "latitude": 25.197197,
            "longitude": 55.27437639999999,
            "time": 10,
            "methods": [
                "walking", "driving"
            ]
        }
    ]
