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
        try:
            self.spreadsheet.save()
            datetime = Time.now()
            print(f"Datetime: {datetime}")
            for crate_name in self.crates_set:
                print(f"{crate_name} data:")
                crate = Crate(crate_name)

                order_histogram_data = self.order_histogram.get_data(crate)
                price_overview_data = self.price_overview.get_data(crate)

                data_extraction_time = Time().start()

                self.spreadsheet.insert_histogram_data(crate, datetime, order_histogram_data)
                self.spreadsheet.insert_price_overview_data(crate, datetime, price_overview_data)
                data_extraction_time.end()
                print(f"Data extraction time: ({data_extraction_time.result:0.3f}s)")

                self.spreadsheet.insert_colors()

                self.spreadsheet.save()
        except PermissionError:
            print('\033[91m' + 'Cannot save workbook' + '\033[0m')

    def __str__(self):
        return '<CratesCrawler>'
