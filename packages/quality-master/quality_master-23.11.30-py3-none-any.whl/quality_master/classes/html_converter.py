from quality_master.classes.base_converter import BaseConverter


class HTMLConverter(BaseConverter):
    def convert(self):
        output = (
            '<html>'
            '    <head>'
            '<style>'
            'body {'
            'text-align: center;'
            'font-family: Arial, sans-serif;'
            '}'
            '.centered-content {'
            'display: inline-block;'
            'text-align: left;'
            'margin-left: auto;'
            'margin-right: auto;'
            '}'
            '</style>'
            '</head>'
            '<body>'
            '<div class="centered-content">'
            '<p><b>Quality-Master Report</b></p>'
        )

        if self.verbose_level == 'v':
            output += (
                '<table border="1" width="1200px" bordercolor="#999999" bgcolor="#DDDDDD"  cellspacing="0" cellpadding="3">'
                '<tr bgcolor="#AAAAAA">'
                '<th>Cost</th>'
                '<th>F</th>'
                '<th>E</th>'
                '<th>W</th>'
                '<th>R</th>'
                '<th>C</th>'
                '<th>I</th>'
                '<th>Path to file</th>'
                '</tr>'
            )

        for file in self.data['files']:
            if self.verbose_level == 'vv':
                output += (
                    '<table border="1" width="1200px" bordercolor="#999999" bgcolor="#DDDDDD"  cellspacing="0" cellpadding="3">'
                    '<tr bgcolor="#AAAAAA">'
                    '<th width="50px">Cost</th>'
                    '<th width="50px">F</th>'
                    '<th width="50px">E</th>'
                    '<th width="50px">W</th>'
                    '<th width="50px">R</th>'
                    '<th width="50px">C</th>'
                    '<th width="50px">I</th>'
                    '<th align="left">Path to file</th>'
                    '</tr>'
                )
            output += (
                '<tr>'
                f'<td align="center">{self.data["files"][file]["cost"]}</td>'
                f'<td align="center">{self.data["files"][file]["messageTypeCount"]["fatal"]}</td>'
                f'<td align="center">{self.data["files"][file]["messageTypeCount"]["error"]}</td>'
                f'<td align="center">{self.data["files"][file]["messageTypeCount"]["warning"]}</td>'
                f'<td align="center">{self.data["files"][file]["messageTypeCount"]["refactor"]}</td>'
                f'<td align="center">{self.data["files"][file]["messageTypeCount"]["convention"]}</td>'
                f'<td align="center">{self.data["files"][file]["messageTypeCount"]["info"]}</td>'
                f'<td>{file}</td>'
                f'</tr>'
            )

            if self.verbose_level == 'vv':
                output += (
                    '<tr bgcolor="#AAAAAA"><td colspan="8">'
                    '<table border="1" width="100%" bordercolor="#999999" bgcolor="#EEEEEE" cellspacing="0" cellpadding="3">'
                    '<tr bgcolor="#CCCCCC">'
                    '<th width="50px">Line</th>'
                    '<th width="50px">Col</th>'
                    '<th width="60px">MSG ID</th>'
                    '<th>Description</th>'
                    '</tr>'
                )

                for index, details in enumerate(self.data['files'][file]['errors']):
                    output += (
                        '<tr>'
                        f'<td align="center">{self.data["files"][file]["errors"][index]["line"]}</td>'
                        f'<td align="center">{self.data["files"][file]["errors"][index]["column"]}</td>'
                        f'<td align="center">{self.data["files"][file]["errors"][index]["messageId"]}</td>'
                        f'<td>{self.data["files"][file]["errors"][index]["message"]}</td>'
                        f'</tr>'
                    )
                output += '</table></td></tr>'

                output += '</table><br></br>'

            #if self.verbose_level == 'v':
            #    output += '</table><br></br>'

        return output + '</div></body></html>'

    def _format_header(self, headers, max_widths):
        header_str = "<tr>"
        for header in headers:
            if header == "File":
                header_str += f'<th align="left">{header}</th>'
            else:
                header_str += f"<th>{header}</th>"
        header_str += "</tr>"
        return header_str

    def _format_row(self, row, max_widths):
        row_str = "<tr>"
        for index, cell in enumerate(row):
            if index == 3:
                row_str += f"<td>{cell}</td>"
            else:
                row_str += f'<td align="center">{cell}</td>'
        row_str += "</tr>"
        return row_str

    def _format_separator(self, headers):
        return ""
