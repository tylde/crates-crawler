from src.Crate import Crate
from src.OrdersHistogramRequest import OrdersHistogramRequest
from src.Spreadsheet import Spreadsheet
from src.Time import Time

from config.index import ITEM_ORDERS_HISTOGRAM_URL, PRICE_OVERVIEW_URL, DATA_FILENAME


class CratesCrawler:
    def __init__(self, api, crates_set):
        self.API = api
        self.PRICE_OVERVIEW_URL = PRICE_OVERVIEW_URL
        self.ITEM_ORDERS_HISTOGRAM_URL = ITEM_ORDERS_HISTOGRAM_URL

        self.crates_set = crates_set

        self.order_histogram = OrdersHistogramRequest(self.API, self.ITEM_ORDERS_HISTOGRAM_URL)
        self.spreadsheet = Spreadsheet('data/' + DATA_FILENAME)

    def get_data(self):
        for crate_name in self.crates_set:
            print(crate_name)
            crate = Crate(crate_name)
            print(crate)

            time = Time.now()
            order_histogram_data = self.order_histogram.get_data(crate)

            self.spreadsheet.insert_histogram_data(crate, time, order_histogram_data)

            self.spreadsheet.save()

