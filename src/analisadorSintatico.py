# coding: utf-8

import ply.yacc as yacc
import ply.lex as lex
from utils import Utils, path_files_test
from analisadorLexico import tokens
from analisadorSemantico import *

# chamar depois do sintatico p[0].avaliaNo .. no retorno do sintatico
# a precedencia é definida de cima para baixo
# baseado na definição da linguagem (versão 1.4)
# os conflitos são resolvidos pela regra shift/reduce

precedence_tokens = (
    ('right', '?'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'DIFFERENT'),
    ('left', 'GTE', 'LTE', 'GT', 'LT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIVIDE', 'MOD'),
    ('right', 'NOT', 'UMINUS')
)


def p_program(p):
    '''
    program : decSeq
    '''
    p[0] = NodeProgram({'program': p[1]})
    p[0].avaliaNo()

def p_dec(p):
    '''
    dec : varDec
        | ID LPAREN paramList RPAREN LKEY block RKEY
        | type ID LPAREN paramList RPAREN LKEY block RKEY
    '''
    if len(p) == 2:
        p[0] = NodeDec({'varDec': p[1]})
    elif len(p) == 8:
        p[0] = NodeDec({'ID': p[1], 'paramList': p[3], 'block': p[6]})
    elif len(p) == 9:
        p[0] = NodeDec({'type': p[1], 'ID': p[2], 'paramList': p[4], 'block': p[7]})


def p_decSeq(p):
    '''
    decSeq : dec
           | dec decSeq
    '''
    if len(p) == 2:
        p[0] = NodeDecSeq({'dec': p[1]})
    elif len(p) == 3:
        p[0] = NodeDecSeq({'dec': p[1], 'decSeq': p[2]})


def p_varDec(p):
    '''
    varDec : type varSpecSeq SEMICOLON
    '''
    p[0] = NodeVarDec({'type': p[1], 'varSpecSeq': p[2]})

def p_varSpecSeq(p):
    '''
    varSpecSeq : varSpec
               | varSpec COMMA varSpecSeq
    '''
    if len(p) == 2:
        p[0] = NodeVarSpecSeq({'varSpec': p[1]})
    elif len(p) == 4:
        p[0] = NodeVarSpecSeq({'varSpec': p[1], 'varSpecSeq': p[3]})



def p_varSpec(p):
    '''
    varSpec : ID
            | ID ASSIGN literal
            | ID LCOR NUMBER RCOR
            | ID LCOR NUMBER RCOR ASSIGN LKEY literalSeq RKEY
    '''
    if len(p) == 2:
        p[0] = NodeVarSpec({'ID': p[1]})
    elif len(p) == 4:
        p[0] = NodeVarSpec({'ID': p[1], 'literal': p[3]})
    elif len(p) == 5:
        p[0] = NodeVarSpec({'ID': p[1], 'NUMBER': p[3]})
    elif len(p) == 9:
        p[0] = NodeVarSpec({'ID': p[1], 'NUMBER': p[3], 'literalSeq': p[7]})


def p_type(p):
    '''
    type : INT
         | STRING
         | BOOLEAN
    '''
    p[0] = NodeType({'type': p[1]})




def p_block(p):
    '''
    block : varDecList stmtList
    '''
    p[0] = NodeBlock({'varDecList': p[1], 'stmtList': p[2]})


def p_stmt(p):
    '''
    stmt : ifStmt
         | whileStmt
         | forStmt
         | breakStmt
         | returnStmt
         | readStmt
         | writeStmt
         | assign SEMICOLON
         | subCall SEMICOLON
         | error
    '''
    if len(p) == 2:
        p[0] = NodeStmt({'stmt': p[1]})
    elif len(p) == 3:
        p[0] = NodeStmt({'stmt': p[1]})


