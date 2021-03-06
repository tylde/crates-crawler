from crates_crawler.model.Crate import Crate
from crates_crawler.model.PriceOverviewData import PriceOverviewData
from crates_crawler.request.Request import Request


class PriceOverviewRequest(Request):
    def __init__(self, api, endpoint):
        super().__init__(api, endpoint, "OV")

    def get_data(self, crate: Crate):
        response = self.make_request(crate.price_overview_name)
        return PriceOverviewRequest.parse_response(response)

    @staticmethod
    def parse_response(response):
        return PriceOverviewData.from_response(response)

    def __str__(self):
        return '<PriceOverviewRequest>'
