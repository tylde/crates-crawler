from openpyxl import load_workbook, Workbook

from src.Crate import Crate
from src.HistogramSheet import HistogramSheet

from config.index import OVERVIEW_SHEET_NAME


class Spreadsheet:
    def __init__(self, filename):
        self.filename = filename
        self.workbook = self._load_workbook()

    def _load_workbook(self):
        try:
            return load_workbook(self.filename)
        except FileNotFoundError:
            return self._create_workbook()

    def _create_workbook(self):
        workbook = Workbook()
        workbook[workbook.sheetnames[0]].title = OVERVIEW_SHEET_NAME
        workbook.save(self.filename)
        return workbook

    def insert_histogram_data(self, crate: Crate, data):
        histogram_sheet = HistogramSheet(self.workbook, crate)
        histogram_sheet.insert_data(data)
        pass

    def save(self):
        self.workbook.save(self.filename)

    def __str__(self):
        return 'Spreadsheet: ' + self.filename
