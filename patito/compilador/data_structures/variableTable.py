#
# José Ángel Rentería Campos // A00832436
#

from collections import defaultdict

class VariableTable:
    def __init__(self):
        self.tables = defaultdict(dict)
        self.constants = defaultdict(dict)

    def add(self, scope, variable_name, variable_type, memory_direction):
        self.tables[scope][variable_name] = {'type': variable_type, 'memory': memory_direction}

    def add_constant(self, memory_direction, constant):
        self.constants[memory_direction] = constant

    def get(self, scope, variable_name):
        return self.tables[scope].get(variable_name, None)
    
    def get_constant(self, memory_direction):
        return self.constants[memory_direction]
    
    def print_all(self):
        for scope, variables in self.tables.items():
            print(f"Scope: {scope}")
            for variable_name, details in variables.items():
                print(f"  Variable: {variable_name}, Details: {details}")

    def print_constants(self):
        for constant in self.constants.items():
            print(f"Constant: {constant}")