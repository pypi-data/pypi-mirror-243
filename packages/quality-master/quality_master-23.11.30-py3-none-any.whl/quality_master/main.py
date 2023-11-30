import argparse
import os

from quality_master.classes.code_quality_analyzer import CodeQualityAnalyzer
from quality_master.classes.code_quality_calculator import CodeQualityCalculator
from quality_master.classes.code_quality_reporter import CodeQualityReporter
from quality_master.classes.pylint_error_classification import PylintErrorClassification
from quality_master.classes.pylint_runner import PylintRunner


def parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(description='Quality-Master')

    argument_parser.add_argument('dir_path', metavar='CWD', nargs='?', default=os.getcwd(),
                                 help='Use path (default: current path)')
    argument_parser.add_argument('-v', '--verbose', action='count', default=1,
                                 help='Increase verbosity level: -v for normal, -vv for debug')
    # argument_parser.add_argument('--output-format', choices=['table', 'html', 'txt'], default='table',
    #                              help='Output format for pylint results: table (default), html, txt')
    argument_parser.add_argument('--output-format', choices=['table', 'html'], default='table',
                                 help='Output format for pylint results: table (default), html')
    argument_parser.add_argument('--output-file',
                                 help='Path to output file. If not specified, output will be printed to terminal')
    argument_parser.add_argument('--error-file', dest='error_file',
                                 help='Path to JSON file with custom error values')
    argument_parser.add_argument('--ignore', action='append', default=[],
                                 help='Excluded module names/dirs, comma separated ')
    argument_parser.add_argument('--rcfile', dest='rcfile',
                                 help='Path to pylint config file (default: )')
    # argument_parser.add_argument('--nofail', dest='nofail', action='store_true',
    #                              help='Do not fail on quality decrease (default: fail)')
    # argument_parser.add_argument('--clean', dest='clean', action='store_true',
    #                              help='Perform clean analyze (do NOT consider previous results)')
    # argument_parser.add_argument('--init',  dest='init', action='store_true',
    #                              help='Init checking on master branch and exit with exit code 0')
    return argument_parser


def main():
    arguments = parser().parse_args()
    pylint_runner = PylintRunner(arguments)
    error_file_path = arguments.error_file
    error_classification = (
        PylintErrorClassification(error_file_path) if error_file_path else PylintErrorClassification()
    )
    code_quality_calculator = CodeQualityCalculator(error_classification, arguments)
    code_quality_reporter = CodeQualityReporter()
    analyzer = CodeQualityAnalyzer(arguments, pylint_runner, code_quality_calculator, code_quality_reporter)
    analyzer.run()


if __name__ == '__main__':
    main()
