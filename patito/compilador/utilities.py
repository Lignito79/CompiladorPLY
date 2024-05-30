#
# José Ángel Rentería Campos // A00832436
#

def limit_range_by_type(lower_limit, upper_limit, type):
    if type == "int":
        upper_limit -= 2000
    elif type == "float":
        lower_limit += 1000
        upper_limit -= 1000
    elif type == "bool":
        lower_limit += 2000
    return lower_limit, upper_limit

def limit_lower_limit_by_type(lower_limit, type):
    if type == "float":
        lower_limit += 1000
    elif type == "bool":
        lower_limit += 2000
    return lower_limit

def read_program_txt(test_txt):
    with open(test_txt, 'r') as file:
        code = file.read()
    return code