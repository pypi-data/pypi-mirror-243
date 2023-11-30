import argparse
import os
from glob import glob

from quality_master.classes.code_quality_calculator import CodeQualityCalculator
from quality_master.classes.code_quality_reporter import CodeQualityReporter
from quality_master.classes.pylint_runner import PylintRunner


class CodeQualityAnalyzer:
    def __init__(self, arguments: argparse.Namespace, pylint_runner: PylintRunner,
                 code_quality_calculator: CodeQualityCalculator, code_quality_reporter: CodeQualityReporter):
        self.arguments = arguments
        self.pylint_runner = pylint_runner
        self.code_quality_calculator = code_quality_calculator
        self.code_quality_reporter = code_quality_reporter

    def run(self):
        pylint_output = [self.run_pylint(file_path) for file_path in self.get_python_files()]
        file_details = self.code_quality_calculator.calculate_code_quality(pylint_output)
        master_cost = self.get_master_cost()
        self.code_quality_reporter.report(master_cost, file_details['fullCost'], self.arguments, file_details)
        self.save_master_cost(file_details['fullCost'])

        # try:
        #
        #     pylint_output = [self.run_pylint(file_path) for file_path in self.get_python_files()]
        #     file_details = self.code_quality_calculator.calculate_code_quality(pylint_output)
        #     master_cost = self.get_master_cost()
        #     self.code_quality_reporter.report(master_cost, file_details['fullCost'], self.arguments, file_details)
        #     self.save_master_cost(file_details['fullCost'])
        #
        # # ToDo: Change Exception to type of Exception
        # except Exception as e:
        #
        #     # ToDo: Add logging.error(message)
        #     print(f"Wystąpił błąd podczas analizy: {e}")


    def run_pylint(self, file_path) -> str:
        return self.pylint_runner.run(file_path)

    def get_python_files(self):
        glob_pattern = os.path.join(self.arguments.dir_path, "**", "*.py")
        python_files = glob(glob_pattern, recursive=True)
        if self.arguments.ignore:
            self.pylint_runner.base_pylint_arguments.extend(["--ignore={0}".format(*self.arguments.ignore)])
            python_files = [path for path in python_files if
                            all(ignore_item not in path for ignore_item in self.arguments.ignore)]
        return python_files

    def get_master_cost(self):
        cost_file_path = os.path.join(self.arguments.dir_path, '.pylint_cost')
        master_cost = 0
        if os.path.exists(cost_file_path):
            with open(cost_file_path, 'r') as cost_file:
                master_cost = int(cost_file.read())
        return master_cost

    def save_master_cost(self, cost: int):
        cost_file_path = os.path.join(self.arguments.dir_path, '.pylint_cost')
        with open(cost_file_path, 'w') as cost_file:
            cost_file.write(str(cost))
