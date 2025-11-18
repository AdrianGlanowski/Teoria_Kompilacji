import sys
from scanner import Scanner
from parser import Mparser
from ParserError import ParserError


if __name__ == '__main__':

    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, "r") as file:
        text = file.read()


    lexer = Scanner()
    parser = Mparser()

    try:
        ast = parser.parse(lexer.tokenize(text))
    except ParserError:
        print(
                f"{'\033[91m'}File couldn't be parsed, aborting.{'\033[0m'}"
            )
    # ast.printTree()
