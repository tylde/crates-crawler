from requests import get, exceptions as ex
from requests.exceptions import HTTPError


class Request:
    def __init__(self, api, endpoint):
        self.api = api
        self.endpoint = endpoint

    def make_request(self, param):
        try:
            url = self.api + self.endpoint + str(param)
            response = get(url)
            print(response.status_code)
            if response.status_code == 200:
                return response.json()
            return None
        except HTTPError as error:
            print(f'HTTP error occurred: {error}')
            print(error.response.status_code)
