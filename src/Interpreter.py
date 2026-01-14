
import AST
from SymbolTable import SymbolTable
from Memory import MemoryStack
from Exceptions import  *
from visit import *
import sys
import operator
import numpy as np

sys.setrecursionlimit(10000)

class Interpreter(object):
    def __init__(self, debug = False):
        self.memory = MemoryStack()
        self.operations = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            ".+": operator.add,
            ".-": operator.sub,
            ".*": operator.mul,
            "./": operator.truediv,
            "==": operator.eq,
            "!=": operator.ne,
            "<": operator.lt,
            ">": operator.gt,
            "<=": operator.le,
            ">=": operator.ge,
            "<": operator.lt,
            "<": operator.lt,
        }
        self.function_calls = {
            "zeros": lambda x: np.zeros((x, x)),
            "ones": lambda x: np.ones((x, x)),
            "eye": lambda x: np.eye(x)
        }
        self.debug = debug
    
    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        for line in node.lines:
            self.visit(line)
            
    @when(AST.Block)
    def visit(self, node):
        for line in node.lines:
            self.visit(line)

    @when(AST.FunctionCall)
    def visit(self, node):    
        size = self.visit(node.arg)
        func = self.function_calls[node.name]
        return func(size)
    
    @when(AST.UnaryExpr)
    def visit(self, node):
        value = self.visit(node.arg)
        return -value if node.op == "MINUS" else value.T
    
    @when(AST.BinaryExpr)
    def visit(self, node):
        value_left = self.visit(node.left)
        op = self.operations[node.op]
        value_right = self.visit(node.right)
        
        return op(value_left, value_right)
    
    @when(AST.IntNum)
    def visit(self, node):
        return node.value
    
    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value
    
    @when(AST.Vector)
    def visit(self, node):
        row = [self.visit(value) for value in node.values]
        return np.array(row)
    
    @when(AST.Matrix)
    def visit(self, node):
        rows = [self.visit(row) for row in node.rows]
        return np.array(rows)
    
    @when(AST.Id)
    def visit(self, node):
        return self.memory.get(node.name)
        
    @when(AST.Assignment)
    def visit(self, node):
        value = self.visit(node.value)

        if node.op == "=":

            if isinstance(node.variable, AST.MatrixRefference):
                matrix = self.memory.get(node.variable.variable.name)
                arg1 = self.visit(node.variable.reffs.values[0])
                arg2 = self.visit(node.variable.reffs.values[1])

                matrix[arg1][arg2] = value
                self.memory.put(node.variable.variable.name, matrix)
                self.memory_dump(node)

                return

            self.memory.put(node.variable.name, value)
            self.memory_dump(node)
            return
        else:
            op = self.operations[node.op[0]]
            variable = node.variable.name
            self.memory.put(variable, op(self.memory.get(variable), value))
            self.memory_dump(node)

    
    @when(AST.IfStatement)
    def visit(self, node):
        condition = self.visit(node.condition)
        if condition:
            self.visit(node.then_branch)
        elif node.else_branch != None:
            self.visit(node.else_branch)
    
    @when(AST.WhileStatement)
    def visit(self, node):
        self.memory.push()
        while (self.visit(node.condition)):
            #execute code
            try:
                self.visit(node.body)  
            except BreakException:
                print("\33[35mBreak happened\033[0m")
                break
            except ContinueException:
                print("\33[35mContinue happened\033[0m")
                continue
            except ReturnValueException as exception:
                print(f"\33[35mFor some reason return({exception.value}) happened\033[0m")
                continue
            
        self.memory.pop()

    @when(AST.Range)
    def visit(self, node):
        return (self.visit(node.start), self.visit(node.end))

    @when(AST.ForStatement)
    def visit(self, node):
        self.memory.push()
        for i in range(*self.visit(node.range)):
            #add/update variable
            self.memory.put(node.variable.name, i)
            self.memory_dump(node)

            #execute code
            try:
                self.visit(node.body)  
            except BreakException:
                print("\33[35mBreak happened\033[0m")
                break
            except ContinueException:
                print("\33[35mContinue happened\033[0m")
                continue
            except ReturnValueException as exception:
                print(f"\33[35mFor some reason return({exception.value}) happened\033[0m")
                continue

        self.memory.pop()
        
    @when(AST.BreakStatement)
    def visit(self, node):
        raise BreakException
    
    @when(AST.ContinueStatement)
    def visit(self, node):
        raise ContinueException

    @when(AST.ReturnStatement)
    def visit(self, node):
        value = self.visit(node.value)
        raise ReturnValueException(value)

    @when(AST.PrintStatement)
    def visit(self, node):
        print_args = []
        for element in node.values:
            print_args.append(self.visit(element))
        print(*print_args)

    @when(AST.MatrixRefference)
    def visit(self, node):
        refference = self.memory.get(node.variable.name)
        arg1 = self.visit(node.reffs.values[0])
        arg2 = self.visit(node.reffs.values[1])

        return refference[arg1][arg2]

    @when(AST.Condition)
    def visit(self, node):
        value_left = self.visit(node.left)
        op = self.operations[node.op]
        value_right = self.visit(node.right)
       
        return op(value_left, value_right)
            
    def memory_dump(self, node):
        if self.debug:
            print(f"\33[33mMemory state for line {node.line_no}: ", self.memory.current_memory.variables, "\033[0m\n")
        return

        




