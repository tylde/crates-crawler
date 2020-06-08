import os
import shutil

from config.index import ITEM_ORDERS_HISTOGRAM_URL, PRICE_OVERVIEW_URL, MAKE_PRICE_OVERVIEW_REQUEST, \
    MAKE_ORDERS_HISTOGRAM_REQUEST, DRAW_COLORS_SHEET
from crates_crawler.model.Crate import Crate
from crates_crawler.request.OrdersHistogramRequest import OrdersHistogramRequest
from crates_crawler.request.PriceOverviewRequest import PriceOverviewRequest
from crates_crawler.spreadsheet.Spreadsheet import Spreadsheet
from crates_crawler.utils.Time import Time


class CratesCrawler:
    def __init__(self, api, required_crates, output_dir, output_filename, output_file_extension):
        self.API = api
        self.PRICE_OVERVIEW_URL = PRICE_OVERVIEW_URL
        self.ITEM_ORDERS_HISTOGRAM_URL = ITEM_ORDERS_HISTOGRAM_URL

        self.required_crates = required_crates
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

    def _check_permissions(self):
        stopper = Time()
        print("Checking permissions...")
        stopper.start()
        self.spreadsheet.save()
        stopper.end()
        print(f"Done. ({stopper.result:0.3f}s)")

    def _save_spreadsheet(self):
        stopper = Time()
        print("Saving...")
        stopper.start()
        self.spreadsheet.save()
        stopper.end()
        print(f"Spreadsheet has been saved. ({stopper.result:0.3f}s)")

    def get_data(self):
        stopper = Time()

        try:
            self._check_permissions()
            datetime = Time.now()
            print(f"Datetime: {datetime}")

            for crate_name in self.required_crates:
                crate = Crate(crate_name)
                print(f"{crate.short_name} data:")

                if MAKE_ORDERS_HISTOGRAM_REQUEST is True:
                    order_histogram_data = self.order_histogram.get_data(crate)
                    stopper.start()
                    self.spreadsheet.insert_histogram_data(crate, datetime, order_histogram_data)
                    stopper.end()
                    print(f"  Data extraction time: ({stopper.result:0.3f}s)")
                if MAKE_PRICE_OVERVIEW_REQUEST is True:
                    price_overview_data = self.price_overview.get_data(crate)
                    stopper.start()
                    self.spreadsheet.insert_price_overview_data(crate, datetime, price_overview_data)
                    stopper.end()
                    print(f"  Data extraction time: ({stopper.result:0.3f}s)")
                if DRAW_COLORS_SHEET is True:
                    self.spreadsheet.insert_colors()

            self._save_spreadsheet()
        except PermissionError:
            print('\033[91m' + 'Permission denied' + '\033[0m')

    def __str__(self):
        return '<CratesCrawler>'
