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
        ("left", '*', '/')
    )


    @_('expr "+" expr')
    def expr(self, p):
        pass

    @_('expr "-" expr')
    def expr(self, p):
        pass
   
    @_('expr "*" expr')
    def expr(self, p):
        pass

    @_('expr "/" expr')
    def expr(self, p):
        pass
    
    @_('"(" expr ")"')
    def expr(self, p):
        pass
    
    @_('INTNUM')
    def expr(self, p):
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

