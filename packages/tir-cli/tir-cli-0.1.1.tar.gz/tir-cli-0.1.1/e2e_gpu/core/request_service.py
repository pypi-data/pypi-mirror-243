import requests

from e2e_gpu.core.constants import BASE_URL


class Request:
    def __init__(self, url, auth_token, payload, request_method, query={}):
        self.headers = {
            'Authorization': 'Bearer ' + auth_token,
            'Content-Type': 'application/json',
            'User-Agent': ""
        }
        self.url = BASE_URL + url
        self.request_method = request_method
        self.query = query
        self.payload = payload

    def make_api_call(self):
        return requests.request(self.request_method, self.url, headers=self.headers, data=self.payload, params=self.query).json()


class Methods:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
