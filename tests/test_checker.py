"""
Test cases for TyC Static Semantic Checker

This module contains 100 test cases for the static semantic checker.
Covers all 8 error types + valid programs comprehensively.

Categories:
  001-010  Valid programs (basic, functions, structs, control flow, type inference)
  011-020  Redeclared (Struct, Function, Variable, Parameter)
  021-030  UndeclaredIdentifier / UndeclaredFunction / UndeclaredStruct
  031-040  TypeCannotBeInferred (auto edge-cases)
  041-060  TypeMismatchInExpression (binary, unary, member, call, assign, struct)
  061-080  TypeMismatchInStatement (if, while, for, switch, return, VarDecl)
  081-090  MustInLoop (break/continue)
  091-100  Mixed advanced / comprehensive valid programs
"""

from tests.utils import Checker


# ==============================================================================
# TEST 001-010: VALID PROGRAMS
# ==============================================================================

def test_001():
    """Valid: minimal void main"""
    source = """
void main() {
    int x = 5;
    int y = x + 1;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_002():
    """Valid: auto inference from literals"""
    source = """
void main() {
    auto x = 10;
    auto y = 3.14;
    auto z = "hello";
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_003():
    """Valid: function call returning int"""
    source = """
int add(int x, int y) {
    return x + y;
}
void main() {
    int sum = add(5, 3);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_004():
    """Valid: struct declaration plus member access"""
    source = """
struct Point {
    int x;
    int y;
};
void main() {
    Point p;
    p.x = 10;
    p.y = 20;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_005():
    """Valid: nested blocks with shadowing"""
    source = """
void main() {
    int x = 10;
    {
        int x = 20;
        int y = x + 1;
    }
    int z = x + 5;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_006():
    """Valid: for loop with break and continue"""
    source = """
void main() {
    for (int i = 0; i < 10; ++i) {
        if (i % 2 == 0) continue;
        if (i > 7) break;
        printInt(i);
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_007():
    """Valid: while loop"""
    source = """
void main() {
    int i = 0;
    while (i < 10) {
        printInt(i);
        ++i;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_008():
    """Valid: switch statement with break"""
    source = """
void main() {
    int day = 2;
    switch (day) {
        case 1:
            printString("Mon");
            break;
        case 2:
            printString("Tue");
            break;
        default:
            printString("Other");
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_009():
    """Valid: built-in functions"""
    source = """
void main() {
    int x = readInt();
    printInt(x);
    float f = readFloat();
    printFloat(f);
    string s = readString();
    printString(s);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_010():
    """Valid: auto without init inferred from assignment"""
    source = """
void main() {
    auto a;
    a = 10;
    int b = a + 5;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


# ==============================================================================
# TEST 011-020: REDECLARED
# ==============================================================================

def test_011():
    """Redeclared Struct in global scope"""
    source = """
struct Point { int x; int y; };
struct Point { int z; };
"""
    assert Checker(source).check_from_source() == "Redeclared(Struct, Point)"


def test_012():
    """Redeclared Function in global scope"""
    source = """
int add(int x, int y) { return x + y; }
int add(int a, int b) { return a + b; }
"""
    assert Checker(source).check_from_source() == "Redeclared(Function, add)"


def test_013():
    """Redeclared Variable in same block"""
    source = """
void main() {
    int count = 10;
    int count = 20;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, count)"


def test_014():
    """Redeclared Parameter"""
    source = """
int calc(int x, float y, int x) {
    return x;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Parameter, x)"


def test_015():
    """Redeclared: function name same as struct"""
    source = """
struct Foo { int a; };
void Foo() {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Function, Foo)"


def test_016():
    """Redeclared Variable inside nested block (same block level)"""
    source = """
void main() {
    {
        int a = 1;
        int a = 2;
    }
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, a)"


def test_017():
    """Valid: shadowing across blocks is OK"""
    source = """
void main() {
    int val = 100;
    {
        int val = 200;
        {
            int val = 300;
        }
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_018():
    """Valid: same variable name in sibling blocks"""
    source = """
void main() {
    int x = 10;
    { int y = 20; }
    int y = 30;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_019():
    """Redeclared: parameter clashes with another parameter"""
    source = """
void foo(int a, int b, float a) {}
"""
    assert Checker(source).check_from_source() == "Redeclared(Parameter, a)"


def test_020():
    """Redeclared: variable same name as parameter (same scope)"""
    source = """
void foo(int x) {
    int x = 5;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, x)"


# ==============================================================================
# TEST 021-030: UNDECLARED
# ==============================================================================

def test_021():
    """UndeclaredIdentifier: undeclared variable"""
    source = """
void main() {
    int result = undeclaredVar + 10;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(undeclaredVar)"


def test_022():
    """UndeclaredIdentifier: variable used before declaration"""
    source = """
void main() {
    int x = y + 5;
    int y = 10;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(y)"


def test_023():
    """UndeclaredIdentifier: cross-function scope"""
    source = """
void method1() {
    int localVar = 42;
}
void method2() {
    int value = localVar + 1;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(localVar)"


def test_024():
    """UndeclaredFunction: call undeclared function"""
    source = """
void main() {
    int result = calculate(5, 3);
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(calculate)"


def test_025():
    """UndeclaredFunction: forward reference (function declared later)"""
    source = """
void test() {
    int value = add(10, 20);
}
int add(int x, int y) {
    return x + y;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(add)"


def test_026():
    """UndeclaredStruct: struct used before declaration"""
    source = """
void main() {
    Point p;
}
struct Point { int x; int y; };
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(Point)"


def test_027():
    """UndeclaredStruct: struct member uses undeclared struct type"""
    source = """
struct Address {
    string street;
    City city;
};
struct City { string name; };
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(City)"


def test_028():
    """UndeclaredStruct: struct used as parameter type before declaration"""
    source = """
void foo(Point p) {}
struct Point { int x; int y; };
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(Point)"


def test_029():
    """Valid: struct declared before use as member"""
    source = """
struct Point { int x; int y; };
struct Line { Point start; Point end; };
void main() {
    Line l;
    l.start.x = 1;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_030():
    """Valid: function declared before call"""
    source = """
int multiply(int x, int y) {
    return x * y;
}
void main() {
    int result = multiply(5, 3);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


# ==============================================================================
# TEST 031-040: TYPE CANNOT BE INFERRED
# ==============================================================================

def test_031():
    """TypeCannotBeInferred: two auto unknowns assigned"""
    source = """
void main() {
    auto x;
    auto y;
    x = y;
}
"""
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(x)"


def test_032():
    """TypeCannotBeInferred: binary op with two unknowns"""
    source = """
void main() {
    auto a;
    auto b;
    auto c = a + b;
}
"""
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(a)"


def test_033():
    """TypeCannotBeInferred: auto = bare struct literal"""
    source = """
void main() {
    auto p = {1, 2};
}
"""
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(p)"


def test_034():
    """TypeCannotBeInferred: circular dependency"""
    source = """
void main() {
    auto a; auto b;
    a = b;
    b = a;
}
"""
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(a)"


def test_035():
    """Valid: auto inferred from printInt parameter"""
    source = """
void main() {
    auto x;
    printInt(x);
    x = 5;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_036():
    """Valid: auto inferred from expression with known literal"""
    source = """
void main() {
    auto x;
    auto y = x + 5;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_037():
    """Valid: function return type inferred from first return"""
    source = """
auto_func() {
    return 3.14;
}
void main() {
    float x = auto_func();
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_038():
    """TypeMismatchInStatement: inferred return type mismatch on second return"""
    source = """
test_func() {
    if (1) {
        return 10;
    }
    return 3.14;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ReturnStmt(return FloatLiteral(3.14)))"


def test_039():
    """Valid: auto with struct type from function call"""
    source = """
struct Point { int x; int y; };
Point getOrigin() {
    return {0, 0};
}
void main() {
    auto p = getOrigin();
    int x = p.x;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_040():
    """Valid: auto without init, inferred from readFloat"""
    source = """
void main() {
    auto f;
    f = readFloat();
    printFloat(f);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


# ==============================================================================
# TEST 041-060: TYPE MISMATCH IN EXPRESSION
# ==============================================================================

def test_041():
    """TypeMismatchInExpression: int + string"""
    source = """
void main() {
    int x = 5;
    string text = "hello";
    int sum = x + text;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(x), +, Identifier(text)))"


def test_042():
    """TypeMismatchInExpression: float % int (modulus requires int only)"""
    source = """
void main() {
    float f = 3.14;
    int x = 10;
    int result = f % x;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(f), %, Identifier(x)))"


def test_043():
    """TypeMismatchInExpression: int % float"""
    source = """
void main() {
    int x = 10;
    float f = 3.14;
    int result = x % f;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(x), %, Identifier(f)))"


def test_044():
    """TypeMismatchInExpression: string == int"""
    source = """
void main() {
    string text = "hello";
    int x = 10;
    int equal = text == x;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(text), ==, Identifier(x)))"


def test_045():
    """TypeMismatchInExpression: float && int (logical requires int only)"""
    source = """
void main() {
    float f = 3.14;
    int x = 10;
    int result = f && x;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(f), &&, Identifier(x)))"


def test_046():
    """TypeMismatchInExpression: float || float"""
    source = """
void main() {
    float a = 1.0;
    float b = 2.0;
    int c = a || b;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(a), ||, Identifier(b)))"


def test_047():
    """TypeMismatchInExpression: !float"""
    source = """
void main() {
    float f = 3.14;
    int not_f = !f;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PrefixOp(!Identifier(f)))"


def test_048():
    """TypeMismatchInExpression: ++float (prefix)"""
    source = """
void main() {
    float f = 3.14;
    ++f;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PrefixOp(++Identifier(f)))"


def test_049():
    """TypeMismatchInExpression: float++ (postfix)"""
    source = """
void main() {
    float f = 3.14;
    f++;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PostfixOp(Identifier(f)++))"


def test_050():
    """TypeMismatchInExpression: ++literal"""
    source = """
void main() {
    ++5;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PrefixOp(++IntLiteral(5)))"


def test_051():
    """TypeMismatchInExpression: --(x + 1) (non-lvalue)"""
    source = """
void main() {
    int x = 5;
    --(x + 1);
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PrefixOp(--BinaryOp(Identifier(x), +, IntLiteral(1))))"


def test_052():
    """TypeMismatchInExpression: (x + 2)++ (non-lvalue postfix)"""
    source = """
void main() {
    int x = 5;
    (x + 2)++;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PostfixOp(BinaryOp(Identifier(x), +, IntLiteral(2))++))"


def test_053():
    """TypeMismatchInExpression: member access on non-struct"""
    source = """
void main() {
    int x = 10;
    int value = x.member;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(MemberAccess(Identifier(x).member))"


def test_054():
    """TypeMismatchInExpression: member access to non-existent field"""
    source = """
struct Point { int x; int y; };
void main() {
    Point p = {10, 20};
    int invalid = p.z;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(MemberAccess(Identifier(p).z))"


def test_055():
    """TypeMismatchInExpression: function call wrong argument type"""
    source = """
void process(int x) {}
void main() {
    string text = "123";
    process(text);
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(FuncCall(process, [Identifier(text)]))"


def test_056():
    """TypeMismatchInExpression: function call too few arguments"""
    source = """
int add(int x, int y) {
    return x + y;
}
void main() {
    int result = add(10);
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(FuncCall(add, [IntLiteral(10)]))"


def test_057():
    """TypeMismatchInExpression: function call too many arguments"""
    source = """
int add(int x, int y) {
    return x + y;
}
void main() {
    int result = add(10, 20, 30);
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(FuncCall(add, [IntLiteral(10), IntLiteral(20), IntLiteral(30)]))"


def test_058():
    """TypeMismatchInExpression: assign int = string"""
    source = """
void main() {
    int x = 10;
    string text = "hello";
    x = text;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(AssignExpr(Identifier(x) = Identifier(text)))"


def test_059():
    """TypeMismatchInExpression: struct equality not supported"""
    source = """
struct Point { int x; int y; };
void main() {
    Point p1 = {1, 2};
    Point p2 = {1, 2};
    int same = p1 == p2;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(p1), ==, Identifier(p2)))"


def test_060():
    """TypeMismatchInExpression: string concatenation not supported"""
    source = """
void main() {
    string s = "a" + "b";
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(StringLiteral('a'), +, StringLiteral('b')))"


# ==============================================================================
# TEST 061-080: TYPE MISMATCH IN STATEMENT
# ==============================================================================

def test_061():
    """TypeMismatchInStatement: if condition is float"""
    source = """
void main() {
    float x = 5.0;
    if (x) {
        printInt(1);
    }
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(IfStmt(if Identifier(x) then BlockStmt([ExprStmt(FuncCall(printInt, [IntLiteral(1)]))])))"


def test_062():
    """TypeMismatchInStatement: if condition is string"""
    source = """
void main() {
    string message = "hello";
    if (message) {
        printString(message);
    }
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(IfStmt(if Identifier(message) then BlockStmt([ExprStmt(FuncCall(printString, [Identifier(message)]))])))"


def test_063():
    """TypeMismatchInStatement: while condition is float"""
    source = """
void main() {
    float f = 1.5;
    while (f) {
        printFloat(f);
    }
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(WhileStmt(while Identifier(f) do BlockStmt([ExprStmt(FuncCall(printFloat, [Identifier(f)]))])))"


def test_064():
    """TypeMismatchInStatement: for condition is string"""
    source = """
void main() {
    int i = 0;
    for (i=1; "s"; i++) {}
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ForStmt(for ExprStmt(AssignExpr(Identifier(i) = IntLiteral(1))); StringLiteral('s'); PostfixOp(Identifier(i)++) do BlockStmt([])))"


def test_065():
    """TypeMismatchInStatement: for condition is string (with VarDecl init)"""
    source = """
void main() {
    for (int i = 0; "hello"; ++i) {}
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); StringLiteral('hello'); PrefixOp(++Identifier(i)) do BlockStmt([])))"


def test_066():
    """TypeMismatchInStatement: switch expression is float"""
    source = """
void main() {
    float f = 3.14;
    switch (f) {
        case 1: break;
    }
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(SwitchStmt(switch Identifier(f) cases [CaseStmt(case IntLiteral(1): [BreakStmt()])]))"


def test_067():
    """TypeMismatchInStatement: case expression is float"""
    source = """
void main() {
    int x = 1;
    switch (x) {
        case 1.5: break;
    }
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(CaseStmt(case FloatLiteral(1.5): [BreakStmt()]))"


def test_068():
    """TypeMismatchInStatement: return string from int function"""
    source = """
int getValue() {
    return "invalid";
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ReturnStmt(return StringLiteral('invalid')))"


def test_069():
    """TypeMismatchInStatement: return without value from non-void function"""
    source = """
int returnVoidError() {
    return;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ReturnStmt(return))"


def test_070():
    """TypeMismatchInStatement: void function returns value"""
    source = """
void doNothing() {
    return 5;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ReturnStmt(return IntLiteral(5)))"


def test_071():
    """TypeMismatchInStatement: return int from string-returning function"""
    source = """
string getText() {
    return 42;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ReturnStmt(return IntLiteral(42)))"


def test_072():
    """TypeMismatchInStatement: VarDecl init type mismatch (int = string)"""
    source = """
void main() {
    int x = "hello";
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(IntType(), x = StringLiteral('hello')))"


def test_073():
    """TypeMismatchInStatement: VarDecl init type mismatch (string = int)"""
    source = """
void main() {
    string s = 42;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(StringType(), s = IntLiteral(42)))"


def test_074():
    """TypeMismatchInStatement: struct literal field count mismatch"""
    source = """
struct Point { int x; int y; };
void main() {
    Point p = {10};
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(StructType(Point), p = StructLiteral({IntLiteral(10)})))"


def test_075():
    """TypeMismatchInStatement: struct literal field type mismatch"""
    source = """
struct Point { int x; int y; };
void main() {
    Point p = {10, "string"};
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(StructType(Point), p = StructLiteral({IntLiteral(10), StringLiteral('string')})))"


def test_076():
    """TypeMismatchInExpression: different struct assignment"""
    source = """
struct Point { int x; int y; };
struct Person { int age; int height; };
void main() {
    Point p;
    Person ps;
    p = ps;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(AssignExpr(Identifier(p) = Identifier(ps)))"


def test_077():
    """TypeMismatchInExpression: printInt with float argument"""
    source = """
void main() {
    printInt(3.14);
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(FuncCall(printInt, [FloatLiteral(3.14)]))"


def test_078():
    """TypeMismatchInExpression: unary minus on string"""
    source = """
void main() {
    string s = -"hello";
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PrefixOp(-StringLiteral('hello')))"


def test_079():
    """TypeMismatchInExpression: < on strings"""
    source = """
void main() {
    int b = "a" < "b";
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(StringLiteral('a'), <, StringLiteral('b')))"


def test_080():
    """TypeMismatchInExpression: chained assignment type mismatch"""
    source = """
void main() {
    int a; float b;
    a = b = 3.14;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(AssignExpr(Identifier(a) = AssignExpr(Identifier(b) = FloatLiteral(3.14))))"


# ==============================================================================
# TEST 081-090: MUST IN LOOP
# ==============================================================================

def test_081():
    """MustInLoop: break outside any loop"""
    source = """
void main() {
    break;
}
"""
    assert Checker(source).check_from_source() == "MustInLoop(BreakStmt())"


def test_082():
    """MustInLoop: continue outside any loop"""
    source = """
void main() {
    continue;
}
"""
    assert Checker(source).check_from_source() == "MustInLoop(ContinueStmt())"


def test_083():
    """MustInLoop: continue in switch (not allowed)"""
    source = """
void main() {
    int x = 1;
    switch (x) {
        case 1:
            break;
            continue;
    }
}
"""
    assert Checker(source).check_from_source() == "MustInLoop(ContinueStmt())"


def test_084():
    """MustInLoop: break in if without loop"""
    source = """
void main() {
    if (1) { break; }
}
"""
    assert Checker(source).check_from_source() == "MustInLoop(BreakStmt())"


def test_085():
    """MustInLoop: continue in if without loop"""
    source = """
void main() {
    if (1) { continue; }
}
"""
    assert Checker(source).check_from_source() == "MustInLoop(ContinueStmt())"


def test_086():
    """Valid: break and continue inside for loop"""
    source = """
void main() {
    for (int i = 0; i < 5; ++i) {
        break;
        continue;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_087():
    """Valid: break inside switch (allowed)"""
    source = """
void main() {
    int day = 2;
    switch (day) {
        case 1:
            printInt(1);
            break;
        case 2:
        case 3:
            printInt(2);
            break;
        default:
            printInt(0);
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_088():
    """Valid: break/continue in nested loop"""
    source = """
void main() {
    for (int i = 0; i < 5; ++i) {
        for (int j = 0; j < 5; ++j) {
            if (i == j) continue;
            if (j > 3) break;
        }
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_089():
    """Valid: break in while loop"""
    source = """
void main() {
    int i = 0;
    while (i < 10) {
        if (i == 5) break;
        ++i;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_090():
    """MustInLoop: break in function called from loop (different scope)"""
    source = """
void helper() {
    break;
}
void main() {
    for (int i = 0; i < 10; ++i) {
        helper();
    }
}
"""
    assert Checker(source).check_from_source() == "MustInLoop(BreakStmt())"


# ==============================================================================
# TEST 091-100: ADVANCED / COMPREHENSIVE
# ==============================================================================

def test_091():
    """Valid: nested struct initialization"""
    source = """
struct Point { int x; int y; };
struct Circle { Point center; float radius; };
void main() {
    Circle c = {{0, 0}, 5.5};
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_092():
    """Valid: function call with struct literal argument"""
    source = """
struct Point { int x; int y; };
void foo(Point p) {}
void main() {
    foo({1, 2});
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_093():
    """TypeMismatchInExpression: struct literal passed to int parameter"""
    source = """
struct Point { int x; int y; };
void foo(int a) {}
void main() {
    foo({1, 2});
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(FuncCall(foo, [StructLiteral({IntLiteral(1), IntLiteral(2)})]))"


def test_094():
    """Valid: struct member increment"""
    source = """
struct Counter { int val; };
void main() {
    Counter c = {0};
    c.val++;
    ++c.val;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_095():
    """TypeMismatchInExpression: postfix increment on function call result (non-lvalue)"""
    source = """
int getVal() { return 5; }
void main() {
    getVal()++;
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PostfixOp(FuncCall(getVal, [])++))"


def test_096():
    """Valid: chained assignment"""
    source = """
void main() {
    int a; int b; int c;
    a = b = c = 10;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_097():
    """Valid: assignment expression inside another expression"""
    source = """
void main() {
    int x;
    int y = (x = 5) + 10;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_098():
    """Valid: switch with constant expression in case"""
    source = """
void main() {
    int x = 5;
    switch (x) {
        case 2 + 3:
            printInt(x);
            break;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_099():
    """Valid: built-in composition"""
    source = """
void main() {
    printInt(readInt() + 5);
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"


def test_100():
    """Valid: comprehensive TyC program with structures, loops, switch, type inference"""
    source = """
struct Stats { int hp; float speed; };
struct Player { string name; Stats stats; };

Player createPlayer(string name) {
    return {name, {100, 5.5}};
}

void main() {
    auto p1 = createPlayer("Hero");
    auto p2 = p1;

    p2.stats.hp = p2.stats.hp - 20;

    for (auto i = 0; i < 5; i++) {
        if (i % 2 == 0) continue;
        p2.stats.speed = p2.stats.speed + 1.0;
    }

    switch (p2.stats.hp) {
        case 80:
            printString("Damaged");
            break;
        default:
            printString("Unknown");
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"