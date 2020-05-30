from src.Crate import Crate
from src.OrdersHistogram import OrdersHistogram
from src.Spreadsheet import Spreadsheet

from config.index import ITEM_ORDERS_HISTOGRAM_URL, STEAM_API, PRICE_OVERVIEW_URL, DATA_FILENAME


class CratesCrawler:
    def __init__(self, crates_set):
        self.API = STEAM_API
        self.PRICE_OVERVIEW_URL = PRICE_OVERVIEW_URL
        self.ITEM_ORDERS_HISTOGRAM_URL = ITEM_ORDERS_HISTOGRAM_URL

        self.crates_set = crates_set

        self.order_histogram = OrdersHistogram(self.API, self.ITEM_ORDERS_HISTOGRAM_URL)
        self.spreadsheet = Spreadsheet('data/' + DATA_FILENAME)

    def get_data(self):
        for crate_name in self.crates_set:
            print(crate_name)
            crate = Crate(crate_name)
            print(crate)
            order_histogram_data = self.order_histogram.get_data(crate)
            print(order_histogram_data)
