from lexer import Lexer
from parser import Parser
from ast_nodes import *

# === Sample PArL program to test the parser ===
source_code = """
fun fullTest(x: int, y: float, z: bool, c: colour) -> int {
    let result: int = x + __random_int(5);
    let red: colour = #ff0000;
    let isValid: bool = false;
    let pi: float = 3.14;
    let width: int = __width;
    let height: int = __height;
    let readVal: int = __read(1, 2);

    if (result > 0 and isValid or not isValid) {
        __print(result);
        __write(1, 2, 255);
        __write_box(1, 1, 3, 3, 0);
        __delay(10);
    }

    for (let i: int = 0; i < 5; i = i + 1) {
        let temp: float = 0.0;
        __print(i);
    }

    while (width > 0) {
        width = width - 1;
    }

    return result;
}

let values: int = [1, 2, 3, 4];
"""

# === Step 1: Run the lexer ===
lexer = Lexer(source_code)
tokens = lexer.tokenize()

# === Step 2: Run the parser ===
parser = Parser(tokens)
ast = parser.parse_program()

# === Step 3: Print the AST ===
def print_ast(node, indent=0):
    pad = '  ' * indent

    if isinstance(node, ASTProgram):
        print(pad + "Program")
        for fn in node.functions:
            print_ast(fn, indent + 1)

    elif isinstance(node, ASTFunctionDeclaration):
        print(pad + f"Function {node.name} -> {node.return_type}")
        for param in node.parameters:
            print_ast(param, indent + 1)
        print_ast(node.body, indent + 1)

    elif isinstance(node, ASTParameter):
        print(pad + f"Param {node.name}: {node.type}")

    elif isinstance(node, ASTBlock):
        print(pad + "Block")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)

    elif isinstance(node, ASTVariableDeclaration):
        print(pad + f"Declare {node.name}: {node.type} =")
        print_ast(node.value, indent + 1)

    elif isinstance(node, ASTReturnStatement):
        print(pad + "Return")
        print_ast(node.expression, indent + 1)

    elif isinstance(node, ASTIfStatement):
        print(pad + "If")
        print(pad + "  Condition:")
        print_ast(node.condition, indent + 2)
        print(pad + "  Then:")
        print_ast(node.then_block, indent + 2)
        if node.else_block:
            print(pad + "  Else:")
            print_ast(node.else_block, indent + 2)

    elif isinstance(node, ASTWhileStatement):
        print(pad + "While")
        print_ast(node.condition, indent + 1)
        print_ast(node.body, indent + 1)

    elif isinstance(node, ASTForStatement):
        print(pad + "For")
        print(pad + "  Init:")
        print_ast(node.init, indent + 2)
        print(pad + "  Condition:")
        print_ast(node.condition, indent + 2)
        print(pad + "  Update:")
        print_ast(node.update, indent + 2)
        print(pad + "  Body:")
        print_ast(node.body, indent + 2)

    elif isinstance(node, ASTAssignment):
        print(pad + f"Assignment {node.name} =")
        print_ast(node.value, indent + 1)

    elif isinstance(node, ASTBuiltinCall):
        print(pad + f"Builtin Call: {node.name}")
        for arg in node.args:
            print_ast(arg, indent + 1)

    elif isinstance(node, ASTFunctionCall):
        print(pad + f"Function Call: {node.name}")
        for arg in node.args:
            print_ast(arg, indent + 1)

    elif isinstance(node, ASTExpressionStatement):
        print(pad + "Expression Statement:")
        print_ast(node.expression, indent + 1)

    elif isinstance(node, ASTBinaryOp):
        print(pad + f"BinaryOp '{node.operator}'")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)

    elif isinstance(node, ASTUnaryOp):
        print(pad + f"UnaryOp '{node.operator}'")
        print_ast(node.operand, indent + 1)

    elif isinstance(node, ASTCast):
        print(pad + f"Cast to {node.target_type}")
        print_ast(node.expression, indent + 1)

    elif isinstance(node, ASTLiteral):
        print(pad + f"Literal {node.value}")

    else:
        print(pad + f"(Unknown node: {type(node).__name__})")

# === Execute ===
print_ast(ast)
