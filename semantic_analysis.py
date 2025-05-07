# semantic_analysis.py - Semantic Analysis for PArL
from ast_nodes import *
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add(self, name, typ, scope):
        """
        Adds a new symbol to the symbol table.
        :param name: The symbol's name.
        :param typ: The type of the symbol (e.g., int, function).
        :param scope: The scope of the symbol (e.g., global, function).
        """
        if name in self.symbols:
            raise ValueError(f"Symbol {name} already declared in this scope")
        self.symbols[name] = (typ, scope)

    def lookup(self, name):
        """
        Looks up a symbol in the symbol table.
        :param name: The name of the symbol.
        :return: The type and scope of the symbol if found, otherwise None.
        """
        return self.symbols.get(name)

    def __str__(self):
        """
        Returns a string representation of the symbol table.
        :return: A string listing all symbols in the symbol table.
        """
        return '\n'.join(f'{name}: {typ}' for name, (typ, scope) in self.symbols.items())

class SemanticAnalyzer:
    def __init__(self):
        """
        Initializes the semantic analyzer with an empty symbol table.
        """
        self.symbol_table = SymbolTable()

    def analyze(self, node):
        """
        Analyzes the AST for semantic correctness.
        :param node: The root AST node to analyze.
        :return: The symbol table after analysis.
        """
        self.traverse(node)
        return self.symbol_table

    def traverse(self, node, scope="global"):
        """
        Recursively traverses the AST and performs semantic checks.
        :param node: The current AST node to analyze.
        :param scope: The current scope (default is "global").
        """
        if isinstance(node, ASTProgram):
            for fn in node.declarations:
                self.traverse(fn, scope)
        elif isinstance(node, ASTFunctionDeclaration):
            # Add function to symbol table
            self.symbol_table.add(node.name, "function", scope)
            for param in node.parameters:
                # Add parameters to the symbol table
                self.symbol_table.add(param.name, param.type, "parameter")
            self.traverse(node.body, scope)
        elif isinstance(node, ASTVariableDeclaration):
            # Check if variable is already declared
            if self.symbol_table.lookup(node.name):
                raise ValueError(f"Variable {node.name} already declared")
            # Add variable to symbol table
            self.symbol_table.add(node.name, node.type, scope)
            self.traverse(node.value, scope)
        elif isinstance(node, ASTAssignment):
            # Check if variable is declared before assignment
            if not self.symbol_table.lookup(node.name):
                raise ValueError(f"Variable {node.name} not declared before assignment")
            self.traverse(node.value, scope)
        elif isinstance(node, ASTBinaryOp):
            # Traverse both sides of binary operation
            self.traverse(node.left, scope)
            self.traverse(node.right, scope)
        elif isinstance(node, ASTUnaryOp):
            # Traverse the operand of the unary operation
            self.traverse(node.operand, scope)
        elif isinstance(node, ASTLiteral):
            pass  # Literal nodes don't require semantic checks
        elif isinstance(node, ASTFunctionCall):
            # Check if the function is declared
            if not self.symbol_table.lookup(node.name):
                raise ValueError(f"Function {node.name} not declared")
            for arg in node.args:
                self.traverse(arg, scope)
        elif isinstance(node, ASTIfStatement):
            # Traverse the condition, then block, and else block
            self.traverse(node.condition, scope)
            self.traverse(node.then_block, scope)
            if node.else_block:
                self.traverse(node.else_block, scope)
        elif isinstance(node, ASTWhileStatement):
            # Traverse the condition and body of the while loop
            self.traverse(node.condition, scope)
            self.traverse(node.body, scope)
        elif isinstance(node, ASTForStatement):
            # Traverse initialization, condition, update, and body
            self.traverse(node.init, scope)
            self.traverse(node.condition, scope)
            self.traverse(node.update, scope)
            self.traverse(node.body, scope)
        elif isinstance(node, ASTExpressionStatement):
            # Traverse the expression in the statement
            self.traverse(node.expression, scope)
        elif isinstance(node, ASTArrayLiteral):
            # Traverse each element of the array literal
            for element in node.elements:
                self.traverse(element, scope)
