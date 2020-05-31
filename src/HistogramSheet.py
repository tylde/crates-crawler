from openpyxl import Workbook

from src.Crate import Crate
from src.Sheet import Sheet
from src.OrdersHistogramData import OrdersHistogramData


class HistogramSheet(Sheet):
    def __init__(self, workbook: Workbook, crate: Crate):
        super().__init__(workbook, crate.short_name)
        self.crate = crate

    def _create(self):
        super()._create()
        self.value('A1', 'Date')
        self.center('A1')
        self.bold('A1')

    def insert_histogram_data(self, time, data: OrdersHistogramData):
        self._set_active()
        sheet = self.workbook.active
        print('ACTIVE: {}'.format(sheet))

        time_row = self._find_row_by_time(time)
        print('time_row', time_row)

        print('insert_data')
        print('Time: {}'.format(time))
        print('Buy orders: {}'.format(data.buy_orders))
        pass
