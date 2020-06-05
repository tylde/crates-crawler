from openpyxl import Workbook

from config.sheet_config import DATE_COLUMN_INDEX, VOLUME_COLUMN_INDEX, BUY_COLUMN_INDEX, SELL_COLUMN_INDEX, \
    BUY_COLUMN_NAME, VOLUME_COLUMN_NAME, DATE_COLUMN_NAME, SELL_COLUMN_NAME, ORDERS_COLUMN_START_INDEX, \
    PRICE_COLUMN_INDEX, PRICE_COLUMN_NAME, STATUS_COLUMN_INDEX, STATUS_COLUMN_NAME
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
        date_cell = self.cell_by_index(1, DATE_COLUMN_INDEX)
        status_cell = self.cell_by_index(1, STATUS_COLUMN_INDEX)
        price_cell = self.cell_by_index(1, PRICE_COLUMN_INDEX)
        volume_cell = self.cell_by_index(1, VOLUME_COLUMN_INDEX)
        buy_cell = self.cell_by_index(1, BUY_COLUMN_INDEX)
        sell_cell = self.cell_by_index(1, SELL_COLUMN_INDEX)

        if date_cell.value != DATE_COLUMN_NAME:
            date_cell.center().border_bottom('thin').border_right('thin').bold().set_value(DATE_COLUMN_NAME)
            self.set_column_index_width(DATE_COLUMN_INDEX, 20)

        if status_cell.value != STATUS_COLUMN_NAME:
            status_cell.center().border_bottom('thin').bold().set_value(STATUS_COLUMN_NAME)
            self.set_column_index_width(STATUS_COLUMN_INDEX, 3)

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

    def _insert_order_list(self, order_list, row_index, pattern_name, pattern_level):
        current_column_index = ORDERS_COLUMN_START_INDEX
        for order in order_list:
            [order_price, order_amount] = order
            header_cell = self.cell_by_index(1, current_column_index)

            while str(order_price) != str(header_cell.value):
                if header_cell.value is None or float(order_price) < float(header_cell.value):
                    self.insert_column(current_column_index)
                    self.cell_by_index(1, current_column_index)\
                        .set_value(str(order_price)).bold().center().border_bottom('thin')
                    self.set_column_index_width(current_column_index, 8)
                else:
                    current_column_index += 1
                header_cell = self.cell_by_index(1, current_column_index)

            order_cell = self.cell_by_index(row_index, current_column_index)
            order_cell.set_value(order_amount).number_format().center().fill_by_pattern(pattern_name, pattern_level)
            current_column_index += 1

    def _get_volume_ratio(self, row_index, data: PriceOverviewData):
        last_day_row_index = self._get_last_day_row_index(row_index)

        if last_day_row_index < 1:
            return 1

        last_day_volume = self.cell_by_index(last_day_row_index, VOLUME_COLUMN_INDEX).value
        if last_day_volume is None:
            return 1

        return data.volume / last_day_volume

    def insert_price_overview_data(self, datetime, data: PriceOverviewData):
        row_index = self._find_by_date_row_index(datetime)
        if row_index == -1:
            row_index = self._find_available_row_index()

        date_cell = self.cell_by_index(row_index, DATE_COLUMN_INDEX)
        if date_cell.value is None:
            date_cell.set_value(datetime).center().border_right('thin')

        if data.status is False:
            status_cell = self.cell_by_index(row_index, STATUS_COLUMN_INDEX)
            status_cell.set_value("!").fill_by_pattern("DARK", 5).border('thin').center()

        volume_ratio = self._get_volume_ratio(row_index, data)
        (volume_color_pattern, volume_color_level) = self._get_ratio_color(volume_ratio)

        volume_cell = self.cell_by_index(row_index, VOLUME_COLUMN_INDEX)
        if volume_cell.value is None:
            volume_cell.set_value(data.volume).number_format().center()\
                .fill_by_pattern(volume_color_pattern, volume_color_level)

    def _get_price_ratio(self, row_index, data: OrdersHistogramData):
        last_day_row_index = self._get_last_day_row_index(row_index)

        if last_day_row_index < 1:
            return 1

        last_day_price = self.cell_by_index(last_day_row_index, PRICE_COLUMN_INDEX).value
        if last_day_price is None:
            return 1

        return data.price / last_day_price

    def _get_sell_orders_ratio(self, row_index, data: OrdersHistogramData):
        last_day_row_index = self._get_last_day_row_index(row_index)

        if last_day_row_index < 1:
            return 1

        last_day_sell_orders = self.cell_by_index(last_day_row_index, SELL_COLUMN_INDEX).value
        if last_day_sell_orders is None:
            return 1

        return data.sell_orders / last_day_sell_orders

    def _get_buy_orders_ratio(self, row_index, data: OrdersHistogramData):
        last_day_row_index = self._get_last_day_row_index(row_index)

        if last_day_row_index < 1:
            return 1

        last_day_buy_orders = self.cell_by_index(last_day_row_index, BUY_COLUMN_INDEX).value
        if last_day_buy_orders is None:
            return 1

        return data.buy_orders / last_day_buy_orders

    def insert_histogram_data(self, datetime, data: OrdersHistogramData):
        row_index = self._find_by_date_row_index(datetime)
        if row_index == -1:
            row_index = self._find_available_row_index()

        date_cell = self.cell_by_index(row_index, DATE_COLUMN_INDEX)
        if date_cell.value is None:
            date_cell.set_value(datetime).center().border_right('thin')

        if data.status is False:
            status_cell = self.cell_by_index(row_index, STATUS_COLUMN_INDEX)
            status_cell.set_value("!").fill_by_pattern("DARK", 5).border('thin').center()

        price_ratio = self._get_price_ratio(row_index, data)
        (price_color_pattern, price_color_level) = self._get_ratio_color(price_ratio)

        buy_orders_ratio = self._get_buy_orders_ratio(row_index, data)
        (buy_orders_color_pattern, buy_orders_color_level) = self._get_ratio_color(buy_orders_ratio)

        sell_orders_ratio = self._get_sell_orders_ratio(row_index, data)
        (sell_orders_color_pattern, sell_orders_color_level) = self._get_ratio_color(sell_orders_ratio, True)

        price_cell = self.cell_by_index(row_index, PRICE_COLUMN_INDEX)
        if price_cell.value is None:
            price_cell.set_value(data.price).center().fill_by_pattern(price_color_pattern, price_color_level)

        buy_cell = self.cell_by_index(row_index, BUY_COLUMN_INDEX)
        if buy_cell.value is None:
            buy_cell.set_value(data.buy_orders).number_format().center()\
                .fill_by_pattern(buy_orders_color_pattern, buy_orders_color_level)

        sell_cell = self.cell_by_index(row_index, SELL_COLUMN_INDEX)
        if sell_cell.value is None:
            sell_cell.set_value(data.sell_orders).border_right('thin').number_format().center()\
                .fill_by_pattern(sell_orders_color_pattern, sell_orders_color_level)

        self._insert_order_list(data.buy_order_list[::-1], row_index, "YELLOW", 0)
        self._insert_order_list(data.sell_order_list, row_index, "BLUE", 0)

    def __str__(self):
        return '<HistogramSheet \"' + self.name + '\">'
