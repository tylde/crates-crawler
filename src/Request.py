from requests import get, exceptions as ex


class Request:
    def __init__(self, api, endpoint):
        self.api = api
        self.endpoint = endpoint

    def make_request(self, param):
        try:
            url = self.api + self.endpoint + str(param)
            print(url)
            response = get(url).json()
            return response
        except ex.ConnectionError:
            pass
        except ex.HTTPError:
            pass
        except ex.TooManyRedirects:
            pass
        except ex.Timeout:
            pass
