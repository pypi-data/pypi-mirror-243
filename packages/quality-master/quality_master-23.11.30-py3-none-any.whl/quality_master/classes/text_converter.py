from quality_master.classes.base_converter import BaseConverter


class TextConverter(BaseConverter):
    def _get_max_column_widths(self, table):
        """Returns a list of maximum widths for each column in the table."""
        widths = [len(header) for header in table[0]]  # start with header widths
        for row in table[1:]:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))
        return widths

    def convert(self):
        output = ''
        ended = False

        longest_file_path_length = max(len(file_path) for file_path in self.data['files'])
        all_messages = [error['message'] for file in self.data['files'].values() for error in file["errors"]]
        longest_description_length = len(max(all_messages, key=len))
        if longest_description_length > longest_file_path_length:
            longest_file_path_length = longest_description_length

        if self.verbose_level == 'v':
            output += f'┌──────┬───┬───┬───┬───┬───┬───┬{(longest_file_path_length - 13) * "─"}┐\n'
            output += f'│ Cost │ F │ E │ W │ R │ C │ I │Path to file{(longest_file_path_length - 26) * " "} │\n'

        for file in self.data['files']:
            if self.verbose_level == 'vv':
                output += ''
                output += f'┌──────┬───┬───┬───┬───┬───┬───┬{(longest_file_path_length - 13) * "─"}┐\n'
                output += f'│ Cost │ F │ E │ W │ R │ C │ I │Path to file{(longest_file_path_length - 26) * " "} │\n'

            output += f'├──────┼───┼───┼───┼───┼───┼───┼{(longest_file_path_length - 13) * "─"}┤\n'
            output += (
                f'│{self.data["files"][file]["cost"]:^6}'
                f'│{self.data["files"][file]["messageTypeCount"]["fatal"]:^3}'
                f'│{self.data["files"][file]["messageTypeCount"]["error"]:^3}'
                f'│{self.data["files"][file]["messageTypeCount"]["warning"]:^3}'
                f'│{self.data["files"][file]["messageTypeCount"]["refactor"]:^3}'
                f'│{self.data["files"][file]["messageTypeCount"]["convention"]:^3}'
                f'│{self.data["files"][file]["messageTypeCount"]["info"]:^3}'
                f'│{file:{longest_file_path_length - 13}}│\n'
            )

            if self.verbose_level == 'vv':
                output += f'├──────┼───┼───┴──┬┴───┴───┴───┴{(longest_file_path_length - 13) * "─"}┤\n'
                output += f'│ Line │Col│MSG ID│ Description{(longest_file_path_length - 13) * " "} │\n'
                output += f'├──────┼───┼──────┼{(longest_file_path_length) * "─"}┤\n'
                for index, details in enumerate(self.data['files'][file]['errors']):
                    output += (
                        f'│{self.data["files"][file]["errors"][index]["line"]:>6}'
                        f'│{self.data["files"][file]["errors"][index]["column"]:^3}'
                        f'│{self.data["files"][file]["errors"][index]["messageId"]:^6}'
                        f'│{self.data["files"][file]["errors"][index]["message"]:{longest_file_path_length}}│\n'
                    )

                output += f'└──────┴───┴──────┴───────────{(longest_file_path_length - 11) * "─"}┘\n'
                ended = True

            if not ended and self.verbose_level == 'vv':
                output += f'└──────┴───┴───┴───┴───┴───┴───┴{(longest_file_path_length - 11) * "─"}┘\n'
        if not ended and self.verbose_level == 'v':
            output += f'└──────┴───┴───┴───┴───┴───┴───┴{(longest_file_path_length - 13) * "─"}┘\n'

        return output + ''

    def _format_header(self, headers, max_widths):
        formatted_headers = [f" {header:{width}} " for header, width in zip(headers, max_widths)]
        return "|" + "|".join(formatted_headers) + "|\n"

    def _format_row(self, row, max_widths):
        formatted_row = [f" {cell:{width}} " for cell, width in zip(row, max_widths)]
        return "|" + "|".join(formatted_row) + "|\n"

    def _format_separator(self, max_widths):
        return "|" + "|".join(["-" * (width + 2) for width in max_widths]) + "|\n"
