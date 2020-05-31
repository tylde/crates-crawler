from src.Crate import Crate
from src.OrdersHistogramData import OrdersHistogramData
from src.Request import Request


class OrdersHistogramRequest(Request):
    def __init__(self, api, endpoint):
        super().__init__(api, endpoint)

    def get_data(self, crate: Crate):
        param = crate.histogram_id
        response = self.make_request(param)
        return OrdersHistogramRequest.parse_response(response)

    @staticmethod
    def parse_response(response):
        return OrdersHistogramData.from_response(response)

    def __str__(self):
        return 'OrdersHistogramRequest'
