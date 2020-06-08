from crates_crawler.model.Crate import Crate
from crates_crawler.model.OrdersHistogramData import OrdersHistogramData
from crates_crawler.spreadsheet.sheet.OverviewSheet import OverviewSheet


class SellOrdersSheet(OverviewSheet):
    def __init__(self, workbook, sheet_name):
        super().__init__(workbook, sheet_name)

    def insert_histogram_data(self, datetime, data: OrdersHistogramData, crate: Crate):
        self._insert_value(datetime, data.status, data.sell_orders, crate, True, True)
