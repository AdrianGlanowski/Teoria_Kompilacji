#!/usr/bin/python
import AST
import SymbolTable as st

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

    def visit_Program(self, node):
        for line in node.lines:
            self.visit(line)

    def visit_Block(self, node):
        for line in node.lines:
            self.visit(line)

    def visit_FunctionCall(self, node):
        
        arg_type = self.visit(node.arg)
        if arg_type != "int":
            self.symbol_table.add_error(f"Argument of a {node.name} function has to be of type int.")
        if node.arg.value <= 0:
            self.symbol_table.add_error(f"Argument of a {node.name} function has to be positive.")
        node.shape = (node.arg.value, node.arg.value)
        node.stored_type = "int"
        
        return "matrix"

    def visit_UnaryExpr(self, node):
        arg_type = self.visit(node.arg)
        
        if node.op == "MINUS":
            if arg_type == "str":
                self.symbol_table.add_error(f"Argument of negation can not be type str.")
            return arg_type
        #transpose
        else:
            if arg_type != "matrix":
                self.symbol_table.add_error(f"Argument of transposition has to be matrix.")
            symbol = self.symbol_table.get(node.arg.name)
            node.shape = (symbol.shape[1], symbol.shape[0])
            return arg_type
        
    def visit_BinaryExpr(self, node):
        type_left = self.visit(node.left)  
        type_right = self.visit(node.right)

        if node.op == "*":
            if type_left == type_right == "matrix":
                if node.left.shape[1] != node.right.shape[0]:
                    self.symbol_table.add_error("Number of columns in the first matrix does not equal the number of rows in the second matrix.")
                return "matrix"
            elif (type_left in ["int", "float"] and type_right == "matrix") or (type_left == "matrix" and type_right in ["int", "float"]):
                return "matrix"
            elif type_left == type_right == "int":
                return "int"
            elif type_left in ["int", "float"] and type_right in ["int", "float"]:
                return "float"
            else:
                self.symbol_table.add_error(f"Unsupported operand types for *: {type_left} and {type_right}")
        
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
                self.symbol_table.add_error(f"Unsupported operand types for {node.op}: '{type_left}' and '{type_right}'")
        
        if node.op in ['.+', '.-', '.*', './']:
            if (type_left == "matrix" and type_right == "matrix"):
                if node.left.shape != node.right.shape:
                    self.symbol_table.add_error("Cannot operate on matrices with different shapes.")
                return 'matrix'
            else:
                self.symbol_table.add_error(f"Arguments for matrix operation have to be matrices, provided: {type_left} and {type_right}.")

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
                self.symbol_table.add_error("Cannot initialize matrix with different row length.")
        node.shape = (len(node.rows), row_length)

        first_element_type = self.visit(node.rows[0].values[0])
        for row in node.rows:
            for val in row.values:
                element_type = self.visit(val)
                if element_type != first_element_type:
                    self.symbol_table.add_error("All elements of the matrix must be of the same type.")
                
        node.stored_type = first_element_type
        
        return 'matrix'

    def visit_Id(self, node):
        var_symbol = self.symbol_table.get(node.name)

        # TO DODAJE DYNAMICZNIE TYPE I SHAPE DO AST.Id, jesli id odnosi sie do matrix
        if isinstance(var_symbol, st.MatrixSymbol):
            node.type = var_symbol.type
            node.shape = var_symbol.shape
        # MIMO ZE TE POLA NIE ISTNIEJA W KLASIE AST.Id
        
        return var_symbol.type

    def visit_Assignment(self, node):

        if node.op == "=":
            value_type = self.visit(node.value)

            #co robi ten pierwszy if???
            if isinstance(node.variable, AST.MatrixRefference):
                stored_type = self.visit(node.variable)
                if stored_type != value_type:
                    self.symbol_table.add_error("Value is of different type than matrix.")
                
                return

            if value_type == "matrix":
                shape = getattr(node.value, 'shape', None)
                stored_type = getattr(node.value, 'stored_type', None)
                self.symbol_table.put_matrix(node.variable.name, value_type, shape, stored_type)
            else:
                self.symbol_table.put_variable(node.variable.name, value_type)

        else: #TODO inne operatory
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
            self.symbol_table.add_error(f"Range has to be defined by two integers, provided: {start_type}:{end_type}")

    def visit_ForStatement(self, node):
        #czy visit variable?
        # self.visit(node.variable)
        self.symbol_table.push_scope()
        print("entering into: ", self.symbol_table.current_scope.level)
        self.symbol_table.put_variable(node.variable.name, "int")
        self.visit(node.range)
        self.visit(node.body)
        
        print("deleting variables: ", self.symbol_table.current_scope.symbols)
        self.symbol_table.pop_scope()
        print("exiting into: ", self.symbol_table.current_scope.level)

    def visit_BreakStatement(self, node):
        #test scope
        if self.symbol_table.current_scope.level == 0:
            self.symbol_table.add_error("Nothing to break out of.")
    
    def visit_ContinueStatement(self, node):
        if self.symbol_table.current_scope.level == 0:
            self.symbol_table.add_error("Nothing to continue.")

    def visit_ReturnStatement(self, node):
        if self.symbol_table.current_scope.level == 0:
            self.symbol_table.add_error("Nowhere to return.")
        
        if node.value != None:
            self.visit(node.value)

    def visit_PrintStatement(self, node):
        for element in node.values:
            self.visit(element)
            
    def visit_MatrixRefference(self, node):
        symbol = self.symbol_table.get(node.variable.name)

        if symbol.type != "matrix":
            self.symbol_table.add_error("Cannot refference non-matrix.")
        
        if len(node.reffs.values) != 2:
            self.symbol_table.add_error("Matrix refference has to be 2 dimentional.")

        type1 = self.visit(node.reffs.values[0])
        type2 = self.visit(node.reffs.values[1])

        if type1 != "int" or type2 != "int":
            self.symbol_table.add_error("Matrix refference indices have to be of type int.")
        
        if node.reffs.values[0].value >= symbol.shape[0] or node.reffs.values[1].value >= symbol.shape[1]:
            self.symbol_table.add_error("Matrix refference out of bounds.")
        
        return symbol.stored_type
    
    def visit_Condition(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        #comparable
        if node.op == "EQ" or node.op == "NEQ":
            if (left_type == right_type) or \
               (left_type in ["int", "float"] and right_type in ["int", "float"]):
                return
            self.symbol_table.add_error(f"Cannot compare {left_type} and {right_type}.")
        
        #order
        if left_type in ["int", "float"] and right_type in ["int", "float"]:
            return
        self.symbol_table.add_error(f"Cannot check order between {left_type} and {right_type}.")




        

    

    
        


