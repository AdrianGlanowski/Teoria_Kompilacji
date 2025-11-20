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

    @addToClass(AST.Function)
    def printTree(self: AST.Function, indent=0):
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

    @addToClass(AST.VariableRefference)
    def printTree(self: AST.VariableRefference, indent=0):
        print("|  " * indent + f"{self.name}")
    
    @addToClass(AST.MatrixRefference)
    def printTree(self: AST.MatrixRefference, indent=0):
        print("|  " * indent + f"REF")
        TreePrinter.safePrintTree(self.variable, indent + 1)
        TreePrinter.safePrintTree(self.reffs, indent + 1)


        
    
    
    # @addToClass(AST.Error)
    # def printTree(self, indent=0):
    #     pass    
    #     # fill in the body


