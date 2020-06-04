from config.colors import PATTERNS, COLORS, PATTERN_RANGE


class Color:
    @staticmethod
    def get_from_pattern(patter_name, level):
        try:
            (range_start, range_end) = PATTERN_RANGE
            if patter_name not in PATTERNS:
                raise ValueError(f"Cannot find {patter_name} in color patterns.")
            if level < range_start or range_end < level:
                raise ValueError(f"Tried to reach color pattern level {level} in range ({range_start}, {range_end})")
            return COLORS[f'{patter_name}_{str(level)}']
        except ValueError:
            return 'ffffff'

    @staticmethod
    def get_rgb_values_from_hex(code):
        lv = len(code)
        return tuple(int(code[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    @staticmethod
    def get_font_color_from_bg(bg_color):
        (r, g, b) = Color.get_rgb_values_from_hex(bg_color)
        a = 1 - (0.299 * r + 0.587 * g + 0.114 * b) / 255
        if a < 0.5:
            return '000000'
        return 'ffffff'
