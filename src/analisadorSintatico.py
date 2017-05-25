# coding: utf-8
import ply.yacc as yacc
import ply.lex as lex
import os
import codecs
import re
import datetime
from utils import Utils
from sys import stdin
from analisadorLexico import tokens

# a precedencia é definida de cima para baixo
# baseado na definição da linguagem (versão 1.4)
# os conflitos são resolvidos pela regra shift/reduce
precedence_tokens = (
    ('right', '?'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'DIFFERENT'),
    ('left', 'GTE', 'LTE', 'GT', 'LT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIVIDE', 'MOD'),
    ('right', 'NOT', 'UMINUS')
)


def p_program(p):
    '''
    program : decSeq
    '''
    p[0] = ('Program', p[1])


def p_dec(p):
    '''
    dec : varDec
        | ID LPAREN paramList RPAREN LKEY block RKEY
        | type ID LPAREN paramList RPAREN LKEY block RKEY
    '''
    if len(p) == 2:
        p[0] = ('dec', p[1])
    elif len(p) == 8:
        p[0] = ('dec', p[3], p[6])
    elif len(p) == 9:
        p[0] = ('dec', p[1], p[4], p[7])


def p_varDec(p):
    '''
    varDec : type varSpecSeq SEMICOLON
    '''
    p[0] = ('varDec', p[1], p[2])


def p_varSpec(p):
    '''
    varSpec : ID
            | ID ASSIGN literal
            | ID LCOR NUMBER RCOR
            | ID LCOR NUMBER RCOR ASSIGN LKEY literalSeq RKEY
    '''
    if len(p) == 2:
        p[0] = ('varSpec', p[1])
    elif len(p) == 4:
        p[0] = ('varSpec', p[1], p[3])
    elif len(p) == 5:
        p[0] = ('varSpec', p[1], p[3])
    elif len(p) == 9:
        p[0] = ('varSpec', p[1], p[7])


def p_type(p):
    '''
    type : INT
         | STRING
         | BOOLEAN
    '''
    p[0] = ('type', p[1])


def p_param(p):
    '''
    param : type ID
          | type ID RCOR LCOR
    '''
    if len(p) == 3:
        p[0] = ('param', p[1])
    elif len(p) == 5:
        p[0] = ('param', p[1])


def p_block(p):
    '''
    block : varDecList stmtList
    '''
    p[0] = ('block', p[1], p[2])


def p_stmt(p):
    '''
    stmt : ifStmt
         | whileStmt
         | forStmt
         | breakStmt
         | returnStmt
         | readStmt
         | writeStmt
         | assign SEMICOLON
         | subCall SEMICOLON
    '''
    if len(p) == 2:
        p[0] = ('stmt', p[1])
    elif len(p) == 3:
        p[0] = ('stmt', p[1])


def p_ifStmt(p):
    '''
    ifStmt : IF LPAREN exp RPAREN LKEY block RKEY
           | IF LPAREN exp RPAREN LKEY block RKEY ELSE LKEY block RKEY
    '''
    if len(p) == 8:
        p[0] = ('ifStmt', p[3], p[6])
    elif len(p) == 12:
        p[0] == ('ifStmt', p[3], p[6], p[10])


def p_whileStmt(p):
    '''
    whileStmt : WHILE LPAREN exp RPAREN LKEY block RKEY
    '''
    p[0] = ('whileStmt', p[3], p[6])


def p_forStmt(p):
    '''
    forStmt : FOR LPAREN assign SEMICOLON exp SEMICOLON assign RPAREN LKEY block RKEY
    '''
    p[0] = ('forStmt', p[3], p[5], p[7], p[10])


def p_breakStmt(p):
    '''
    breakStmt : BREAK SEMICOLON
    '''
    p[0] = ('breakStmt', p[1])


def p_readStmt(p):
    '''
    readStmt : READ var SEMICOLON
    '''
    p[0] = ('readStmt', p[2])


def p_writeStmt(p):
    '''
    writeStmt : WRITE expList SEMICOLON
    '''
    p[0] = ('writeStmt', p[2])


def p_returnStmt(p):
    '''
    returnStmt : RETURN SEMICOLON
               | RETURN exp SEMICOLON
    '''
    if len(p) == 3:
        p[0] = ('returnStmt', p[1])
    elif len(p) == 4:
        p[0] = ('returnStmt', p[1], p[2])


def p_subCall(p):
    '''
    subCall : ID LPAREN expList RPAREN
    '''
    p[0] = ('subCall', p[1], p[3])


def p_assign(p):
    '''
    assign : var ASSIGN exp
           | var PLUSASSIGN exp
           | var MINUSASSIGN exp
           | var MULTASSIGN exp
           | var DIVIDEASSIGN exp
           | var MODASSIGN exp
    '''
    if p[2] == '=':
        p[0] = ('=', p[1], p[3])
    elif p[2] == '+=':
        p[0] = ('+=', p[1], p[3])
    elif p[2] == '-=':
        p[0] = ('-=', p[1], p[3])
    elif p[2] == '*=':
        p[0] = ('*=', p[1], p[3])
    elif p[2] == '/=':
        p[0] = ('/=', p[1], p[3])
    elif p[2] == '%=':
        p[0] = ('%=', p[1], p[3])


