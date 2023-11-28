from typing import Dict, List, Any
import httpx


class PropertiaClient:
    SMARTSCORE_ENDPOINT = '/smartscore/'

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
        data = {
            "needs": needs,
            "properties": properties,
        }
        return self.make_post_call(self.SMARTSCORE_ENDPOINT, data)

    def make_post_call(self, endpoint: str, data: Dict) -> Dict[str, List]:
        return self.client.post(endpoint, json=data).json()
