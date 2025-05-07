# parser.py - Hand-crafted LL(1) Parser for PArL
from token_types import TokenType
from token1 import Token
import ast_nodes as ast

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        return self.tokens[self.current]

    def advance(self):
        if self.current < len(self.tokens) - 1:
            self.current += 1
        return self.peek()

    def match(self, *expected):
        if self.peek().type in expected or self.peek().lexeme in expected:
            return self.advance()
        return None

    def expect(self, expected):
        tok = self.peek()
        if tok.type == expected or tok.lexeme == expected:
            return self.advance()
        raise ParserError(f"Expected {expected}, got {tok.lexeme} at line {tok.line}")

    def parse_program(self):
        functions = []
        statements = []

        while self.peek().type != TokenType.EOF:
            if self.peek().lexeme == 'fun':
                functions.append(self.parse_function())
            elif self.peek().lexeme == 'let':
                statements.append(self.parse_variable_decl())
            else:
                raise ParserError(f"Unexpected top-level token {self.peek().lexeme} at line {self.peek().line}")

        return ast.ASTProgram(functions + statements)

    def parse_function(self):
        print(f"[DEBUG] Parsing function at line {self.peek().line}")
        self.expect('fun')
        name = self.expect(TokenType.IDENTIFIER)
        self.expect('(')
        params = self.parse_parameters()
        self.expect(')')
        self.expect('->')
        return_type = self.expect(TokenType.KEYWORD)
        body = self.parse_block()
        return ast.ASTFunctionDeclaration(name.lexeme, params, return_type.lexeme, body)

    def parse_parameters(self):
        params = []
        if self.peek().lexeme == ')':
            return params
        while True:
            print(f"[DEBUG] Parsing parameter at line {self.peek().line}")
            name = self.expect(TokenType.IDENTIFIER)
            self.expect(':')
            typ = self.expect(TokenType.KEYWORD)
            params.append(ast.ASTParameter(name.lexeme, typ.lexeme))
            if self.peek().lexeme == ')':
                break
            self.expect(',')
        return params

    def parse_block(self):
        self.expect('{')
        statements = []
        while self.peek().lexeme != '}':
            print(f"[DEBUG] Parsing statement at line {self.peek().line}")
            statements.append(self.parse_statement())
        self.expect('}')
        return ast.ASTBlock(statements)

    def parse_statement(self):
        tok = self.peek()
        print(f"[DEBUG] Entering parse_statement with token {tok.lexeme} at line {tok.line}")
        if tok.type == TokenType.KEYWORD:
            if tok.lexeme == 'let':
                return self.parse_variable_decl()
            elif tok.lexeme == 'return':
                return self.parse_return()
            elif tok.lexeme == 'if':
                return self.parse_if()
            elif tok.lexeme == 'while':
                return self.parse_while()
            elif tok.lexeme == 'for':
                return self.parse_for()
        elif tok.type == TokenType.BUILTIN:
            return self.parse_builtin_call()
        elif tok.type == TokenType.IDENTIFIER:
            if self.tokens[self.current + 1].lexeme == '=':
                return self.parse_assignment_statement()
            return self.parse_expression_statement()
        raise ParserError(f"Unexpected token {tok.lexeme} at line {tok.line}")

    def parse_variable_decl(self):
        print(f"[DEBUG] Parsing variable declaration at line {self.peek().line}")
        self.expect('let')
        name = self.expect(TokenType.IDENTIFIER)
        self.expect(':')
        typ = self.expect(TokenType.KEYWORD)
        self.expect('=')
        expr = self.parse_expression()
        self.expect(';')
        return ast.ASTVariableDeclaration(name.lexeme, typ.lexeme, expr)

    def parse_assignment_statement(self):
        print(f"[DEBUG] Parsing assignment statement at line {self.peek().line}")
        name = self.expect(TokenType.IDENTIFIER)
        self.expect('=')
        expr = self.parse_expression()
        self.expect(';')
        return ast.ASTAssignment(name.lexeme, expr)

    def parse_assignment(self):
        name = self.expect(TokenType.IDENTIFIER)
        self.expect('=')
        expr = self.parse_expression()
        return ast.ASTAssignment(name.lexeme, expr)

    def parse_return(self):
        print(f"[DEBUG] Parsing return statement at line {self.peek().line}")
        self.expect('return')
        expr = self.parse_expression()
        self.expect(';')
        return ast.ASTReturnStatement(expr)

    def parse_if(self):
        self.expect('if')
        self.expect('(')
        condition = self.parse_expression()
        self.expect(')')
        then_block = self.parse_block()
        else_block = None
        if self.peek().lexeme == 'else':
            self.advance()
            else_block = self.parse_block()
        return ast.ASTIfStatement(condition, then_block, else_block)

    def parse_while(self):
        self.expect('while')
        self.expect('(')
        condition = self.parse_expression()
        self.expect(')')
        body = self.parse_block()
        return ast.ASTWhileStatement(condition, body)

    def parse_for(self):
        self.expect('for')
        self.expect('(')
        init = self.parse_variable_decl()
        condition = self.parse_expression()
        self.expect(';')
        update = self.parse_assignment()
        self.expect(')')
        body = self.parse_block()
        return ast.ASTForStatement(init, condition, update, body)

    def parse_builtin_call(self):
        builtin = self.expect(TokenType.BUILTIN)
        self.expect('(')
        args = []
        if self.peek().lexeme != ')':
            while True:
                args.append(self.parse_expression())
                if self.peek().lexeme == ')':
                    break
                self.expect(',')
        self.expect(')')
        self.expect(';')
        return ast.ASTBuiltinCall(builtin.lexeme, args)

    def parse_expression_statement(self):
        expr = self.parse_expression()
        self.expect(';')
        return ast.ASTExpressionStatement(expr)

    def parse_expression(self):
        return self.parse_as()

    def parse_as(self):
        expr = self.parse_or()
        while self.peek().lexeme == 'as':
            self.advance()
            type_token = self.expect(TokenType.KEYWORD)
            expr = ast.ASTCast(expr, type_token.lexeme)
        return expr

    def parse_or(self):
        left = self.parse_and()
        while self.peek().lexeme == 'or':
            op = self.advance()
            right = self.parse_and()
            left = ast.ASTBinaryOp(op.lexeme, left, right)
        return left

    def parse_and(self):
        left = self.parse_equality()
        while self.peek().lexeme == 'and':
            op = self.advance()
            right = self.parse_equality()
            left = ast.ASTBinaryOp(op.lexeme, left, right)
        return left

    def parse_equality(self):
        left = self.parse_comparison()
        while self.peek().lexeme in ('==', '!='):
            op = self.advance()
            right = self.parse_comparison()
            left = ast.ASTBinaryOp(op.lexeme, left, right)
        return left

    def parse_comparison(self):
        left = self.parse_term()
        while self.peek().lexeme in ('<', '<=', '>', '>='):
            op = self.advance()
            right = self.parse_term()
            left = ast.ASTBinaryOp(op.lexeme, left, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.peek().lexeme in ('+', '-'):
            op = self.advance()
            right = self.parse_factor()
            left = ast.ASTBinaryOp(op.lexeme, left, right)
        return left

    def parse_factor(self):
        left = self.parse_unary()
        while self.peek().lexeme in ('*', '/'):
            op = self.advance()
            right = self.parse_unary()
            left = ast.ASTBinaryOp(op.lexeme, left, right)
        return left

    def parse_unary(self):
        if self.peek().lexeme in ('-', 'not'):
            op = self.advance()
            expr = self.parse_unary()
            return ast.ASTUnaryOp(op.lexeme, expr)
        return self.parse_primary()

    def parse_primary(self):
        tok = self.peek()
        print(f"[DEBUG] Entering parse_primary with token {tok.type}: {tok.lexeme} at line {tok.line}")
        if tok.lexeme == '(':
            self.advance()
            expr = self.parse_expression()
            self.expect(')')
            return expr
        if tok.lexeme == '[':
            self.advance()
            elements = []
            if self.peek().lexeme != ']':
                while True:
                    elements.append(self.parse_expression())
                    if self.peek().lexeme == ']':
                        break
                    self.expect(',')
            self.expect(']')
            return ast.ASTArrayLiteral(elements)
        if tok.type == TokenType.IDENTIFIER:
            identifier = self.advance()
            if self.peek().lexeme == '(':
                self.advance()
                args = []
                if self.peek().lexeme != ')':
                    while True:
                        args.append(self.parse_expression())
                        if self.peek().lexeme == ')':
                            break
                        self.expect(',')
                self.expect(')')
                return ast.ASTFunctionCall(identifier.lexeme, args)
            return ast.ASTLiteral(identifier.lexeme)
        if tok.type == TokenType.BUILTIN:
            name = self.advance()
            if self.peek().lexeme == '(':
                self.advance()
                args = []
                if self.peek().lexeme != ')':
                    while True:
                        args.append(self.parse_expression())
                        if self.peek().lexeme == ')':
                            break
                        self.expect(',')
                self.expect(')')
                return ast.ASTFunctionCall(name.lexeme, args)
            return ast.ASTLiteral(name.lexeme)
        if tok.type in (TokenType.INT_LITERAL, TokenType.FLOAT_LITERAL, TokenType.BOOLEAN_LITERAL, TokenType.COLOUR_LITERAL):
            return ast.ASTLiteral(self.advance().lexeme)
        if tok.type == TokenType.KEYWORD and tok.lexeme in ('true', 'false'):
            return ast.ASTLiteral(self.advance().lexeme)

        print(f"[DEBUG] Unexpected token in parse_primary: {tok.type} '{tok.lexeme}' at line {tok.line}")
        raise ParserError(f"Unexpected primary expression at line {tok.line}")
