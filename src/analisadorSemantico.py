# coding: utf-8
from analisadorLexico import *
from analisadorSintatico import *

lista_expSeq, lista_literalSeq, lista_decSeq, lista_varDec, lista_paramSeq, lista_specSeq = [[] for _ in range(6)]

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
            print('variavel: ', self.dicionario['varDec'].avaliaNo())
            self.dicionario['varDec'].avaliaNo()
        elif len(self.dicionario) == 3:  #(procedure)
            print('procedure')
            self.dicionario['paramList'].avaliaNo()
            self.dicionario['block'].avaliaNo()
            #atualiza_tabela_procedure(self.dicionario)
        elif(len(self.dicionario)) == 5:  # função
            print('funcao')
            tipo_funcao = self.dicionario['type'].avaliaNo()
            #atualiza_tabela_funcao(tipo_funcao, self.dicionario)
        # verifica se eh variavel, ou funcao ou procedure e trata cada um com uma funcao atualiza_tabela


class NodeVarDec(Node):
    def avaliaNo(self):
        print(self.dicionario)
        tipo_variavel = self.dicionario['type'].avaliaNo()
        variavel = self.dicionario['varSpecSeq'].avaliaNo()
        #atualiza_tabela_variavel(tipo_variavel, variavel)


class NodeVarSpec(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if len(self.dicionario) == 1:
            return self.dicionario['ID']
        elif 'literal' in self.dicionario:
            self.dicionario['literal'].avaliaNo()
            return self.dicionario['ID']
        elif 'NUMBER' in self.dicionario:
            return self.dicionario['ID']
        elif 'literalSeq' in self.dicionario:
            self.dicionario['literalSeq'].avaliaNo()
            return self.dicionario['ID']


class NodeType(Node):
    def avaliaNo(self):
        print(self.dicionario)
        print('tipo ', self.dicionario['type'])
        return self.dicionario['type']


class NodeParam(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if len(self.dicionario) == 2:
            return {'type': self.dicionario['type'], 'ID': self.dicionario['ID'], 'tipo_var': 'NORMAL'}
        elif len(self.dicionario) == 4:
            return {'type': self.dicionario['type'], 'ID': self.dicionario['ID'], 'tipo_var': 'VETOR'}
        else:
            return "Número de parâmetros do dicionário do sintático tá errado."


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
        if self.dicionario['exp'].avaliaNo() in ['TRUE', 'FALSE']:
            pass
        else:
            return 'Expressão do nó IF não retorna um booleano. Retorno: ' + self.dicionario['exp'].avaliaNo()
        if len(self.dicionario) == 2:
            self.dicionario['block'].avaliaNo()
        elif len(self.dicionario) == 3:
            self.dicionario['block1'].avaliaNo()
            self.dicionario['block2'].avaliaNo()


class NodeWhileStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if self.dicionario['exp'].avaliaNo() in ['TRUE', 'FALSE']:
             self.dicionario['block'].avaliaNo()
        else:
            return 'Erro porque nao retornou expressao booleana no nó while'


class NodeForStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        # Atualiza escopo das variaveis, em NodeAssign é feita a verificação se estão declaradas.
        variavel = self.dicionario['assign1'].avaliaNo()
        #atualiza_tabela_assign(variavel)
        variavel = self.dicionario['assign2'].avaliaNo()
        #atualiza_tabela_assign(variavel)
        if self.dicionario['exp'].avaliaNo() in ['TRUE', 'FALSE']:
            self.dicionario['block'].avaliaNo()
        else:
            return 'Deu erro no nó FOR, exp não é boolean. exp é: ', self.dicionario['exp'].avaliaNo()


class NodeBreakStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if verificaEscopoBreak():
            pass
        else:
            return 'Deu erro no break, ele não está dentro de um laço segundo a função verificaEscopoBreak.'


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
        escopo = verifica_escopo_return()
        if escopo == False:
            return 'return não está dentro de um subprograma'
        if escopo == 'funcao':
            tipo_retorno_exp = self.dicionario['exp'].avaliaNo()
            avalia_tipo_retorno_com_declaracao(tipo_retorno_exp)
        if escopo == 'procedimento':
            if 'exp' in self.dicionario:
                return 'retorno de exp dentro de procedimento ERRO.'


class NodeSubCall(Node):
    def avaliaNo(self):

        print(self.dicionario)
        '''
        if not verifica_declaracao_procedimento(self.dicionario['ID']):
            return 'SubCall '+self.dicionario['ID']+' não definido.'
        expList = self.dicionario['expList'].avaliaNo()  # Retornar uma lista
        if not verifica_parametros_procedimento(self.dicionario['ID'], expList):
            return 'Subcall '+self.dicionario['ID']+' com número e/ou tipo incompativel de parametros'
        '''
        self.dicionario['expList'].avaliaNo()
        #print('expList (sou eu aqui olha o//): ', expList)

class NodeAssign(Node):
    def avaliaNo(self):
        print(self.dicionario)
        '''
        if self.dicionario['var'].avaliaNo() not in tabela_simbolos:
            return "variável "+self.dicionario['var'].avaliaNo()+" não está declarada."
        else:
            self.dicionario['exp'].avaliaNo()  # variável está na TS, verifica se exp está correto.
        '''
        self.dicionario['exp'].avaliaNo()

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
        if self.dicionario['exp1'].avaliaNo() == self.dicionario['exp2'].avaliaNo():
            return self.dicionario['exp1'].avaliaNo()
        else:
            return 'Comparação entre tipos de variáveis diferentes'


class NodeExpLogic(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if len(self.dicionario) == 3:
            if self.dicionario['exp1'].avaliaNo() in ['TRUE', 'FALSE'] and self.dicionario['exp2'].avaliaNo() in ['TRUE', 'FALSE']:
                return self.dicionario['exp1'].avaliaNo()  # Retorno aqui deveria ser BOOL mas como não temos isso, retornar TRUE ou FALSE tbm da certo.
            else:
                return 'Expressão lógica entre tipos diferentes'
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
        else:
            return 'NodeExpLogic não entrou em nenhum if.'


class NodeExpTernary(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if self.dicionario['exp'].avaliaNo() not in ['TRUE', 'FALSE']:
            return 'exp retornou: '+self.dicionario['exp'].avaliaNo()+' esperava-se um booleano'
        if (self.dicionario['block1'].avaliaNo() != self.dicionario['block2'].avaliaNo()):
            return 'expressão consequente e alternativa de tipos diferentes'
        # "tipo resultante tem q ser do mesmo tipo da consequente ?! n entendi"
        else:
            return 'ERRO: Padrão (pretty fucking informative)'


class NodeExpSubCall(Node):
    def avaliaNo(self):
        self.dicionario['subCall'].avaliaNo()


class NodeExpVar(Node):
    def avaliaNo(self):
        self.dicionario['var'].avaliaNo()


class NodeExpLiteral(Node):
    def avaliaNo(self):
        self.dicionario['literal'].avaliaNo()


class NodeExpMultParent(Node):
    def avaliaNo(self):
        print(self.dicionario)
        self.dicionario['exp'].avaliaNo()


class NodeVar(Node):
    def avaliaNo(self):
        print(self.dicionario)
        return self.dicionario['ID']


class NodeLiteral(Node):
    def avaliaNo(self):
        print(self.dicionario)
        return self.dicionario['literal']


class NodeParamList(Node):
    def avaliaNo(self):
        print(self.dicionario)
        for key, value in self.dicionario.items():
            if value == None:
                print('oi cogu')
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


#vardec eh a declaração com o tipo e o semicolon
#varspec eh a especificação das variaveis com id, assign, etc, lcor, rcor.
class NodeVarSpecSeq(Node):
    def avaliaNo(self):
        print(self.dicionario)
        global lista_specSeq
        lista_specSeq.append(self.dicionario['varSpec'].avaliaNo())
        if 'varSpecSeq' in self.dicionario:
            self.dicionario['varSpecSeq'].avaliaNo()
        else:
            lista_specSeq_retorno = lista_specSeq
            lista_specSeq = []
            return lista_specSeq_retorno


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
            print('lista decseq', self.dicionario)
            return lista_decSeq_retorno


class NodeStmtList(Node):  # Como não tem retorno, só chama todos os stmts pra ser feita a análise semântica deles.
    def avaliaNo(self):
        print(self.dicionario)
        self.dicionario['stmt'].avaliaNo()
        if self.dicionario['stmtList'] != None:
            self.dicionario['stmtList'].avaliaNo()  # Avalia o stmtList


class NodeLiteralSeq(Node):
    global lista_literalSeq
    def avaliaNo(self, lista_literalSeq):
        print(self.dicionario)
        if 'literalSeq' in self.dicionario:
            lista_literalSeq.append(self.dicionario['literal'].avaliaNo())
            self.dicionario['literalSeq'].avaliaNo()
        else:
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
	def __init__(self):
		pass
