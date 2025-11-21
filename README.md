# Teoria kompilacji
Interpreter napisany własnoręcznie w ramach przedmiotu Teoria Kompilacji na 5 semestrze Informatyki AGH z wykorzystaniem biblioteki [SLY](https://sly.readthedocs.io/en/latest/sly.html).
Implementacja spełnia [wymagania przedstawione za zajęciach](https://home.agh.edu.pl/~mkuta/tklab/).

[Helpful information for each step](https://stackoverflow.com/a/58068689)

---
## [Lexer](src/scanner.py)
Skaner przetwarzający tekst wejściowy na listę tokenów, w przypadku nierozpoznania tokenu wypisywany jest błąd.

---
## [Parser](src/parser.py)
Parser budujący gramatykę języka.

---
## [AST](src/AST.py)
Moduł do tworzenia drzewa syntaktycznego (Abstract Syntax Tree).