def p_ifStmt(p):
    '''
    ifStmt : IF LPAREN exp RPAREN LKEY block RKEY
           | IF LPAREN exp RPAREN LKEY block RKEY ELSE LKEY block RKEY
    '''
    if len(p) == 8:
        p[0] = NodeIfStmt({'exp': p[3], 'block': p[6]})
    elif len(p) == 12:
        p[0] = NodeIfStmt({'exp': p[3], 'block1': p[6], 'block2': p[10]})


def p_whileStmt(p):
    '''
    whileStmt : WHILE LPAREN exp RPAREN LKEY block RKEY
    '''
    p[0] = NodeWhileStmt({'exp': p[3], 'block': p[6]})


def p_forStmt(p):
    '''
    forStmt : FOR LPAREN assign SEMICOLON exp SEMICOLON assign RPAREN LKEY block RKEY
    '''
    p[0] = NodeForStmt({'assign1': p[3], 'exp': p[5], 'assign2': p[7], 'block':p[10]})


def p_breakStmt(p):
    '''
    breakStmt : BREAK SEMICOLON
    '''
    p[0] = NodeBreakStmt({'breakStmt': p[1]})


def p_readStmt(p):
    '''
    readStmt : READ var SEMICOLON
    '''
    p[0] = NodeReadStmt({'var': p[2]})


def p_writeStmt(p):
    '''
    writeStmt : WRITE expList SEMICOLON
    '''
    p[0] = NodeWriteStmt({'expList': p[2]})


def p_returnStmt(p):
    '''
    returnStmt : RETURN SEMICOLON
               | RETURN exp SEMICOLON
    '''
    p[0] = NodeReturnStmt({'return': p[1], 'exp': p[2]})


def p_subCall(p):
    '''
    subCall : ID LPAREN expList RPAREN
    '''
    p[0] = NodeSubCall({'ID': p[1], 'expList': p[3]})


def p_assign(p):
    '''
    assign : var ASSIGN exp
           | var PLUSASSIGN exp
           | var MINUSASSIGN exp
           | var MULTASSIGN exp
           | var DIVIDEASSIGN exp
           | var MODASSIGN exp
    '''
    p[0] = NodeAssign({'var': p[1], 'exp': p[3]})


def p_expArithmetic(p):
    '''
    exp : exp PLUS exp
        | exp MINUS exp
        | exp MULT exp
        | exp DIVIDE exp
        | exp MOD exp
    '''
    p[0] = NodeExpArithimetic({'exp1': p[1], 'exp2': p[3]})


def p_expComparison(p):
    '''
    exp : exp EQUALS exp
        | exp DIFFERENT exp
        | exp GT exp
        | exp GTE exp
        | exp LT exp
        | exp LTE exp
    '''
    p[0] = NodeExpComparison({'exp1': p[1], 'exp2': p[3]})


def p_expLogic(p):
    '''
    exp : exp AND exp
        | exp OR exp
        | NOT exp
        | UMINUS exp
    '''
    if p[2] == '&&' or '||':
        p[0] = NodeExpLogic({'exp1': p[1], 'op': p[2],'exp2': p[3]})
    elif p[1] == '!' or '-':
        p[0] = NodeExpLogic({'op': p[1] ,'exp': p[2]})


def p_expTernary(p):
    '''
    exp : exp QMARK exp COLON exp
    '''
    p[0] = NodeExpTernary({'exp1': p[1], 'exp2': p[3], 'exp3': p[5]})


def p_expSubCall(p):
    '''
    exp : subCall
    '''
    p[0] = NodeExpSubCall({'subCall': p[1]})


def p_expVar(p):
    '''
    exp : var
    '''
    p[0] = NodeExpVar({'var': p[1]})


def p_expLiteral(p):
    '''
    exp : literal
    '''
    p[0] = NodeExpLiteral({'literal': p[1]})


def p_expMultParent(p):
    '''
    exp : LPAREN exp RPAREN
    '''
    p[0] = NodeExpMultParent({'exp': p[2]})


