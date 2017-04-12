import ply.lex as lex
import re
import os
import datetime


# Definição dos tokens que a linguagem reconhece
tokens = [
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'MULT', 'DIVIDE', 'MOD',
    'NE', 'LT', 'LTE', 'GT', 'GTE', 'LPAREN', 'RPAREN', 'EQUALS',
    'DOT', 'COMMA', 'SEMICOLON',
    ]

# De acordo com a linguagem itilizada, foi definida as palavras_reservadas
palavras_reservadas = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'def': 'DEF',
    'class': 'CLASS',
    'return': 'RETURN',
    'length': 'LENGTH',
    'int': 'INT',
    'boolean': 'BOOLEAN',
    'true': 'TRUE',
    'false': 'FALSE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'string': 'STRING',
    'null': 'NULL'
}
tokens += list(palavras_reservadas.values())

# implementando utilizando expressoes regulares
t_ignore_COMMENT = r'\#.*'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_NE = r'<>'
t_LT = r'<'
t_LTE = r'<='
t_GT = r'>'
t_GTE = r'=>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_DOT = r'\.'
t_COMMA = r','
t_SEMICOLON = r';'


# Funções seguindo o padrão da doc (http://www.dabeaz.com/ply/ply.html#ply_nn6)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = palavras_reservadas.get(t.value, 'ID')
    return t


# verifica se existe comentário na linha, assumimos que seja #
# varias vezes (*), pelo menos uma vez(+)
def t_COMMENT(t):
    r'\#.*'
    pass


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Valor do inteiro muito grande %d", t.value)
        t.value = 0
    return t


def t_error(t):
    """ trato o erro que ocorre quando é verificado um Caracter ao longo
    da leitura do arquivo, encontra o erro e continua """
    print ("Caracter ilegal '%s' " % t.value[0])
    t.lexer.skip(1)


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    t.lexer.current = t.lexer.lexpos - 1


# Compute column.
#     input is the input text string
#     token is a token instance
# def find_column(cadeia_caracteres, t):
#     print("FIND column")
#     last_cr = input.rfind('\n', 0, t.lexpos)
#     if last_cr < 0:
#         last_cr = 0
#     column = (t.lexpos - last_cr) + 1
#     return columnn


# Ignora tabs e espaços
t_ignore = ' \t'


def buscar_arquivos():
    # verifica todos os arquivos do diretorio test
    arquivos = []
    numero_arquivo = ''
    resposta = False
    contador = 1

    for base, dirs, files in os.walk(diretorio_teste):
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


analisador_lexer = lex.lex()

# arquivos de Teste
diretorio_teste = '/home/juliano/Workspace/Compiladores/test/'
arquivo = buscar_arquivos()
teste = diretorio_teste + arquivo
arquivo_teste = open(teste, "r")
cadeia_caracteres = arquivo_teste.read()
arquivo_teste.close()

# arquivos de Resulado
diretorio_resultado = '/home/juliano/Workspace/Compiladores/result/'
i = datetime.datetime.now()
resultado = diretorio_resultado + arquivo + "__" + ("%s-%s-%s" % (i.day, i.month, i.year)) + \
            "__" + ("%s:%s:%s" % (i.hour, i.minute, i.second))
arquivo_resultado = open(resultado, "w+")

# usa a cadeia_caracteres como entrada para o AL
analisador_lexer.input(cadeia_caracteres)

# Printa a lista de token
while True:
    token = analisador_lexer.token()
    if not token:
        break
    print(token)
    arquivo_resultado.write(str(token)+"\n")
print("\n")
arquivo_resultado.close()
