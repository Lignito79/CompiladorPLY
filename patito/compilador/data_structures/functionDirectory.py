#
# José Ángel Rentería Campos // A00832436
#

from collections import defaultdict

class FunctionDirectory:
    def __init__(self):
        self.directory = defaultdict(lambda: {'params': []})

    def add_function(self, function_name, params):
        self.directory[function_name]['params'] = params

    def get_function_info(self, function_name):
        return self.directory[function_name]

function_directory = FunctionDirectory()