from typing import Any, Dict, List

import httpx


class PropertiaClient:
    SMARTSCORE_ENDPOINT = '/smartscore/'
    ISOCHRONES_ENDPOINT = '/isochrones/'
    TRAVEL_TIME_ENDPOINT = '/travel-time/'

    def __init__(self, api_key: str, host: str = "https://propertia.searchsmartly.co") -> None:
        self._host = host.rstrip("/")
        self._api_key = api_key
        self._headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        self.client = httpx.Client(transport=httpx.HTTPTransport(retries=3), base_url=self._host, headers=self._headers)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def get_scores(self, properties: List, needs: Dict[str, Any]) -> Dict[str, List]:
        payload = {
            "needs": needs,
            "properties": properties,
        }
        return self.make_post_call(self.SMARTSCORE_ENDPOINT, payload)

    def get_isochrones(self, destinations: List, aggregated: bool) -> Dict[str, Any]:
        """
        The destinations parameter is a list of 1 or 2 dictionaries, each of which must contain the following:
        {
            "id": "destination",
            "latitude": 25.197197,
            "longitude": 55.27437639999999,
            "time": 10,
            "methods": [
                "walking", "driving", "cycling", "public_transport"
            ]
        }
        The aggregated parameter is a boolean that specifies whether to return a single isochrone or a list of them
        """
        payload = {
            "destinations": destinations,
            "aggregated": aggregated
        }
        return self.make_post_call(self.ISOCHRONES_ENDPOINT, payload)

    def get_travel_time(self, destinations: List, properties: List) -> Dict[str, List]:
        """
        The destinations parameter is a list of 1 or 2 dictionaries, each of which must contain the following:
        {
            "id": "destination",
            "latitude": 25.197197,
            "longitude": 55.27437639999999,
            "time": 10,
            "methods": [
                "walking", "driving", "cycling", "public_transport"
            ]
        }
        The properties parameter is a list of dictionaries, each of which must contain the following:
        {
            "id": "string",
            "latitude": -90,
            "longitude": -180
        }
        """
        payload = {
            "origin": destinations,
            "properties": properties,
        }
        return self.make_post_call(self.TRAVEL_TIME_ENDPOINT, payload)

    def make_post_call(self, endpoint: str, payload: Dict) -> Dict[str, List]:
        return self.client.post(endpoint, json=payload).json()
