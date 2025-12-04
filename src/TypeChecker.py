#!/usr/bin/python
import AST
import SymbolTable as st
from errors import UndeclaredVariableError

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        print(f"visiting: {method}")
        visitor = getattr(self, method, None)
        return visitor(node)

    # def generic_visit(self, node):        
    #     if isinstance(node, list):
    #         for elem in node:
    #             self.visit(elem)
    #     else:
    #         for child in node.children:
    #             if isinstance(child, list):
    #                 for item in child:
    #                     if isinstance(item, AST.Node):
    #                         self.visit(item)
    #             elif isinstance(child, AST.Node):
    #                 self.visit(child)



class TypeChecker(NodeVisitor):

    def __init__(self):
        self.symbol_table = st.SymbolTable()
        self.errors = []

    def add_error(self, message, line_no):
        self.errors.append((message, line_no))

    def symbol_table_safe_get(self, name, line_no):
        try:
            return self.symbol_table.get(name)
        except UndeclaredVariableError:
            self.add_error(f"Undeclared variable {name}", line_no)

            # return dummy symbol to avoid crashes???
            return st.VariableSymbol(name, "undefined")

    def print_errors(self):
        for error, line in self.errors:
            print(f"\033[91mType Error: {error} at line {line}\033[0m")

    def visit_Program(self, node):
        for line in node.lines:
            self.visit(line)

    def visit_Block(self, node):
        for line in node.lines:
            self.visit(line)

    def visit_FunctionCall(self, node):
        
        arg_type = self.visit(node.arg)
        if arg_type != "int":
            self.add_error(f"Argument of a {node.name} function has to be of type int", node.line_no)
        if node.arg.value <= 0:
            self.add_error(f"Argument of a {node.name} function has to be positive", node.line_no)
        node.shape = (node.arg.value, node.arg.value)
        node.stored_type = "int"
        
        return "matrix"

    def visit_UnaryExpr(self, node):
        arg_type = self.visit(node.arg)

        
        if node.op == "MINUS":
            if arg_type == "str":
                self.add_error(f"Argument of negation can not be type str", node.line_no)
            return arg_type
        #transpose
        else:
            if arg_type != "matrix":
                self.add_error(f"Argument of transposition has to be matrix", node.line_no)
            symbol = self.symbol_table_safe_get(node.arg.name, node.line_no)
            node.shape = (symbol.shape[1], symbol.shape[0])
            return arg_type
    
    def visit_BinaryExpr(self, node):
        type_left = self.visit(node.left)  
        type_right = self.visit(node.right)

        if node.op == "*":
            if type_left == type_right == "matrix":
                if node.left.shape[1] != node.right.shape[0]:
                    self.add_error("Number of columns in the first matrix does not equal the number of rows in the second matrix", node.line_no)
                    return "undefined"
                return "matrix"
            elif (type_left in ["int", "float"] and type_right == "matrix") or (type_left == "matrix" and type_right in ["int", "float"]):
                return "matrix"
            elif type_left == type_right == "int":
                return "int"
            elif type_left in ["int", "float"] and type_right in ["int", "float"]:
                return "float"
            else:
                self.add_error(f"Unsupported operand types for *: {type_left} and {type_right}", node.line_no)
                return "undefined"

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
                self.add_error(f"Unsupported operand types for {node.op}: '{type_left}' and '{type_right}'", node.line_no)
                return "undefined"

        if node.op in ['.+', '.-', '.*', './']:
            if (type_left == "matrix" and type_right == "matrix"):
                if node.left.shape != node.right.shape:
                    self.add_error("Cannot operate on matrices with different shapes", node.line_no)
                return 'matrix'
            else:
                self.add_error(f"Arguments for matrix operation have to be matrices, provided: {type_left} and {type_right}", node.line_no)
                return "matrix"

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
                self.add_error("Cannot initialize matrix with different row length", node.line_no)
                return "matrix"
        node.shape = (len(node.rows), row_length)

        first_element_type = self.visit(node.rows[0].values[0])
        for row in node.rows:
            for val in row.values:
                element_type = self.visit(val)
                if element_type != first_element_type:
                    self.add_error("All elements of the matrix must be of the same type", node.line_no)
                
        node.stored_type = first_element_type
        
        return 'matrix'

    def visit_Id(self, node):
        symbol = self.symbol_table_safe_get(node.name, node.line_no)

        # TO DODAJE DYNAMICZNIE TYPE I SHAPE DO AST.Id, jesli id odnosi sie do matrix
        if isinstance(symbol, st.MatrixSymbol):
            node.type = symbol.type
            node.shape = symbol.shape
        # MIMO ZE TE POLA NIE ISTNIEJA W KLASIE AST.Id
        
        return symbol.type

    def visit_Assignment(self, node):

        if node.op == "=":
            value_type = self.visit(node.value)

            #co robi ten pierwszy if???
            if isinstance(node.variable, AST.MatrixRefference):
                stored_type = self.visit(node.variable)
                if stored_type != value_type:
                    self.add_error("Value is of different type than matrix", node.line_no)
                
                return

            if value_type == "matrix":
                shape = getattr(node.value, 'shape', None)
                stored_type = getattr(node.value, 'stored_type', None)
                self.symbol_table.put_matrix(node.variable.name, value_type, shape, stored_type)
            else:
                self.symbol_table.put_variable(node.variable.name, value_type)

        elif node.op == "+=": #TODO inne operatory
        #czy mozna zrobic binary expr aktualnego typu vara z value?
            pass
        

    def visit_IfStatement(self, node):
        self.visit(node.condition)
        self.visit(node.then_branch)
        if node.else_branch != None:
            self.visit(node.else_branch)

    def visit_WhileStatement(self, node):
        self.symbol_table.push_scope()
        self.visit(node.condition)
        self.visit(node.body)
        self.symbol_table.pop_scope()

    def visit_Range(self, node):
        start_type = self.visit(node.start)
        end_type = self.visit(node.end)
        if not (start_type == end_type == "int"):
            self.add_error(f"Range has to be defined by two integers, provided: {start_type}:{end_type}", node.line_no)

    def visit_ForStatement(self, node):
        #czy visit variable?
        # self.visit(node.variable)
        self.symbol_table.push_scope()
        print("\33[33mentering into: ", self.symbol_table.current_scope.level, "\033[0m")
        self.symbol_table.put_variable(node.variable.name, "int")
        self.visit(node.range)
        self.visit(node.body)
        
        print("\33[35mdeleting variables: ", self.symbol_table.current_scope.symbols, "\033[0m")
        self.symbol_table.pop_scope()
        print("\33[33mexiting into: ", self.symbol_table.current_scope.level, "\033[0m")

    def visit_BreakStatement(self, node):
        #test scope
        if self.symbol_table.current_scope.level == 0:
            self.add_error("Nothing to break out of", node.line_no)
    
    def visit_ContinueStatement(self, node):
        if self.symbol_table.current_scope.level == 0:
            self.add_error("Nothing to continue", node.line_no)

    def visit_ReturnStatement(self, node):
        if self.symbol_table.current_scope.level == 0:
            self.add_error("Nowhere to return", node.line_no)
        
        if node.value != None:
            self.visit(node.value)

    def visit_PrintStatement(self, node):
        for element in node.values:
            self.visit(element)
            
    def visit_MatrixRefference(self, node):
        symbol = self.symbol_table_safe_get(node.variable.name, node.line_no)

        if symbol.type != "matrix":
            self.add_error("Cannot refference non-matrix", node.line_no)
        
        if len(node.reffs.values) != 2:
            self.add_error("Matrix refference has to be 2 dimentional", node.line_no)

        if len(node.reffs.values) >= 2:
            type1 = self.visit(node.reffs.values[0])
            type2 = self.visit(node.reffs.values[1])

            if type1 != "int" or type2 != "int":
                self.add_error("Matrix refference indices have to be of type int", node.line_no)
            
            if node.reffs.values[0].value >= symbol.shape[0] or node.reffs.values[1].value >= symbol.shape[1]:
                self.add_error("Matrix refference out of bounds", node.line_no)
            
        return symbol.stored_type
    
    def visit_Condition(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        #comparable
        if node.op == "EQ" or node.op == "NEQ":
            if (left_type == right_type) or \
               (left_type in ["int", "float"] and right_type in ["int", "float"]):
                return
            self.add_error(f"Cannot compare {left_type} and {right_type}", node.line_no)
        
        #order
        if left_type in ["int", "float"] and right_type in ["int", "float"]:
            return
        self.add_error(f"Cannot check order between {left_type} and {right_type}", node.line_no)
