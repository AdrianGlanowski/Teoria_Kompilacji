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
        op = node.op

        # --- Zmienne pomocnicze dla czytelności ---
        is_numeric_left = type_left in ["int", "float"]
        is_numeric_right = type_right in ["int", "float"]
        is_matrix_left = type_left == "matrix"
        is_matrix_right = type_right == "matrix"

        # Ustalanie typu wynikowego dla operacji na samych liczbach
        # int op int -> int (chyba że dzielenie, ale tu upraszczamy)
        # float op int -> float
        numeric_result_type = "float"
        if type_left == "int" and type_right == "int":
            numeric_result_type = "int"

        # ==========================================
        # 1. OPERATORY ELEMENT-WISE (z kropką)
        #    .+, .-, .*, ./
        # ==========================================
        if op in ['.+', '.-', '.*', './']:
            # A. Macierz .op Macierz (musi być ten sam rozmiar)
            if is_matrix_left and is_matrix_right:
                if node.left.shape != node.right.shape:
                    self.add_error(f"Element-wise operation {op} requires same shapes", node.line_no)
                return "matrix"
            
            # B. Skalar .op Macierz lub Macierz .op Skalar (Broadcasting)
            elif (is_numeric_left and is_matrix_right) or (is_matrix_left and is_numeric_right):
                return "matrix"
                
            # C. Skalar .op Skalar (traktujemy jak zwykłe działanie)
            elif is_numeric_left and is_numeric_right:
                return numeric_result_type
                
            else:
                self.add_error(f"Invalid types for {op}: {type_left}, {type_right}", node.line_no)
                return "matrix" # Zwracamy cokolwiek, by nie wysypać reszty

        # ==========================================
        # 2. STANDARDOWE MNOŻENIE (*)
        # ==========================================
        elif op == "*":
            # A. Macierz * Macierz (Algebra: colsA == rowsB)
            if is_matrix_left and is_matrix_right:
                # Uwaga: shape[0] to wiersze, shape[1] to kolumny
                if node.left.shape[1] != node.right.shape[0]:
                    self.add_error(f"Matrix multiplication error: {node.left.shape} vs {node.right.shape}", node.line_no)
                return "matrix"
            
            # B. Skalar * Macierz (Skalowanie)
            elif (is_numeric_left and is_matrix_right) or (is_matrix_left and is_numeric_right):
                return "matrix"
                
            # C. Skalar * Skalar
            elif is_numeric_left and is_numeric_right:
                return numeric_result_type
                
            else:
                self.add_error(f"Invalid types for *: {type_left}, {type_right}", node.line_no)

        # ==========================================
        # 3. STANDARDOWE DZIELENIE (/)
        # ==========================================
        elif op == "/":
            # A. Macierz / Skalar (Dozwolone skalowanie)
            if is_matrix_left and is_numeric_right:
                return "matrix"
                
            # B. Skalar / Skalar
            elif is_numeric_left and is_numeric_right:
                return "float" # Dzielenie zazwyczaj daje float
                
            # C. BŁĘDY: Macierz / Macierz ORAZ Skalar / Macierz
            elif is_matrix_right: 
                self.add_error("Division by a matrix is not supported. Use './' for element-wise division.", node.line_no)
                return "matrix" # Dummy return
                
            else:
                self.add_error(f"Invalid types for /: {type_left}, {type_right}", node.line_no)

        # ==========================================
        # 4. DODAWANIE I ODEJMOWANIE (+, -)
        # ==========================================
        elif op in ['+', '-']:
            # A. Macierz +/- Macierz (ten sam rozmiar)
            if is_matrix_left and is_matrix_right:
                if node.left.shape != node.right.shape:
                    self.add_error(f"Matrix addition/subtraction requires same shapes", node.line_no)
                return "matrix"
                
            # B. Skalar +/- Macierz (Broadcasting - opcjonalne, ale wygodne)
            elif (is_numeric_left and is_matrix_right) or (is_matrix_left and is_numeric_right):
                return "matrix"
                
            # C. Skalar +/- Skalar
            elif is_numeric_left and is_numeric_right:
                return numeric_result_type
                
            else:
                self.add_error(f"Invalid types for {op}: {type_left}, {type_right}", node.line_no)

        return "float" # Fallback

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
            self.add_error(f"Range has to be defined by two integers, provided: {start_type}:{end_type}", node.line_no)

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
