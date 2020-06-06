from config.sheet_config import DATE_COLUMN_INDEX, DATE_COLUMN_NAME, STATUS_COLUMN_NAME, STATUS_COLUMN_INDEX
from crates_crawler.model.Crate import Crate
from crates_crawler.model.OrdersHistogramData import OrdersHistogramData
from crates_crawler.spreadsheet.sheet.Sheet import Sheet


class PriceSheet(Sheet):
    def __init__(self, workbook, sheet_name):
        super().__init__(workbook, sheet_name)
        self._init()

    def _init(self):
        self._create_date_header()

    def _create_date_header(self):
        date_cell = self.cell_by_index(1, DATE_COLUMN_INDEX)
        if date_cell.value != DATE_COLUMN_NAME:
            date_cell.center().border_bottom('thin').border_right('thin').bold().set_value(DATE_COLUMN_NAME)
            self.set_column_index_width(DATE_COLUMN_INDEX, 20)

        status_cell = self.cell_by_index(1, STATUS_COLUMN_INDEX)
        if status_cell.value != STATUS_COLUMN_NAME:
            status_cell.center().border_bottom('thin').border_right('thin').bold().set_value(STATUS_COLUMN_NAME)
            self.set_column_index_width(STATUS_COLUMN_INDEX, 3)

    def _get_price_ratio(self, row_index, column_index, data: OrdersHistogramData):
        last_day_row_index = self._get_last_day_row_index(row_index)
        if last_day_row_index < 1:
            return 1

        last_day_price = self.cell_by_index(last_day_row_index, column_index).value
        if last_day_price is None:
            return 1

        return data.price / last_day_price

    def insert_histogram_data(self, datetime, data: OrdersHistogramData, crate: Crate):
        row_index = self._find_by_date_row_index(datetime)
        if row_index == -1:
            row_index = self._find_available_row_index()

        column_index = self._find_by_header_name(crate.short_name)
        if column_index == -1:
            column_index = self._find_available_column_index()
            # todo maybe add create_header function
            self.cell_by_index(1, column_index).set_value(crate.short_name).bold().center().border('thin')
            self.set_column_index_width(column_index, 12)

        date_cell = self.cell_by_index(row_index, DATE_COLUMN_INDEX)
        if date_cell.value is None:
            date_cell.set_value(datetime).center().border_right('thin')

        status_cell = self.cell_by_index(row_index, STATUS_COLUMN_INDEX)
        status_cell.border_right('thin')
        if data.status is False:
            status_cell.set_value("!").fill_by_pattern("DARK", 5).border('thin').center()

        price_ratio = self._get_price_ratio(row_index, column_index, data)
        (price_color_pattern, price_color_level) = self._get_ratio_color(price_ratio)

        value_cell = self.cell_by_index(row_index, column_index)
        if value_cell.value is None:
            value_cell.set_value(data.price).center()\
                .fill_by_pattern(price_color_pattern, price_color_level)
