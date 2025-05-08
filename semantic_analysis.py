from ast_nodes import *

class SemanticAnalysisError(Exception):
    """Custom exception for semantic analysis errors."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, node):
        # Start semantic analysis from the root node
        if isinstance(node, ASTProgram):
            self.analyze_program(node)
        else:
            raise SemanticAnalysisError("Unknown root node type.")

    def analyze_program(self, node):
        # Analyze function declarations
        for decl in node.declarations:
            if isinstance(decl, ASTFunctionDeclaration):
                self.analyze_function(decl)

    def analyze_function(self, func):
        # Add function to the symbol table
        self.symbol_table.add_function(func.name)
        
        # Analyze parameters of the function
        for param in func.parameters:
            self.symbol_table.add_variable(param.name, param.type)

        # Analyze function body
        self.analyze_block(func.body)

    def analyze_block(self, block):
        # Process each statement in the block
        for statement in block.statements:
            self.analyze_statement(statement)

    def analyze_statement(self, stmt):
        if isinstance(stmt, ASTVariableDeclaration):
            self.analyze_variable_declaration(stmt)
        elif isinstance(stmt, ASTAssignment):
            self.analyze_assignment(stmt)
        elif isinstance(stmt, ASTIfStatement):
            self.analyze_if_statement(stmt)
        elif isinstance(stmt, ASTWhileStatement):
            self.analyze_while_statement(stmt)
        elif isinstance(stmt, ASTForStatement):
            self.analyze_for_statement(stmt)
        elif isinstance(stmt, ASTFunctionCall):
            self.analyze_function_call(stmt)

    def analyze_variable_declaration(self, decl):
        # Ensure variable is not redeclared
        if self.symbol_table.lookup_variable(decl.name):
            raise SemanticAnalysisError(f"Variable '{decl.name}' already declared.")
        
        # Add variable to the symbol table
        self.symbol_table.add_variable(decl.name, decl.type)
        # Analyze the expression assigned to the variable
        self.analyze_expression(decl.value)

    def analyze_assignment(self, stmt):
        # Ensure variable is declared before assignment
        if not self.symbol_table.lookup_variable(stmt.name):
            raise SemanticAnalysisError(f"Variable '{stmt.name}' is not declared.")
        
        # Analyze the expression being assigned
        self.analyze_expression(stmt.value)

    def analyze_function_call(self, call):
        # Check if function exists in the symbol table
        if not self.symbol_table.lookup_function(call.name):
            raise SemanticAnalysisError(f"Function '{call.name}' is not declared.")
        
        # Analyze the arguments of the function call
        for arg in call.args:
            self.analyze_expression(arg)

    def analyze_expression(self, expr):
        # Handle expressions such as binary operations, literals, and identifiers
        if isinstance(expr, ASTBinaryOp):
            self.analyze_expression(expr.left)
            self.analyze_expression(expr.right)
        elif isinstance(expr, ASTUnaryOp):
            self.analyze_expression(expr.operand)
        elif isinstance(expr, ASTLiteral):
            pass  # No need to analyze literals
        elif isinstance(expr, ASTIdentifier):
            # Check if identifier is declared
            if not self.symbol_table.lookup_variable(expr.name):
                raise SemanticAnalysisError(f"Variable '{expr.name}' is not declared.")
        else:
            raise SemanticAnalysisError(f"Unknown expression type: {type(expr)}")

    def analyze_if_statement(self, stmt):
        # Analyze the condition and both blocks of the if statement
        self.analyze_expression(stmt.condition)
        self.analyze_block(stmt.then_block)
        if stmt.else_block:
            self.analyze_block(stmt.else_block)

    def analyze_while_statement(self, stmt):
        # Analyze the condition and body of the while loop
        self.analyze_expression(stmt.condition)
        self.analyze_block(stmt.body)

    def analyze_for_statement(self, stmt):
        # Analyze the initialization, condition, update, and body of the for loop
        self.analyze_variable_declaration(stmt.init)
        self.analyze_expression(stmt.condition)
        self.analyze_assignment(stmt.update)
        self.analyze_block(stmt.body)

class SymbolTable:
    def __init__(self):
        self.functions = {}
        self.variables = {}

    def add_function(self, name):
        if name in self.functions:
            raise SemanticAnalysisError(f"Function '{name}' already declared.")
        self.functions[name] = True

    def add_variable(self, name, var_type):
        if name in self.variables:
            raise SemanticAnalysisError(f"Variable '{name}' already declared.")
        self.variables[name] = var_type

    def lookup_variable(self, name):
        return name in self.variables

    def lookup_function(self, name):
        return name in self.functions
