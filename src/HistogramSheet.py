from openpyxl import Workbook

from src.Crate import Crate


class HistogramSheet:
    def __init__(self, workbook: Workbook, crate: Crate):
        self.workbook = workbook
        self.crate = crate

    def _change_to_sheet(self):
        try:
            sheet_index = self.workbook.worksheets.index(self.crate.short_name)
        except ValueError:
            self.workbook.create_sheet(self.crate.short_name)
            sheet_index = self.workbook.worksheets.index(self.crate.short_name)
            pass

    def insert_data(self, data):
        pass
