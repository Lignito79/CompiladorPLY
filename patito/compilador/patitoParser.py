#
# José Ángel Rentería Campos // A00832436
# Parser
#

from ply import yacc
from patitoScanner import tokens, scanner

from data_structures.quadStack import QuadStack
from data_structures.tempArray import TempArray
from data_structures.functionDirectory import FunctionDirectory
from data_structures.variableTable import VariableTable
from data_structures.scopeStack import ScopeStack
from data_structures.jumpStack import JumpStack
from data_structures.oStack import OStack
from data_structures.operatorStack import OperatorStack
from data_structures.typeStack import TypeStack
from data_structures.assignTypeStack import AssignTypeStack
from data_structures.semanticCube import semanticCube
import re
from utilities import *


# Directorio de funciones y tabla de variables (dejamos declaradas las globales por default)
quad_stack = QuadStack()
temp_array = TempArray()
function_directory = FunctionDirectory()
variable_table = VariableTable()
assign_type_stack = AssignTypeStack()
scope_stack = ScopeStack()
o_stack = OStack()
operator_stack = OperatorStack()
jump_stack = JumpStack()
type_stack = TypeStack()


# Contadores de direcciones de memoria
# Los contadores solo tienen el numero de elementos, no la direccion en memoria
# La dirección en memoria se calcula al declarar una variable

# Del 0 al 2999
counter_GI = 100 # 100 al 999, Porque dejamos los primeros 100 libres
counter_GF = 0 # 1000 al 1999
counter_GB = 0 # 2000 al 2999

# Del 3000 al 5999
counter_TI = 0 # 3000 al 3999
counter_TF = 0 # 4000 al 4999
counter_TB = 0 # 5000 al 5999

# Del 6000 al 8999
counter_LI = 0 # 6000 al 6999
counter_LF = 0 # 7000 al 7999
counter_LB = 0 # 8000 al 8999

# Del 8000 al 9999
counter_CTEs = 0 # 8000 al 9999

# Precedencia
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'LPARENTH', 'RPARENTH')
)

def add_to_counter(lower_bound, type):
    lower_limit = limit_lower_limit_by_type(lower_bound, type)
    global counter_GI, counter_GF, counter_TI, counter_TF, counter_LI, counter_LF, counter_CTEs

    if lower_limit == 0:
        counter_GI = counter_GI + 1
        return lower_limit + counter_GI
    elif lower_limit == 1000:
        counter_GF = counter_GF + 1
        return lower_limit + counter_GF
    elif lower_limit == 2000:
        counter_TI = counter_TI + 1
        return lower_limit + counter_TI
    elif lower_limit == 3000:
        counter_TF = counter_TF + 1
        return lower_limit + counter_TF
    elif lower_limit == 4000:
        counter_LI = counter_LI + 1
        return lower_limit + counter_LI
    elif lower_limit == 5000:
        counter_LF = counter_LF + 1
        return lower_limit + counter_LF
    elif lower_limit == 6000:
        counter_CTEs = counter_CTEs + 1
        return lower_limit + counter_CTEs

def add_to_counter(lower_bound, type):
    global counter_GI, counter_GF, counter_GB
    global counter_TI, counter_TF, counter_TB
    global counter_LI, counter_LF, counter_LB
    global counter_CTEs

    lower_limit = limit_lower_limit_by_type(lower_bound, type)

    ranges = {
        range(0, 1000): 'counter_GI',
        range(1000, 2000): 'counter_GF',
        range(2000, 3000): 'counter_GB',
        range(3000, 4000): 'counter_TI',
        range(4000, 5000): 'counter_TF',
        range(5000, 6000): 'counter_TB',
        range(6000, 7000): 'counter_LI',
        range(7000, 8000): 'counter_LF',
        range(8000, 9000): 'counter_LB',
        range(8000, 10000): 'counter_CTEs'
    }

    for addr_range, counter_name in ranges.items():
        if lower_limit in addr_range:
            globals()[counter_name] += 1
            return lower_limit + globals()[counter_name]

    return None

def get_memory_direction(scope, operand):
    return variable_table.get(scope, operand)['memory']

#
#
# Reglas gramaticales. Funciona, aunque en el parser.out salen varios conflictos. Falta checar eso
#
#


# Program
def p_program(p):
    '''program : PROGRAM ID SEMICOLON global_scope checkVars cicloFuncs MAIN body END'''
    p[0] = ('PROGRAM', p[2], p[5], p[6], p[8])
    scope_stack.pop()


def p_global_scope(p):
    "global_scope :"
    scope = ["global", 0, 2999]
    scope_stack.push(scope)

