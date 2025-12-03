#!/usr/bin/python


class VariableSymbol:

    def __init__(self, name, type, shape):
        self.name = name
        self.type = type
        self.shape = shape

class Scope:
    symbols = dict()

    def __init__(self, parent, level):
        self.parent = parent
        self.level = level

    def put(self, name, type, shape):
        self.symbols[name] = VariableSymbol(name, type, shape)
    
    def get(self, name):
        return self.symbols[name]

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
    
    def put(self, name, type, shape):
        self.current_scope.put(name, type, shape)

