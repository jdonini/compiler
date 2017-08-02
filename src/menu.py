# coding: utf-8

import os
import errno

def clean_files():
    for base, dirs, files in os.walk('../src/'):
        for archive in files:
            if archive.endswith('.pyc'):
                os.remove(os.path.join(base, archive))
            if archive.endswith('.out'):
                os.remove(os.path.join(base, archive))
            if archive.startswith('parsetab'):
                os.remove(os.path.join(base, archive))
    for base, dirs, files in os.walk('..'):
        for archive in files:
            if archive.endswith('.DS_Store'):
                os.remove(os.path.join(base, archive))


def create_folder():
    try:
        os.makedirs('../result')
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def menu():
    print("""
         ++++++++++++++++++++++++++++++++++++ Compilador para a Linguagem cmm ++++++++++++++++++++++++++++++++++++

         1 - Analisador Léxico
         2 - Analisador Sintático e Analisador Semântico

         0 - Sair
           """)
    clean_files()
    create_folder()


def analisadorLexico():
    from analisadorLexico import test_output_lexer
    from utils import Utils, path_files_result
    print("\n++++++++++++++++++++++++++++++++++++ Análisador Léxico ++++++++++++++++++++++++++++++++++++\n")
    test_output_lexer(Utils.save_archives_test(Utils.archive, path_files_result))
    print()


def analisadorSintatico():
    from analisadorSintatico import test_output_sintatico
    from utils import Utils, path_files_result
    print()
    print("\n++++++++++++++++++++++++++++++++ Árvore Sintática Abstrata ++++++++++++++++++++++++++++++++\n")
    import analisadorSemantico
    print(analisadorSemantico.dicionario_de_simbolos)
    test_output_sintatico(Utils.save_archives_test(Utils.archive, path_files_result))
    print()


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
    0: sair
    }


try:
    menu()
    switch(int(input('Escolha uma opção: ')))
except ValueError:
    print ('\nO valor digitado não é um número')
    menu()
    switch(int(input('Escolha uma opção: ')))
