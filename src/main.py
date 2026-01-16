import sys
from scanner import Scanner
from parser import Mparser
from errors import ParserError
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker
from Interpreter import Interpreter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    parser = Mparser()

    try:
        ast = parser.parse(lexer.tokenize(text))
    except ParserError as pe:
        print(
                f"{'\033[91m'}File couldn't be parsed, aborting.{'\033[0m'}"
            )
        if pe.args:
            print(f"\033[91mReason: {pe}\033[0m")

        exit(1)
    # ast.printTree()


    # Below code shows how to use visitor
    typeChecker = TypeChecker()
    try:
        typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)
    finally:
        typeChecker.print_errors()
        if len(typeChecker.errors) > 0:
            exit(1)

    # Below code shows how to use visitor
    interpreter = Interpreter(False)
    interpreter.visit(ast)
    
    # in future
    # ast.accept(OptimizationPass1())
    # ast.accept(OptimizationPass2())
    # ast.accept(CodeGenerator())
    