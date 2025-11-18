# pyright: reportUndefinedVariable=false
from sly import Parser
from scanner import Scanner

import AST

# wyrażenia binarne,
# wyrażenia relacyjne,
# instrukcje przypisania,
# instrukcje warunkowe if-else,
# pętle: while oraz for,
# instrukcje break, continue oraz return,
# instrukcje print,
# instrukcje złożone,
# tablice oraz ich zakresy.


class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = "parser.out"

    # Zadanie polega na stworzeniu parsera języka do operacji macierzowych.

    # tablice i macierze oraz ich indeksy (ewentualnie zakresy).
    # customowe bledy w parsingu
    precedence = (
        ("nonassoc", "IFX"),
        ("nonassoc", "ELSE"),
        ("right", "MUL_ASSIGN", "DIV_ASSIGN", "SUB_ASSIGN", "ADD_ASSIGN"),
        ("nonassoc", "<", ">", "LTE", "GTE", "NEQ", "EQ"),
        ("left", "+", "-"),
        ("left", "*", "/"),
        ("left", "DOT_ADD", "DOT_SUB"),
        ("left", "DOT_MUL", "DOT_DIV"),
        ("right", "UMINUS"),
        ("left", "'"),
    )

    # ---------------------------
    # program to ciąg linijek (lines)
    @_("lines")
    def program(self, p):
        pass

    # ---------------------------
    # lines
    @_("line lines")
    def lines(self, p):
        pass

    @_("")
    def lines(self, p):
        pass

    # ---------------------------
    # line
    @_(
        'assignment ";"',
        'statement ";"',
        "if_statement",
        "while_statement",
        "for_statement",
        "matrix_assign ';'"
    )
    def line(self, p):
        pass

    # ---------------------------
    # statements

    # BREAK I CONTINUE DZIALA WSZEDZIE, A POWINIEN TYLKO W PETLI
    @_("BREAK")
    def statement(self, p):
        pass

    @_("CONTINUE")
    def statement(self, p):
        pass

    @_("RETURN expr")
    def statement(self, p):
        pass

    @_("PRINT print_args")
    def statement(self, p):
        pass

    @_("print_args ',' print_arg")
    def print_args(self, p):
        pass

    @_("print_arg")
    def print_args(self, p):
        pass

    @_("expr")
    def print_arg(self, p):
        pass

    @_("STRING")
    def print_arg(self, p):
        pass

    # ---------------------------
    # assignments
    @_('var "=" expr', 'var "=" STRING')
    def assignment(self, p):
        pass

    @_("var ADD_ASSIGN expr")
    def assignment(self, p):
        pass

    @_("var SUB_ASSIGN expr")
    def assignment(self, p):
        pass

    @_("var MUL_ASSIGN expr")
    def assignment(self, p):
        pass

    @_("var DIV_ASSIGN expr")
    def assignment(self, p):
        pass

    # ---------------------------
    # warunki i petle
    # pomysl: osobny if dla petli
    @_('IF "(" condition ")" block %prec IFX')
    def if_statement(self, p):
        pass

    @_('IF "(" condition ")" block ELSE block')
    def if_statement(self, p):
        pass

    # @_("if_statement ELSE if_statement")
    # def if_statement(self, p):
    #     pass

    @_('WHILE "(" condition ")" block')
    def while_statement(self, p):
        pass

    @_('FOR var "=" expr ":" expr block')
    def for_statement(self, p):
        pass

    # ---------------------------
    # blok
    @_("line", '"{" lines "}"')
    def block(self, p):
        pass

    # ---------------------------
    # condition
    @_('">"', '"<"', "EQ", "NEQ", "GTE", "LTE")
    def comp_op(self, p):
        pass

    @_("expr comp_op expr")
    def condition(self, p):
        pass

    # ---------------------------
    # expressions
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        pass

    @_('expr "+" expr',
       'expr "-" expr',
       'expr "*" expr',
       'expr "/" expr',
       "expr DOT_ADD expr",
       "expr DOT_SUB expr",
       "expr DOT_MUL expr",
       "expr DOT_DIV expr")
    def expr(self, p):
        return AST.BinExpr(p[1], p[0], p[2])


    @_('"(" expr ")"')
    def expr(self, p):
        pass

    @_("matrix")
    def expr(self, p):
        pass

    @_("matrix_element")
    def expr(self, p):
        pass

    @_('var "\'" ')
    def expr(self, p):
        pass

    @_("INTNUM")
    def expr(self, p):
        pass

    @_("FLOATNUM")
    def expr(self, p):
        pass

    @_("var")
    def expr(self, p):
        pass

    # ---------------------------
    # variable
    @_("ID")
    def var(self, p):
        pass

    # ---------------------------
    # matrix
    @_('matrix "\'"')
    def matrix(self, p):
        pass

    # matrix_style_1 -> example1.m
    # @_('"[" "]"')
    # def matrix(self, p):
    #     pass

    # @_("matrix1")
    # def matrix(self, p):
    #     pass

    # @_('"[" rows1 "]"')
    # def matrix1(self, p):
    #     pass

    # @_('rows1 ";" row')
    # def rows1(self, p):
    #     pass

    # @_("row")
    # def rows1(self, p):
    #     pass

    # matrix_style_2 -> example.txt
    @_("matrix2")
    def matrix(self, p):
        pass

    @_('"[" rows2 "]"')
    def matrix2(self, p):
        pass

    @_('rows2 "," "[" row "]"')
    def rows2(self, p):
        pass

    @_('"[" row "]"')
    def rows2(self, p):
        pass

    # rows
    @_('row "," expr')
    def row(self, p):
        pass

    @_("expr")
    def row(self, p):
        pass

    # matrix creation with functions
    @_('ZEROS "(" INTNUM ")"')
    def matrix(self, p):
        pass

    @_('ONES "(" INTNUM ")"')
    def matrix(self, p):
        pass

    @_('EYE "(" INTNUM ")"')
    def matrix(self, p):
        pass

    @_('var "[" indices "]" ')
    def matrix_element(self, p):
        pass

    @_('matrix_element "=" expr')
    def matrix_assign(self, p):
        pass

    @_("expr")
    def indices(self, p):
        pass

    @_('expr "," indices')
    def indices(self, p):
        pass

    def error(self, p):
        if p:
            print(
                f"{'\033[91m'}Syntax error at token {p.type}, value={p.value!r}, line={p.lineno}{'\033[0m'}"
            )
        else:
            print(f"{'\033[91m'}Syntax error at end of input{'\033[0m'}")
