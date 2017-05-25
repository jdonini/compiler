def menu():
    print("""
         ++++++ Compilador para a Linguagem cmm ++++++

         1 - Analisador Léxico
         2 - Analisador Sintático
         3 - Analisador Semântico

         0 - Sair
           """)


def analisadorLexico():
    print ('\nanalisadorLexico()\n')
    menu()
    switch(int(input('Escolha uma opção: ')))


def analisadorSintatico():
    print ('\nanalisadorSintatico()\n')
    menu()
    switch(int(input('Escolha uma opção: ')))


def analisadorSemantico():
    print ('\nanalisadorSemantico()\n')
    menu()
    switch(int(input('Escolha uma opção: ')))


def sair():
    print ("\nSaindo ...\n")


def case_default():
    print ('\nVálor inválido, favor digitar uma opção entre 0 e 3\n')
    menu()
    switch(int(input('Escolha uma opção: ')))


def switch(x):
    dict.get(x, case_default)()


dict = {
    1: analisadorLexico,
    2: analisadorSintatico,
    3: analisadorSemantico,
    0: sair
    }


try:
    menu()
    switch(int(input('Escolha uma opção: ')))
except ValueError:
    print ('\nO valor digitado não é um número')
    menu()
    switch(int(input('Escolha uma opção: ')))
