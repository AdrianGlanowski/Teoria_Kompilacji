class NumericType:
    pass

class IntType(NumericType):
    pass

class FloatType(NumericType):
    pass

class MatrixType:
    def __init__(self, shape, stored_type):
        self.shape = shape
        self.stored_type = stored_type

class String:
    pass

class UndefinedType:
    pass