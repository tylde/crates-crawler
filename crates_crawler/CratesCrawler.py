import os
import shutil
import time

from config.index import ITEM_ORDERS_HISTOGRAM_URL, PRICE_OVERVIEW_URL
from crates_crawler.model.Crate import Crate
from crates_crawler.request.OrdersHistogramRequest import OrdersHistogramRequest
from crates_crawler.request.PriceOverviewRequest import PriceOverviewRequest
from crates_crawler.spreadsheet.Spreadsheet import Spreadsheet
from crates_crawler.utils.Time import Time


class CratesCrawler:
    def __init__(self, api, crates_set, output_dir, output_filename, output_file_extension):
        self.API = api
        self.PRICE_OVERVIEW_URL = PRICE_OVERVIEW_URL
        self.ITEM_ORDERS_HISTOGRAM_URL = ITEM_ORDERS_HISTOGRAM_URL

        self.crates_set = crates_set
        self.output_dir = output_dir
        self.output_filename = output_filename
        self.output_file_extension = output_file_extension
        self.output = self.output_dir + self.output_filename + self.output_file_extension

        self.order_histogram = OrdersHistogramRequest(self.API, self.ITEM_ORDERS_HISTOGRAM_URL)
        self.price_overview = PriceOverviewRequest(self.API, self.PRICE_OVERVIEW_URL)
        self.spreadsheet = Spreadsheet(self.output)

        self._backup()

    def _backup(self):
        backup_time = Time.backup()
        backup = self.output_dir + self.output_filename + "_" + backup_time + self.output_file_extension
        is_backup_exist = os.path.exists(backup)
        if is_backup_exist is False:
            shutil.copy(self.output, backup)

    def get_data(self):
        try:
            self.spreadsheet.save()
            datetime = Time.now()
            print(f"Datetime: {datetime}")
            for crate_name in self.crates_set:
                crate = Crate(crate_name)
                print(f"{crate.short_name} data:")

                order_histogram_data = self.order_histogram.get_data(crate)
                price_overview_data = self.price_overview.get_data(crate)

                data_extraction_time = Time().start()

                self.spreadsheet.insert_histogram_data(crate, datetime, order_histogram_data)
                self.spreadsheet.insert_price_overview_data(crate, datetime, price_overview_data)

                data_extraction_time.end()
                print(f"  Data extraction time: ({data_extraction_time.result:0.3f}s)")

                # colors sheet
                self.spreadsheet.insert_colors()

                self.spreadsheet.save()

                time.sleep(1)
        except PermissionError:
            print('\033[91m' + 'Cannot save workbook' + '\033[0m')

    def __str__(self):
        return '<CratesCrawler>'
