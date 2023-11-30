from abc import ABC, abstractmethod
import json


class ErrorClassification(ABC):
    @abstractmethod
    def get_error_classification(self):
        pass


class PylintErrorClassification(ErrorClassification):
    fatal: int = 6
    error: int = 5
    warning: int = 4
    refactor: int = 3
    convention: int = 2
    info: int = 1
    file_path: str = ''

    def __init__(self, file_path: str = None):
        if file_path:
            self.file_path = file_path
            self.load_from_file(file_path)

    def load_from_file(self, file_path: str):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for key, value in data.items():
                setattr(self, key, value)

    def get_error_classification(self):
        items = self.__class__.__dict__.items()
        if self.file_path:
            items = self.__dict__.items()

        return {
            key: value for key, value in items if
            not key.startswith("__") and isinstance(value, int)
        }
