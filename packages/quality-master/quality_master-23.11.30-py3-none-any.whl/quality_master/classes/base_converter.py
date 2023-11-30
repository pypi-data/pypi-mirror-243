class BaseConverter:
    verbose_level: str = 'v'

    def __init__(self, data):
        self.data = data

    def convert(self):
        raise NotImplementedError("Method 'convert' must be implemented in child class")

    def _format_header(self, headers, max_widths):
        raise NotImplementedError("Method '_format_header' must be implemented in child class")

    def _format_row(self, row, max_widths):
        raise NotImplementedError("Method '_format_row' must be implemented in child class")

    def _format_separator(self, headers):
        raise NotImplementedError("Method '_format_separator' must be implemented in child class")

    def set_verbose_level(self, level_value):
        self.verbose_level = level_value * 'v'
        if level_value > 2:
            self.verbose_level = 'vv'
