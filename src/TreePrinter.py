import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:
    def safePrintTree(obj, indent):
        """Helper function to handle primitives and objects with `printTree`."""
        prefix = "|  " * indent
        if isinstance(obj, (int, float, str)):
            print(f"{prefix}{obj}")
        elif obj is not None:
            obj.printTree(indent)
        else:
            print(f"{prefix}None")


    @addToClass(AST.Program)
    def printTree(self, indent=0):
        for line in self.lines:
            TreePrinter.safePrintTree(line, indent)

    @addToClass(AST.Assignment)
    def printTree(self: AST.Assignment, indent=0):
        print("|  " * indent + f"{self.op}")
        TreePrinter.safePrintTree(self.variable, indent + 1)
        TreePrinter.safePrintTree(self.value, indent + 1)
    
    @addToClass(AST.BinExpr)
    def printTree(self: AST.BinExpr, indent=0):
        print("|  " * indent + f"{self.op}")
        TreePrinter.safePrintTree(self.left, indent + 1)
        TreePrinter.safePrintTree(self.right, indent + 1)

    @addToClass(AST.UnaryExpr)
    def printTree(self: AST.UnaryExpr, indent=0):
        print("|  " * indent + f"{self.op}")
        TreePrinter.safePrintTree(self.arg, indent + 1)

    @addToClass(AST.IntNum)
    def printTree(self: AST.IntNum, indent=0):
        print("|  " * indent + f"{self.value}")
    
    @addToClass(AST.FloatNum)
    def printTree(self: AST.FloatNum, indent=0):
        print("|  " * indent + f"{self.value}")

    @addToClass(AST.FunctionCall)
    def printTree(self: AST.FunctionCall, indent=0):
        print("|  " * indent + f"{self.name}")
        TreePrinter.safePrintTree(self.args, indent + 1)
    
    @addToClass(AST.Matrix)
    def printTree(self: AST.Matrix, indent=0):
        print("|  " * indent + f"MATRIX")
        for row in self.rows:
            TreePrinter.safePrintTree(row, indent + 1)

    @addToClass(AST.Vector)
    def printTree(self: AST.Vector, indent=0):
        print("|  " * indent + f"VECTOR")
        for value in self.values:
            TreePrinter.safePrintTree(value, indent + 1)

    @addToClass(AST.Id)
    def printTree(self: AST.Id, indent=0):
        print("|  " * indent + f"{self.name}")
    
    @addToClass(AST.MatrixRefference)
    def printTree(self: AST.MatrixRefference, indent=0):
        print("|  " * indent + f"REF")
        TreePrinter.safePrintTree(self.variable, indent + 1)
        TreePrinter.safePrintTree(self.reffs, indent + 1)

    @addToClass(AST.ForStatement)
    def printTree(self: AST.ForStatement, indent=0):
        print("|  " * indent + f"FOR")
        TreePrinter.safePrintTree(self.variable, indent + 1)
        TreePrinter.safePrintTree(self.range, indent + 1)
        TreePrinter.safePrintTree(self.body, indent + 1)

    @addToClass(AST.Range)
    def printTree(self: AST.Range, indent=0):
        print("|  " * indent + f"RANGE")
        TreePrinter.safePrintTree(self.start, indent + 1)
        TreePrinter.safePrintTree(self.end, indent + 1)

    @addToClass(AST.Block)
    def printTree(self: AST.Block, indent=0):
        for line in self.lines:
            TreePrinter.safePrintTree(line, indent)

    @addToClass(AST.PrintStatement)
    def printTree(self: AST.PrintStatement, indent=0):
        print("|  " * indent + f"PRINT")
        for value in self.values:
            TreePrinter.safePrintTree(value, indent)
        
    @addToClass(AST.IfStatement)
    def printTree(self: AST.IfStatement, indent=0):
        print("|  " * indent + f"IF")
        TreePrinter.safePrintTree(self.condition, indent + 1)
        TreePrinter.safePrintTree(self.then_branch, indent + 1)
        if self.else_branch:
            print("|  " * indent + f"ELSE")
            TreePrinter.safePrintTree(self.else_branch, indent + 1)
    
    @addToClass(AST.WhileStatement)
    def printTree(self: AST.WhileStatement, indent=0):
        print("|  " * indent + f"WHILE")
        TreePrinter.safePrintTree(self.condition, indent + 1)
        TreePrinter.safePrintTree(self.body, indent + 1)

    @addToClass(AST.BreakStatement)
    def printTree(self, indent=0):
        print("|  " * indent + "BREAK")

    @addToClass(AST.ContinueStatement)
    def printTree(self, indent=0):
        print("|  " * indent + "CONTINUE")

    @addToClass(AST.ReturnStatement)
    def printTree(self: AST.ReturnStatement, indent=0):
        print("|  " * indent + "RETURN")
        if self.value:
            TreePrinter.safePrintTree(self.value, indent + 1)

    @addToClass(AST.Condition)
    def printTree(self: AST.Condition, indent=0):
        print("|  " * indent + f"{self.op}")
        TreePrinter.safePrintTree(self.left, indent + 1)
        TreePrinter.safePrintTree(self.right, indent + 1)

    # @addToClass(AST.Error)
    # def printTree(self, indent=0):
    #     pass    
    #     # fill in the body


