from crates_crawler.model.Crate import Crate
from crates_crawler.model.OrdersHistogramData import OrdersHistogramData
from crates_crawler.request.Request import Request


class OrdersHistogramRequest(Request):
    def __init__(self, api, endpoint):
        super().__init__(api, endpoint, "HG")

    def get_data(self, crate: Crate):
        response = self.make_request(crate.histogram_id)
        return OrdersHistogramRequest.parse_response(response)

    @staticmethod
    def parse_response(response):
        return OrdersHistogramData.from_response(response)

    def __str__(self):
        return '<OrdersHistogramRequest>'
