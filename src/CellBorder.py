from openpyxl.styles import Border, Side


class CellBorder:
    def __init__(self, cell):
        self.cell = cell

        self._b_top = self.cell.border.top.style
        self._b_right = self.cell.border.right.style
        self._b_bottom = self.cell.border.bottom.style
        self._b_left = self.cell.border.left.style

    def _set_border(self):
        self.cell.border = Border(
            top=Side(style=self._b_top),
            right=Side(style=self._b_right),
            bottom=Side(style=self._b_bottom),
            left=Side(style=self._b_left)
        )

    def border(self, style=None):
        self._b_left = style
        self._b_right = style
        self._b_top = style
        self._b_bottom = style
        self._set_border()
        return self

    def border_left(self, style=None):
        self._b_left = style
        self._set_border()
        return self

    def border_right(self, style=None):
        self._b_right = style
        self._set_border()
        return self

    def border_top(self, style=None):
        self._b_top = style
        self._set_border()
        return self

    def border_bottom(self, style=None):
        self._b_bottom = style
        self._set_border()
        return self
