import ply.lex as lex
import re
import codecs
import os
import sys

# 1. Definición de tokens
tokens = [
    'MAYORIGUAL', 'MENORIGUAL', 'MENORQUE', 'MAYORQUE',
    'ILOGICO', 'OLOGICO', 'IGUALIGUAL', 'DIFERENTE',
    'LKEY', 'RKEY', 'LPAR', 'RPAR', 'LCOR', 'RCOR',
    'NEGBOOL', 'UMINUS', 'MEN', 'SUM', 'MULT', 'DIV', 'MOD', 'IGUAL',
    'DOT', 'COMMA', 'DOTCOMMA', 'ID', 'NUMERO', 'CAD'
    ]

# tokens_unused = ['BINARIO', 'NEWLINE', 'COMENTARIO']
# palavras_reservadas_unused = {'void':'VOID'}

# De acordo com a linguagem itilizada
palavras_reservadas = {
    'class': 'CLASS',
    'return': 'RETURN',
    'this': 'THIS',
    'extends': 'EXTENDS',
    'if': 'IF',
    'new': 'NEW',
    'else': 'ELSE',
    'length': 'LENGTH',
    'int': 'INT',
    'while': 'WHILE',
    'true': 'TRUE',
    'boolean': 'BOOLEAN',
    'break': 'BREAK',
    'false': 'FALSE',
    'string': 'STRING',
    'continue': 'CONTINUE',
    'null': 'NULL'
}
tokens += list(palavras_reservadas.values())

# implementando utilizando expressoes regulares
# t_COMENTARIO = '\/\/.*'
# t_COMENTARIO = r'\/\*.*\n\*\/'
# t_ignore_COMENTARIO = '\/\/.*'
# t_COMENTARIO = r'\/\*\s*([^\s]*)\s*\s*\/'
t_MAYORIGUAL = '>='
t_MENORIGUAL = '<='
t_MENORQUE = '<'
t_MAYORQUE = '>'
t_ILOGICO = '&&'
t_OLOGICO = r'\|\|'
t_IGUALIGUAL = r'=='
t_DIFERENTE = '!='
t_LKEY = '\{'
t_RKEY = '\}'
t_LPAR = '\('
t_RPAR = '\)'
t_LCOR = '\['
t_RCOR = r'\]'
t_NEGBOOL = '!'
t_MEN = '-'
t_UMINUS = '\-'
t_SUM = '\+'
t_MULT = '\*'
t_DIV = r'/'
t_MOD = '%'
t_IGUAL = '='
t_DOT = r'\.'
t_COMMA = ','
t_DOTCOMMA = ';'


def t_COMENTARIO(t):
    """ Verifica os comentarios """
    r'(/\*(.|\n|\r|\t)*?\*/)|//.*'
    # t.value = str(t.value)
    return t


# BINARIO-----------------------------------------------
def t_BINARIO(t):
    r'[b]\'[01]+\''
    t.value = int(t.value[2:-1], 2)
    # t.value = str(t.value)
    return t

# -----------------------------------------------------------------
# def t_error_CAD(t):
#     r'"([\x20-\x7E]|\\\\|\\n|\\t|\\r)*'
#     print"la cadena no quedo bien cerrada"


def t_CAD(t):

    r'"([\x20-\x7E]|\t|\r)*"'
    # t.value = str(t.value)
    return t


# ERROR ID ---------------------------------------------
def t_error_ID(t):
    r'[ñÑáÁéÉíÍÓóúÚ\d][A-Za-z]([0-9a-zA-ZñÑáÁéÉíÍÓóúÚ]*[A-Za-z])?'
    t.value = re.sub(r'[ñÑáÁéÉíÍÓóúÚ]', '_', t.value)
    print("El identidicador %s no es valido" % t.value)
    t.type = palavras_reservadas.get(t.value, 'ID')
    t.lexer.skip(1)
    # t.value = str(t.value)


# ID---------------------------------------------------
def t_ID(t):  # done
    r'[A-Za-z]([0-9a-zA-ZñÑáÁéÉíÍÓóúÚ]*)?[A-Za-zñÑáÁéÉíÍÓóúÚ]*'

    # reemplazando la ñ y los caracteres tildados
    t.value = re.sub(r'[ñÑáÁéÉíÍÓóúÚ]', '_', t.value)
    t.type = palavras_reservadas.get(t.value, 'ID')
    # t.value = str(t.value)
    return t

# NUMERO-----------------------------------------------
# reconoce los token como caracteres y la convertimos a un numero para
# escribirlo, si no es un numero tira una exepcion


def t_NUMERO(t):

    r'(-?[0-9]+(\.[0-9]+)?)([eE]-?\+?[0-9]+)?'

    try:
        #  coge la cadena y se convierte en numero
        t.value = float(t.value)
        if t.value < -2147483648.0 or t.value > 2147483647.0:
            print ("ERROR valor fuera de rango en la linea %d" % t.lineno)
            t.value = 0

    except ValueError:
        print ("El valor no es correcto %d", t.value)
        t.value = 0
        # t.value = str(t.value)
        return t

# RETURN-----------------------------------------------
# detecta la palabra reservada return
# NOTA: no hay necesidad de realizar esta funcion, puesto que
# esta dentro de las palabras reservadas


def t_RETURN(t):
    r'return'
    # t.value = str(t.value)
    return t
# IF---------------------------------------------------
# def t_IF(t):
#   r'if'
#  return t


# 3. Caracteres que se reconocen e ignoran
# aca se esta ignorando el espacio
t_ignore = " \t"

# NEWLINE----------------------------------------------
# reconoce un salto de linea y cuenta los saltos de linea para saber
# cuantas lineas hay


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    # t.value = str(t.value)

# ERROR------------------------------------------------
# entra aca si no concuerda con ningun caracter, es decir si no reconoce
# un token


def t_error(t):
    # se encontrar erro o analisador continua (skip)
    print("Caracter não reconhecido '%s'" % t.value[0])
    t.lexer.skip(1)


def buscar_arquivos():
    # verifica todos os arquivos do diretorio test
    arquivos = []
    numero_arquivo = ''
    resposta = False
    cont = 1

    for base, dirs, files in os.walk(diretorio):
        arquivos.append(files)

        for file in files:
            print(str(cont)+". "+file)
            cont = cont+1

        if resposta is False:
            numero_arquivo = input('\nNumero do Teste: ')
            for file in files:
                if file == files[int(numero_arquivo)-1]:
                    break

            print("Você escolheu \"%s\" \n" % files[int(numero_arquivo)-1])

            return files[int(numero_arquivo)-1]

analisador = lex.lex()

print("Selecione o teste")
print("Presiona Ctrl+z para sair\n")


diretorio = '/home/juliano/Workspace/Compiladores/test/'
arquivo = buscar_arquivos()
teste = diretorio+arquivo
fp = codecs.open(teste, "r", "utf-8")
cadeia = fp.read()
fp.close()


analisador.input(cadeia)

# Printa a lista de token
while True:
    token = analisador.token()
    if not token:
        break
    print(token)
