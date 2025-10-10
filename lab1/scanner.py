import sys
from sly import Lexer


class Scanner(Lexer):

# słowa kluczowe: if, else, for, while
# słowa kluczowe: break, continue oraz return
# słowa kluczowe: eye, zeros oraz ones
# słowa kluczowe: print

# liczby całkowite
# liczby zmiennoprzecinkowe
# stringi
# Dla rozpoznanych leksemów stworzony skaner powinien zwracać:
# odpowiadający token
# rozpoznany leksem
# numer linii
# Następujące znaki powinny być pomijane:
# białe znaki: spacje, tabulatory, znaki nowej linii
# komentarze: komentarze rozpoczynające się znakiem # do znaku końca linii

    tokens = {PLUS, MINUS, TIMES, DIVIDE,
            L_PARENTHESIS, R_PARENTHESIS, L_SQ_PARENTHESIS, R_SQ_PARENTHESIS, L_CURL_PARENTHESIS, R_CURL_PARENTHESIS,
            COMMA, COLON, SEMICOLON,
            DOT_ADD, DOT_SUB, DOT_MUL, DOT_DIV, TRANSPOSE,
            EQ, NEQ, BT, BTE, LT, LTE, 
            ASSIGN, ADD_ASSIGN, SUB_ASSIGN, MUL_ASSIGN, DIV_ASSIGN, 
            ID, INTNUM}

    
    ignore = ' \t'
    literals = {'+', '-', '*', '/', '(', ')', '[', ']', '{', '}', '\'', ',', ':', ';', '>', '=', '<'}

    #matrixes
    DOT_ADD = r'\.\+'
    DOT_SUB = r'\.\-'
    DOT_MUL = r'\.\*'
    DOT_DIV = r'\.\/'


    #relative operators
    EQ = r'=='
    NEQ = r'!='
    BTE = r'>='
    LTE = r'<='


    #assign
    ADD_ASSIGN = r'\+='
    SUB_ASSIGN = r'-='
    MUL_ASSIGN = r'\*='
    DIV_ASSIGN = r'/='

    #ogolne
    ID = r'[_a-zA-Z][_a-zA-Z0-9]*'
    # proper_number = r'[1-9][0-9]*|0'
    INTNUM = fr'[(-)?0(E\+|e)?0]|0'

    

    
    
if __name__ == '__main__':

    lexer = Scanner()

    filename = sys.argv[1] if len(sys.argv) > 1 else "lab1/examples/example.txt"
    with open(filename, "r") as file:
        text = file.read()

    for tok in lexer.tokenize(text):
        print(f"{tok.lineno}: {tok.type}({tok.value})")


  