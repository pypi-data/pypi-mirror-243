from unittest.mock import patch

from propertia.client import PropertiaClient


@patch(
    target='propertia.client.PropertiaClient.make_post_call',
    return_value={
        "Property A": {
            "walking": {
                "origin_method_time": 10
            }
        },
        "Property B": {
            "walking": {
                "origin_method_time": 12
            }
        },
        "Property C": {
            "walking": {
                "origin_method_time": 16
            }
        }
    }
)
def test_get_travel_time(destinations, properties):
    with PropertiaClient(api_key="dummy") as client:
        results = client.get_travel_time(destinations, properties)
        assert len(results) == 3
