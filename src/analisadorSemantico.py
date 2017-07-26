# coding: utf-8
from analisadorLexico import *
from analisadorSintatico import *

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
        self.dicionario['program'].avaliaNo()


class NodeDecSeq(Node):
    def avaliaNo(self):
        self.dicionario['dec'].avaliaNo()


class NodeDec(Node):
    def avaliaNo(self):
        if len(self.dicionario) == 1:  # variavel
            self.dicionario['varDec'].avaliaNo()
        elif len(self.dicionario) == 3:  #(procedure)
            atualiza_tabela_procedure(self.dicionario)
        elif(len(self.dicionario)) == 5:  # função
            tipo_funcao = self.dicionario['type'].avaliaNo()
            atualiza_tabela_funcao(tipo_funcao, self.dicionario)
        # verifica se eh variavel, ou funcao ou procedure e trata cada um com uma funcao atualiza_tabela


class NodeVarDec(Node):
    def avaliaNo(self):
        tipo_variavel = self.dicionario['type'].avaliaNo()
        variavel = self.dicionario['varSpecSeq'].avaliaNo()
        atualiza_tabela_variavel(tipo_variavel, variavel)


class NodeVarSpec(Node):
    def avaliaNo(self):
        return self.dicionario['ID'].value()


class NodeType(Node):
    def avaliaNo(self):
        return self.dicionario['type'].value()


class NodeParam(Node):
    def avaliaNo(self):
        if len(self.dicionario) == 2:
            return {'type': self.dicionario['type'].value(), 'ID': self.dicionario['ID'].value(), 'tipo_var': 'NORMAL'}
        elif len(self.dicionario) == 4:
            return {'type': self.dicionario['type'].value(), 'ID': self.dicionario['ID'].value(), 'tipo_var': 'VETOR'}
        else:
            return "Número de parâmetros do dicionário do sintático tá errado."


class NodeBlock(Node):
    def avaliaNo(self):
        self.dicionario['varDecList'].avaliaNo()
        self.dicionario['stmtList'].avaliaNo()


class NodeStmt(Node):
    def avaliaNo(self):
        self.dicionario['stmt'].avaliaNo()


class NodeIfStmt(Node):
    def avaliaNo(self):
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
        if self.dicionario['exp'].avaliaNo() in ['TRUE', 'FALSE']:
             self.dicionario['block'].avaliaNo()
        else:
            return 'Erro porque nao retornou expressao booleana no nó while'


class NodeForStmt(Node):
    def avaliaNo(self):
        # Atualiza escopo das variaveis, em NodeAssign é feita a verificação se estão declaradas.
        variavel = self.dicionario['assign1'].avaliaNo()
        atualiza_tabela_assign(variavel)
        variavel = self.dicionario['assign2'].avaliaNo()
        atualiza_tabela_assign(variavel)
        if self.dicionario['exp'].avaliaNo() in ['TRUE', 'FALSE']:
            self.dicionario['block'].avaliaNo()
        else:
            return 'Deu erro no nó FOR, exp não é boolean. exp é: ', self.dicionario['exp'].avaliaNo()


class NodeBreakStmt(Node):
    def avaliaNo(self):
        if verificaEscopoBreak():
            pass
        else:
            return 'Deu erro no break, ele não está dentro de um laço segundo a função verificaEscopoBreak.'


class NodeReadStmt(Node):
    def avaliaNo(self):
        self.dicionario['var'].avaliaNo()


class NodeWriteStmt(Node):
    def avaliaNo(self):
        self.dicionario['expList'].avaliaNo()


class NodeReturnStmt(Node):
    def avaliaNo(self):
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
        if not verifica_declaracao_procedimento(self.dicionario['id'].value):
            return 'SubCall '+self.dicionario['ID'].value+' não definido.'
        expList = self.dicionario['expList'].avaliaNo()  # Retornar uma lista
        if not verifica_parametros_procedimento(self.dicionario['ID'].value, expList):
            return 'Subcall '+self.dicionario['ID'].value+' com número e/ou tipo incompativel de parametros'


class NodeAssign(Node):
    def avaliaNo(self):
        if self.dicionario['var'].avaliaNo() not in tabela_simbolos:
            return "variável "+self.dicionario['var'].avaliaNo()+" não está declarada."
        else:
            self.dicionario['exp'].avaliaNo()  # variável está na TS, verifica se exp está correto.


