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


path_files_test = '/Users/juliano/Workspace/Compiladores/test/'
path_files_result = '/Users/juliano/Workspace/Compiladores/result/'


def find_files(path_files_test):
    archives = []
    number_archives = ''
    answer = False
    count = 1

    for base, dirs, files in os.walk(path_files_test):
        archives.append(files)

        for file in files:
            print(str(count)+". "+file)
            count += 1

        if answer is False:
            number_archives = input('\nNúmero do Teste: ')
            for file in files:
                if file == files[int(number_archives)-1]:
                    break
            print("Você escolheu \"%s\" \n" % files[int(number_archives)-1])

            return files[int(number_archives)-1]


analisador_lexico = lex.lex()
archive = find_files(path_files_test)


def find_files_test(archive, path_files_test):
    test_directory = path_files_test
    test = test_directory + archive
    test_archive = open(test, "r")
    input_string = test_archive.read()
    test_archive.close()
    return input_string


analisador_lexico.input(find_files_test(archive, path_files_test))


def save_archives_test(archive, path_files_result):
    result_directory = path_files_result
    time = datetime.datetime.now()
    result = result_directory + archive + \
        "__" + ("%s-%s-%s" % (time.day, time.month, time.year)) + \
        "__" + ("%s:%s:%s" % (time.hour, time.minute, time.second)) + ".txt"
    return result


def test_output_lexer(result):
    while True:
        token = analisador_lexico.token()
        last_cr = lex.lexer.lexdata.rfind('\n', 0, lex.lexer.lexpos)
        column = lex.lexer.lexpos - last_cr - 1
        if not token:
            break
        print_lexer = 'LexToken(Token: %s, Valor: %r, Linha: %d, Coluna: %d)' % (token.type, token.value, token.lineno, column)
        print (print_lexer)
        with open(result, 'a') as file:
            file.write(print_lexer + '\n')
            file.close()


test_output_lexer(save_archives_test(archive, path_files_result))
