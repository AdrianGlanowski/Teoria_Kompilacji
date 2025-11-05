# pyright: reportUndefinedVariable=false
from sly import Parser
from scanner import Scanner

class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'

    # Zadanie polega na stworzeniu parsera języka do operacji macierzowych. 
     
    # tablice i macierze oraz ich indeksy (ewentualnie zakresy).
    #customowe bledy w parsingu
    precedence = (
        ('right', 'ELSE'),
        ('right', 'MUL_ASSIGN', 'DIV_ASSIGN', 'SUB_ASSIGN', 'ADD_ASSIGN'),
        ('nonassoc', '<', '>', 'LTE', 'GTE', 'NEQ', 'EQ'),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', 'DOT_ADD', 'DOT_SUB'),
        ('left', 'DOT_MUL', 'DOT_DIV'),
        ('right', 'UMINUS'),
        ('left', "'"),
    )
    
    #---------------------------
    #program to ciąg statementow
    @_('lines')
    def program(self, p):
        pass

    #---------------------------
    #statementy
    @_('lines line')
    def lines(self, p):
        pass
    
    @_('line')
    def lines(self, p):
        pass

    @_('assign ";"')
    def line(self, p):
        pass

    #break dziala wszedzie, a powinien tylko w petli
    @_('BREAK ";"')
    def line(self, p):
        pass
    #continue dziala wszedzie, a powinien tylko w petli
    @_('CONTINUE ";"')
    def line(self, p):
        pass

    @_('RETURN statement_values ";"')
    def line(self, p):
        pass
    
    @_('add_assign ";"')
    def line(self, p):
        pass

    @_('sub_assign ";"')
    def line(self, p):
        pass

    @_('mul_assign ";"')
    def line(self, p):
        pass

    @_('div_assign ";"')
    def line(self, p):
        pass

    @_('matrix_assign ";"')
    def line(self, p):
        pass

    @_('PRINT statement_values ";"')
    def line(self, p):
        pass

    @_('if_statement')
    def line(self, p):
        pass

    @_('line',
       '"{" lines "}"')
    def block(self, p):
        pass 

    #pomysl: osobny if dla petli
    @_('IF "(" relative ")" block')
    def if_statement(self, p):
        pass

    @_('if_statement ELSE block')
    def if_statement(self, p):
        pass
    
    @_('if_statement ELSE if_statement')
    def if_statement(self, p):
        pass
    
    @_('while_statement')
    def line(self, p):
        pass

    @_('WHILE "(" relative ")" block')
    def while_statement(self, p):
        pass

    @_('for_statement')
    def line(self, p):
        pass
    
    @_('FOR variable "=" expr ":" expr block')
    def for_statement(self, p):
        pass
    
    #---------------------------
    #polecenia
    @_('variable "=" expr')
    def assign(self, p):
        pass

    @_('variable "=" STRING')
    def assign(self, p):
        pass

    @_('variable ADD_ASSIGN expr')
    def add_assign(self, p):
        pass

    @_('variable SUB_ASSIGN expr')
    def sub_assign(self, p):
        pass

    @_('variable MUL_ASSIGN expr')
    def mul_assign(self, p):
        pass

    @_('variable DIV_ASSIGN expr')
    def div_assign(self, p):
        pass
    
    @_('ID "[" indexes "]" "=" expr')
    def matrix_assign(self, p):
        pass

    @_('ID "[" index "]" "=" expr')
    def matrix_assign(self, p):
        pass

    #---------------------------
    #matrix
    @_('matrix "\'"')
    def matrix(self, p):
        pass
    
    @_('INTNUM "," INTNUM')
    def indexes(self, p):
        pass

    @_('INTNUM')
    def index(self, p):
        pass

    #matrix_style_1 -> example1.m
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

    #matrix_style_2 -> example.txt
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

    @_('row "," number')
    def row(self,p):
        pass

    @_('number')
    def row(self,p):
        pass

    @_('INTNUM',
       'FLOATNUM')
    def number(self, p):
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

    @_('number')
    def expr(self, p):
        pass
    
    @_('variable "\'"')
    def expr(self, p):
        pass

    @_('variable')
    def expr(self, p):
        pass

    @_('ID')
    def variable(self, p):
        pass 
   
    #---------------------------
    #relative
    @_('">"', '"<"', 'EQ', 'NEQ', 'GTE', 'LTE')
    def rel_op(self, p):
        pass
    @_('expr rel_op expr')
    def relative(self, p):
        pass

    #---------------------------

    @_('statement_values "," statement_value')
    def statement_values(self, p):
        pass
    
    @_('statement_value')
    def statement_values(self, p):
        pass

    @_('STRING', 'expr', 'variable')
    def statement_value(self, p):
        pass

   

