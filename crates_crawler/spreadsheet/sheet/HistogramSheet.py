from openpyxl import Workbook

from config.sheet_config import DATE_COLUMN_INDEX, VOLUME_COLUMN_INDEX, BUY_COLUMN_INDEX, SELL_COLUMN_INDEX, \
    BUY_COLUMN_NAME, VOLUME_COLUMN_NAME, DATE_COLUMN_NAME, SELL_COLUMN_NAME, ORDERS_COLUMN_START_INDEX, \
    PRICE_COLUMN_INDEX, PRICE_COLUMN_NAME, STATUS_COLUMN_INDEX, STATUS_COLUMN_NAME, DATE_COLUMN_WIDTH, \
    STATUS_COLUMN_WIDTH, PRICE_COLUMN_WIDTH, BUY_COLUMN_WIDTH, VOLUME_COLUMN_WIDTH, SELL_COLUMN_WIDTH,\
    HEADER_ROW_INDEX, ORDERS_COLUMN_WIDTH
from crates_crawler.model.Crate import Crate
from crates_crawler.model.OrdersHistogramData import OrdersHistogramData
from crates_crawler.model.PriceOverviewData import PriceOverviewData
from crates_crawler.spreadsheet.sheet.Sheet import Sheet


class HistogramSheet(Sheet):
    def __init__(self, workbook: Workbook, crate: Crate):
        super().__init__(workbook, crate.short_name)
        self._init()

        self.crate = crate

    def _init(self):
        self._create_date_header()

    def _create_date_header(self):
        date_cell = self.cell_by_index(HEADER_ROW_INDEX, DATE_COLUMN_INDEX)
        if date_cell.value != DATE_COLUMN_NAME:
            self._create_header(DATE_COLUMN_INDEX, DATE_COLUMN_NAME, DATE_COLUMN_WIDTH)

        status_cell = self.cell_by_index(HEADER_ROW_INDEX, STATUS_COLUMN_INDEX)
        if status_cell.value != STATUS_COLUMN_NAME:
            self._create_header(STATUS_COLUMN_INDEX, STATUS_COLUMN_NAME, STATUS_COLUMN_WIDTH)

        price_cell = self.cell_by_index(HEADER_ROW_INDEX, PRICE_COLUMN_INDEX)
        if price_cell.value != PRICE_COLUMN_NAME:
            self._create_header(PRICE_COLUMN_INDEX, PRICE_COLUMN_NAME, PRICE_COLUMN_WIDTH)

        volume_cell = self.cell_by_index(HEADER_ROW_INDEX, VOLUME_COLUMN_INDEX)
        if volume_cell.value != VOLUME_COLUMN_NAME:
            self._create_header(VOLUME_COLUMN_INDEX, VOLUME_COLUMN_NAME, VOLUME_COLUMN_WIDTH)

        buy_cell = self.cell_by_index(HEADER_ROW_INDEX, BUY_COLUMN_INDEX)
        if buy_cell.value != BUY_COLUMN_NAME:
            self._create_header(BUY_COLUMN_INDEX, BUY_COLUMN_NAME, BUY_COLUMN_WIDTH)

        sell_cell = self.cell_by_index(HEADER_ROW_INDEX, SELL_COLUMN_INDEX)
        if sell_cell.value != SELL_COLUMN_NAME:
            self._create_header(SELL_COLUMN_INDEX, SELL_COLUMN_NAME, SELL_COLUMN_WIDTH)

    def _insert_order_list(self, order_list, row_index, pattern_name, pattern_level):
        current_column_index = ORDERS_COLUMN_START_INDEX
        for order in order_list:
            [order_price, order_amount] = order
            header_cell = self.cell_by_index(HEADER_ROW_INDEX, current_column_index)

            while str(order_price) != str(header_cell.value):
                if header_cell.value is None or float(order_price) < float(header_cell.value):
                    self._insert_column(current_column_index)
                    self._create_header(current_column_index, str(order_price), ORDERS_COLUMN_WIDTH)
                else:
                    current_column_index += 1
                header_cell = self.cell_by_index(HEADER_ROW_INDEX, current_column_index)

            order_cell = self.cell_by_index(row_index, current_column_index)
            order_cell.set_value(order_amount).number_format().center()
            order_cell.fill_by_pattern(pattern_name, pattern_level)

            current_column_index += 1

    def insert_price_overview_data(self, datetime, data: PriceOverviewData):
        row_index = self._find_by_date_row_index(datetime)
        if row_index == -1:
            row_index = self._find_available_row_index()

        date_cell = self.cell_by_index(row_index, DATE_COLUMN_INDEX)
        if date_cell.value is None:
            date_cell.set_value(datetime).center().border_right('thin')

        status_cell = self.cell_by_index(row_index, STATUS_COLUMN_INDEX)
        status_cell.border_right('thin')
        if data.status is False:
            status_cell.set_value("!").fill_by_pattern("DARK", 5).border('thin').center()

        volume_cell = self.cell_by_index(row_index, VOLUME_COLUMN_INDEX)
        if volume_cell.value is None:
            volume_cell.set_value(data.volume).number_format().center()
            self._fill_cell_ratio(row_index, VOLUME_COLUMN_INDEX)

    def insert_histogram_data(self, datetime, data: OrdersHistogramData):
        row_index = self._find_by_date_row_index(datetime)
        if row_index == -1:
            row_index = self._find_available_row_index()

        date_cell = self.cell_by_index(row_index, DATE_COLUMN_INDEX)
        if date_cell.value is None:
            date_cell.set_value(datetime).center().border_right('thin')

        status_cell = self.cell_by_index(row_index, STATUS_COLUMN_INDEX)
        status_cell.border_right('thin')
        if data.status is False:
            status_cell.set_value("!").fill_by_pattern("DARK", 5).center()

        price_cell = self.cell_by_index(row_index, PRICE_COLUMN_INDEX)
        if price_cell.value is None:
            price_cell.set_value(data.price).center()
            self._fill_cell_ratio(row_index, PRICE_COLUMN_INDEX)

        buy_cell = self.cell_by_index(row_index, BUY_COLUMN_INDEX)
        if buy_cell.value is None:
            buy_cell.set_value(data.buy_orders).number_format().center()
            self._fill_cell_ratio(row_index, BUY_COLUMN_INDEX)

        sell_cell = self.cell_by_index(row_index, SELL_COLUMN_INDEX)
        if sell_cell.value is None:
            sell_cell.set_value(data.sell_orders).border_right('thin').number_format().center()
            self._fill_cell_ratio(row_index, SELL_COLUMN_INDEX, True)

        self._insert_order_list(data.buy_order_list[::-1], row_index, "YELLOW", 0)
        self._insert_order_list(data.sell_order_list, row_index, "BLUE", 0)
