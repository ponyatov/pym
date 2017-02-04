SRC = '''

pp = {X:X+Y}

'''

class Sym:
    def __init__(self, V): self.val = V
    def __repr__(self): return self.head()
    def head(self): return '<%s>' % self.val

import ply.lex  as lex
import ply.yacc as yacc

t_ignore = ' \t\r\n'
tokens = [ 'SYM' ]

def t_SYM(t):
    r'[a-zA-Z0-9_]+|[\=\+\{\:\}]'
    t.value = Sym(t.value) ; return t

def p_REPL_none(p):
    r' REPL : '
def p_REPL_recur(p):
    r' REPL : REPL SYM '
    print p[2]

def t_error(t): print 'lexer/error',t
def p_error(p): print 'parse/error',p

lex.lex()
yacc.yacc(debug=False, write_tables=False).parse(SRC)  
