from lexer import Lexer

test_program = """
// Function definition with all parameter types and return
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

// Array declaration
let values: int = [1, 2, 3, 4];
"""

lexer = Lexer(test_program)
tokens = lexer.tokenize()

for token in tokens:
    print(f"{token.type}: '{token.lexeme}' (Line {token.line}, Col {token.column})")
