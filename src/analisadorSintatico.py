import ply.yacc as yacc
import os
import codecs
import re
from sys import stdin
from analisadorLexico import tokens

# a precedencia é definida de cima para baixo
# baseado na definição da linguagem (versão 1.2)
precedencia_tokens = (
    ('right', 'ASSIGN'),
    ('right', 'TERNARY'),
    ('right', 'NOT'),
    ('left', 'MULT', 'DIVIDE', 'MULTASSING', 'DIVIDEASSING'),
    ('left', 'MODASSING'),
    ('left', 'PLUS', 'MINUS', 'PLUSASSING', 'MINUSASSING'),
    ('left', 'LT', 'LTE'),
    ('left', 'GT', 'GTE'),
    ('left', 'EQUALS', 'DIFFERENT'),
    ('left', 'AND'),
    ('left', 'OR'),
    ('left', 'LCOR', 'RCOR'),
    ('left', 'LPAREN', 'RPAREN'),
    ('left', 'LKEY', 'RKEY'),
)


# P quer dizer que vamos analisar as produções
def p_program(p):
    ''' program = bloco e P são as produções '''
    # p[0] = program(p[1], "programa")
    pass
