SRC = '''

pp = {X:X+Y}
pp @ 0

'''

class Sym:
    tag = 'sym'
    def __init__(self, V): self.val = V ; self.nest = [] ; self.attr = {}
    def __iadd__(self,o): self.nest.append(o) ; return self
    def __repr__(self): return self.head()
    def head(self): return '<%s:%s>' % (self.tag, self.val)
    def dump(self, depth=0):
        S = '\n' + '\t' * depth + self.head()
        for i in self.attr:
            S += '\n' + '\t' * (depth + 1) + i + ' ='
            S += self.attr[i].dump(depth + 2)
        for i in self.nest: S += i.dump(depth + 1)
        return S
    def eval(self, E):
        try: return E.attr[self.val]
        except KeyError: return self
    def eq(self, o, E): E.attr[self.val] = o; return o

class Op(Sym):
    tag = 'op'
    def eval(self, E):
        # nested eval (non-lazy)
        if self.val == '=': self.nest[1] = self.nest[1].eval(E)
        else: Sym.eval(self, E)
        # call operator methods
        if self.val == '=': return self.nest[0].eq(self.nest[1], E)
        return self
    
class Lambda(Sym): tag = 'lambda'

class Env(Sym): tag = 'env'
glob = Env('global')

import ply.lex  as lex
import ply.yacc as yacc

tokens = [ 'SYM' , 'OP' , 'LC','RC','COLON' , 'EQ' ]

t_ignore = ' \t\r'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_LC(t):
    r'\{'
    t.value = Op(t.value) ; return t
def t_RC(t):
    r'\}'
    t.value = Op(t.value) ; return t
def t_COLON(t):
    r'\:'
    t.value = Op(t.value) ; return t
def t_EQ(t):
    r'\='
    t.value = Op(t.value) ; return t
def t_OP(t):
    r'[\@\+]'
    t.value = Op(t.value) ; return t
def t_SYM(t):
    r'[a-zA-Z0-9_]+'
    t.value = Sym(t.value) ; return t

def p_REPL_none(p):
    ' REPL : '
def p_REPL_recur(p):
    ' REPL : REPL ex '
    print p[2].dump()
    print '-' * 20,
    print p[2].eval(glob).dump()
    print '-' * 20,
    print glob.dump()
    print '=' * 40
def p_ex_sym(p):
    ' ex : SYM '
    p[0] = p[1]
def p_ex_eq(p):
    ' ex : SYM EQ ex '
    p[0] = p[2] ; p[0] += p[1] ; p[0] += p[3]
def p_ex_binop(p):
    ' ex : ex OP ex '
    p[0] = p[2] ; p[0] += p[1] ; p[0] += p[3]
def p_ex_lambda(p):
    ' ex : LC lambda RC '
    p[0] = p[2]
def p_lambda_new(p):
    ' lambda : '
    p[0] = Lambda('')
def p_lambda_par(p):
    ' lambda : lambda SYM COLON '
    p[0] = p[1] ; p[0].attr[p[2].val] = p[2]
def p_lambda_ex(p):
    ' lambda : lambda ex '
    p[0] = p[1] ; p[0] += p[2]

def t_error(t): print 'lexer/error',t
def p_error(p): print 'parse/error',p

lexer = lex.lex() ; lexer.input(SRC)
# for i in iter(lexer.token,None): print i
yacc.yacc(debug=False, write_tables=False).parse(SRC)  
