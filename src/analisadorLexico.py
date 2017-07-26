# coding: utf-8

import ply.lex as lex
from utils import Utils, path_files_test

# Funções seguindo o padrão da doc(http://www.dabeaz.com/ply/ply.html\ply_nn6)
tokens = [
    'LPAREN', 'RPAREN', 'LCOR', 'RCOR', 'LKEY', 'RKEY', 'COMMA', 'SEMICOLON', 'ID', 'NUMBER', 'STRING_LITERAL',
    'PLUS', 'MINUS', 'MULT', 'DIVIDE', 'EQUALS', 'DIFFERENT', 'GT', 'GTE', 'LT', 'LTE', 'MOD', 'UMINUS',
    'OR', 'AND', 'NOT', 'ASSIGN', 'PLUSASSIGN', 'MINUSASSIGN', 'MULTASSIGN', 'DIVIDEASSIGN', 'MODASSIGN', 'QMARK',
    'COLON'
    ]

reserved = {
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
tokens += list(reserved.values())

t_QMARK = r'\?'
t_COLON = r':'
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
t_MINUSASSIGN = r'\-='
t_MULTASSIGN = r'\*='
t_DIVIDEASSIGN = r'/='
t_MODASSIGN = r'%='
t_STRING_LITERAL = r'\"(.|\n)*?\"'
t_ignore = ' \t\v\r'


def t_id(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
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


analisador_lexico = lex.lex()


def test_output_lexer(result):
    analisador_lexico.input(Utils.find_files_test(Utils.archive, path_files_test))
    lex.lexer.lineno = 1
    dict_token = {}
    count = 1
    while True:
        token = analisador_lexico.token()
        last_cr = lex.lexer.lexdata.rfind('\n', 0, lex.lexer.lexpos)
        column = lex.lexer.lexpos - last_cr - 1
        if not token:
            break
        print_lexer = 'LexToken(Token: %s, Valor: %r, Linha: %d, Coluna: %d)' % (token.type, token.value, token.lineno, column)
        print (print_lexer)
        lista_tokens = []
        lista_tokens.append(token.type)
        for item in lista_tokens:
            if ('ID' in item) and (token.value not in dict_token.keys()):
                dict_token[token.value] = count
                count += 1
        with open(result, 'a') as file:
            file.write(print_lexer + '\n')
            file.close()
    print("\n\n+++++++++++++++++++++++++++++++++++++ Lista de Ocorrências +++++++++++++++++++++++++++++++++++++\n")
    print_dict_token = '\nLista de Ocorrências %s' % (dict_token)
    print(print_dict_token)
    with open(result, 'a') as file:
        file.write(str(print_dict_token) + '\n')
        file.close()