def p_checkVars(p):
    '''checkVars    : vars
                    | empty'''
    if p[1]:
        p[0] = p[1]
    else:
        p[0] = None

def p_cicloFuncs(p):
    '''cicloFuncs   : funcs cicloFuncs
                    | funcs
                    | empty'''
    if len(p) > 2:
        p[0] = (p[1], p[2])
    elif len(p) == 2 and p[1]:
        p[0] = p[1]
    else:
        p[0] = None
        


# Variables
def p_vars(p):
    '''vars : VAR nombresVars'''
    p[0] = p[2]
    

def p_nombresVars(p):
    '''nombresVars  : nombresVars declVar
                    | declVar'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]

def p_declVar(p):
    '''declVar  : idsVars COLON type SEMICOLON'''
    p[0] = p[1]
    p[0].append(p[3])

    # Aquí se insertan las variables dependiendo del scope y el tipo. También se verifica si están repetidos o no,
    # pero aún no hay manejo de errores de acuerdo a eso.

    var_type = assign_type_stack.top()

    scope = scope_stack.top()
    
    for var_definition in p[0]:
        if var_definition[0] == 'VAR':
            if variable_table.get(scope_stack.top()[0], var_definition[1]) == None:
                memory_direction = add_to_counter(scope[1], var_type)
                variable_table.add(scope_stack.top()[0], var_definition[1], assign_type_stack.top(), memory_direction)
            else:
                raise RuntimeError("Error: La variable \"" + var_definition[1] + "\" ya fue declarada" )


    assign_type_stack.pop()

def p_idsVars(p):
    '''idsVars  : idsVars COMMA ID
                | ID'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(('VAR', p[3]))
    else:
        p[0] = [('VAR', p[1])]

# Funcion
def p_funcs(p):
    '''funcs : VOID ID LPARENTH groupParams add_function RPARENTH LSQUAREB new_scope checkVars body RSQUAREB SEMICOLON'''
    p[0] = ('FUNCS', p[2], p[4], p[9], p[10])
    scope_stack.pop()

def p_add_function(p):
    '''add_function :'''
    function_directory.add_function(p[-3], p[-1])

def p_new_scope(p):
    "new_scope :"
    scope = [p[-6], 6000, 8999]
    scope_stack.push(scope)

def p_groupParams(p):
    '''groupParams  : groupParams COMMA idsParams
                    | idsParams
                    | empty'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]

def p_idsParams(p):
    '''idsParams : ID COLON type'''
    p[0] = (p[1], p[3])


# Types
def p_type(p):
    '''type : INT new_type
            | FLOAT new_type'''
    p[0] = ('TYPE', p[1])

def p_new_type(p):
    '''new_type :'''
    assign_type_stack.push(p[-1])

# Body
def p_body(p):
    '''body : LCURLYB bodyStatements RCURLYB'''
    p[0] = p[2]

def p_bodyStatements(p):
    '''bodyStatements   : bodyStatements statement
                        | statement
                        | empty'''
    
    if len(p) == 2 and p[1]:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = None


# Statement
def p_statement(p):
    '''statement    : assign
                    | condition
                    | cycle
                    | fCall
                    | print'''
    p[0] = p[1]


# Assign
def p_assign(p):
    '''assign : ID EQUALS expresion SEMICOLON'''
    p[0] = ('ASSIGN', p[1], p[3])

    right_operand = o_stack.pop()
    
    left_operand = p[1]

    quad = ['=', right_operand['memory'], '', get_memory_direction(scope_stack.top()[0], left_operand)]
    quad_stack.push(quad)
    

# Condition
def p_condition(p):
    '''condition : IF LPARENTH expresion RPARENTH evaluate_condition body conditionElse end_condition SEMICOLON'''
    p[0] = ('IF', p[3], p[6], p[7])

def p_end_condition(p):
    '''end_condition :'''
    end = jump_stack.pop()
    quad_stack.fill(end, quad_stack.size())

def p_evaluate_condition(p):
    '''evaluate_condition :'''
    
    exp_type = type_stack.pop()
    
    if exp_type != 'bool':
        raise TypeError("Type mismatch")
    
    result = o_stack.pop()
    quad = ['GoToF', result['memory'], '', '']
    quad_stack.push(quad)

    jump_stack.push(quad_stack.size()-1)


def p_conditionElse(p):
    '''conditionElse    : ELSE evaluate_else body
                        | empty'''

    if len(p) == 4:
        p[0] = ('ELSE', p[3])
    else:
        p[0] = None

def p_evaluate_else(p):
    '''evaluate_else :'''
    quad = ['GoTo', '', '', '']
    quad_stack.push(quad)
    pending_jump = jump_stack.pop()
    jump_stack.push(quad_stack.size()-1)

    quad_stack.fill(pending_jump, quad_stack.size())


# Cycle
def p_cycle(p):
    '''cycle : DO startof_cycle body WHILE expresion check_expression SEMICOLON'''
    p[0] = ('DOWHILE', p[3], p[5])
    

def p_startof_cycle(p):
    '''startof_cycle :'''
    start = quad_stack.size()
    jump_stack.push(start)

def p_check_expression(p):
    '''check_expression :'''
    exp_type = type_stack.pop()
    if exp_type != 'bool':
        raise TypeError("Type-mismatch")
    else:
        result = o_stack.pop()
        quad = ['GoToT', result['memory'], '', jump_stack.pop()]
        quad_stack.push(quad)

# Function Call
def p_fCall(p):
    '''fCall : ID LPARENTH expresionFCall RPARENTH SEMICOLON'''
    p[0] = (p[1], p[3])

def p_expresionFCall(p):
    '''expresionFCall   : expresionFCall COMMA expresion
                        | expresion
                        | empty'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    elif len(p) == 2 and p[1]:
        p[0] = [p[1]]
    else:
        p[0] = None

