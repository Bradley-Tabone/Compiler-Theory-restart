# lexer.py (fully table-driven DFA implementation)
from token_types import TokenType
from token1 import Token

CHAR_CLASSES = {
    'LETTER': 0,
    'DIGIT': 1,
    'HASH': 2,
    'DOT': 3,
    'WHITESPACE': 4,
    'OPERATOR_CHAR': 5,
    'SEPARATOR': 6,
    'UNDERSCORE': 7,
    'OTHER': 8
}

PAD_BUILTINS = {
    '__width', '__height', '__read', '__random_int', '__delay', '__write', '__write_box', '__print'
}

MULTI_CHAR_OPERATORS = {
    '==', '!=', '<=', '>=', '->'
}

class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.start_column = 1

        self.keywords = {
            'fun', 'let', 'return', 'if', 'else', 'while', 'for',
            'true', 'false', 'as', 'int', 'float', 'bool', 'colour'
        }
        self.operators = {
            '+', '-', '*', '/', '==', '!=', '=', '<', '<=', '>', '>=',
            'and', 'or', 'not', '->'
        }
        self.separators = {'(', ')', '{', '}', '[', ']', ';', ',', ':'}

    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            print(f"{token}")

            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens

    def get_next_token(self):
        self.skip_whitespace_and_comments()

        if self.position >= len(self.source):
            return Token(TokenType.EOF, 'EOF', self.line, self.column)

        self.start_column = self.column

        # Handle multi-character operators
        char = self.peek()
        two_char = char + (self.peek(1) or '')
        if two_char in MULTI_CHAR_OPERATORS:
            self.advance()
            self.advance()
            return Token(TokenType.OPERATOR, two_char, self.line, self.start_column)

        # DFA processing
        current_state = 0
        lexeme = ''
        last_accepting_state = None
        last_accepting_lexeme = ''
        last_accepting_pos = self.position
        hex_count = 0

        while self.position < len(self.source):
            char = self.peek()
            char_class = self.get_char_class(char)

            next_state = DFA_TRANSITIONS.get(current_state, {}).get(char_class, -1)
            if next_state == -1:
                break

            lexeme += self.advance()
            current_state = next_state

            if current_state == 3:
                if char_class in (CHAR_CLASSES['DIGIT'], CHAR_CLASSES['LETTER']):
                    hex_count += 1
                if hex_count == 6:
                    last_accepting_state = current_state
                    last_accepting_lexeme = lexeme
                    last_accepting_pos = self.position
                elif hex_count > 6:
                    break
            elif current_state in DFA_ACCEPTING_STATES:
                last_accepting_state = current_state
                last_accepting_lexeme = lexeme
                last_accepting_pos = self.position

        if last_accepting_state is not None:
            self.position = last_accepting_pos
            self.column = self.start_column + len(last_accepting_lexeme)
            token_type = DFA_ACCEPTING_STATES[last_accepting_state]

            if token_type == TokenType.IDENTIFIER:
                if last_accepting_lexeme in self.keywords:
                    token_type = TokenType.KEYWORD
                elif last_accepting_lexeme in self.operators:
                    token_type = TokenType.OPERATOR
                elif last_accepting_lexeme in PAD_BUILTINS:
                    token_type = TokenType.BUILTIN

            return Token(token_type, last_accepting_lexeme, self.line, self.start_column)

        error_char = self.advance()
        return Token(TokenType.ERROR, error_char, self.line, self.start_column)

    def skip_whitespace_and_comments(self):
        while self.position < len(self.source):
            ch = self.peek()
            if ch in ' \t\r\n':
                self.advance()
            elif ch == '/' and self.peek(1) == '/':
                while self.peek() and self.peek() != '\n':
                    self.advance()
            elif ch == '/' and self.peek(1) == '*':
                self.advance(); self.advance()
                while self.peek() and not (self.peek() == '*' and self.peek(1) == '/'):
                    self.advance()
                if self.peek():
                    self.advance(); self.advance()
            else:
                break

    def get_char_class(self, ch):
        if ch.isalpha():
            return CHAR_CLASSES['LETTER']
        elif ch.isdigit():
            return CHAR_CLASSES['DIGIT']
        elif ch == '#':
            return CHAR_CLASSES['HASH']
        elif ch == '.':
            return CHAR_CLASSES['DOT']
        elif ch in '+-*/=<>!':
            return CHAR_CLASSES['OPERATOR_CHAR']
        elif ch in self.separators:
            return CHAR_CLASSES['SEPARATOR']
        elif ch == '_':
            return CHAR_CLASSES['UNDERSCORE']
        elif ch in ' \t\r\n':
            return CHAR_CLASSES['WHITESPACE']
        else:
            return CHAR_CLASSES['OTHER']

    def peek(self, offset=0):
        pos = self.position + offset
        return self.source[pos] if pos < len(self.source) else None

    def advance(self):
        ch = self.source[self.position]
        self.position += 1
        if ch == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

# DFA Transitions Table
DFA_TRANSITIONS = {
    0: {
        CHAR_CLASSES['LETTER']: 1,
        CHAR_CLASSES['UNDERSCORE']: 1,
        CHAR_CLASSES['DIGIT']: 2,
        CHAR_CLASSES['HASH']: 3,
        CHAR_CLASSES['DOT']: 6,
        CHAR_CLASSES['OPERATOR_CHAR']: 4,
        CHAR_CLASSES['SEPARATOR']: 5
    },
    1: {
        CHAR_CLASSES['LETTER']: 1,
        CHAR_CLASSES['DIGIT']: 1,
        CHAR_CLASSES['UNDERSCORE']: 1
    },
    2: {
        CHAR_CLASSES['DIGIT']: 2,
        CHAR_CLASSES['DOT']: 6
    },
    3: {
        CHAR_CLASSES['DIGIT']: 3,
        CHAR_CLASSES['LETTER']: 3
    },
    4: {},
    5: {},
    6: {
        CHAR_CLASSES['DIGIT']: 7
    },
    7: {
        CHAR_CLASSES['DIGIT']: 7
    }
}

DFA_ACCEPTING_STATES = {
    1: TokenType.IDENTIFIER,
    2: TokenType.INT_LITERAL,
    3: TokenType.COLOUR_LITERAL,
    4: TokenType.OPERATOR,
    5: TokenType.SEPARATOR,
    7: TokenType.FLOAT_LITERAL
}
