# coding: utf-8
import ply.yacc as yacc
import ply.lex as lex
import os
import codecs
import re
import datetime
from sys import stdin
from analisadorLexico import tokens

# a precedencia é definida de cima para baixo
# baseado na definição da linguagem (versão 1.4)
# os conflitos são resolvidos pela regra shift/reduce
precedencia_tokens = (
    ('right', 'NEGUNARY', 'NOT'),
    ('right', 'NOT'),
    ('left', 'MULT', 'DIVIDE', 'MOD'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'GTE', 'LTE', 'GT', 'LT'),
    ('left', 'EQUALS', 'DIFFERENT'),
    ('left', 'AND'),
    ('left', 'OR'),
    ('right', '?')
)


# os terminais são os tokens
# os não terminais da gramatica, serão os nomes das funcões
# P quer dizer que vamos analisar as produções
def p_program(p):
    '''
    program : decSeq
    '''
    p[0] = (p[1], "Programa")


def p_dec(p):
    '''
    dec : varDec
        | ID LPAREN paramList RPAREN LKEY block RKEY
        | type ID LPAREN paramList RPAREN LKEY block RKEY
    '''
    if len(p) == 2:
        p[0] = ('Declaração', p[1])
    elif len(p) == 8:
        p[0] = ('Declaração', p[1], p[2], p[3], p[4], p[5], p[6], p[7])
    elif len(p) == 9:
        p[0] = ('Declaração', p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])


def p_varDec(p):
    '''
    varDec : type varSpecSeq SEMICOLON
    '''
    p[0] = ('Declaração Variável', p[1], p[2], p[3])


def p_varSpec(p):
    '''
    varSpec : ID
            | ID ASSING literal
            | ID LCOR NUMBER RCOR
            | ID LCOR NUMBER RCOR ASSING LKEY literalSeq RKEY
    '''
    if len(p) == 2:
        p[0] = ('Especificação de variável', p[1])
    elif len(p) == 4:
        p[0] = ('Especificação de variável', p[1], p[2], p[3])
    elif len(p) == 5:
        p[0] = ('Especificação de variável', p[1], p[2], p[3], p[4])
    elif len(p) == 9:
        p[0] = ('Especificação de variável', p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])


def p_type(p):
    '''
    type : INT
         | STRING
         | BOOLEAN
    '''
    p[0] = ('Tipo', p[1])


def p_param(p):
    '''
    param : type ID
          | type ID RCOR LCOR
    '''
    if len(p) == 3:
        p[0] = ('Parâmetro', p[1], p[2])
    elif len(p) == 5:
        p[0] = ('Parâmetro', p[1], p[2], p[3], p[4])


def p_block(p):
    '''
    block : varDecList stmtList
    '''
    p[0] = ('Bloco', p[1], p[2])


def p_stmt(p):
    '''
    stmt : ifStmt
         | whileStmt
         | forStmt
         | breakStmt
         | returnStmt
         | readStmt
         | writeStmt
         | assing SEMICOLON
         | subCall SEMICOLON
    '''
    if len(p) == 2:
        p[0] = ('Comandos', p[1])
    elif len(p) == 3:
        p[0] = ('Comandos', p[1], p[2])


def p_ifStmt(p):
    '''
    ifStmt : IF LPAREN exp RPAREN LKEY block RKEY
           | IF LPAREN exp RPAREN LKEY block RKEY ELSE LKEY block RKEY
    '''
    if len(p) == 8:
        p[0] = ('IF', p[1], p[2], p[3], p[4], p[5], p[6], p[7])
    elif len(p) == 12:
        p[0] == ('IF', p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11])


def p_whileStmt(p):
    '''
    whileStmt : WHILE LPAREN exp RPAREN LKEY block RKEY
    '''
    p[0] = ('WHILE', p[1], p[2], p[3], p[4], p[5], p[6], p[7])


def p_forStmt(p):
    '''
    forStmt : FOR LPAREN assing SEMICOLON exp SEMICOLON assing RPAREN LKEY block RKEY
    '''
    p[0] = ('FOR', p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11])


