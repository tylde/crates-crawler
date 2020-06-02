from src.Crate import Crate
from src.OrdersHistogramRequest import OrdersHistogramRequest
from src.PriceOverviewRequest import PriceOverviewRequest
from src.Spreadsheet import Spreadsheet
from src.Time import Time

from config.index import ITEM_ORDERS_HISTOGRAM_URL, PRICE_OVERVIEW_URL


class CratesCrawler:
    def __init__(self, api, crates_set, output):
        self.API = api
        self.PRICE_OVERVIEW_URL = PRICE_OVERVIEW_URL
        self.ITEM_ORDERS_HISTOGRAM_URL = ITEM_ORDERS_HISTOGRAM_URL

        self.crates_set = crates_set
        self.output = output

        self.order_histogram = OrdersHistogramRequest(self.API, self.ITEM_ORDERS_HISTOGRAM_URL)
        self.price_overview = PriceOverviewRequest(self.API, self.PRICE_OVERVIEW_URL)
        self.spreadsheet = Spreadsheet(self.output)

    def get_data(self):
        for crate_name in self.crates_set:
            crate = Crate(crate_name)

            time = Time.now()
            order_histogram_data = self.order_histogram.get_data(crate)
            price_overview_data = self.price_overview.get_data(crate)

            self.spreadsheet.insert_histogram_data(crate, time, order_histogram_data)
            self.spreadsheet.insert_price_overview_data(crate, time, price_overview_data)

            self.spreadsheet.save()

    def __str__(self):
        return '<CratesCrawler>'
