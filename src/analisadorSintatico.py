# coding: utf-8
import ply.yacc as yacc
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
    ('right', 'ID'),
    ('right', 'IF', 'WHILE', 'FOR'),
    ('right', 'BREAK', 'READ', 'WRITE'),
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
def p_program(p):
    '''
    program ::= sequenciaDeclaracao
    '''
    if len(p) == 2:
        p[0] = (p[1], "programa")


def p_declaracao(p):
    '''
    declaracao ::= variavelDeclaracao
                | ID LPAREN listaParametro RPAREN LKEY bloco RKEY
                | tipo ID LPAREN listaParametro RPAREN LKEY bloco RKEY
    '''
    if len(p) == 2:
        p[0] = (p[1], "Declaração")
    elif len(p) == 8:
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], "Declaração")
    elif len(p) == 9:
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], "Declaração")


def p_variavelDeclaracao(p):
    '''
    variavelDeclaracao ::= tipo variavelEspecificacaoSeq ';'
    '''
    p[0] = (p[1], p[2], p[3], "Declaração Variavel")


def p_variavelEspecificacao(p):
    '''
    variavelEspecificacao ::= ID
                            | ID ASSIGN valor
                            | ID LCOR NUMBER RCOR
                            | ID LCOR NUMBER RCOR ASSIGN LKEY sequenciaValor RKEY
    '''
    if len(p) == 2:
        p[0] = (p[1], "Especificacao de variavel")
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3], "Especificacao de variavel")
    elif len(p) == 5:
        p[0] = (p[1], p[2], p[3], p[4], "Especificacao de variavel")
    elif len(p) == 9:
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], "Especificacao de variavel")


def p_tipo(p):
    '''
    tipo ::= INT
          |  STRING
          |  BOOLEAN
    '''
    p[0] = (p[1], "tipo")


def p_parametro(p):
    '''
    parametro ::= tipo ID
                | tipo ID LCOR RCOR
    '''
    if len(p) == 3:
        p[0] = (p[1], p[2], "Parametro")
    elif len(p) == 5:
        p[0] = (p[1], p[2], p[3], p[4], "Parametro")


def p_bloco(p):
    '''
    bloco ::= variavelDeclaracaoList listaComando
    '''
    p[0] = (p[1], p[2], "bloco")


def p_comando(p):
    '''
    comando ::= comandoIf
             |  comandoWhile
             |  comandoFor
             |  comandoBreak
             |  comandoReturn
             |  comandoRead
             |  comandoWrite
             |  expressaoAtrib SEMICOLON
             |  chamadaDeFuncao SEMICOLON
    '''
    if len(p) == 2:
        p[0] = (p[1], "Comandos")
    elif len(p) == 3:
        p[0] = (p[1], p[2], "Comandos")


def p_comandoIf(p):
    '''
    comandoIf ::= IF LPAREN expressao RPAREN LKEY bloco RKEY
                | IF LPAREN expressao LPAREN LKEY bloco RKEY ELSE LKEY bloco RKEY
    '''
    if len(p) == 8:
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], "IF")
    elif len(p) == 12:
        p[0] == (p[1], p[2], p[3], p[4], p[5], p[6], p[7],
                 p[8], p[9], p[10], p[11], "IF")


def p_comandoWhile(p):
    '''
    comandoWhile ::= WHILE LPAREN expressao RPAREN LKEY bloco RKEY
    '''
    if len(p) == 8:
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], "WHILE")


def p_comandoFor(p):
    '''
    comandoFor ::= FOR LPAREN expressaoAtrib SEMICOLON expressao SEMICOLON expressaoAtrib RPAREN LKEY bloco RKEY
    '''
    if len(p) == 12:
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], "FOR")


def p_comandoBreak(p):
    '''
    comandoBreak ::= BREAK SEMICOLON
    '''
    if len(p) == 4:
        p[0] = (p[1], p[2], "BREAK")


def p_comandoRead(p):
    '''
    comandoRead ::= READ variavel SEMICOLON
    '''
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3], "READ")


def p_comandoWrite(p):
    '''
    comandoWrite ::= WRITE listaExpressao SEMICOLON
    '''
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3], "WRITE")


def p_comandoReturn(p):
    '''
    comandoReturn ::= RETURN SEMICOLON
                     | RETURN expressao SEMICOLON
    '''
    if len(p) == 3:
        p[0] = (p[1], p[2], "RETURN")
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3], "RETURN")


def p_chamadaDeFuncao(p):
    '''
    chamadaDeFuncao ::= ID LPAREN listaExpressao RPAREN
    '''
    p[0] = (p[1], p[2], p[3], p[4], "Chamada de função")


def p_op(p):
    '''
    op ::= PLUS
        |  MINUS
        |  MULT
        |  DIVIDE
        |  MOD
        |  EQUALS
        |  DIFFERENT
        |  LTE
        |  GTE
        |  GT
        |  LT
        |  AND
        |  OR
    '''
    if len(p) == 2:
        if p == '+':
            p[0] = (p[1], "Adição")
        elif p == '-':
            p[0] = (p[1], "Subtração")
        elif p == '*':
            p[0] = (p[1], "Multiplicação")
        elif p == '/':
            p[0] = (p[1], "Divisão")
        elif p == '%':
            p[0] = (p[1], "Módulo")
        elif p == '==':
            p[0] = (p[1], "Comparação")
        elif p == '!=':
            p[0] = (p[1], "Diferente")
        elif p == '<=':
            p[0] = (p[1], "Menor igual")
        elif p == '>=':
            p[0] = (p[1], "Maior menor")
        elif p == '>':
            p[0] = (p[1], "Maior")
        elif p == '<':
            p[0] = (p[1], "Menor")
        elif p == '&&':
            p[0] = (p[1], "AND")
        elif p == '||':
            p[0] = (p[1], "OR")


