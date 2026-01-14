class NumericType:
    pass

class IntType(NumericType):
    def __str__(self):
        return "IntType"

class FloatType(NumericType):
    def __str__(self):
        return "FloatType"

class MatrixType:
    def __init__(self, shape, stored_type):
        self.shape = shape
        self.stored_type = stored_type
    def __str__(self):
        return f"MatrixType({self.shape[0]}, {self.shape[1]}) of {str(self.stored_type)}"
class StringType:
    def __str__(self):
        return "StringType"

class UndefinedType:
    def __str__(self):
        return "UndefinedType"