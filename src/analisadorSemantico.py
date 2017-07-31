# coding: utf-8
from analisadorLexico import *
from analisadorSintatico import *


lista_expSeq, lista_literalSeq, lista_specSeq_retorno, lista_decSeq, lista_varDec, lista_paramSeq, lista_specSeq = [[] for _ in range(7)]
tipo = 0
tipo_id = None
nome_id = None
dicionario_de_simbolos = {}


def atualizaTabela(dicionario_de_simbolos, idd, tipo):
    if not isinstance(idd, list):
        k = []
        k.append(idd)
        idd = k
    for item in idd:
        if item not in dicionario_de_simbolos:
            dicionario_de_simbolos[item] = tipo
        else:
            print('ERRO: Variavel ja foi declarada: ', item)
    print('DICIONARIO DE SIMBOLOS:', dicionario_de_simbolos)


import abc
class Node:
    __metaclass__ = abc.ABCMeta

    def __init__(self, dicionario):
        self.dicionario = dicionario

    @abc.abstractmethod
    def avaliaNo(self):
        pass


class NodeProgram(Node):
    def avaliaNo(self):
        print(self.dicionario)
        self.dicionario['program'].avaliaNo()


class NodeDecSeq(Node):
    def avaliaNo(self):
        print(self.dicionario)
        self.dicionario['dec'].avaliaNo()


