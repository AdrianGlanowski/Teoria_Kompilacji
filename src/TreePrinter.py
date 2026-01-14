import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:
    def __init__(self, indent_symbol='|  '):
        self.indent_symbol = indent_symbol

    def safePrintTree(obj, indent):
        """Helper function to handle primitives and objects with `printTree`."""
        prefix = obj.indent_symbol * indent
        if obj is not None:
            obj.printTree(indent)
        else:
            print(f"{prefix}None")

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        for line in self.lines:
            TreePrinter.safePrintTree(line, indent)

    @addToClass(AST.Assignment)
    def printTree(self: AST.Assignment, indent=0):
        print(self.indent_symbol * indent + f"{self.op}")
        TreePrinter.safePrintTree(self.variable, indent + 1)
        TreePrinter.safePrintTree(self.value, indent + 1)
    
    @addToClass(AST.BinaryExpr)
    def printTree(self: AST.BinaryExpr, indent=0):
        print(self.indent_symbol * indent + f"{self.op}")
        TreePrinter.safePrintTree(self.left, indent + 1)
        TreePrinter.safePrintTree(self.right, indent + 1)

    @addToClass(AST.UnaryExpr)
    def printTree(self: AST.UnaryExpr, indent=0):
        print(self.indent_symbol * indent + f"{self.op}")
        TreePrinter.safePrintTree(self.arg, indent + 1)

    @addToClass(AST.IntNum)
    def printTree(self: AST.IntNum, indent=0):
        print(self.indent_symbol * indent + f"{self.value}")

    @addToClass(AST.String)
    def printTree(self: AST.String, indent=0):
        print(self.indent_symbol * indent + f"{self.value}")
    
    @addToClass(AST.FloatNum)
    def printTree(self: AST.FloatNum, indent=0):
        print(self.indent_symbol * indent + f"{self.value}")

    @addToClass(AST.FunctionCall)
    def printTree(self: AST.FunctionCall, indent=0):
        print(self.indent_symbol * indent + f"{self.name}")
        TreePrinter.safePrintTree(self.args, indent + 1)
    
    @addToClass(AST.Matrix)
    def printTree(self: AST.Matrix, indent=0):
        print(self.indent_symbol * indent + f"MATRIX")
        for row in self.rows:
            TreePrinter.safePrintTree(row, indent + 1)

    @addToClass(AST.Vector)
    def printTree(self: AST.Vector, indent=0):
        print(self.indent_symbol * indent + f"VECTOR")
        for value in self.values:
            TreePrinter.safePrintTree(value, indent + 1)

    @addToClass(AST.Id)
    def printTree(self: AST.Id, indent=0):
        print(self.indent_symbol * indent + f"{self.name}")
    
    @addToClass(AST.MatrixRefference)
    def printTree(self: AST.MatrixRefference, indent=0):
        print(self.indent_symbol * indent + f"REF")
        TreePrinter.safePrintTree(self.variable, indent + 1)
        TreePrinter.safePrintTree(self.reffs, indent + 1)

    @addToClass(AST.ForStatement)
    def printTree(self: AST.ForStatement, indent=0):
        print(self.indent_symbol * indent + f"FOR")
        TreePrinter.safePrintTree(self.variable, indent + 1)
        TreePrinter.safePrintTree(self.range, indent + 1)
        TreePrinter.safePrintTree(self.body, indent + 1)

    @addToClass(AST.Range)
    def printTree(self: AST.Range, indent=0):
        print(self.indent_symbol * indent + f"RANGE")
        TreePrinter.safePrintTree(self.start, indent + 1)
        TreePrinter.safePrintTree(self.end, indent + 1)

    @addToClass(AST.Block)
    def printTree(self: AST.Block, indent=0):
        for line in self.lines:
            TreePrinter.safePrintTree(line, indent)

    @addToClass(AST.PrintStatement)
    def printTree(self: AST.PrintStatement, indent=0):
        print(self.indent_symbol * indent + f"PRINT")
        for value in self.values:
            TreePrinter.safePrintTree(value, indent+1)
    
    @addToClass(AST.IfStatement)
    def printTree(self: AST.IfStatement, indent=0):
        print(self.indent_symbol * indent + f"IF")
        for value in self.values:
            TreePrinter.safePrintTree(value, indent)
        
    @addToClass(AST.IfStatement)
    def printTree(self: AST.IfStatement, indent=0):
        print(self.indent_symbol * indent + f"IF")
        TreePrinter.safePrintTree(self.condition, indent + 1)
        TreePrinter.safePrintTree(self.then_branch, indent + 1)
        if self.else_branch:
            print(self.indent_symbol * indent + f"ELSE")
            TreePrinter.safePrintTree(self.else_branch, indent + 1)
    
    @addToClass(AST.WhileStatement)
    def printTree(self: AST.WhileStatement, indent=0):
        print(self.indent_symbol * indent + f"WHILE")
        TreePrinter.safePrintTree(self.condition, indent + 1)
        TreePrinter.safePrintTree(self.body, indent + 1)

    @addToClass(AST.BreakStatement)
    def printTree(self, indent=0):
        print(self.indent_symbol * indent + "BREAK")

    @addToClass(AST.ContinueStatement)
    def printTree(self, indent=0):
        print(self.indent_symbol * indent + "CONTINUE")

    @addToClass(AST.ReturnStatement)
    def printTree(self: AST.ReturnStatement, indent=0):
        print(self.indent_symbol * indent + "RETURN")
        if self.value:
            TreePrinter.safePrintTree(self.value, indent + 1)

    @addToClass(AST.Condition)
    def printTree(self: AST.Condition, indent=0):
        print(self.indent_symbol * indent + f"{self.op}")
        TreePrinter.safePrintTree(self.left, indent + 1)
        TreePrinter.safePrintTree(self.right, indent + 1)

