#
# José Ángel Rentería Campos // A00832436
# Virtual Machine
#

from collections import defaultdict
import re

class VirtualMachine:
    def __init__(self):
        self.memory = defaultdict(int)

    def print_memory(self):
        print("Memory State:")
        for address, value in self.memory.items():
            print(f"Address {address}: {value}")
        print("Instructions:")

    def load_file_lines(self):
        with open('obj.txt', 'r') as file:
            self.memory[99] = "\n"
            lines = file.readlines()
            
            in_memory_section = False
            current_line_index = 0
            start_index_instructions = 0
            
            while current_line_index < len(lines):
                line = lines[current_line_index].strip()
                
                if line == '%%':
                    in_memory_section = not in_memory_section
                    current_line_index += 1
                    if in_memory_section == False:
                        start_index_instructions = current_line_index
                    continue
                
                if in_memory_section:
                    constant = line.split(maxsplit=1)
                    if len(constant) == 2:
                        memory_address = int(constant[0])
                        value = constant[1]
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1] 
                        else:
                            try:
                                value = int(value)
                            except ValueError:
                                pass
                        self.memory[memory_address] = value
                
                else:
                    instruction = line.split()
                    if instruction[0] == '+':
                        left_operand = self.memory[int(instruction[1])]
                        right_operand = self.memory[int(instruction[2])]
                        self.memory[int(instruction[3])] = left_operand + right_operand
                    elif instruction[0] == '-':
                        left_operand = self.memory[int(instruction[1])]
                        right_operand = self.memory[int(instruction[2])]
                        self.memory[int(instruction[3])] = left_operand - right_operand
                    elif instruction[0] == '*':
                        left_operand = self.memory[int(instruction[1])]
                        right_operand = self.memory[int(instruction[2])]
                        self.memory[int(instruction[3])] = left_operand * right_operand
                    elif instruction[0] == '/':
                        left_operand = self.memory[int(instruction[1])]
                        right_operand = self.memory[int(instruction[2])]
                        self.memory[int(instruction[3])] = left_operand / right_operand
                    elif instruction[0] == '>':
                        left_operand = self.memory[int(instruction[1])]
                        right_operand = self.memory[int(instruction[2])]
                        self.memory[int(instruction[3])] = left_operand > right_operand
                    elif instruction[0] == '<':
                        left_operand = self.memory[int(instruction[1])]
                        right_operand = self.memory[int(instruction[2])]
                        self.memory[int(instruction[3])] = left_operand < right_operand
                    elif instruction[0] == '!=':
                        left_operand = self.memory[int(instruction[1])]
                        right_operand = self.memory[int(instruction[2])]
                        self.memory[int(instruction[3])] = left_operand != right_operand
                    elif instruction[0] == '=':
                        self.memory[int(instruction[2])] = self.memory[int(instruction[1])]
                    elif instruction[0] == 'print':
                        print(self.memory[int(instruction[1])], end = '')
                    elif instruction[0] == 'GoTo':
                        if len(instruction) == 2:
                            target_line = int(instruction[1])
                            current_line_index = start_index_instructions + target_line
                            continue
                    elif instruction[0] == 'GoToF':
                        if len(instruction) == 3:
                            target_line = int(instruction[2])
                            if self.memory[int(instruction[1])] == False:
                                current_line_index = start_index_instructions + target_line
                                continue
                    elif instruction[0] == 'GoToT':
                        if len(instruction) == 3:
                            target_line = int(instruction[2])
                            if self.memory[int(instruction[1])] == True:
                                current_line_index = start_index_instructions + target_line
                                continue
                
                current_line_index += 1

# YA JALÓ LA MEMORIA Y ESTRUCTURA DE CUADRUPLOS
# AHORA SOLO TENGO QUE LEER LAS INSTRUCCIONES, EJECUTARLAS Y GUARDARLAS EN MEMORIA (O HACER PRINT)
vm = VirtualMachine()

vm.load_file_lines()