class NodeExpArithimetic(Node):
    def avaliaNo(self):
        if self.dicionario['exp1'].avaliaNo() == self.dicionario['exp2'].avaliaNo(): # verifica o tipo, retorno disso eh number, string, etc...
            return self.dicionario['exp1'].avaliaNo()
        else:
            return 'Operação aritimetica entre tipos de variáveis diferentes'


class NodeExpComparison(Node):
    def avaliaNo(self):
        if self.dicionario['exp1'].avaliaNo() == self.dicionario['exp2'].avaliaNo():
            return self.dicionario['exp1'].avaliaNo()
        else:
            return 'Comparação entre tipos de variáveis diferentes'


class NodeExpLogic(Node):
    def avaliaNo(self):
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
        self.dicionario['exp'].avaliaNo()


class NodeVar(Node):
    def avaliaNo(self):
        return self.dicionario['ID'].value


class NodeLiteral(Node):
    def avaliaNo(self):
        return self.dicionario['literal'].value()


class NodeParamList(Node):
    def avaliaNo(self):
        if 'empty' in self.dicionario:
            return 0
        else:
            return len(self.dicionario['paramlist'].avaliaNo())


class NodeParamSeq(Node):
    global lista_de_parametros
    def avaliaNo(self, lista_de_parametros):
        param = self.dicionario['param'].avaliaNo()
        lista_de_parametros.append(param)
        if 'paramSeq' in self.dicionario:
            self.dicionario['paramSeq'].avaliaNo()
        else:
            lista_de_retorno = lista_de_parametros
            lista_de_parametros = []
            return lista_de_retorno

class NodeVarDecList(Node):
    global lista_varDec
    def avaliaNo(self, lista_varDec):
        if 'empty' in self.dicionario:
            return []
        if 'varDecList' in self.dicionario:
            lista_varDec.append(self.dicionario['varDec'].avaliaNo())
            self.dicionario['varDecList'].avaliaNo()
        else:
            lista_varDec_retorno = lista_varDec
            lista_varDec = []
            return lista_varDec_retorno

#vardec eh a declaração com o tipo e o semicolon
#varspec eh a especificação das variaveis com id, assign, etc, lcor, rcor.
class NodeVarSpecSeq(Node):
    global lista_specSeq
    def avaliaNo(self, lista_specSeq):
        if 'varSpecSeq' in self.dicionario:
            lista_specSeq.append(self.dicionario['varSpec'].avaliaNo())
            self.dicionario['varSpecSeq'].avaliaNo()
        else:
            lista_specSeq_retorno = lista_specSeq
            lista_specSeq = []
            return lista_specSeq_retorno


class NodeDecSeq(Node):
    global lista_decSeq
    def avaliaNo(self, lista_decSeq):
        if 'decSeq' in self.dicionario:
            lista_decSeq.append(self.dicionario['dec'].avaliaNo())
            self.dicionario['decSeq'].avaliaNo()
        else:
            lista_decSeq_retorno = lista_decSeq
            lista_decSeq = []
            return lista_decSeq_retorno


class NodeStmtList(Node):  # Como não tem retorno, só chama todos os stmts pra ser feita a análise semântica deles.
    def avaliaNo(self):
        if 'stmtList' in self.dicionario:
            self.dicionario['stmt'].avaliaNo()  # Faz a nálise do stmt
            self.dicionario['stmtList'].avaliaNo()  # Avalia o stmtList


class NodeLiteralSeq(Node):
    global lista_literalSeq
    def avaliaNo(self, lista_literalSeq):
        if 'literalSeq' in self.dicionario:
            lista_literalSeq.append(self.dicionario['literal'].avaliaNo())
            self.dicionario['literalSeq'].avaliaNo()
        else:
            lista_literalSeq_retorno = lista_literalSeq
            lista_literalSeq = []
            return lista_literalSeq_retorno


class NodeExpList(Node):
    def avaliaNo(self):
        if 'empty' in self.dicionario:
            return []
        else:
            self.dicionario['expSeq'].avaliaNo()


class NodeExpSeq(Node):
    global lista_expSeq
    def avaliaNo(self, lista_expSeq):
        if 'expSeq' in self.dicionario:
            lista.append(self.dicionario['exp'].avaliaNo())
            self.dicionario['expSeq'].avaliaNo()
        else:
            lista_expSeq = []
            lista_expSeq_retorno = lista_expSeq
            return lista_expSeq_retorno


class NodeEmpty(Node):
	def __init__(self):
		pass
