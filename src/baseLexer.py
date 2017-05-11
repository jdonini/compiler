import ply.lex as lex


class BaseLexer(object):
    """ Herdando o Base para utilizar o linestart para ajustar contador de Coluna"""
    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.linestart = 0

    def __iter__(self):
        return iter(self.lexer)

    def token(self):
        return self.lexer.token()

    def input(self, data):
        self.lexer.input(data)