def p_opAtrib(p):
    '''
    opAtrib ::= ASSIGN
             |  PLUSASSIGN
             |  MINUSASSIGN
             |  MULTASSIGN
             |  DIVIDEASSIGN
             |  MODASSIGN
    '''
    if len(p) == 2:
        if p == '=':
            p[0] = (p[1], "Atribuição")
        elif p == '+=':
            p[0] = (p[1], "Mais igual")
        elif p == '-=':
            p[0] = (p[1], "Menos igual")
        elif p == '*=':
            p[0] = (p[1], "Multiplicação igual")
        elif p == '/=':
            p[0] = (p[1], "Divisão igual")
        elif p == '%=':
            p[0] = (p[1], "Resto igual")


def p_expressaoAtrib(p):
    '''
    expressaoAtrib ::= variavel opAtrib  expressao
    '''
    p[0] = (p[1], "Expressão de Atribuição")


def p_variavel(p):
    '''
    variavel ::= ID
               | ID LCOR expressao RCOR
    '''
    if len(p) == 2:
        p[0] = (p[1], "Variável")
    elif len(p) == 5:
        p[0] = (p[1], p[2], p[3], p[4], "Variável")


def p_expressao(p):
    '''
    expressao ::= expressao op expressao
             | NOT expressao
             | MINUS expressao
             | expressao '?' expressao ':' expressao
             | chamadaDeFuncao
             | variavel
             | valor
             | LPAREN expressao RPAREN
    '''
    if len(p) == 2:
        p[0] = (p[1], p[2], "Expressão")
    elif len(p) == 3:
        if p[1] == '!':
            p[0] = (p[1], p[2], "Expressão")
        elif p[1] == '-':
            p[0] = (p[1], p[2], "Expressão")
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3], "Expressão")
    elif len(p) == 6:
        p[0] = (p[1], p[2], p[3], p[4], [5], "Expressão")


def p_valor(p):
    '''
    valor ::= NUMBER
            | STRING
            | TRUE
            | FALSE
    '''
    p[0] = (p[1], "Valor")


def p_listaParametro(p):
    '''
    listaParametro ::= sequenciaParametro
                      | 'ε'
    '''
    p[0] = (p[1], "Lista de parametros")


def p_listaParametroNull(p):
    '''
    program : empty
    '''
    p[0] is None


def p_sequenciaParametro(p):
    '''
    sequenciaParametro ::= parametro COMMA sequenciaParametro
                          |  parametro
    '''
    if len(p) == 2:
        p[0] = (p[1], "Sequencia de parametros")
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3], "Sequencia de parametros")


def p_variavelDeclaracaoList(p):
    '''
    variavelDeclaracaoList ::= variavelDeclaracao variavelDeclaracaoList
                              | 'ε'
    '''
    p[0] = (p[1], p[2], "Lista de declaração de variável")


# def p_variavelDeclaracaoListNull(p):
#     p[0] is None


def p_variavelEspecificacaoSeq(p):
    '''
    variavelEspecificacaoSeq ::= variavelEspecificacao COMMA variavelEspecificacaoSeq
                               |   variavelEspecificacao
    '''
    if len(p) == 2:
        p[0] = (p[1], "Sequencia de variável")
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3], "Sequencia de variável")


def p_sequenciaDeclaracao(p):
    '''
    sequenciaDeclaracao ::= declaracao sequenciaDeclaracao
                           |   declaracao
    '''
    if len(p) == 2:
        p[0] = (p[1], "Sequencia de declaração")
    elif len(p) == 3:
        p[0] = (p[1], p[2], "Sequencia de declaração")


def p_listaComando(p):
    '''
    listaComando ::= comando listaComando
                    | 'ε'
    '''
    p[0] = (p[1], p[2], "Lista de comando")


# def p_listaComandoNull(p):
#     p[0] is None


def p_sequencialValor(p):
    '''
    sequenciaValor ::= valor sequenciaValor
                      |  valor
    '''
    if len(p) == 2:
        p[0] = (p[1], "Valor da sequencia")
    elif len(p) == 3:
        p[0] = (p[1], p[2], "Valor da sequencia")


def p_listaExpressao(p):
    '''
    listaExpressao ::= sequenciaExpressao
                      | 'ε'
    '''
    if len(p) == 2:
        p[0] = (p[1], "Sequencia de Expressão")


# def p_listaExpressaoNull(p):
#     p[0] is None


def p_sequencialExpressao(p):
    '''
    sequenciaExpressao ::= expressao ',' sequenciaExpressao
                          |  expressao
    '''
    if len(p) == 2:
        p[0] = (p[1], "Expressão")
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3], "Expressão")


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    print ('Erro de sintaxe %s' % p)
    print ('Erro na linha %s' % str(p.lexer.lineno))


def buscar_arquivos(diretorio_teste):
    # verifica todos os arquivos do diretorio test
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
