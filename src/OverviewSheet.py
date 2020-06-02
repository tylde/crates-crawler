from src.Crate import Crate
from src.OrdersHistogramData import OrdersHistogramData
from src.Sheet import Sheet


class OverviewSheet(Sheet):
    def __init__(self, workbook, sheet_name):
        super().__init__(workbook, sheet_name)

    def insert_histogram_data(self, datetime, data: OrdersHistogramData, crate: Crate):
        row_index = self._find_by_date_row_index(datetime)
        if row_index == -1:
            row_index = self._find_available_row_index()
        pass
