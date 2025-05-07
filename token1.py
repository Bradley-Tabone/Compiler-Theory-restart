# token.py
class Token:
    def __init__(self, type_, lexeme, line, column):
        self.type = type_
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __repr__(self):
        return f"{self.type}: '{self.lexeme}' (Line {self.line}, Col {self.column})"
