import ply.yacc as yacc
import os
import codecs
import re
from sys import stdin
from analisadorLexico import tokens

# a precedencia é definida de cima para baixo
# baseado na definição da linguagem (versão 1.4)
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


# os terminais são os tokens
# os não terminais da gramatica, serão os nomes das funcões
# P quer dizer que vamos analisar as produções
def p_programa(p):
    ''' program = bloco e P são as produções
    <programa> ::= <seqDeclaração>
    primeiro nó irá se chamar programa'''
    # p[0] = programa(p[1], "programa")
    print('programa')


def p_seqDeclaracao(p):
    pass


def p_declaracao(p):
    pass


def p_tipo(p):
    pass


def p_valor(p):
    pass


def p_variavel(p):
    pass


def p_num(p):
    pass


def p_dig(p):
    pass


def p_logico(p):
    pass


def p_op(p):
    pass


def p_opAtrib(p):
    pass


def p_comando(p):
    pass


def p_expressao(p):
    pass


def p_comandoIf(p):
    pass


def p_comandoFor(p):
    pass


def p_comandoWhile(p):
    pass


def p_comandoAtrib(p):
    pass


def p_comandoReturn(p):
    pass


def p_comandoBreak(p):
    pass


def p_comandoChamadaProc(p):
    pass


def p_comandoRead(p):
    pass


def p_comandoWrite(p):
    pass


def p_bloco(p):
    pass


def p_chamadaDeFuncao(p):
    pass


def p_listaDeParametros(p):
    pass


def p_comentario(p):
    pass


def p_error(p):
    print ('Erro de sintaxe %s' % p)
    print ('Erro na linha %s' % str(p.lexer.lineno))