def p_expArithmetic(p):
    '''
    exp : exp PLUS exp
        | exp MINUS exp
        | exp MULT exp
        | exp DIVIDE exp
        | exp MOD exp
    '''
    if p[2] == '+':
        p[0] = ('+', p[1], p[3])
    elif p[2] == '-':
        p[0] = ('-', p[1], p[3])
    elif p[2] == '/':
        p[0] = ('/', p[1], p[3])
    elif p[2] == '*':
        p[0] = ('*', p[1], p[3])
    elif p[2] == '%':
        p[0] = ('%', p[1], p[3])


def p_expComparison(p):
    '''
    exp : exp EQUALS exp
        | exp DIFFERENT exp
        | exp LTE exp
        | exp GTE exp
        | exp GT exp
        | exp LT exp
    '''
    if p[2] == '==':
        p[0] = ('==', p[1], p[3])
    elif p[2] == '!=':
        p[0] = ('!=', p[1], p[3])
    elif p[2] == '<=':
        p[0] = ('<=', p[1], p[3])
    elif p[2] == '>=':
        p[0] = ('>=', p[1], p[3])
    elif p[2] == '>':
        p[0] = ('>', p[1], p[3])
    elif p[2] == '<':
        p[0] = ('<', p[1], p[3])


def p_expLogic(p):
    '''
    exp : exp AND exp
        | exp OR exp
        | NOT exp
        | UMINUS exp
    '''
    if p[2] == '&&':
        p[0] = ('AND', p[1], p[3])
    elif p[2] == '||':
        p[0] = ('OR', p[1], p[3])
    elif p[1] == '!':
        p[0] = ('NOT', p[1], p[2])
    elif p[1] == '-':
        p[0] = ('UMINUS', -p[2])


def p_expTernary(p):
    '''
    exp : exp '?' exp ':' exp
    '''
    p[0] = ('Ternary', p[1], p[3], p[5])


def p_expSubCall(p):
    '''
    exp : subCall
    '''
    p[0] = ('expSubCall', p[1])


def p_expVar(p):
    '''
    exp : var
    '''
    p[0] = ('expVar', p[1])


def p_expLiteral(p):
    '''
    exp : literal
    '''
    p[0] = ('literal', p[1])


def p_expMultParent(p):
    '''
    exp : LPAREN exp RPAREN
    '''
    p[0] = ('expMultParent', p[2])


def p_var(p):
    '''
    var : ID
        | ID LCOR exp RCOR
    '''
    if len(p) == 2:
        p[0] = ('var', p[1])
    elif len(p) == 5:
        p[0] = ('var', p[1], p[3])


def p_literal(p):
    '''
    literal : NUMBER
            | STRING_LITERAL
            | FALSE
            | TRUE
    '''
    p[0] = ('Literal', p[1])


def p_paramList(p):
    '''
    paramList : paramSeq
              | empty
    '''
    if len(p) == 2:
        p[0] = ('paramList', p[1])


def p_paramListNull(p):
    '''
    program : empty
    '''


def p_paramSeq(p):
    '''
    paramSeq : param
             | param COMMA paramSeq
    '''
    if len(p) == 2:
        p[0] = ('paramSeq', p[1])
    elif len(p) == 4:
        p[0] = ('paramSeq', p[1], p[3])


def p_varDecList(p):
    '''
    varDecList : varDec varDecList
               | empty
    '''
    if len(p) == 3:
        p[0] = ('varDecList', p[1], p[2])


def p_varSpecSeq(p):
    '''
    varSpecSeq : varSpec
               | varSpec COMMA varSpecSeq
    '''
    if len(p) == 2:
        p[0] = ('varSpecSeq', p[1])
    elif len(p) == 4:
        p[0] = ('varSpecSeq', p[1], p[3])


def p_decSeq(p):
    '''
    decSeq : dec
           | dec decSeq
    '''
    if len(p) == 2:
        p[0] = ('decSeq', p[1])
    elif len(p) == 3:
        p[0] = ('decSeq', p[1], p[2])


def p_stmtList(p):
    '''
    stmtList : stmt stmtList
             | empty
    '''
    if len(p) == 3:
        p[0] = ('stmtList', p[1], p[2])


def p_literalSeq(p):
    '''
    literalSeq : literal
               | literal COMMA literalSeq
    '''
    if len(p) == 2:
        p[0] = ('literalSeq', p[1])
    elif len(p) == 3:
        p[0] = ('literalSeq', p[1], p[3])


def p_expList(p):
    '''
    expList : expSeq
            | empty
    '''
    if len(p) == 2:
        p[0] = ('expSeq', p[1])


def p_expSeq(p):
    '''
    expSeq : exp
           | exp COMMA expSeq
    '''
    if len(p) == 2:
        p[0] = ('expSeq', p[1])
    elif len(p) == 4:
        p[0] = ('expSeq', p[1], p[3])


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    last_cr = lex.lexer.lexdata.rfind('\n', 0, lex.lexer.lexpos)
    column = lex.lexer.lexpos - last_cr - 1
    print("LexToken(ERROR Sintático: Linha: %s, Coluna: %s, Token invávildo: %s)" % (p.lexer.lineno, column, p.value[0]))
    p.lexer.skip(1)


path_files_test = '../test/'
path_files_result = '../result/'
archive = Utils.find_files(path_files_test)
parser = yacc.yacc()
analisador_sintatico = parser.parse(Utils.find_files_test(archive, path_files_test))


print (analisador_sintatico)
