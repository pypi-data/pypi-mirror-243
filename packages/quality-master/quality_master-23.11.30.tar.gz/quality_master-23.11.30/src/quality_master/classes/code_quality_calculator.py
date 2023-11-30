import argparse
import json
from collections import defaultdict
from typing import List

from quality_master.classes.file_detail_provider import FileDetailProvider
from quality_master.classes.pylint_error_classification import ErrorClassification


class CodeQualityCalculator:
    def __init__(self, error_classification: ErrorClassification, arguments: argparse.Namespace):
        self.error_classification = error_classification
        self.arguments = arguments
    #
    # def print_results(self, file_details, output_format, output_file=None):
    #     verbose_level = self.arguments.verbose
    #     max_path_length = max(len("File"), max(len(file_path) for file_path in file_details['files'].keys()))
    #
    #     if verbose_level == 1:
    #         headers = ["File".ljust(max_path_length), "Cost".rjust(6)]
    #     else:
    #         headers = ["File".ljust(max_path_length), "F", "E", "W", "R", "C", "I", "Cost".rjust(6)]
    #
    #     main_header_line = '| ' + ' | '.join(headers) + ' |\n'
    #     main_splitter_line = '|-' + '-|-'.join(['-' * len(header) for header in headers]) + '-|\n'
    #
    #     main_header = main_header_line + main_splitter_line
    #
    #     table_data = ''
    #     for file_path, details in file_details['files'].items():
    #         if verbose_level == 1:
    #             row = [
    #                 file_path.ljust(max_path_length),
    #                 str(details['cost']).rjust(6)
    #             ]
    #             table_data += '| ' + ' | '.join(row) + ' |\n'
    #         elif verbose_level == 2:
    #             row = [
    #                 file_path.ljust(max_path_length),
    #                 str(details['messageTypeCount']['fatal']).rjust(2),
    #                 str(details['messageTypeCount']['error']).rjust(2),
    #                 str(details['messageTypeCount']['warning']).rjust(2),
    #                 str(details['messageTypeCount']['refactor']).rjust(2),
    #                 str(details['messageTypeCount']['convention']).rjust(2),
    #                 str(details['messageTypeCount']['info']).rjust(2),
    #                 str(details['cost']).rjust(6)
    #             ]
    #             table_data += '| ' + ' | '.join(row) + ' |\n'
    #         elif verbose_level >= 3:
    #             row = [
    #                 file_path.ljust(max_path_length),
    #                 str(details['messageTypeCount']['fatal']).rjust(2),
    #                 str(details['messageTypeCount']['error']).rjust(2),
    #                 str(details['messageTypeCount']['warning']).rjust(2),
    #                 str(details['messageTypeCount']['refactor']).rjust(2),
    #                 str(details['messageTypeCount']['convention']).rjust(2),
    #                 str(details['messageTypeCount']['info']).rjust(2),
    #                 str(details['cost']).rjust(6)
    #             ]
    #             table_data += '| ' + ' | '.join(row) + ' |\n'
    #             error_headers = ["Line".rjust(5), "Col".rjust(3), "Error ID".ljust(8), "Description".ljust(100)]
    #             table_data += '| ' + ' | '.join(error_headers) + ' |\n'
    #             table_data += '|-' + '-|-'.join(['-' * len(header) for header in error_headers]) + '-|\n'
    #             for error in details['errors']:
    #                 error_row = [
    #                     str(error['line']).rjust(5),
    #                     str(error['column']).rjust(3),
    #                     error.get('messageId', 'Unknown').ljust(8),
    #                     error.get('message', 'Unknown').ljust(100)
    #                 ]
    #                 table_data += '| ' + ' | '.join(error_row) + ' |\n'
    #     table_data = main_header + table_data
    #
    #     if output_file:
    #         with open(output_file, 'w') as file:
    #             file.write(table_data)
    #     else:
    #         print(table_data)

    def calculate_code_quality(self, pylint_output: List[str]):
        error_classification = self.error_classification.get_error_classification()
        file_details = {
            'fullCost': 0,
            'files': defaultdict(FileDetailProvider.get_default_file_details),
        }

        for file_info in pylint_output:
            json_file_info = json.loads(file_info)
            try:
                path = json_file_info['messages'][0]['path']
            except IndexError:
                continue

            for message in json_file_info['messages']:
                file_details['files'][path]['errors'].append(message)

            for key, value in json_file_info['statistics']['messageTypeCount'].items():
                file_details['files'][path]['messageTypeCount'][key] = value
                file_details['files'][path]['cost'] += error_classification.get(key, 0) * value
            file_details['fullCost'] += file_details['files'][path]['cost']
        # ToDo: Refactor self.print_results
        # self.print_results(file_details, self.arguments.output_format, self.arguments.output_file)
        return file_details

