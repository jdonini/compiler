# coding: utf-8
import ply.lex as lex
import re
import os
import sys
import datetime

# Funções seguindo o padrão da doc(http://www.dabeaz.com/ply/ply.html\ply_nn6)
tokens = [
    'LPAREN', 'RPAREN', 'LCOR', 'RCOR', 'LKEY', 'RKEY', 'COMMA', 'SEMICOLON', 'ID', 'NUMBER', 'STRING_LITERAL',
    'PLUS', 'MINUS', 'MULT', 'DIVIDE', 'EQUALS', 'DIFFERENT', 'GT', 'GTE', 'LT', 'LTE', 'MOD', 'UMINUS',
    'OR', 'AND', 'NOT', 'ASSIGN', 'PLUSASSIGN', 'MINUSASSIGN', 'MULTASSIGN', 'DIVIDEASSIGN', 'MODASSIGN'
    ]

palavras_reservadas = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN',
    'string': 'STRING',
    'int': 'INT',
    'bool': 'BOOLEAN',
    'true': 'TRUE',
    'false': 'FALSE',
    'break': 'BREAK',
    'read': 'READ',
    'write': 'WRITE',
}
tokens += list(palavras_reservadas.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCOR = '\['
t_RCOR = r'\]'
t_LKEY = r'\{'
t_RKEY = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'=='
t_DIFFERENT = r'!='
t_MOD = r'%'
t_GT = r'>'
t_GTE = r'>='
t_LT = r'<'
t_LTE = r'<='
t_OR = r'\|\|'
t_AND = r'&&'
t_NOT = r'!'
t_UMINUS = r'-'
t_ASSIGN = r'='
t_PLUSASSIGN = r'\+='
t_MINUSASSIGN = r'-='
t_MULTASSIGN = r'\*='
t_DIVIDEASSIGN = r'/='
t_MODASSIGN = r'%='
t_STRING_LITERAL = r'\".*?\"'
t_ignore = ' \t\v\r'


def t_id(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = palavras_reservadas.get(t.value, 'ID')
    return t


def t_comment_multline(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    t.lexer.lineno += t.value.count("\n")
    pass


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Valor do inteiro muito grande %d", t.value)
        t.value = 0
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    column = token.lexpos - last_cr
    return column


def t_error(t):
    '''
    Trata o erro que ocorre quando é verificado um Caracter ao longo
    da leitura do arquivo, encontra o erro e continua
    '''
    column = find_column(t.lexer.lexdata, t)
    print("LexToken(ERROR Léxico: Linha: %d, Coluna: %d, Token invávildo: %s)" % (t.lexer.lineno, column, t.value[0]))
    t.lexer.skip(1)


def buscar_arquivos():
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


analisador_lexico = lex.lex()
arquivo = buscar_arquivos()


def buscar_arquivos_teste(arquivo):
    diretorio_teste = '/Users/juliano/Workspace/Compiladores/test/'
    teste = diretorio_teste + arquivo
    arquivo_teste = open(teste, "r")
    cadeia_caracteres = arquivo_teste.read()
    arquivo_teste.close()
    return cadeia_caracteres


analisador_lexico.input(buscar_arquivos_teste(arquivo))


def escrever_arquivos_resultado(arquivo):
    diretorio_resultado = '/Users/juliano/Workspace/Compiladores/result/'
    time = datetime.datetime.now()
    resultado = diretorio_resultado + arquivo + \
        "__" + ("%s-%s-%s" % (time.day, time.month, time.year)) + \
        "__" + ("%s:%s:%s" % (time.hour, time.minute, time.second)) + ".txt"
    return resultado


def test_output_lexer(resultado):
    while True:
        token = analisador_lexico.token()
        last_cr = lex.lexer.lexdata.rfind('\n', 0, lex.lexer.lexpos)
        column = lex.lexer.lexpos - last_cr - 1
        if not token:
            break
        result = 'LexToken(Token: %s, Valor: %r, Linha: %d, Coluna: %d)' % (token.type, token.value, token.lineno, column)
        print (result)
        with open(resultado, 'a') as file:
            file.write(result + '\n')
            file.close()