# Print
def p_print(p):
    '''print : PRINT LPARENTH printExpresion RPARENTH print_new_line SEMICOLON'''
    p[0] = ('PRINT', p[3])

def p_print_new_line(p):
    '''print_new_line :'''
    quad = ['print', '', '', '99']
    quad_stack.push(quad)

def p_printExpresion(p):
    '''printExpresion   : printExpresion COMMA expresOrString
                        | expresOrString'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]

def p_expresOrString(p):
    '''expresOrString   : expresion
                        | STRINGVALUE'''
    p[0] = p[1]

    if isinstance(p[1], tuple):
        right_operand = o_stack.pop()
        right_type = type_stack.pop()

        quad = ['print', '', '', right_operand['memory']]
        quad_stack.push(quad)
        
    else:
        constant_memory_direction = add_to_counter(8000, p[1])
        variable_table.add_constant(constant_memory_direction, p[1])
        f.write(str(constant_memory_direction) + " " + str(p[1]) + "\n")

        quad = ['print', '', '', constant_memory_direction]
        quad_stack.push(quad)


# Exp
def p_exp(p):
    '''exp : termino solve_exp cicloExp'''
    p[0] = (p[1], p[3])


def p_solve_exp(p):
    '''solve_exp :'''
    if not operator_stack.is_empty() and not o_stack.is_empty():
        if operator_stack.top() == '+' or operator_stack.top() == '-':
            solve_operation()


def p_cicloExp(p):
    '''cicloExp : operadoresExp exp
                | empty'''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = None

def p_operadoresExp(p):
    '''operadoresExp    : PLUS
                        | MINUS'''
    p[0] = p[1]
    
    operator_stack.push(p[0])
    

# Expresion
def p_expresion(p):
    '''expresion : exp comparacion solve_comparacion'''
    p[0] = (p[1], p[2])
    

def p_solve_comparacion(p):
    '''solve_comparacion :'''
    if not operator_stack.is_empty() and not o_stack.is_empty():
        if operator_stack.top() == '>' or operator_stack.top() == '<' or operator_stack.top() == '!=':
            solve_operation()

def p_comparacion(p):
    '''comparacion  : operadoresComp exp
                    | empty'''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = None
        

def p_operadoresComp(p):
    '''operadoresComp   : GT
                        | LT
                        | NE'''
    p[0] = p[1]

    operator_stack.push(p[0])
    


# Termino
def p_termino(p):
    '''termino : factor solve_term cicloTerm'''
    p[0] = (p[1], p[3])
    

def p_solve_term(p):
    '''solve_term :'''
    if not operator_stack.is_empty() and not o_stack.is_empty():
        if operator_stack.top() == '*' or operator_stack.top() == '/':
            solve_operation()

def solve_operation():
    right_operand = o_stack.pop()
    right_type = type_stack.pop()

    left_operand = o_stack.pop()
    left_type = type_stack.pop()

    operator = operator_stack.pop()


    result_type = semanticCube[left_type][right_type][operator]
   
    if result_type != 'ERROR':
        
        result = temp_array.next()

        scope = scope_stack.top()

        temporal_memory_direction = add_to_counter(3000, result_type)

        quad = [operator, left_operand['memory'], right_operand['memory'], temporal_memory_direction]
        quad_stack.push(quad)

        o_stack.push({'name': result, 'temporary': True, 'constant': False, 'memory': temporal_memory_direction})
        type_stack.push(result_type)
        
        if left_operand['temporary']:
            temp_array.return_temporary(left_operand['name'])
        if right_operand['temporary']:
            temp_array.return_temporary(right_operand['name'])
    else:
        raise TypeError("Type mismatch")

def p_cicloTerm(p):
    '''cicloTerm    : operadoresTerm termino
                    | empty'''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = None
        

def p_operadoresTerm(p):
    '''operadoresTerm   : TIMES
                        | DIVIDE'''
    p[0] = p[1]

    operator_stack.push(p[0])
    

# Factor
def p_factor(p):
    '''factor   : factorExp
                | factorIdCte'''
    p[0] = p[1]
    

def p_factorExp(p):
    '''factorExp : LPARENTH expresion RPARENTH'''
    p[0] = p[2]
    

def p_factorIdCte(p):
    '''factorIdCte : factorOperadores idOrCte'''    
    p[0] = (p[1], p[2])

    if isinstance(p[0][1], tuple):
        constant_memory_direction = add_to_counter(8000, p[0][1][1])
        variable_table.add_constant(constant_memory_direction,  p[0][1][1])
        f.write(str(constant_memory_direction) + " " + str( p[0][1][1]) + "\n")
        o_stack.push({'name': constant_memory_direction, 'temporary': False, 'constant': True, 'memory': constant_memory_direction})

        type_stack.push(p[0][1][0])
    else:
        aux_type = variable_table.get(scope_stack.top()[0], p[0][1])['type']
        aux_memory = variable_table.get(scope_stack.top()[0], p[0][1])['memory']
        if aux_type == 'int' or aux_type == 'float':
            p[2] = (aux_type, p[0][1])
            o_stack.push({'name': p[0][1], 'temporary': False, 'constant': False, 'memory': aux_memory})
            type_stack.push(aux_type)
            p[0] = (p[1], p[2])
        else:
            raise TypeError("Variable was not declared in this scope")
        


def p_factorOperadores(p):
    '''factorOperadores : operadoresExp
                        | empty'''
    p[0] = p[1]
    

def p_idOrCte(p):
    '''idOrCte  : ID
                | cte'''
    p[0] = p[1]

def p_cte(p):
    '''cte  : INTVALUE
            | FLOATVALUE'''
    
    if re.match(r'\d+', p[1]) :
        p[0] = ('int', eval(p[1]))
    else:
        p[0] = ('float', eval(p[1]))

    #print("cte")


# Empty
def p_empty(p):
    '''empty : '''


# Catastrophic error handler
def p_error(p):
    if p:
        raise RuntimeError("Syntax error at line", p.lineno-1)
    else:
        raise RuntimeError("Syntax error at EOF")
        

patitoParser = yacc.yacc()

print('''
1-. Programa simple sin errores
2-. Programa con if y else sin errores
3-. Programa con Do While sin errores (FIBONACCI)
4-. Programa con Do While sin errores (FACTORIAL)
5-. Error de sintaxis: Punto y coma faltante
6-. Error de sintaxis: Llave de cierre faltante
7-. Error de sintaxis: Palabra de final de archivo faltante (end)
8-. Error de sintaxis: Palabra clave mal escrita
''')
opcion_prueba = input("Elija un número del 1 al 10 para seleccionar una prueba: ")

# Dependiendo del numero elegido, se usa la correspondiente función
if opcion_prueba == "1":
    data = read_program_txt('prueba1.txt')

elif opcion_prueba == "2":
    data = read_program_txt('prueba2.txt')

elif opcion_prueba == "3":
    data = read_program_txt('prueba3.txt')

elif opcion_prueba == "4":
    data = read_program_txt('prueba4.txt')

elif opcion_prueba == "5":
    data = read_program_txt('prueba5.txt')

elif opcion_prueba == "6":
    data = read_program_txt('prueba6.txt')

elif opcion_prueba == "7":
    data = read_program_txt('prueba7.txt')

elif opcion_prueba == "8":
    data = read_program_txt('prueba8.txt')

else:
    raise Exception('Numero de prueba invalido')


open('obj.txt', 'w').close()
f = open("obj.txt", "a")
f.write("%%\n")

def parse(data, debug=0):
    patitoParser.error = 0
    p = patitoParser.parse(data, debug=debug)
    if patitoParser.error:
        return None
    return p

parse(data)

f.write("%%\n")
f.close()
quad_stack.writeOBJ()