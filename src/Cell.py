from openpyxl.styles import PatternFill, Protection

from src.CellAlignment import CellAlignment
from src.CellBorder import CellBorder
from src.CellFont import CellFont


class Cell(CellAlignment, CellBorder, CellFont):
    def __init__(self, cell):
        CellAlignment.__init__(self, cell)
        CellBorder.__init__(self, cell)
        CellFont.__init__(self, cell)

        self.cell = cell

    @classmethod
    def get(cls, workbook, sheet_name, cell_name):
        sheet_index = workbook.sheetnames.index(sheet_name)
        cell = workbook.worksheets[sheet_index][cell_name]
        return cls(cell)

    def fill(self, color):
        self.cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
        return self

    def lock(self):
        self.cell.protection = Protection(locked=True)
        return self

    def unlock(self):
        self.cell.protection = Protection(locked=False)
        return self

    def value(self, value):
        self.cell.value = value
        return self
