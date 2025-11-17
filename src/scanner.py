# pyright: reportUndefinedVariable=false
import sys
from sly import Lexer


class Scanner(Lexer):

    tokens = {
            DOT_ADD, DOT_SUB, DOT_MUL, DOT_DIV,
            EQ, NEQ, GTE, LTE,
            ADD_ASSIGN, SUB_ASSIGN, MUL_ASSIGN, DIV_ASSIGN,

            ID, INTNUM,
            IF, ELSE, FOR, WHILE, BREAK, CONTINUE, RETURN, EYE, ZEROS, ONES, PRINT,
            FLOATNUM, INTNUM, STRING, PRINT
            }

    ignore = ' \t'
    ignore_comment = r'\#.*'
    literals = '+-*/()[]{}\',:;>=<'

    #matrixes
    DOT_ADD = r'\.\+'
    DOT_SUB = r'\.\-'
    DOT_MUL = r'\.\*'
    DOT_DIV = r'\.\/'

    #relative operators
    EQ = r'=='
    NEQ = r'!='
    GTE = r'>='
    LTE = r'<='

    #assign
    ADD_ASSIGN = r'\+='
    SUB_ASSIGN = r'-='
    MUL_ASSIGN = r'\*='
    DIV_ASSIGN = r'/='

    #first is .num, second is num., last is special case of first with 0. 
    FLOATNUM = r'(0?\.\d+|[1-9]\d*\.\d*|0\.\d*)((E|e)(-|\+)?\d+)?'  
    INTNUM = r'(0|[1-9]\d*)((E|e)\+?\d+)?'   
    STRING = r'\"[^"\n]*\"|\'[^\'\n]*\''
    

    #keywords
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE 
    ID['break'] = BREAK 
    ID['continue'] = CONTINUE 
    ID['return'] = RETURN 
    ID['eye'] = EYE 
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    ID['print'] = PRINT
    
    #general
    ID = r'[_a-zA-Z][_a-zA-Z0-9]*'
 
    @_(r'\n+')
    def count_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f'{'\033[91m'}Line {self.lineno}: Bad character {t.value[0]}{'\033[0m'}')
        self.index += 1

if __name__ == '__main__':

    lexer = Scanner()

    filename = sys.argv[1] if len(sys.argv) > 1 else "lab1/examples/example.txt"
    with open(filename, "r") as file:
        text = file.read()

    for tok in lexer.tokenize(text):
        print(f"{tok.lineno}: {tok.type}({tok.value})")


  
