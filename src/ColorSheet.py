from utils.Color import Color
from src.Sheet import Sheet
from config.colors import PATTERNS, PATTERN_RANGE


class ColorSheet(Sheet):
    def __init__(self, workbook, sheet_name):
        super().__init__(workbook, sheet_name)

    def fill_colors(self):
        for p in range(len(PATTERNS)):
            pattern_name = PATTERNS[p]
            (start, end) = PATTERN_RANGE

            self.cell_by_index(1, p + 1).border_bottom('thin').set_value(pattern_name).bold().center()

            for level in range(start, end + 1):
                fill_color = Color.get_from_pattern(pattern_name, level)
                font_color = Color.get_font_color_from_bg(fill_color)
                self.cell_by_index(level + 2, p + 1).fill(fill_color).font_color(font_color).set_value(level).center()
