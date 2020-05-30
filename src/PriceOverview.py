from src.Crate import Crate
from src.Request import Request


class PriceOverview(Request):
    def __init__(self, api, endpoint):
        super().__init__(api, endpoint)

    def get_data(self, crate: Crate):
        param = crate.price_overview_name
        response = self.make_request(param)
        return self.parse_response(response)

    def parse_response(self, response):
        return response

    def __str__(self):
        return 'OrdersHistogram'
