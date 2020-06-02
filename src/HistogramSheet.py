from openpyxl import Workbook

from config.sheet_config import DATE_COLUMN_INDEX, VOLUME_COLUMN_INDEX, BUY_COLUMN_INDEX, SELL_COLUMN_INDEX, \
    BUY_COLUMN_NAME, VOLUME_COLUMN_NAME, DATE_COLUMN_NAME, SELL_COLUMN_NAME, ORDERS_COLUMN_START_INDEX, \
    PRICE_COLUMN_INDEX, PRICE_COLUMN_NAME
from src.Crate import Crate
from src.OrdersHistogramData import OrdersHistogramData
from src.PriceOverviewData import PriceOverviewData
from src.Sheet import Sheet

from config.contants import BUY_HISTOGRAM_COLOR, SELL_HISTOGRAM_COLOR, VOLUME_HISTOGRAM_COLOR, PRICE_HISTOGRAM_COLOR


class HistogramSheet(Sheet):
    def __init__(self, workbook: Workbook, crate: Crate):
        super().__init__(workbook, crate.short_name)
        self._init()

        self.crate = crate

    def _init(self):
        self._create_date_header()

    def _create_date_header(self):
        date_cell = self.cell_by_index(1, DATE_COLUMN_INDEX)
        price_cell = self.cell_by_index(1, PRICE_COLUMN_INDEX)
        volume_cell = self.cell_by_index(1, VOLUME_COLUMN_INDEX)
        buy_cell = self.cell_by_index(1, BUY_COLUMN_INDEX)
        sell_cell = self.cell_by_index(1, SELL_COLUMN_INDEX)

        if date_cell.value != DATE_COLUMN_NAME:
            date_cell.center().border_bottom('thin').border_right('thin').bold().set_value(DATE_COLUMN_NAME)
            self.set_column_index_width(DATE_COLUMN_INDEX, 20)

        if price_cell.value != PRICE_COLUMN_NAME:
            price_cell.center().border_bottom('thin').bold().set_value(PRICE_COLUMN_NAME)
            self.set_column_index_width(PRICE_COLUMN_INDEX, 12)

        if volume_cell.value != VOLUME_COLUMN_NAME:
            volume_cell.center().border_bottom('thin').bold().set_value(VOLUME_COLUMN_NAME)
            self.set_column_index_width(VOLUME_COLUMN_INDEX, 12)

        if buy_cell.value != BUY_COLUMN_NAME:
            buy_cell.center().border_bottom('thin').bold().set_value(BUY_COLUMN_NAME)
            self.set_column_index_width(BUY_COLUMN_INDEX, 12)

        if sell_cell.value != SELL_COLUMN_NAME:
            sell_cell.center().border_bottom('thin').border_right('thin').bold().set_value(SELL_COLUMN_NAME)
            self.set_column_index_width(SELL_COLUMN_INDEX, 12)

    def _insert_order_list(self, order_list, row_index, color):
        current_column_index = ORDERS_COLUMN_START_INDEX
        for order in order_list:
            [order_price, order_amount] = order
            header_cell = self.cell_by_index(1, current_column_index)

            while str(order_price) != str(header_cell.value):
                if header_cell.value is None or float(order_price) < float(header_cell.value):
                    self.insert_column(current_column_index)
                    self.cell_by_index(1, current_column_index)\
                        .set_value(str(order_price)).bold().center().border_bottom('thin')
                    self.set_column_index_width(current_column_index, 10)
                else:
                    current_column_index += 1
                header_cell = self.cell_by_index(1, current_column_index)

            order_cell = self.cell_by_index(row_index, current_column_index)
            order_cell.set_value(order_amount).number_format().center().fill(color)
            current_column_index += 1

    def insert_price_overview_data(self, datetime, data: PriceOverviewData):
        row_index = self._find_by_date_row_index(datetime)
        if row_index == -1:
            row_index = self._find_available_row_index()
        volume_cell = self.cell_by_index(row_index, VOLUME_COLUMN_INDEX)
        if volume_cell.value is None:
            volume_cell.set_value(data.volume).number_format().center().fill(VOLUME_HISTOGRAM_COLOR)

    def insert_histogram_data(self, datetime, data: OrdersHistogramData):
        row_index = self._find_by_date_row_index(datetime)
        if row_index == -1:
            row_index = self._find_available_row_index()

        date_cell = self.cell_by_index(row_index, DATE_COLUMN_INDEX)
        price_cell = self.cell_by_index(row_index, PRICE_COLUMN_INDEX)
        buy_cell = self.cell_by_index(row_index, BUY_COLUMN_INDEX)
        sell_cell = self.cell_by_index(row_index, SELL_COLUMN_INDEX)

        if date_cell.value is None:
            date_cell.set_value(datetime).center().border_right('thin')

        if price_cell.value is None:
            price_cell.set_value(data.price).center().fill(PRICE_HISTOGRAM_COLOR)

        if buy_cell.value is None:
            buy_cell.set_value(data.buy_orders).number_format().center().fill(BUY_HISTOGRAM_COLOR)

        if sell_cell.value is None:
            sell_cell.set_value(data.sell_orders).border_right('thin').number_format().center().fill(SELL_HISTOGRAM_COLOR)

        self._insert_order_list(data.buy_order_list[::-1], row_index, BUY_HISTOGRAM_COLOR)
        self._insert_order_list(data.sell_order_list, row_index, SELL_HISTOGRAM_COLOR)

    def __str__(self):
        return '<HistogramSheet \"' + self.name + '\">'
