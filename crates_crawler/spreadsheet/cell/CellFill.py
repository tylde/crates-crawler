from openpyxl.styles import PatternFill

from crates_crawler.spreadsheet.cell.CellFont import CellFont
from crates_crawler.utils.Color import Color


class CellFill(CellFont):
    def __init__(self, cell):
        CellFont.__init__(self, cell)
        self.cell = cell

        self._start_color = self.cell.fill.start_color
        self._end_color = self.cell.fill.end_color

    def _set_fill(self):
        self.cell.fill = PatternFill(
            start_color=self._start_color,
            end_color=self._end_color,
            fill_type="solid"
        )

    def fill(self, color):
        self._start_color = color
        self._end_color = color
        self._set_fill()
        font_color = Color.get_font_color_from_bg(color)
        self.font_color(font_color)
        return self

    def fill_by_pattern(self, pattern_name, level):
        color = Color.get_from_pattern(pattern_name, level)
        self._start_color = color
        self._end_color = color
        self._set_fill()
        font_color = Color.get_font_color_from_bg(color)
        self.font_color(font_color)
        return self