def p_readStmt(p):
    '''
    breakStmt : BREAK SEMICOLON
    '''
    p[0] = ('BREAK', p[1], p[2])


def p_comandoRead(p):
    '''
    readStmt : READ var SEMICOLON
    '''
    p[0] = ('READ', p[1], p[2], p[3])


def p_writeStmt(p):
    '''
    writeStmt : WRITE expList SEMICOLON
    '''
    p[0] = ('WRITE', p[1], p[2], p[3])


def p_returnStmt(p):
    '''
    returnStmt : RETURN SEMICOLON
               | RETURN exp SEMICOLON
    '''
    if len(p) == 3:
        p[0] = ('RETURN', p[1], p[2])
    elif len(p) == 4:
        p[0] = ('RETURN', p[1], p[2], p[3])


def p_subCall(p):
    '''
    subCall : ID LPAREN expList RPAREN
    '''
    p[0] = ('Chamada de Função', p[1], p[2], p[3], p[4])


def p_assing(p):
    '''
    assing : var ASSING exp
           | var PLUSASSING exp
           | var MINUSASSING exp
           | var MULTASSING exp
           | var DIVIDEASSING exp
           | var MODASSING exp
    '''
    if p[2] == '=':
        p[0] = ('Atribuição', p[1], p[2], p[3])
    elif p[2] == '+=':
        p[0] = ('SomaAtribuição', p[1], p[2], p[3])
    elif p[2] == '-=':
        p[0] = ('SubAtribuição', p[1], p[2], p[3])
    elif p[2] == '*=':
        p[0] = ('MultAtribuição', p[1], p[2], p[3])
    elif p[2] == '/=':
        p[0] = ('DivAtribuição', p[1], p[2], p[3])
    elif p[2] == '%=':
        p[0] = ('ModAtribuição', p[1], p[2], p[3])


def p_expArithmetic(p):
    '''
    exp : exp PLUS exp
        | exp MINUS exp
        | exp MULT exp
        | exp DIVIDE exp
        | exp MOD exp
    '''
    if p[2] == '+':
        p[0] = ('Adição', p[1] + p[3])
    elif p[2] == '-':
        p[0] = ('Subtração', p[1] - p[3])
    elif p[2] == '/':
        p[0] = ('Divisão', p[1] / p[3])
    elif p[2] == '*':
        p[0] = ('Multiplicação', p[1] * p[3])
    elif p[2] == '%':
        p[0] = ('Módulo', p[1] % p[3])


def p_expComparasion(p):
    '''
    exp : exp EQUALS exp
        | exp DIFFERENT exp
        | exp LTE exp
        | exp GTE exp
        | exp GT exp
        | exp LT exp
    '''
    if p[2] == '==':
        p[0] = ('Igual', p[1] == p[3])
    elif p[2] == '!=':
        p[0] = ('Diferente', p[1] != p[3])
    elif p[2] == '<=':
        p[0] = ('Menor igual', p[1] <= p[3])
    elif p[2] == '>=':
        p[0] = ('Maior igual', p[1] >= p[3])
    elif p[2] == '>':
        p[0] = ('Maior', p[1] > p[3])
    elif p[2] == '<':
        p[0] = ('Menor', p[1] < p[3])


def p_expLogic(p):
    '''
    exp : exp AND exp
        | exp OR exp
        | NOT exp
        | NEGUNARY exp
    '''
    if p[2] == '&&':
        p[0] = ('AND', p[1], p[2], p[3])
    elif p[2] == '||':
        p[0] = ('OR', p[1], p[2], p[3])
    elif p[1] == '!':
        p[0] = ('Negação', p[1], p[2])
    elif p[1] == '-':
        p[0] = ('Menos', -p[2])


def p_expTernary(p):
    '''
    exp : exp '?' exp ':' exp
    '''
    p[0] = ('Ternário', p[1], p[2], p[3], p[4], p[5])


def p_expSubCall(p):
    '''
    exp : subCall
    '''
    p[0] = ('Chamada de Função', p[1])


def p_expVar(p):
    '''
    exp : var
    '''
    p[0] = ('Variável', p[1])


