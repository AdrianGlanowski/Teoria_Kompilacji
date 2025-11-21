#!/usr/bin/python
import AST


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
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

    def visit_BinaryExpr(self, node):
                                          # alternative usage,
                                          # requires definition of accept method in class Node
        type1 = self.visit(node.left)     # type1 = node.left.accept(self) 
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.op

        if op == '*':
            if type1 == 'matrix' and type2 == 'matrix':
                return 'matrix'
            elif (type1 in ['int', 'float'] and type2 == 'matrix') or (type1 == 'matrix' and type2 in ['int', 'float']):
                return 'matrix'
            else:
                raise TypeError(f"Unsupported operand types for *: '{type1}' and '{type2}'")
        if op in ['+', '-', '*', '/']:
            if type1 == 'int' and type2 == 'int':
                return 'int'
            elif (type1 == 'int' and type2 == 'float') or (type1 == 'float' and type2 == 'int') or (type1 == 'float' and type2 == 'float'):
                return 'float'
            else:
                raise TypeError(f"Unsupported operand types for {op}: '{type1}' and '{type2}'")
        elif op in ['==', '!=', '<', '>', '<=', '>=']:
            if (type1 in ['int', 'float'] and type2 in ['int', 'float']):
                return 'bool'
            else:
                raise TypeError(f"Unsupported operand types for {op}: '{type1}' and '{type2}'")

 

    def visit_Id(self, node):
        print("Visiting Id:", node.name)
        return 'var'

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_Program(self, node):
        for line in node.lines:
            self.visit(line)

    def visit_IfStatement(self, node):
        pass

    def visit_WhileStatement(self, node):
        pass

    def visit_ForStatement(self, node):
        pass

    def visit_Assignment(self, node):
        print("Assignment variable:", node.variable)
        print("Assignment value:", node.value)
        type1 = self.visit(node.variable)
        print(type1)
        type2 = self.visit(node.value)



        

    

    
        


