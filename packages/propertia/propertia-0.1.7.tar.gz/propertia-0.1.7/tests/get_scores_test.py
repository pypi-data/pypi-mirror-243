from unittest.mock import patch

from propertia.client import PropertiaClient


@patch(
    target='propertia.client.PropertiaClient.make_post_call',
    return_value={
        "results": [
            {
                "id": "Property C",
                "latitude": "51.2",
                "longitude": "0.2",
                "smartscore": 10,
                "scores": {
                    "food-and-drink": 10
                }
            },
            {
                "id": "Property B",
                "latitude": "51.1",
                "longitude": "0.1",
                "smartscore": 8,
                "scores": {
                    "food-and-drink": 8
                }
            },
            {
                "id": "Property A",
                "latitude": "51.0",
                "longitude": "0.0",
                "smartscore": 6,
                "scores": {
                    "food-and-drink": 6
                }
            }
        ]
    }
)
def test_get_scores(properties, needs):
    with PropertiaClient(api_key="dummy") as client:
        scores = client.get_scores(properties, needs)
        assert len(scores["results"]) == 3
        assert scores["results"][0]["id"] == "Property C"
        assert scores["results"][1]["id"] == "Property B"
        assert scores["results"][2]["id"] == "Property A"
