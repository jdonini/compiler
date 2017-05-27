from analisadorLexico import test_output_lexer
from analisadorSintatico import test_output_sintatico
from utils import Utils, path_files_result


def menu():
    print("""
         ++++++++++++++++++++++++++++++++++++ Compilador para a Linguagem cmm ++++++++++++++++++++++++++++++++++++

         1 - Analisador Léxico
         2 - Analisador Sintático
         3 - Analisador Semântico

         0 - Sair
           """)


def analisadorLexico():
    print("\n++++++++++++++++++++++++++++++++++++ Análisador Léxico ++++++++++++++++++++++++++++++++++++\n")
    test_output_lexer(Utils.save_archives_test(Utils.archive, path_files_result))
    print()
    menu()
    switch(int(input('Escolha uma opção: ')))


def analisadorSintatico():
    print("\n++++++++++++++++++++++++++++++++++++ Análisador Léxico ++++++++++++++++++++++++++++++++++++\n")
    test_output_lexer(Utils.save_archives_test(Utils.archive, path_files_result))
    print()
    print("\n++++++++++++++++++++++++++++++++ Árvore Sintática Abstrata ++++++++++++++++++++++++++++++++\n")
    test_output_sintatico(Utils.save_archives_test(Utils.archive, path_files_result))
    print()
    menu()
    switch(int(input('Escolha uma opção: ')))


def analisadorSemantico():
    print()
    print ('\nanalisadorSemantico()\n')
    print()
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
