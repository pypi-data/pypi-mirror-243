from html.parser import HTMLParser


class HTMLFormatter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.indent_level = 0
        self.formatted_html = ""

    def handle_starttag(self, tag, attrs):
        self.formatted_html += '    ' * self.indent_level + '<' + tag
        for attr in attrs:
            self.formatted_html += f' {attr[0]}="{attr[1]}"'
        self.formatted_html += '>\n'
        self.indent_level += 1

    def handle_endtag(self, tag):
        self.indent_level -= 1
        self.formatted_html += '    ' * self.indent_level + f'</{tag}>\n'

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.formatted_html += '    ' * self.indent_level + f'{text}\n'

    def format(self, html_content):
        self.feed(html_content)
        html_source = self.formatted_html.replace('<br>', '')
        result = '\n'.join([line for line in html_source.splitlines() if line.strip() != ''])
        return result
