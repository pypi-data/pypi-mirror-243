import argparse

from quality_master.classes.html_converter import HTMLConverter
from quality_master.classes.html_formatter import HTMLFormatter
from quality_master.classes.text_converter import TextConverter


class CodeQualityReporter:
    def report(self, master_cost: int, current_cost: int, arguments: argparse.Namespace, file_details):
        # if arguments.verbose:
        if arguments.output_format == 'html':
            html_converter = HTMLConverter(file_details)
            html_converter.set_verbose_level(arguments.verbose)
            html_output = html_converter.convert()
            print(html_output)
            formatter = HTMLFormatter()
            formatted_html = formatter.format(html_output)
            print(20 * '\n')
            print(formatted_html)
            if arguments.output_file:
                with open(arguments.output_file, 'w') as file:
                    file.write(formatted_html)
            else:
                print(formatted_html)
        elif arguments.output_format == 'txt':
            print('Not implemented')
        else:  # default is txt
            text_converter = TextConverter(file_details)
            text_converter.set_verbose_level(arguments.verbose)
            text_output = text_converter.convert()

            if arguments.output_file:
                with open(arguments.output_file, 'w') as file:
                    file.write(text_output)
            else:
                print(text_output)

        if current_cost > master_cost:
            status = '[-] Your change degrades the quality of the code.'
        elif current_cost == master_cost:
            status = '[=] Your change does not affect the quality of the code.'
        else:
            status = '[+] Your change improves the quality of the code.'

        print(f'Master cost: {master_cost}')
        print(f'Current cost: {current_cost}')
        print(f'Status: {status}')
