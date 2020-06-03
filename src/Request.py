from requests import get
from requests.exceptions import HTTPError, ConnectionError

from src.Time import Time


class Request:
    def __init__(self, api, endpoint):
        self.api = api
        self.endpoint = endpoint

    def make_request(self, param):
        request_time = Time()
        request_status = 500
        try:
            request_time.start()
            url = self.api + self.endpoint + str(param)
            response = get(url)
            request_status = response.status_code
            if response.status_code == 200:
                return response.json()
            return None
        except ConnectionError:
            request_status = 500
            return None
        except HTTPError as error:
            request_status = error.response.status_code
        finally:
            request_time.end()
            print(f"Request: {request_status} ({request_time.result:0.3f}s)")