class NodeDec(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if len(self.dicionario) == 1:  # variavel
            variavel = self.dicionario['varDec'].avaliaNo()
        elif len(self.dicionario) == 3:  #(procedure)
            print('procedure')
            self.dicionario['paramList'].avaliaNo()
            self.dicionario['block'].avaliaNo()
            atualizaTabela(dicionario_de_simbolos, self.dicionario['ID'], None)
        elif(len(self.dicionario)) == 4:  # função
            print('funcao')
            tipo_funcao = self.dicionario['type'].avaliaNo()
            self.dicionario['paramList'].avaliaNo()
            self.dicionario['block'].avaliaNo()
            atualizaTabela(dicionario_de_simbolos, self.dicionario['ID'], tipo_funcao)


class NodeVarDec(Node):
    def avaliaNo(self):
        global tipo
        print(self.dicionario)
        var_tipo = self.dicionario['type'].avaliaNo()
        var_id = self.dicionario['varSpecSeq'].avaliaNo(var_tipo)


class NodeVarSpecSeq(Node):
    def avaliaNo(self, tipo):
        global dicionario_de_simbolos
        global lista_specSeq
        print(self.dicionario)
        lista_specSeq.append(self.dicionario['varSpec'].avaliaNo())
        if 'varSpecSeq' in self.dicionario:
            self.dicionario['varSpecSeq'].avaliaNo(tipo)
        else:
            print('tipo das variaveis', tipo)
            atualizaTabela(dicionario_de_simbolos, lista_specSeq, tipo)
            lista_specSeq_retorno = lista_specSeq
            lista_specSeq = []
            return lista_specSeq_retorno



class NodeVarSpec(Node):
    def avaliaNo(self):
        global tipo_id
        global nome_id
        print(self.dicionario)
        if len(self.dicionario) == 1:
            return self.dicionario['ID']
        elif 'literal' in self.dicionario:
            literal = self.dicionario['literal'].avaliaNo()
            return self.dicionario['ID']
        elif 'NUMBER' in self.dicionario and 'literalSeq' not in self.dicionario:
            return self.dicionario['ID']
        elif 'literalSeq' in self.dicionario:
            print(self.dicionario)
            NUMBER = self.dicionario['NUMBER']
            self.dicionario['literalSeq'].avaliaNo(NUMBER)
            return self.dicionario['ID']


class NodeType(Node):
    def avaliaNo(self):
        print(self.dicionario)
        #print('tipo ', self.dicionario['type'])
        return self.dicionario['type']


class NodeParam(Node):
    def avaliaNo(self):
        print(self.dicionario)
        param_type = self.dicionario['type'].avaliaNo()
        if len(self.dicionario) == 2:
            print({'type': param_type, 'ID': self.dicionario['ID'], 'tipo_var': 'NORMAL'})
        elif len(self.dicionario) == 4:
            print({'type': param_type, 'ID': self.dicionario['ID'], 'tipo_var': 'VETOR'})
        else:
            return "Número de parâmetros do dicionário do sintático está errado."


class NodeBlock(Node):
    def avaliaNo(self):
        print(self.dicionario)
        self.dicionario['varDecList'].avaliaNo()
        self.dicionario['stmtList'].avaliaNo()


class NodeStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        self.dicionario['stmt'].avaliaNo()


class NodeIfStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        #print(self.dicionario['exp'].avaliaNo())
        #self.dicionario['exp'].avaliaNo())
        #check_if_declared()
        if self.dicionario['exp'].avaliaNo() == 'bool':
            pass
        else:
            print('ERRO: exp do IFSTMT retornou', self.dicionario['exp'].avaliaNo())
            return 'Expressão do nó IF não retorna um booleano. Retorno: '
        if len(self.dicionario) == 2:
            self.dicionario['block'].avaliaNo()
        elif len(self.dicionario) == 3:
            self.dicionario['block1'].avaliaNo()
            self.dicionario['block2'].avaliaNo()


class NodeWhileStmt(Node):
    def avaliaNo(self):
        print()
        print(self.dicionario)
        print()
        if self.dicionario['exp'].avaliaNo() != 'bool':
            return 'ERRO exp do no while nao retorna bool'
        self.dicionario['block'].avaliaNo()


class NodeForStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        variavel1 = self.dicionario['assign1'].avaliaNo()
        variavel2 = self.dicionario['assign2'].avaliaNo()
        if self.dicionario['exp'].avaliaNo() in ['TRUE', 'FALSE']:
            self.dicionario['block'].avaliaNo()
        else:
            return 'Deu erro no nó FOR, exp não é boolean. exp é: ', self.dicionario['exp'].avaliaNo()


class NodeBreakStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        # Verificar escopo do break, alterar escopo após break.

class NodeReadStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        self.dicionario['var'].avaliaNo()


class NodeWriteStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        self.dicionario['expList'].avaliaNo()


class NodeReturnStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if 'exp' in self.dicionario:
            self.dicionario['exp'].avaliaNo()
        '''
        escopo = verifica_escopo_return()
        if escopo == False:
            return 'return não está dentro de um subprograma'
        if escopo == 'funcao':
            tipo_retorno_exp = self.dicionario['exp'].avaliaNo()
            avalia_tipo_retorno_com_declaracao(tipo_retorno_exp)
        if escopo == 'procedimento':
            if 'exp' in self.dicionario:
                return 'retorno de exp dentro de procedimento ERRO.'
        '''

class NodeSubCall(Node):
    def avaliaNo(self):

        print(self.dicionario)
        if self.dicionario['ID'] not in dicionario_de_simbolos:
            print('ERRO: Subcall'+self.dicionario['ID']+'() não declarada.')
        self.dicionario['expList'].avaliaNo()
        #print('expList (sou eu aqui olha o//): ', expList)

class NodeAssign(Node):
    def avaliaNo(self):
        print(self.dicionario)
        variavel_assign = self.dicionario['var'].avaliaNo()  # variável está na TS, verifica se exp está correto.
        self.dicionario['exp'].avaliaNo()
        return variavel_assign
class NodeExpArithimetic(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if self.dicionario['exp1'].avaliaNo() == self.dicionario['exp2'].avaliaNo(): # verifica o tipo, retorno disso eh number, string, etc...
            return self.dicionario['exp1'].avaliaNo()
        else:
            return 'Operação aritimetica entre tipos de variáveis diferentes'


class NodeExpComparison(Node):
    def avaliaNo(self):
        print(self.dicionario)
        var_tipo1 = self.dicionario['exp1'].avaliaNo()
        print('var_tipo1: ', var_tipo1)
        var_tipo2 = self.dicionario['exp2'].avaliaNo()
        print('var_tipo2: ', var_tipo2)
        if var_tipo1 == var_tipo2:
            return 'bool'
        else:
            print('Comparação entre tipos de variáveis diferentes '+ var_tipo1+ ' <> '+var_tipo2)


class NodeExpLogic(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if len(self.dicionario) == 3:
            if self.dicionario['exp1'].avaliaNo() == self.dicionario['exp2'].avaliaNo():
                return self.dicionario['exp1'].avaliaNo()  # Retorno aqui deveria ser BOOL mas como não temos isso, retornar TRUE ou FALSE tbm da certo.
            else:
                return 'Expressão lógica entre tipos diferentes'+self.dicionario['exp1'].avaliaNo()
        if 'NOT' in self.dicionario:
            if self.dicionario['exp'].avaliaNo() in ['TRUE', 'FALSE']:
                return self.dicionario['exp'].avaliaNo()
            else:
                return 'ERRO: Negação de uma expressão que não retorna um booleano'
        if 'UMINUS' in self.dicionario:
            if self.dicionario['exp'].avaliaNo() == 'NUMBER':
                return self.dicionario['exp'].avaliaNo()
            else:
                return 'ERRO: Esperava-se um inteiro depois de UMINUS e retornou '+self.dicionario['exp'].avaliaNo()



class NodeExpTernary(Node):
    def avaliaNo(self):
        print(self.dicionario)
        exp1 = self.dicionario['exp1'].avaliaNo()
        exp2 = self.dicionario['exp2'].avaliaNo()
        exp3 = self.dicionario['exp3'].avaliaNo()
        if exp1 != 'bool':
            print('ERRO: exp1 retornou: '+str(exp1)+' esperava-se um booleano')
        if exp2 != exp3:
            print('ERRO: exp2 <> exp3 Operador Ternário')


class NodeExpSubCall(Node):
    def avaliaNo(self):
        self.dicionario['subCall'].avaliaNo()


class NodeExpVar(Node):
    def avaliaNo(self):
        return self.dicionario['var'].avaliaNo()


class NodeExpLiteral(Node):
    def avaliaNo(self):
        return self.dicionario['literal'].avaliaNo()


class NodeExpMultParent(Node):
    def avaliaNo(self):
        print(self.dicionario)
        self.dicionario['exp'].avaliaNo()


class NodeVar(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if self.dicionario['ID'] not in dicionario_de_simbolos:
            print('ERRO: Variavel '+self.dicionario['ID']+' nao foi declarada')
            atualizaTabela(dicionario_de_simbolos, self.dicionario['ID'], None)
        return dicionario_de_simbolos[self.dicionario['ID']]


class NodeLiteral(Node):
    def avaliaNo(self):
        print(self.dicionario)
        literal = self.dicionario['literal']
        #tipo_literal = type(self.dicionario['literal']).__name__
        #if tipo_literal != tipo_id:
        #    print('ERRO Semantico: A variavel {} foi definida como {} e foi atribuido um {}.'.format(nome_id, tipo_id, tipo_literal))
        return type(self.dicionario['literal']).__name__


class NodeParamList(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if self.dicionario['paramSeq'] == None:
            return []
        else:
            return self.dicionario['paramSeq'].avaliaNo()


class NodeParamSeq(Node):
    def avaliaNo(self):
        print(self.dicionario)
        global lista_paramSeq
        lista_paramSeq.append(self.dicionario['param'].avaliaNo())
        if 'paramSeq' in self.dicionario:
            self.dicionario['paramSeq'].avaliaNo()
        else:
            lista_paramSeq_retorno = lista_paramSeq
            lista_paramSeq = []
            return lista_paramSeq_retorno


class NodeVarDecList(Node):
    def avaliaNo(self):
        print(self.dicionario)
        global lista_varDec
        if 'empty' in self.dicionario:
            lista_varDec_retorno = lista_varDec
            return lista_varDec_retorno
        if 'varDecList' in self.dicionario:
            lista_varDec.append(self.dicionario['varDec'].avaliaNo())
            self.dicionario['varDecList'].avaliaNo()


class NodeDecSeq(Node):
    def avaliaNo(self):
        print(self.dicionario)
        global lista_decSeq
        lista_decSeq.append(self.dicionario['dec'].avaliaNo())
        if 'decSeq' in self.dicionario:
            self.dicionario['decSeq'].avaliaNo()
        else:
            lista_decSeq_retorno = lista_decSeq
            lista_decSeq = []
            return lista_decSeq_retorno


class NodeStmtList(Node):  # Como não tem retorno, só chama todos os stmts pra ser feita a análise semântica deles.
    def avaliaNo(self):
        print(self.dicionario)
        if 'empty' in self.dicionario:
            return
        self.dicionario['stmt'].avaliaNo()
        if self.dicionario['stmtList'] != None:
            self.dicionario['stmtList'].avaliaNo()  # Avalia o stmtList


class NodeLiteralSeq(Node):
    def avaliaNo(self, NUMBER):
        global lista_literalSeq
        print(self.dicionario)
        lista_literalSeq.append(self.dicionario['literal'].avaliaNo())
        if 'literalSeq' in self.dicionario:
            self.dicionario['literalSeq'].avaliaNo(NUMBER)
        else:
            if len(lista_literalSeq) != NUMBER:
                print('ERRO: Tamanho do vetor <> do tamanho declarado: '+str(len(lista_literalSeq))+ ' <> '+str(NUMBER))
            lista_literalSeq_retorno = lista_literalSeq
            lista_literalSeq = []
            return lista_literalSeq_retorno


class NodeExpList(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if 'empty' in self.dicionario:
            return []
        else:
            self.dicionario['expSeq'].avaliaNo()


class NodeExpSeq(Node):
    def avaliaNo(self):
        print(self.dicionario)
        global lista_expSeq
        lista_expSeq.append(self.dicionario['exp'].avaliaNo())
        if 'expSeq' in self.dicionario:
            self.dicionario['expSeq'].avaliaNo()
        else:
            lista_expSeq_retorno = lista_expSeq
            lista_expSeq = []
            return lista_expSeq_retorno


class NodeEmpty(Node):
	def avaliaNo(self):
		pass
