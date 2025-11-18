# wyrażenia binarne,
# wyrażenia relacyjne,
# instrukcje przypisania,
# instrukcje warunkowe if-else,
# pętle: while oraz for,
# instrukcje break, continue oraz return,
# instrukcje print,
# instrukcje złożone,
# tablice oraz ich zakresy.


class Root:
    pass


class Statement(Root):
    pass


class BinExpr(Statement):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class IntNum(BinExpr):
    def __init__(self, value):
        self.value = value


class FloatNum(BinExpr):
    def __init__(self, value):
        self.value = value


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




# class Variable(Node):
#     def __init__(self, name):
#         self.name = name


# class Condition(Node):
#     def __init__(self, op, left, right):
#         self.op = op
#         self.left = left
#         self.right = right


# class Array(Node):
#     def __init__(self, elements):
#         self.elements = elements


# class Block(Node):
#     def __init__(self, statements):
#         self.statements = statements


# class ArrayRange(Node):
#     def __init__(self, array, start, end):
#         self.array = array
#         self.start = start
#         self.end = end



# class Error(Node):
#     def __init__(self):
#         pass
