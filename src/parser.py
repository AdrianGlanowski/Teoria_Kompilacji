# pyright: reportUndefinedVariable=false
from sly import Parser
from scanner import Scanner


class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'

    # Zadanie polega na stworzeniu parsera języka do operacji macierzowych. 
    # Parser powinien rozponawać (akceptować) kod źródłowy w formie tokenów, bądz zglaszać bląd parsingu w przypadku nieprawidlowego wejścia. 
    # Parser powinien rozpoznawać następujące konstrukcje:
    # wyrażenia binarne, w tym operacje macierzowe 'element po elemencie'
    # wyrażenia relacyjne,
    # negację unarną,
    # transpozycję macierzy,
    # inicjalizację macierzy konkretnymi wartościami,
    # macierzowe funkcje specjalne,
    # instrukcję przypisania, w tym różne operatory przypisania
    # instrukcję warunkową if-else,
    # pętle: while and for,
    # instrukcje break, continue oraz return,
    # instrukcję print,
    # instrukcje złożone,
    # tablice i macierze oraz ich indeksy (ewentualnie zakresy).

    precedence = (
        ("left", '+', '-'),
        ("left", '*', '/'),
        ("right", UMINUS),
        ("right", ELSE)
    )
    
    #---------------------------
    #program to ciąg statementow
    @_('statements')
    def program(self, p):
        pass

    #---------------------------
    #statementy
    @_('statements statement')
    def statements(self, p):
        pass
    
    @_('statement')
    def statements(self, p):
        pass

    @_('assign ";"')
    def statement(self, p):
        pass

    #break dziala wszedzie, a powinien tylko w petli
    @_('BREAK ";"')
    def statement(self, p):
        pass
    #continue dziala wszedzie, a powinien tylko w petli
    @_('CONTINUE ";"')
    def statement(self, p):
        pass

    @_('RETURN return_values ";"')
    def statement(self, p):
        pass
    
    @_('add_assign ";"')
    def statement(self, p):
        pass

    @_('sub_assign ";"')
    def statement(self, p):
        pass

    @_('mul_assign ";"')
    def statement(self, p):
        pass

    @_('div_assign ";"')
    def statement(self, p):
        pass

    @_('PRINT ID ";"')
    def statement(self, p):
        pass

    @_('PRINT print_values ";"')
    def statement(self, p):
        pass

    @_('if_statement')
    def statement(self, p):
        pass

    @_('IF "(" relative ")" statement')
    def if_statement(self, p):
        pass

    @_('IF "(" relative ")" "{" statement "}"')
    def if_statement(self, p):
        pass

    @_('if_statement ELSE if_statement')
    def if_statement(self, p):
        pass

    @_('if_statement ELSE statements')
    def if_statement(self, p):
        pass


    # @_('IF "(" relative ")" statement ELSE statement')
    # def if_statement(self, p):
    #     pass        

    # @_('IF "(" relative ")" "{" statements "}" ELSE if_statement')
    # def if_statement(self, p):
    #     pass

    # @_('IF "(" relative ")" "{" statements "}" ELSE "{" statements "}"')
    # def if_statement(self, p):
    #     pass

    @_('while_statement')
    def statement(self, p):
        pass

    @_('WHILE "(" relative ")" "{" statements "}"')
    def while_statement(self, p):
        pass

    @_('WHILE "(" relative ")" statement')
    def while_statement(self, p):
        pass

    @_('for_statement')
    def statement(self, p):
        pass
    
    @_('FOR ID "=" expr ":" expr "{" statements "}"')
    def for_statement(self, p):
        pass
    
    @_('FOR ID "=" expr ":" expr statement')
    def for_statement(self, p):
        pass
   
    #---------------------------
    #polecenia
    @_('ID "=" expr')
    def assign(self, p):
        pass

    @_('ID "=" STRING')
    def assign(self, p):
        pass

    @_('ID ADD_ASSIGN expr')
    def add_assign(self, p):
        pass

    @_('ID SUB_ASSIGN expr')
    def sub_assign(self, p):
        pass

    @_('ID MUL_ASSIGN expr')
    def mul_assign(self, p):
        pass

    @_('ID DIV_ASSIGN expr')
    def div_assign(self, p):
        pass
    
    @_('ID "[" row "]" "=" expr')
    def mul_assign(self, p):
        pass


    #---------------------------
    #matrix
    @_('matrix "\'"')
    def matrix(self, p):
        pass
    
    #matrix_style_1
    @_('"[" "]"')
    def matrix(self, p):
        pass

    @_('matrix1')
    def matrix(self, p):
        pass

    @_('"[" rows1 "]"')
    def matrix1(self,p):
        pass

    @_('rows1 ";" row')
    def rows1(self,p):
        pass

    @_('row')
    def rows1(self,p):
        pass

   

    #matrix_style_2
    @_('matrix2')
    def matrix(self, p):
        pass

    @_('"[" rows2 "]"')
    def matrix2(self,p):
        pass

    @_('rows2 "," "[" row "]"')
    def rows2(self,p):
        pass

    @_('"[" row "]"')
    def rows2(self,p):
        pass


    @_('row "," INTNUM')
    def row(self,p):
        pass

    @_('INTNUM')
    def row(self,p):
        pass


    @_('ZEROS "(" INTNUM ")"')
    def matrix(self, p):
        pass

    @_('ONES "(" INTNUM ")"')
    def matrix(self, p):
        pass

    @_('EYE "(" INTNUM ")"')
    def matrix(self, p):
        pass

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        pass

    @_('expr "+" expr')
    def expr(self, p):
        pass

    @_('expr DOT_ADD expr')
    def expr(self, p):
        pass

    @_('expr "-" expr')
    def expr(self, p):
        pass

    @_('expr DOT_SUB expr')
    def expr(self, p):
        pass
   
    @_('expr "*" expr')
    def expr(self, p):
        pass

    @_('expr DOT_MUL expr')
    def expr(self, p):
        pass

    @_('expr "/" expr')
    def expr(self, p):
        pass

    @_('expr DOT_DIV expr')
    def expr(self, p):
        pass
    
    @_('"(" expr ")"')
    def expr(self, p):
        pass

    @_('matrix')
    def expr(self, p):
        pass

    @_('INTNUM')
    def expr(self, p):
        pass

    @_('FLOATNUM')
    def expr(self, p):
        pass
    
    @_('ID "\'"')
    def expr(self, p):
        pass 

    @_('ID')
    def expr(self, p):
        pass 
   
    #---------------------------
    #relative
    @_('expr ">" expr')
    def relative(self, p):
        pass

    @_('expr GTE expr')
    def relative(self, p):
        pass

    @_('expr "<" expr')
    def relative(self, p):
        pass

    @_('expr LTE expr')
    def relative(self, p):
        pass

    @_('expr EQ expr')
    def relative(self, p):
        pass

    @_('expr NEQ expr')
    def relative(self, p):
        pass

    #---------------------------

    @_('print_values "," print_value')
    def print_values(self, p):
        pass
    
    @_('print_value')
    def print_values(self, p):
        pass

    @_('STRING')
    def print_value(self, p):
        pass

    @_('ID')
    def print_value(self, p):
        pass

    @_('return_values "," return_value')
    def return_values(self, p):
        pass
    
    @_('return_value')
    def return_values(self, p):
        pass

    @_('STRING')
    def return_value(self, p):
        pass

    @_('ID')
    def return_value(self, p):
        pass

    @_('FLOATNUM')
    def return_value(self, p):
        pass

    @_('expr')
    def return_value(self, p):
        pass

    # @_('instructions_opt')
    # def program(p):
    #     pass

    # @_('instructions')
    # def instructions_opt(p):
    #     pass

    # @_('')
    # def instructions_opt(p):
    #     pass

    # @_('instructions instruction')
    # def instructions(p):
    #     pass

    # @_('instruction')
    # def instructions(p):
    #     pass

    

    # to finish the grammar
    # ....

