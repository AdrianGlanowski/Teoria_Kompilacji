#!/usr/bin/python
import AST


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        print(f"visiting: {method}")
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
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

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)



class TypeChecker(NodeVisitor):

    def visit_Program(self, node):
        for line in node.lines:
            self.visit(line)

    def visit_Block(self, node):
        for line in node.lines:
            self.visit(line)

    def visit_FunctionCall(self, node):
        arg_type = self.visit(node.args)
        if arg_type != "int":
            raise TypeError(f"Argument of a {node.name} function has to be of type int.")
        if node.args.value <= 0:
            raise TypeError(f"Argument of a {node.name} function has to be positive.")
        return "matrix"

    def visit_UnaryExpr(self, node):
        arg_type = self.visit(node.arg)
        if node.op == "MINUS":
            if arg_type == "str":
                raise TypeError(f"Argument of negation can not be type str.")
            return arg_type
        else:
            if arg_type != "matrix":
                raise TypeError(f"Argument of transposition has to be matrix.")
            return arg_type
        
    def visit_BinaryExpr(self, node):

        type_left = self.visit(node.left)  
        type_right = self.visit(node.right) 

        if node.op == "*":
            if type_left == type_right == "matrix":
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
            #co z result = int/int? czy int(result), wiec int jak w C czy float czy jak?
            elif type_left in ["int", "float"] and type_right in ["int", "float"]:
                return "float"
            
        if node.op in ['+', '-']:
            if type_left == type_right == 'int': 
                return 'int'
            elif type_left in ["int", "float"] and type_right in ["int", "float"]:
                return 'float'
            elif type_left == type_right == "matrix":
                return "matrix"
            else:
                raise TypeError(f"Unsupported operand types for {node.op}: '{type_left}' and '{type_right}'")
        
        if node.op in ['DOT_ADD', 'DOT_SUB', 'DOT_MUL', 'DOT_DIV']:
            if (type_left == "matrix" and type_right == "matrix"):
                #TODO wymiary macierzy dla operacji
                return 'matrix'
            else:
                raise TypeError(f"Arguments for matrix operation have to be matrixes, provided: {type_left} and {type_right}.")

    def visit_IntNum(self, node):
        return 'int'
 
    def visit_FloatNum(self, node):
        return 'float'

    def visit_String(self, node):
        return 'str'
    
    def visit_Vector(self, node):
        #teoretycznie nie mamy takiego typu, wiec co tu zrobic, moze po prostu return? 
        return 'vector'

    def visit_Matrix(self, node):
        column_count = len(node.rows[0].values)
        for i in range(1, len(node.rows)):
            if len(node.rows[i].values) != column_count:
                raise TypeError("Cannot initialize matrix with different row length.")
        node.shape = (len(node.rows), column_count)
        
        return 'matrix'

    def visit_Id(self, node):
        #return current var type?
        return 'var'

    def visit_Assignment(self, node):
        if node.op == "=":
            self.visit(node.value)
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
        self.visit(node.variable)
        self.visit(node.range)
        self.visit(node.body)

    def visit_BreakStatement(self, node):
        return
    
    def visit_ContinueStatement(self, node):
        return

    def visit_ReturnStatement(self, node):
        self.visit(node.value)

    def visit_PrintStatement(self, node):
        for element in self.values:
            type = self.visit(element)
            if type != None: #czego nie mozna wyprintowac?
                raise TypeError(f"")
            
    #co z wektorami?

    def visit_MatrixRefference(self, node):
        #visit id - czy jest macierza?
        #ogolnie co tu zrobic?
        return
    
    def visit_Condition(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        if node.op == "EQ" or node.op == "NEQ":
            if (left_type != right_type or left_type not in ["str", "matrix", "int", "float"]) or \
               (left_type not in ["int", "float"] or not right_type not in ["int", "float"]):
                raise TypeError(f"Cannot compare {left_type} and {right_type}.")
            else:
                return
        else:
            if left_type not in ["int", "float"] or not right_type not in ["int", "float"]:
                raise TypeError(f"Cannot check order between {left_type} and {right_type}.")
            else:
                return




        

    

    
        


