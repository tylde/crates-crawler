from openpyxl.styles import Font


class CellFont:
    def __init__(self, cell):
        self.cell = cell

        self._font_family = self.cell.font.name
        self._font_color = self.cell.font.color
        self._font_size = self.cell.font.size
        self._bold = self.cell.font.bold
        self._italic = self.cell.font.italic
        self._underline = self.cell.font.underline
        self._strike = self.cell.font.strike

    def _set_font(self):
        self.cell.font = Font(
            name=self._font_family,
            color=self._font_color,
            size=self._font_size,
            bold=self._bold,
            italic=self._italic,
            underline=self._underline,
            strike=self._strike
        )

    def font_family(self, font_family='Calibri'):
        self._font_family = font_family
        self._set_font()
        return self

    def font_color(self, font_color=True):
        self._font_color = font_color
        self._set_font()
        return self

    def font_size(self, font_size=11):
        self._font_size = font_size
        self._set_font()
        return self

    def bold(self, bold=True):
        self._bold = bold
        self._set_font()
        return self

    def italic(self, italic=True):
        self._italic = italic
        self._set_font()
        return self

    def underline(self, underline=True):
        self._underline = underline
        self._set_font()
        return self

    def strike(self, strike=True):
        self._strike = strike
        self._set_font()
        return self
