from config.sheet_config import DATE_COLUMN_INDEX, DATE_COLUMN_NAME, STATUS_COLUMN_NAME, STATUS_COLUMN_INDEX, \
    VALUE_COLUMN_WIDTH, HEADER_ROW_INDEX, STATUS_COLUMN_WIDTH, DATE_COLUMN_WIDTH
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
        date_cell = self.cell_by_index(HEADER_ROW_INDEX, DATE_COLUMN_INDEX)
        if date_cell.value != DATE_COLUMN_NAME:
            self._create_header(DATE_COLUMN_INDEX, DATE_COLUMN_NAME, DATE_COLUMN_WIDTH)

        status_cell = self.cell_by_index(HEADER_ROW_INDEX, STATUS_COLUMN_INDEX)
        if status_cell.value != STATUS_COLUMN_NAME:
            self._create_header(STATUS_COLUMN_INDEX, STATUS_COLUMN_NAME, STATUS_COLUMN_WIDTH)

    def insert_histogram_data(self, datetime, data: OrdersHistogramData, crate: Crate):
        row_index = self._find_by_date_row_index(datetime)
        if row_index == -1:
            row_index = self._find_available_row_index()

        column_index = self._find_by_header_name(crate.short_name)
        if column_index == -1:
            column_index = self._find_available_column_index()
            self._create_header(column_index, crate.short_name, VALUE_COLUMN_WIDTH)

        date_cell = self.cell_by_index(row_index, DATE_COLUMN_INDEX)
        if date_cell.value is None:
            date_cell.set_value(datetime).center().border_right('thin')

        status_cell = self.cell_by_index(row_index, STATUS_COLUMN_INDEX)
        status_cell.border_right('thin')
        if data.status is False:
            status_cell.set_value("!").fill_by_pattern("DARK", 5).border('thin').center()

        value_cell = self.cell_by_index(row_index, column_index)
        if value_cell.value is None:
            value_cell.set_value(data.price).center()
            self._fill_cell_ratio(row_index, column_index)