def p_var(p):
    '''
    var : ID
        | ID LCOR exp RCOR
    '''
    if len(p) == 2:
        p[0] = NodeVar({'ID': p[1]})
    elif len(p) == 5:
        p[0] = NodeVar({'ID': p[1], 'exp': p[3]})


def p_literal(p):
    '''
    literal : NUMBER
            | STRING_LITERAL
            | FALSE
            | TRUE
    '''
    p[0] = NodeLiteral({'literal': p[1]})


def p_paramList(p):
    '''
    paramList : paramSeq
              | empty
    '''
    if len(p) == 2:
        p[0] = NodeParamList({'paramSeq': p[1]})


def p_paramSeq(p):
    '''
    paramSeq : param
             | param COMMA paramSeq
    '''
    if len(p) == 2:
        p[0] = NodeParamSeq({'param': p[1]})
    elif len(p) == 4:
        p[0] = NodeParamSeq({'param': p[1], 'paramSeq': p[3]})


def p_param(p):
    '''
    param : type ID
          | type ID LCOR RCOR
    '''
    if len(p) == 3:
        p[0] = NodeParam({'type': p[1], 'ID': p[2]})
    elif len(p) == 5:
        p[0] = NodeParam({'type': p[1], 'ID': p[2], 'LCOR': p[3], 'RCOR': p[4]})


def p_varDecList(p):
    '''
    varDecList : varDec varDecList
               | empty
    '''
    if len(p) == 2:
        p[0] = NodeVarDecList({'empty': p[1]})
    if len(p) == 3:
        p[0] = NodeVarDecList({'varDec': p[1], 'varDecList': p[2]})





def p_stmtList(p):
    '''
    stmtList : stmt stmtList
             | empty
    '''
    if len(p) == 3:
        p[0] = NodeStmtList({'stmt': p[1], 'stmtList': p[2]})
    if len(p) == 2:
        p[0] = NodeStmtList({'empty': p[1]})


def p_literalSeq(p):
    '''
    literalSeq : literal
               | literal COMMA literalSeq
    '''
    if len(p) == 2:
        p[0] = NodeLiteralSeq({'literal': p[1]})
    elif len(p) == 4:
        p[0] = NodeLiteralSeq({'literal': p[1], 'literalSeq': p[3]})


def p_expList(p):
    '''
    expList : expSeq
            | empty
    '''
    if len(p) == 2:
        p[0] = NodeExpList({'expSeq': p[1]})


def p_expSeq(p):
    '''
    expSeq : exp
           | exp COMMA expSeq
    '''
    if len(p) == 2:
        p[0] = NodeExpSeq({'exp': p[1]})
    elif len(p) == 4:
        p[0] = NodeExpSeq({'exp': p[1], 'expSeq': p[3]})


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    last_cr = lex.lexer.lexdata.rfind('\n', 0, lex.lexer.lexpos)
    column = lex.lexer.lexpos - last_cr - 1
    if p:
        print("\nErro de sintaxe: Linha: %d, Coluna: %d, Tipo do erro: %s" % (p.lexer.lineno, column, p.type))
        parser.errok()
    else:
        print("Erro de sintaxe: EOF")

parser = yacc.yacc()
analisador_sintatico = parser.parse(Utils.find_files_test(Utils.archive, path_files_test))


def test_output_sintatico(result):
    #print (analisador_sintatico)
    #print (analisador_sintatico.dicionario['program'])
    #print (analisador_sintatico.dicionario['program'].dicionario['dec'])
    #print (analisador_sintatico.dicionario['program'].dicionario['dec'].dicionario['varDec'])
    #print (analisador_sintatico.dicionario['program'].dicionario['dec'].dicionario['varDec'].dicionario['type'])
    #print (analisador_sintatico.dicionario['program'].dicionario['dec'].dicionario['varDec'].dicionario['type'].dicionario['type'])
    with open(result, 'a') as file:
        file.write(str(analisador_sintatico) + '\n')
        file.close()
