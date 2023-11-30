class FileDetailProvider:
    @staticmethod
    def get_default_file_details():
        return {
            'messageTypeCount': {
                'fatal': 0,
                'error': 0,
                'warning': 0,
                'refactor': 0,
                'convention': 0,
                'info': 0,
            },
            'errors': [],
            'cost': 0,
        }
