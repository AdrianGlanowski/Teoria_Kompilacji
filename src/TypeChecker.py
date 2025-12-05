#!/usr/bin/python
import AST
import SymbolTable as st
from errors import UndeclaredVariableError
from custom_types import MatrixType, IntType, FloatType, String, UndefinedType, NumericType

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


def isinstance2(type_left, type_right, type1, type2=None):
    if type2 is None:
        type2 = type1
        
    if isinstance(type_left, type1) and isinstance(type_right, type2):
        return True
    return False


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
            return st.VariableSymbol(name, UndefinedType())

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
            print(dir(node), node.arg, node.op, arg_type)
            if arg_type != "matrix":
                self.add_error(f"Argument of transposition has to be matrix", node.line_no)
                return "undefined"
    
            node.shape = (node.arg.shape[1], node.arg.shape[0])
            node.stored_type = node.arg.stored_type

            return arg_type
    


    def visit_BinaryExpr(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)

        if node.op == "*":
            if isinstance2(type_left, type_right, MatrixType):
                if type_left.shape[1] != type_right.shape[0]:
                    self.add_error("Number of columns in the first matrix does not equal the number of rows in the second matrix", node.line_no)
                    return UndefinedType()
 
                return MatrixType((type_left.shape[0], type_right.shape[1]), type_left.stored_type)
            
            if isinstance2(type_left, type_right, NumericType, MatrixType):
                return MatrixType(type_right.shape, type_right.stored_type)
            
            if isinstance2(type_left, type_right, MatrixType, NumericType):
                return MatrixType(type_left.shape, type_left.stored_type)

            # elif type_left == type_right == "int":
            if isinstance2(type_left, type_right, IntType):
                return IntType()
            
            # elif type_left in ["int", "float"] and type_right in ["int", "float"]:
            if isinstance2(type_left, type_right, NumericType):
                return FloatType()
            
            self.add_error(f"Unsupported operand types for *: {type_left} and {type_right}", node.line_no)
            return UndefinedType()

        if node.op == "/":

            # if type_left == "matrix" and type_right in ["int", "float"]:
            if isinstance2(type_left, type_right, MatrixType, NumericType):
                return MatrixType(type_left.shape, FloatType())
            
            # elif type_left in ["int", "float"] and type_right in ["int", "float"]:
            if isinstance2(type_left, type_right, NumericType):
                return FloatType()
            
        if node.op in ['+', '-']:
            # if type_left == type_right == 'int': 
            if isinstance2(type_left, type_right, IntType):
                return IntType()
            
            if isinstance2(type_left, type_right, NumericType):
                return FloatType()
            
            self.add_error(f"Unsupported operand types for {node.op}: '{type_left}' and '{type_right}'", node.line_no)
            return UndefinedType()

        if node.op in ['.+', '.-', '.*', './']:
            # if (type_left == "matrix" and type_right == "matrix"):
            if isinstance2(type_left, type_right, MatrixType):
                # if node.left.shape != node.right.shape:
                if type_left.shape != type_right.shape:
                    self.add_error("Cannot operate on matrices with different shapes", node.line_no)
                    return UndefinedType()
                
                # dodawanie dwoch intow jest floatem!
                return MatrixType(type_left.shape, FloatType())
            
            self.add_error(f"Arguments for matrix operation have to be matrices, provided: {type_left} and {type_right}", node.line_no)
            return UndefinedType()
            
    def visit_IntNum(self, node):
        return IntType()
 
    def visit_FloatNum(self, node):
        return FloatType()

    def visit_String(self, node):
        return String()
    
    def visit_Vector(self, node):
        return

    def visit_Matrix(self, node):
        row_length = len(node.rows[0].values)
        for i in range(1, len(node.rows)):
            if len(node.rows[i].values) != row_length:
                self.add_error("Cannot initialize matrix with different row length", node.line_no)
                return UndefinedType()

        first_element_type = self.visit(node.rows[0].values[0])
        for row in node.rows:
            for val in row.values:
                element_type = self.visit(val)
                if not isinstance(element_type, type(first_element_type)):
                    self.add_error("All elements of the matrix must be of the same type", node.line_no)
                    return UndefinedType()
        
        return MatrixType((len(node.rows), row_length), first_element_type)

    def visit_Id(self, node):
        symbol = self.symbol_table_safe_get(node.name, node.line_no)

        # TO DODAJE DYNAMICZNIE TYPE I SHAPE DO AST.Id, jesli id odnosi sie do matrix
        # if isinstance(symbol, st.MatrixSymbol):
            # return MatrixType(symbol.shape, symbol.stored_type)
            # node.type = symbol.type
            # node.shape = symbol.shape
            # node.stored_type = symbol.stored_type
        # MIMO ZE TE POLA NIE ISTNIEJA W KLASIE AST.Id
        
        return symbol.type

    def visit_Assignment(self, node):
        value_type = self.visit(node.value)

        if node.op == "=":
            if isinstance(node.variable, AST.MatrixRefference):
                stored_type = self.visit(node.variable)
                if not isinstance(value_type, type(stored_type)):
                    self.add_error("Value is of different type than matrix", node.line_no)
                
                return

            self.symbol_table.put(node.variable.name, value_type)

        elif node.op == "+=" or node.op == "-=":
            variable_type = self.visit(node.variable)
            
            if not isinstance(variable_type, NumericType):
                self.add_error(f"Left side has to be of numeric type to use {node.op}, provided {variable_type}", node.line_no)
            
            if not isinstance(value_type, NumericType):
                self.add_error(f"Right side has to be of numeric type to use {node.op}, provided {value_type}", node.line_no)

        
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
        if not isinstance2(start_type, end_type, IntType):
            self.add_error(f"Range has to be defined by two integers, provided: {start_type}:{end_type}", node.line_no)

    def visit_ForStatement(self, node):
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

        if not isinstance(symbol.type, MatrixType):
            self.add_error("Cannot refference non-matrix", node.line_no)
        
        if len(node.reffs.values) != 2:
            self.add_error("Matrix refference has to be 2 dimentional", node.line_no)

        if len(node.reffs.values) >= 2:
            type1 = self.visit(node.reffs.values[0])
            type2 = self.visit(node.reffs.values[1])

            if not isinstance2(type1, type2, IntType):
                self.add_error("Matrix refference indices have to be of type int", node.line_no)
            
            if node.reffs.values[0].value >= symbol.type.shape[0] or node.reffs.values[1].value >= symbol.type.shape[1]:
                self.add_error("Matrix refference out of bounds", node.line_no)
            
        return symbol.type.stored_type
    
    def visit_Condition(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        #comparable
        if node.op == "EQ" or node.op == "NEQ":
            if (type(left_type) == type(right_type)) or \
                isinstance2(left_type, right_type, NumericType):

                return
            
            self.add_error(f"Cannot compare {left_type} and {right_type}", node.line_no)
        
        #order
        # if left_type in ["int", "float"] and right_type in ["int", "float"]:
        if isinstance2(left_type, right_type, NumericType):
            return
        
        self.add_error(f"Cannot check order between {left_type} and {right_type}", node.line_no)
