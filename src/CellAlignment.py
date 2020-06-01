from openpyxl.styles import Alignment


class CellAlignment:
    def __init__(self, cell):
        self.cell = cell

        self.a_horizontal = self.cell.alignment.horizontal
        self.a_vertical = self.cell.alignment.vertical

    def _set_alignment(self):
        self.cell.alignment = Alignment(
            horizontal=self.a_horizontal,
            vertical=self.a_vertical
        )

    def left(self):
        self.a_horizontal = 'left'
        self._set_alignment()
        return self

    def center(self):
        self.a_horizontal = 'center'
        self._set_alignment()
        return self

    def right(self):
        self.a_horizontal = 'right'
        self._set_alignment()
        return self

    def justify(self):
        self.a_horizontal = 'justify'
        self._set_alignment()
        return self

    def top(self):
        self.a_vertical = 'top'
        self._set_alignment()
        return self

    def middle(self):
        self.a_vertical = 'middle'
        self._set_alignment()
        return self

    def bottom(self):
        self.a_vertical = 'bottom'
        self._set_alignment()
        return self
