class Node:
    pass


class Program(Node):
    def __init__(self, lines):
        self.lines = lines


# instrukcje złożone
class Block(Node):
    def __init__(self, lines):
        self.lines = lines


class FunctionCall(Node):
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg


class UnaryExpr(Node):
    def __init__(self, op, arg):
        self.op = "MINUS" if op == "-" else "TRANSPOSE"
        self.arg = arg


# wyrażenia binarne
class BinaryExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class IntNum(Node):
    def __init__(self, value):
        self.value = int(value)


class FloatNum(Node):
    def __init__(self, value):
        self.value = float(value)


class String(Node):
    def __init__(self, value):
        self.value = value


class Vector(Node):
    def __init__(self, values):
        self.values = values


class Matrix(Node):
    def __init__(self, rows):
        self.rows = rows
        self.shape = None
        self.stored_type = None


class Id(Node):
    def __init__(self, name):
        self.name = name


# instrukcje przypisania
class Assignment(Node):
    def __init__(self, op, variable, value):
        self.op = op
        self.variable = variable
        self.value = value


# instrukcje warunkowe if-else
class IfStatement(Node):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


# pętle: while oraz for
class WhileStatement(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class Range(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class ForStatement(Node):
    def __init__(self, variable, start, end, body):
        self.variable = variable
        self.range = Range(start, end)
        self.body = body


# instrukcje break, continue oraz return
class BreakStatement(Node):
    pass


class ContinueStatement(Node):
    pass


class ReturnStatement(Node):
    def __init__(self, value=None):
        self.value = value


# instrukcje print
class PrintStatement(Node):
    def __init__(self, values):
        self.values = values


# tablice oraz ich zakresy
class MatrixRefference(Node):
    def __init__(self, variable, reffs):
        self.variable = variable
        self.reffs = reffs


class Condition(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


# class Error(Node):
#     def __init__(self):
#         pass
