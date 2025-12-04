import sys
from TypeChecker import TypeChecker
from scanner import Scanner
from parser import Mparser
from TreePrinter import TreePrinter
from ParserError import ParserError


if __name__ == '__main__':

    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, "r") as file:
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
    typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)
    typeChecker.print_errors()
    



