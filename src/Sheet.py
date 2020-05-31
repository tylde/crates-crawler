from openpyxl.styles import Alignment, Font, Border
from openpyxl.worksheet.dimensions import Dimension


class Sheet:
    def __init__(self, workbook, name):
        self.workbook = workbook
        self.name = name

    def _create(self):
        self.workbook.create_sheet(self.name)

    def _get_sheet_index(self):
        try:
            return self.workbook.sheetnames.index(self.name)
        except ValueError:
            self._create()
            return self.workbook.sheetnames.index(self.name)

    def _set_active(self):
        sheet_index = self._get_sheet_index()
        self.workbook.active = sheet_index

    def get(self):
        sheet_index = self._get_sheet_index()
        self.workbook.active = sheet_index
        return self.workbook.active

    def center(self, cell):
        self.get()[cell].alignment = Alignment(horizontal='center')

    def bold(self, cell):
        self.get()[cell].font = Font(bold=True)

    def value(self, cell, value):
        self.get()[cell].value = value

    def border(self, sell, border):
        pass

    def width(self, column, width):
        pass

    def _find_row_by_time(self, time):
        for row in self.get()['A']:
            if row.value == time:
                return row
        return None
