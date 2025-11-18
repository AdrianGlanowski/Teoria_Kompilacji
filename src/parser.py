# pyright: reportUndefinedVariable=false
from sly import Parser
from scanner import Scanner
from ParserError import ParserError
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
        return p.lines

    # ---------------------------
    # lines
    @_("line lines")
    def lines(self, p):
        return [p.line] + p.lines

    @_("")
    def lines(self, p):
        return []

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
        return AST.BreakStatement()

    @_("CONTINUE")
    def statement(self, p):
        return AST.ContinueStatement()
        
    @_("RETURN expr")
    def statement(self, p):
        return AST.ReturnStatement(p.expr)

    @_("PRINT print_args")
    def statement(self, p):
        return AST.PrintStatement(p[1])

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
        return str(p[0])

    # ---------------------------
    # assignments
    @_('var "=" expr',
       'var "=" STRING',
       'var ADD_ASSIGN expr',
       'var SUB_ASSIGN expr',
       'var MUL_ASSIGN expr',
       'var DIV_ASSIGN expr')
    def assignment(self, p):
        return AST.Assignment(p.var, p[1], p[2])


    # ---------------------------
    # warunki i petle
    # pomysl: osobny if dla petli
    @_('IF "(" condition ")" block %prec IFX')
    def if_statement(self, p):
        return AST.IfStatement(p.condition, p.block)

    @_('IF "(" condition ")" block ELSE block')
    def if_statement(self, p):
        return AST.IfStatement(p.condition, p.block0, p.block1)

    @_('WHILE "(" condition ")" block')
    def while_statement(self, p):
        return AST.WhileStatement(p.condition, p.block)


    @_('FOR var "=" expr ":" expr block')
    def for_statement(self, p):
        return AST.ForStatement(p.var, p.expr0, p.expr1, p.block)

    # ---------------------------
    # blok
    @_("line")
    def block(self, p):
        return [p.line]
    
    @_('"{" lines "}"')
    def block(self, p):
        return p.lines

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
        return p.expr

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
        return int(p[0])

    @_("FLOATNUM")
    def expr(self, p):
        return float(p[0])

    @_("var")
    def expr(self, p):
        return p.var

    # ---------------------------
    # variable
    @_("ID")
    def var(self, p):
        return p[0]

    # ---------------------------
    # matrix
    @_('matrix "\'"')
    def matrix(self, p):
        pass

    @_('"[" vectors "]"')
    def matrix(self, p):
        pass

    @_('vectors "," vector')
    def vectors(self, p):
        pass

    @_('vector')
    def vectors(self, p):
        pass

    @_('"[" row "]"')
    def vector(self, p):
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

    @_('var vector')
    def matrix_element(self, p):
        pass

    @_('matrix_element "=" expr')
    def matrix_assign(self, p):
        pass

    def error(self, p):
        if p:
            print(
                f"{'\033[91m'}Syntax error at token {p.type}, value={p.value!r}, line={p.lineno}{'\033[0m'}"
            )
        else:
            print(f"{'\033[91m'}Syntax error at end of input{'\033[0m'}")
        raise ParserError
