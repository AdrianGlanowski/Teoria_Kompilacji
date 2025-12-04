#!/usr/bin/python


class VariableSymbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class MatrixSymbol:
    def __init__(self, name, type, shape, stored_type):
        self.name = name
        self.type = type
        self.shape = shape
        self.stored_type = stored_type

class Scope:

    def __init__(self, parent, level):
        self.parent = parent
        self.level = level
        self.symbols = dict()

    def put_variable(self, name, type):
        self.symbols[name] = VariableSymbol(name, type)
    
    def put_matrix(self, name, type, shape, stored_type):
        self.symbols[name] = MatrixSymbol(name, type, shape, stored_type)
    
    def get(self, name):

        if name in self.symbols:
            return self.symbols[name]
        
        if self.parent == None:
            raise TypeError(f"Undeclared variable {name}.")
        
        return self.parent.get(name)
         

    def get_parent(self):
        return self.parent
    


class SymbolTable:
    def __init__(self):
        self.global_scope = Scope(None, 0)
        self.current_scope = self.global_scope

    def push_scope(self):
        self.current_scope = Scope(self.current_scope, self.current_scope.level+1)

    def pop_scope(self):
        self.current_scope = self.current_scope.get_parent()

    def get(self, name):
        return self.current_scope.get(name)
    
    def put_variable(self, name, type):
        self.current_scope.put_variable(name, type)

    def put_matrix(self, name, type, shape, stored_type):
        self.current_scope.put_matrix(name, type, shape, stored_type)