def p_expLiteral(p):
    '''
    exp : literal
    '''
    p[0] = ('Literal', p[1])


def p_expMultParent(p):
    '''
    exp : LPAREN exp RPAREN
    '''
    p[0] = ('Multiplos parênteses', p[1], p[2], p[3])


def p_var(p):
    '''
    var : ID
        | ID LCOR exp RCOR
    '''
    if len(p) == 2:
        p[0] = ('Variável', p[1])
    elif len(p) == 5:
        p[0] = ('Variável', p[1], p[2], p[3], p[4])


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
              | 'ε'
    '''
    p[0] = ('Lista de parametros', p[1])


def p_paramListNull(p):
    '''
    program : empty
    '''
    p[0] is None


def p_paramSeq(p):
    '''
    paramSeq : param
             | param COMMA paramSeq
    '''
    if len(p) == 2:
        p[0] = ('Sequência de parâmetros', p[1])
    elif len(p) == 4:
        p[0] = ('Sequência de parâmetros', p[1], p[2], p[3])


def p_varDecList(p):
    '''
    varDecList : varDec varDecList
               | 'ε'
    '''
    p[0] = ('Lista de declaração de variável', p[1], p[2])


def p_varSpecSeq(p):
    '''
    varSpecSeq : varSpec
               | varSpec COMMA varSpecSeq
    '''
    if len(p) == 2:
        p[0] = ('Sequencia de variável', p[1])
    elif len(p) == 4:
        p[0] = ('Sequencia de variável', p[1], p[2], p[3])


def p_decSeq(p):
    '''
    decSeq : dec
           | dec decSeq
    '''
    if len(p) == 2:
        p[0] = ('Sequência de declaração', p[1])
    elif len(p) == 3:
        p[0] = ('Sequência de declaração', p[1], p[2])


def p_stmtList(p):
    '''
    stmtList : stmt stmtList
             | 'ε'
    '''
    p[0] = ('Lista de comando', p[1], p[2])


def p_literalSeq(p):
    '''
    literalSeq : literal
               | literal literalSeq
    '''
    if len(p) == 2:
        p[0] = ('Valor da sequência', p[1])
    elif len(p) == 3:
        p[0] = ('Valor da sequência', p[1], p[2])


def p_expList(p):
    '''
    expList : expSeq
            | 'ε'
    '''
    p[0] = ('Sequência de Expressão', p[1])


def p_expSeq(p):
    '''
    expSeq : exp
           | exp COMMA expSeq
    '''
    if len(p) == 2:
        p[0] = ('Sequência de Expressões', p[1])
    elif len(p) == 4:
        p[0] = ('Sequência de Expressões', p[1], p[2], p[3])


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    last_cr = lex.lexer.lexdata.rfind('\n', 0, lex.lexer.lexpos)
    column = lex.lexer.lexpos - last_cr - 1
    print("LexToken(ERROR Sintático: Linha: %s, Coluna: %s, Token invávildo: %s)" % (p.lexer.lineno, column, p.value[0]))
    p.lexer.skip(1)


def buscar_arquivos(diretorio_teste):
    arquivos = []
    numero_arquivo = ''
    resposta = False
    contador = 1

    for base, dirs, files in os.walk('/Users/juliano/Workspace/Compiladores/test/'):
        arquivos.append(files)

        for file in files:
            print(str(contador)+". "+file)
            contador += 1

        if resposta is False:
            numero_arquivo = input('\nNúmero do Teste: ')
            for file in files:
                if file == files[int(numero_arquivo)-1]:
                    break
            print("Você escolheu \"%s\" \n" % files[int(numero_arquivo)-1])

            return files[int(numero_arquivo)-1]


diretorio_teste = '/Users/juliano/Workspace/Compiladores/test/'
arquivo = buscar_arquivos(diretorio_teste)
teste = diretorio_teste + arquivo
arquivo_teste = open(teste, "r")
cadeia_caracteres = arquivo_teste.read()
arquivo_teste.close()

parser = yacc.yacc()
analisadorSintatico = parser.parse(cadeia_caracteres)
print (analisadorSintatico)
