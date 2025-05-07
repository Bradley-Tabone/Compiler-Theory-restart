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

    def __str__(self):
        params = ', '.join(str(param) for param in self.parameters)
        return f"Function {self.name}({params}) -> {self.return_type}"

class ASTParameter(ASTNode):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return f"{self.name}: {self.type}"

class ASTBlock(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class ASTVariableDeclaration(ASTNode):
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value

    def __str__(self):
        return f"let {self.name}: {self.type} = {self.value}"

class ASTAssignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name} = {self.value}"

class ASTReturnStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return f"return {self.expression}"

class ASTIfStatement(ASTNode):
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __str__(self):
        else_part = f" else {self.else_block}" if self.else_block else ""
        return f"if ({self.condition}) then {self.then_block}{else_part}"

class ASTWhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self):
        return f"while ({self.condition}) {self.body}"

class ASTForStatement(ASTNode):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def __str__(self):
        return f"for ({self.init}; {self.condition}; {self.update}) {self.body}"

class ASTExpressionStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return f"{self.expression}"

class ASTBuiltinCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        return f"{self.name}({', '.join(str(arg) for arg in self.args)})"

class ASTFunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        return f"{self.name}({', '.join(str(arg) for arg in self.args)})"

class ASTBinaryOp(ASTNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"

class ASTUnaryOp(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __str__(self):
        return f"({self.operator} {self.operand})"

class ASTCast(ASTNode):
    def __init__(self, expression, target_type):
        self.expression = expression
        self.target_type = target_type

    def __str__(self):
        return f"({self.expression} as {self.target_type})"

class ASTLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class ASTArrayLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements

    def __str__(self):
        return f"[{', '.join(str(e) for e in self.elements)}]"

class ASTIdentifier(ASTNode):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
