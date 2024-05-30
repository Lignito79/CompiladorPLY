#
# José Ángel Rentería Campos // A00832436
# Analizador Léxico
#

from ply import *
from ply import lex

# Palabras reservadas:

keywords = (
    'PROGRAM',
    'END',
    'PRINT', 
    'IF',
    'ELSE',
    'DO',
    'WHILE', 
    'VAR',
    'VOID',
    'MAIN',
    'INT',
    'FLOAT'
)

# Tokens:

tokens = keywords + (
    'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LT', 'GT', 'NE',
    'COMMA', 'COLON', 'SEMICOLON', 'LPARENTH', 'RPARENTH', 'LCURLYB', 'RCURLYB', 'LSQUAREB', 'RSQUAREB',
    'INTVALUE', 'FLOATVALUE', 'STRINGVALUE', 'ID', 'NEWLINE'
)

# REGEX de tokens y palabras reservadas:

t_ignore = ' \t\r'

t_EQUALS = r'\='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'

t_LT = r'<'
t_GT = r'>'
t_NE = r'!='

t_LPARENTH = r'\('
t_RPARENTH = r'\)'
t_LCURLYB = r'\{'
t_RCURLYB = r'\}'
t_LSQUAREB = r'\['
t_RSQUAREB = r'\]'

t_COMMA = r'\,'
t_COLON = r':'
t_SEMICOLON = r';'

t_INTVALUE = r'\d+'
t_FLOATVALUE = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRINGVALUE = r'\".*?\"'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_PRINT(t):
    r'print'
    if t.value in keywords:
        t.type = t.value
    return t

def t_IF(t):
    r'if'
    if t.value in keywords:
        t.type = t.value
    return t

def t_ELSE(t):
    r'else'
    if t.value in keywords:
        t.type = t.value
    return t

def t_DO(t):
    r'do'
    if t.value in keywords:
        t.type = t.value
    return t

def t_WHILE(t):
    r'while'
    if t.value in keywords:
        t.type = t.value
    return t

def t_PROGRAM(t):
    r'program'
    if t.value in keywords:
        t.type = t.value
    return t

def t_END(t):
    r'end'
    if t.value in keywords:
        t.type = t.value
    return t

def t_MAIN(t):
    r'main'
    if t.value in keywords:
        t.type = t.value
    return t

def t_VAR(t):
    r'var'
    if t.value in keywords:
        t.type = t.value
    return t

def t_VOID(t):
    r'void'
    if t.value in keywords:
        t.type = t.value
    return t

def t_INT(t):
    r'int'
    if t.value in keywords:
        t.type = t.value
    return t

def t_FLOAT(t):
    r'float'
    if t.value in keywords:
        t.type = t.value
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    if t.value in keywords:
        t.type = t.value
    return t

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

scanner = lex.lex()