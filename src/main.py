import sys
from scanner import Scanner
from parser import Mparser

def main():
        lexer = Scanner()
        parser = Mparser()

        filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
        with open(f"src/examples/{filename}", "r") as file:
            text = file.read()

        parser.parse(lexer.tokenize(text))


if __name__ == '__main__':
    main()