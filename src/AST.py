# wyrażenia binarne,
# wyrażenia relacyjne,
# instrukcje przypisania,
# instrukcje warunkowe if-else,
# pętle: while oraz for,
# instrukcje break, continue oraz return,
# instrukcje print,
# instrukcje złożone,
# tablice oraz ich zakresy.

from ParserError import ParserError

class Root:
    pass

class Program(Root):
    def __init__(self, lines):
        self.lines = lines

class Block(Root):
    def __init__(self, lines):
        self.lines = lines

class Statement(Program):
    pass

class Function(Statement):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Expr(Statement):
    pass

class UnaryExpr(Expr):
    def __init__(self, op, arg):
        self.op = "MINUS" if op == "-" else "TRANSPOSE"
        self.arg = arg

class BinExpr(Expr):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class IntNum(Expr):
    def __init__(self, value):
        self.value = value

class FloatNum(Expr):
    def __init__(self, value):
        self.value = value

class Variable(Expr):
    def __init__(self, name):
        self.name = name

class Vector(Expr):
    def __init__(self, values):
        self.values = values

class Matrix(Expr):
    def __init__(self, rows):
        self.rows = rows


class Assignment(Statement):
    def __init__(self, variable, op, value):
        self.variable = variable
        self.op = op
        self.value = value


class IfStatement(Statement):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ForStatement(Statement):
    def __init__(self, variable, start, end, body):
        self.variable = variable
        self.start = start
        self.end = end
        self.body = body


class BreakStatement(Statement):
    def __init__(self):
        pass


class ContinueStatement(Statement):
    def __init__(self):
        pass


class ReturnStatement(Statement):
    def __init__(self, value=None):
        self.value = value


class PrintStatement(Statement):
    def __init__(self, value):
        self.value = value




class Refference():
    pass

class VariableRefference(Refference):
    def __init__(self, name):
        self.name = name

class MatrixRefference(Refference):
    def __init__(self, variable, reffs):
        self.variable = variable
        if not all(isinstance(v, int) or (isinstance(v, Expr) and not (isinstance(v, FloatNum))) for v in reffs.values):
            raise ParserError("Arrays can be only refferenced by ints")
        self.reffs = reffs


# class Error(Node):
#     def __init__(self):
#         pass
