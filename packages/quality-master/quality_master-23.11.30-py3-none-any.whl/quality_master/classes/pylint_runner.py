import io

from pylint.lint import Run
from pylint.reporters.json_reporter import JSON2Reporter


class PylintRunner:
    def __init__(self, arguments):
        self.base_pylint_arguments = ['--disable=F0010', '--disable=E0001']
        if arguments.rcfile:
            self.base_pylint_arguments.append(f'--rcfile={arguments.rcfile}')
        self.arguments = arguments

    def run(self, file_path) -> str:
        pylint_output = io.StringIO()
        Run(
            args=[file_path] + self.base_pylint_arguments,
            reporter=JSON2Reporter(pylint_output),
            exit=False,
        )
        return pylint_output.getvalue()
