from lexer import Lexer
from parser import Parser
from ast_nodes import *
from semantic_analysis import *

# === Sample PArL program to test the parser ===
source_code = """
// This function takes two integers and return true if
// the first argument is greater than the second.
// Otherwise it returns false.
fun XGreaterY(x: int, y: int) -> bool {
    let ans: bool = true;
    if (y > x) { ans = false; }
    return ans;
}

// Same functionality as function above but using less code
fun XGreaterY_2(x: int, y: int) -> bool {
    return x > y;
}

// Allocates memory space for 4 variables (x, y, t0, t1).
fun AverageOfTwo(x: int, y: int) -> float {
    let t0: int = x + y;
    let t1: float = t0 / 2 as float; // casting expression to a float
    return t1;
}

// Same functionality as function above but using less code.
// Note the use of the brackets in the expression following
// the return statement. Allocates space for 2 variables.
fun AverageOfTwo_2(x: int, y: int) -> float {
    return (x + y) / 2 as float;
}

// Takes two integers and returns the max of the two.
fun Max(x: int, y: int) -> int {
    let m: int = x;
    if (y > x) { m = y; }
    return m;
}

// Writes to the console with some custom delay
__write 10, 14, #00ff00;
__delay 100;
__write_box 10, 14, 2, 2, #0000ff;

for (let i: int = 0; i < 10; i = i + 1) {
    __print(i);
}

fun Race(p1_c: colour, p2_c: colour, score_max: int) -> int {
    let p1_score: int = 0;
    let p2_score: int = 0;

    while ((p1_score < score_max) and (p2_score < score_max)) {
        let p1_toss: int = __randi 1000;
        let p2_toss: int = __randi 1000;

        if (p1_toss > p2_toss) {
            p1_score = p1_score + 1;
            __write 1, p1_score, p1_c;
        } else {
            p2_score = p2_score + 1;
            __write 2, p2_score, p2_c;
        }

        __delay 100;
    }

    if (p2_score > p1_score) {
        return 2;
    }
    return 1;
}

// Execution (program entry point) starts at the first statement
// that is not a function declaration. This should go in the .main
// function of ParIR.
let c1: colour = #00ff00;  // green
let c2: colour = #0000ff;  // blue
let m: int = __height;  // the height (y-values) of the pad
let w: int = Race(c1, c2, m);  // call function Race
__print w;  // prints value of expression to VM logs
"""

# === Step 1: Run the lexer ===
lexer = Lexer(source_code)
tokens = lexer.tokenize()

# === Step 2: Run the parser ===
parser = Parser(tokens)
ast = parser.parse_program()

# === Step 3: Run the semantic analysis ===
semantic_analyzer = SemanticAnalyzer()
semantic_analyzer.analyze(ast)

# === Step 4: Print the AST ===
def print_ast(node, indent=0):
    pad = '  ' * indent

    if isinstance(node, ASTProgram):
        print(pad + "Program")
        for decl in node.declarations:
            print_ast(decl, indent + 1)

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

    elif isinstance(node, ASTArrayLiteral):
        print(pad + "Array Literal")
        for el in node.elements:
            print_ast(el, indent + 1)

    else:
        print(pad + f"(Unknown node: {type(node).__name__})")

# === Execute the printing for the valid AST ===
print_ast(ast)
