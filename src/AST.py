class Node:
    def __init__(self, line_no):
        self.line_no = line_no


class Program(Node):
    def __init__(self, line_no, lines):
        super().__init__(line_no)
        self.lines = lines

# instrukcje złożone
class Block(Node):
    def __init__(self, line_no, lines):
        super().__init__(line_no)
        self.lines = lines

class FunctionCall(Node):
    def __init__(self, line_no, name, arg):
        super().__init__(line_no)
        self.name = name
        self.arg = arg

class UnaryExpr(Node):
    def __init__(self, line_no, op, arg):
        super().__init__(line_no)
        self.op = "MINUS" if op == "-" else "TRANSPOSE"
        self.arg = arg

# wyrażenia binarne
class BinaryExpr(Node):
    def __init__(self, line_no, op, left, right):
        super().__init__(line_no)
        self.op = op
        self.left = left
        self.right = right

class IntNum(Node):
    def __init__(self, line_no, value):
        super().__init__(line_no)
        self.value = int(value)

class FloatNum(Node):
    def __init__(self, line_no, value):
        super().__init__(line_no)
        self.value = float(value)

class String(Node):
    def __init__(self, line_no, value):
        super().__init__(line_no)
        self.value = value

class Vector(Node):
    def __init__(self, line_no, values):
        super().__init__(line_no)
        self.values = values

class Matrix(Node):
    def __init__(self, line_no, rows):
        super().__init__(line_no)
        self.rows = rows

class Id(Node):
    def __init__(self, line_no, name):
        super().__init__(line_no)
        self.name = name

# instrukcje przypisania
class Assignment(Node):
    def __init__(self, line_no, op, variable, value):
        super().__init__(line_no)
        self.op = op
        self.variable = variable
        self.value = value

# instrukcje warunkowe if-else
class IfStatement(Node):
    def __init__(self, line_no, condition, then_branch, else_branch=None):
        super().__init__(line_no)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

# pętle: while oraz for
class WhileStatement(Node):
    def __init__(self, line_no, condition, body):
        super().__init__(line_no)
        self.condition = condition
        self.body = body

class Range(Node):
    def __init__(self, line_no, start, end):
        super().__init__(line_no)
        self.start = start
        self.end = end

class ForStatement(Node):
    def __init__(self, line_no, variable, start, end, body):
        super().__init__(line_no)
        self.variable = variable
        self.range = Range(line_no, start, end)
        self.body = body

# instrukcje break, continue oraz return
class BreakStatement(Node):
    def __init__(self, line_no):
        super().__init__(line_no)

class ContinueStatement(Node):
    def __init__(self, line_no):
        super().__init__(line_no)

class ReturnStatement(Node):
    def __init__(self, line_no, value=None):
        super().__init__(line_no)
        self.value = value

# instrukcje print
class PrintStatement(Node):
    def __init__(self, line_no, values):
        super().__init__(line_no)
        self.values = values

# tablice oraz ich zakresy
class MatrixRefference(Node):
    def __init__(self, line_no, variable, reffs):
        super().__init__(line_no)
        self.variable = variable
        self.reffs = reffs

class Condition(Node):
    def __init__(self, line_no, op, left, right):
        super().__init__(line_no)
        self.op = op
        self.left = left
        self.right = right
