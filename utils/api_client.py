import requests

BASE_URL = "https://restful-booker.herokuapp.com"
class APIClient:

    def __init__(self):
        self.base_url = BASE_URL

    def post(self, endpoint, payload=None, headers=None):
        return requests.post(
            f"{self.base_url}{endpoint}",
            json=payload,
            headers=headers
        )

    def get(self, endpoint, headers=None, params=None):
        return requests.get(
            f"{self.base_url}{endpoint}",
            headers=headers,
            params=params
        )

    def put(self, endpoint, payload=None, headers=None, cookies=None):
        return requests.put(
            f"{self.base_url}{endpoint}",
            json=payload,
            headers=headers,
            cookies=cookies
        )

    def patch(self, endpoint, payload=None, headers=None, cookies=None):
        return requests.patch(
            f"{self.base_url}{endpoint}",
            json=payload,
            headers=headers,
            cookies=cookies
        )

    def delete(self, endpoint, headers=None, cookies=None):
        return requests.delete(
            f"{self.base_url}{endpoint}",
            headers=headers,
            cookies=cookies
        )