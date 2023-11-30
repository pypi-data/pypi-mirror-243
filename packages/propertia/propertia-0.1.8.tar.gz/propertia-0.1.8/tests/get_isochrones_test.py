from unittest.mock import patch

from propertia.client import PropertiaClient


@patch(
    target='propertia.client.PropertiaClient.make_post_call',
    return_value={
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": ["some_coordinates_for_you"]
                },
            }
        ]
    }
)
def test_get_isochrones(destinations):
    with PropertiaClient(api_key="dummy") as client:
        polygon = client.get_isochrones(destinations, True)
        assert polygon["type"] == "FeatureCollection"
