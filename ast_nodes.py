# ast_nodes.py - AST node definitions for PArL

class ASTNode:
    pass

class ASTProgram(ASTNode):
    def __init__(self, declarations):
        self.declarations = declarations

class ASTFunctionDeclaration(ASTNode):
    def __init__(self, name, parameters, return_type, body):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body

class ASTParameter(ASTNode):
    def __init__(self, name, type):
        self.name = name
        self.type = type

class ASTBlock(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class ASTVariableDeclaration(ASTNode):
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value

class ASTAssignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class ASTReturnStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class ASTIfStatement(ASTNode):
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class ASTWhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ASTForStatement(ASTNode):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class ASTExpressionStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class ASTBuiltinCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ASTFunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ASTBinaryOp(ASTNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class ASTUnaryOp(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

class ASTCast(ASTNode):
    def __init__(self, expression, target_type):
        self.expression = expression
        self.target_type = target_type

class ASTLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

class ASTArrayLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements
