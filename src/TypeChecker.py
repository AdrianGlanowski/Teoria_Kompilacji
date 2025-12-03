#!/usr/bin/python
import AST
from SymbolTable import SymbolTable


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        print(f"visiting: {method}")
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):        
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit_Program(self, node):
        for line in node.lines:
            self.visit(line)

    def visit_Block(self, node):
        for line in node.lines:
            self.visit(line)

    def visit_FunctionCall(self, node):
        arg_type = self.visit(node.arg)
        if arg_type != "int":
            raise TypeError(f"Argument of a {node.name} function has to be of type int.")
        if node.arg.value <= 0:
            raise TypeError(f"Argument of a {node.name} function has to be positive.")
        return "matrix"

    def visit_UnaryExpr(self, node):
        arg_type = self.visit(node.arg)
        if node.op == "MINUS":
            if arg_type == "str":
                raise TypeError(f"Argument of negation can not be type str.")
            return arg_type
        #transpose
        else:
            if arg_type != "matrix":
                raise TypeError(f"Argument of transposition has to be matrix.")
            return arg_type
        
    def visit_BinaryExpr(self, node):

        type_left = self.visit(node.left)  
        type_right = self.visit(node.right) 
        print(type_left, type_right)

        if node.op == "*":
            if type_left == type_right == "matrix":
                if node.left.shape[1] != node.right.shape[0]:
                    raise TypeError("Number of columns in the first matrix does not equal the number of rows in the second matrix.")
                return "matrix"
            elif (type_left in ["int", "float"] and type_right == "matrix") or (type_left == "matrix" and type_right in ["int", "float"]):
                return "matrix"
            elif type_left == type_right == "int":
                return "int"
            elif type_left in ["int", "float"] and type_right in ["int", "float"]:
                return "float"
            else:
                raise TypeError(f"Unsupported operand types for *: {type_left} and {type_right}")
        
        if node.op == "/":
            if type_left == "matrix" and type_right in ["int", "float"]:
                return "matrix"
            elif type_left in ["int", "float"] and type_right in ["int", "float"]:
                return "float"
            
        if node.op in ['+', '-']:
            if type_left == type_right == 'int': 
                return 'int'
            elif type_left in ["int", "float"] and type_right in ["int", "float"]:
                return 'float'
            else:
                raise TypeError(f"Unsupported operand types for {node.op}: '{type_left}' and '{type_right}'")
        
        if node.op in ['.+', '.-', '.*', './']:
            print(node.left, node.right)
            print("jestem tu")
            if (type_left == "matrix" and type_right == "matrix"):
                if node.left.shape != node.right.shape:
                    raise TypeError("Cannot operate on matrices with different shapes.")
                return 'matrix'
            else:
                raise TypeError(f"Arguments for matrix operation have to be matrices, provided: {type_left} and {type_right}.")

    def visit_IntNum(self, node):
        return 'int'
 
    def visit_FloatNum(self, node):
        return 'float'

    def visit_String(self, node):
        return 'str'
    
    def visit_Vector(self, node):
        #teoretycznie nie mamy takiego typu, wiec co tu zrobic, moze po prostu return? 
        print(node.values)
        return  

    def visit_Matrix(self, node):
        row_length = len(node.rows[0].values)
        for i in range(1, len(node.rows)):
            if len(node.rows[i].values) != row_length:
                raise TypeError("Cannot initialize matrix with different row length.")
        node.shape = (len(node.rows), row_length)
        
        return 'matrix'

    def visit_Id(self, node):
        #return current var type?

        var_symbol = self.symbol_table.get(node.name)
        if not var_symbol:
            raise TypeError(f"Niezadeklarowana zmienna: '{node.name}'.")
        
        print(var_symbol)

        # TO DODAJE DYNAMICZNIE TYPE I SHAPE DO AST.Id
        node.type = var_symbol.type
        node.shape = var_symbol.shape
        # MIMO ZE TE POLA NIE ISTNIEJA W KLASIE AST.Id

        return var_symbol.type

    def visit_Assignment(self, node):

        if node.op == "=":
            value_type = self.visit(node.value)
            shape = getattr(node.value, 'shape', None)
            self.symbol_table.put(node.variable.name, value_type, shape)
        #czy mozna zrobic binary expr aktualnego typu vara z value?
        

    def visit_IfStatement(self, node):
        self.visit(node.condition)
        self.visit(node.then_branch)
        self.visit(node.else_branch)

    def visit_WhileStatement(self, node):
        self.visit(node.condition)
        self.visit(node.body)
    
    def visit_Range(self, node):
        start_type = self.visit(node.start)
        end_type = self.visit(node.end)
        if not (start_type == end_type == "int"):
            raise TypeError(f"Range has to be defined by two integers, provided: {start_type}:{end_type}")

    def visit_ForStatement(self, node):
        #czy visit variable?
        # self.visit(node.variable)
        self.visit(node.range)
        self.visit(node.body)

    # def visit_BreakStatement(self, node):
    #     return
    
    # def visit_ContinueStatement(self, node):
    #     return

    def visit_ReturnStatement(self, node):
        self.visit(node.value)

    def visit_PrintStatement(self, node):
        for element in self.values:
            type = self.visit(element)
            # if type != None: #czego nie mozna wyprintowac?
            #     raise TypeError(f"")
            
    def visit_MatrixRefference(self, node):
        #visit id - czy jest macierza?
        #ogolnie co tu zrobic?
        
        if len(node.reffs.values) != 2:
            raise TypeError("Matrix refference has to be 2 dimentional.")
        #czy referencja jest w zakresie
        # if node.reffs.values[0].value 
        return
    
    def visit_Condition(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        #comparable
        if node.op == "EQ" or node.op == "NEQ":
            if (left_type == right_type) or \
               (left_type in ["int", "float"] and right_type in ["int", "float"]):
                return
            raise TypeError(f"Cannot compare {left_type} and {right_type}.")
        
        #order
        if left_type in ["int", "float"] and right_type in ["int", "float"]:
            return
        raise TypeError(f"Cannot check order between {left_type} and {right_type}.")






        

    

    
        


