import ply.lex as lex
import re
import os
import datetime
import baseLexer

# Definição dos tokens que a linguagem reconhece
tokens = [
    'LPAREN', 'RPAREN', 'LCOR', 'RCOR', 'LKEY', 'RKEY', 'COMMA', 'SEMICOLON',
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'MULT', 'DIVIDE', 'EQUALS', 'DIFFERENT',
    'GT', 'GTE', 'LT', 'LTE',  'OR', 'AND', 'NOT', 'ASSIGN', 'PLUSASSIGN',
    'MINUSASSIGN', 'MULTASSIGN', 'DIVIDEASSIGN', 'MODASSIGN', 'TERNARY',
    'DOT', 'STRING',
    ]

# De acordo com a linguagem itilizada, foi definida as palavras_reservadas
palavras_reservadas = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN',
    'int': 'INT',
    'bool': 'BOOLEAN',
    'string': 'STRING',
    'true': 'TRUE',
    'false': 'FALSE',
    'break': 'BREAK',
    'read': 'READ',
    'write': 'WRITE',
    'main': 'MAIN',
}
tokens += list(palavras_reservadas.values())

# o Caracter T antes das funcões quer dizer que vamos reconhecer um token
# passando T como paramentro, vamos analisar os tokens na função

# implementando utilizando expressoes regulares
t_ignore_COMMENT = r'\#.*'
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
t_GT = r'>'
t_GTE = r'=>'
t_LT = r'<'
t_LTE = r'<='
t_OR = r'\|\|'
t_AND = r'&&'
t_NOT = r'!'
t_ASSIGN = r'='
t_PLUSASSIGN = r'\+='
t_MINUSASSIGN = r'-='
t_MULTASSIGN = r'\*='
t_DIVIDEASSIGN = r'/='
t_MODASSIGN = r'%='
t_TERNARY = r'\? :'
t_DOT = r'\.'
t_STRING = r'\".*?\"'
# Ignora tabs e espaços
t_ignore = ' \t\v\r'


# Funções seguindo o padrão da doc(http://www.dabeaz.com/ply/ply.html\ply_nn6)
def t_id(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = palavras_reservadas.get(t.value, 'ID')
    return t


# Verifica se existe comentário na(s) linha(s)
def t_comment_multline(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    # ignora tudo que é comentario, porém em toda quebra de linha add +1
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


def t_error(t):
    """ Trata o erro que ocorre quando é verificado um Caracter ao longo
    da leitura do arquivo, encontra o erro e continua """
    print("LexToken(ERROR Léxico: Linha: %d, Coluna %d, Token invávildo: %s)" % (t.lexer.lineno, t.lexer.lexpos, t.value[0]))
    #  t.lexer.lexpos - t.lexer.linestart + 1
    t.lexer.skip(1)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


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
# diretorio_resultado = '/home/juliano/Workspace/Compiladores/result/'
# i = datetime.datetime.now()
# resultado = diretorio_resultado + arquivo + \
#             "__" + ("%s-%s-%s" % (i.day, i.month, i.year)) + \
#             "__" + ("%s:%s:%s" % (i.hour, i.minute, i.second))
# arquivo_resultado = open(resultado, "w+")

# usa a cadeia_caracteres como entrada para o AL
analisador_lexer.input(cadeia_caracteres)

# Printa a lista de token
while True:
    token = analisador_lexer.token()
    if not token:
        break
    print(token)
    # arquivo_resultado.write(str(token)+"\n")
print("\n")
# arquivo_resultado.close()
