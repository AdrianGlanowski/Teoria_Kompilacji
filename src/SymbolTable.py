#!/usr/bin/python


class VariableSymbol:

    def __init__(self, name, type, shape):
        self.name = name
        self.type = type
        self.shape = shape

class Scope:
    variables = dict()

    def __init__(self, parent, level):
        self.parent = parent
        self.level = level

    def put(self, name, type, shape): # put variable symbol
        self.variables[name] = VariableSymbol(name, type, shape)
    
    def get(self, name): # get variable symbol
        return self.variables[name]

    def get_parent(self):
        return self.parent


class SymbolTable:
    def __init__(self):
        self.global_scope = Scope(None, 0)
        self.current_scope = self.global_scope

    def push_scope(self):
        self.current_scope =  Scope(self.current_scope, self.current_scope.level+1)

    def pop_scope(self):
        self.current_scope = self.current_scope.get_parent()

    def get_type(self, name):
        return self.current_scope.get(name).type
    
    def add(self, name, _type, shape=None):
        self.current_scope.put(name, _type, shape)

