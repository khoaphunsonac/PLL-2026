import pytest
from tests.utils import ASTGenerator

def check(source, expected):
    ast = ASTGenerator(source).generate()
    assert str(ast) == expected

# ============================================================================
# GROUP 1: Empty & Basic Programs, Struct Declarations (001-010)
# ============================================================================
def test_001(): check("", "Program([])")
def test_002(): check("struct A{};", "Program([StructDecl(A, [])])")
def test_003(): check("struct A{int x;};", "Program([StructDecl(A, [MemberDecl(IntType(), x)])])")
def test_004(): check("struct A{float x; string y;};", "Program([StructDecl(A, [MemberDecl(FloatType(), x), MemberDecl(StringType(), y)])])")
def test_005(): check("struct A{B x;};", "Program([StructDecl(A, [MemberDecl(StructType(B), x)])])")
def test_006(): check("void main(){}", "Program([FuncDecl(VoidType(), main, [], BlockStmt([]))])")
def test_007(): check("int f(){}", "Program([FuncDecl(IntType(), f, [], BlockStmt([]))])")
def test_008(): check("float f(){}", "Program([FuncDecl(FloatType(), f, [], BlockStmt([]))])")
def test_009(): check("string f(){}", "Program([FuncDecl(StringType(), f, [], BlockStmt([]))])")
def test_010(): check("A f(){}", "Program([FuncDecl(StructType(A), f, [], BlockStmt([]))])")

# ============================================================================
# GROUP 2: Function Declarations & Inferred Returns (011-014)
# ============================================================================
def test_011(): check("f(){}", "Program([FuncDecl(auto, f, [], BlockStmt([]))])")
def test_012(): check("void f(int a){}", "Program([FuncDecl(VoidType(), f, [Param(IntType(), a)], BlockStmt([]))])")
def test_013(): check("void f(int a, float b){}", "Program([FuncDecl(VoidType(), f, [Param(IntType(), a), Param(FloatType(), b)], BlockStmt([]))])")
def test_014(): check("void f(A a){}", "Program([FuncDecl(VoidType(), f, [Param(StructType(A), a)], BlockStmt([]))])")

# ============================================================================
# GROUP 3: Variable Declarations (015-025)
# ============================================================================
def test_015(): check("void main(){ int a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), a)]))])")
def test_016(): check("void main(){ float a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(FloatType(), a)]))])")
def test_017(): check("void main(){ string a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StringType(), a)]))])")
def test_018(): check("void main(){ A a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(A), a)]))])")
def test_019(): check("void main(){ auto a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a)]))])")
def test_020(): check("void main(){ int a = 1; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), a = IntLiteral(1))]))])")
def test_021(): check("void main(){ float a = 1.5; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(FloatType(), a = FloatLiteral(1.5))]))])")
def test_022(): check("void main(){ string a = \"hcmut\"; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StringType(), a = StringLiteral('hcmut'))]))])")
def test_023(): check("void main(){ auto a = 1; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, a = IntLiteral(1))]))])")
def test_024(): check("void main(){ A a = {1, 2}; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(A), a = StructLiteral({IntLiteral(1), IntLiteral(2)}))]))])")
def test_025(): check("void main(){ A a = {{1}, 2}; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(A), a = StructLiteral({StructLiteral({IntLiteral(1)}), IntLiteral(2)}))]))])")

# ============================================================================
# GROUP 4: Primary Expressions & Literals (026-034)
# ============================================================================
def test_026(): check("void main(){ 1; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(IntLiteral(1))]))])")
def test_027(): check("void main(){ 1.5; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(FloatLiteral(1.5))]))])")
def test_028(): check("void main(){ \"hcmut\"; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(StringLiteral('hcmut'))]))])")
def test_029(): check("void main(){ a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(Identifier(a))]))])")
def test_030(): check("void main(){ a.b; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(MemberAccess(Identifier(a).b))]))])")
def test_031(): check("void main(){ a.b.c; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(MemberAccess(MemberAccess(Identifier(a).b).c))]))])")
def test_032(): check("void main(){ f(); }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(FuncCall(f, []))]))])")
def test_033(): check("void main(){ f(1); }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(FuncCall(f, [IntLiteral(1)]))]))])")
def test_034(): check("void main(){ f(1, a); }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(FuncCall(f, [IntLiteral(1), Identifier(a)]))]))])")

# ============================================================================
# GROUP 5: Assignments (035-037)
# ============================================================================
def test_035(): check("void main(){ a = 1; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(a) = IntLiteral(1)))]))])")
def test_036(): check("void main(){ a.b = 1; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(MemberAccess(Identifier(a).b) = IntLiteral(1)))]))])")
def test_037(): check("void main(){ a = b = 1; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(a) = AssignExpr(Identifier(b) = IntLiteral(1))))]))])")

# ============================================================================
# GROUP 6: Arithmetic & Parentheses (038-044)
# ============================================================================
def test_038(): check("void main(){ 1 + 2; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(IntLiteral(1), +, IntLiteral(2)))]))])")
def test_039(): check("void main(){ 1 - 2; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(IntLiteral(1), -, IntLiteral(2)))]))])")
def test_040(): check("void main(){ 1 * 2; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(IntLiteral(1), *, IntLiteral(2)))]))])")
def test_041(): check("void main(){ 1 / 2; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(IntLiteral(1), /, IntLiteral(2)))]))])")
def test_042(): check("void main(){ 1 % 2; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(IntLiteral(1), %, IntLiteral(2)))]))])")
def test_043(): check("void main(){ 1 + 2 * 3; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(IntLiteral(1), +, BinaryOp(IntLiteral(2), *, IntLiteral(3))))]))])")
def test_044(): check("void main(){ (1 + 2) * 3; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(BinaryOp(IntLiteral(1), +, IntLiteral(2)), *, IntLiteral(3)))]))])")

# ============================================================================
# GROUP 7: Relational & Logical Expressions (045-054)
# ============================================================================
def test_045(): check("void main(){ 1 < 2; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(IntLiteral(1), <, IntLiteral(2)))]))])")
def test_046(): check("void main(){ 1 > 2; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(IntLiteral(1), >, IntLiteral(2)))]))])")
def test_047(): check("void main(){ 1 <= 2; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(IntLiteral(1), <=, IntLiteral(2)))]))])")
def test_048(): check("void main(){ 1 >= 2; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(IntLiteral(1), >=, IntLiteral(2)))]))])")
def test_049(): check("void main(){ 1 == 2; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(IntLiteral(1), ==, IntLiteral(2)))]))])")
def test_050(): check("void main(){ 1 != 2; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(IntLiteral(1), !=, IntLiteral(2)))]))])")
def test_051(): check("void main(){ a && b; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(Identifier(a), &&, Identifier(b)))]))])")
def test_052(): check("void main(){ a || b; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(Identifier(a), ||, Identifier(b)))]))])")
def test_053(): check("void main(){ a || b && c; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(Identifier(a), ||, BinaryOp(Identifier(b), &&, Identifier(c))))]))])")
def test_054(): check("void main(){ a && b || c; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(BinaryOp(Identifier(a), &&, Identifier(b)), ||, Identifier(c)))]))])")

# ============================================================================
# GROUP 8: Unary, Prefix, Postfix (055-063)
# ============================================================================
def test_055(): check("void main(){ !a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PrefixOp(!Identifier(a)))]))])")
def test_056(): check("void main(){ -a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PrefixOp(-Identifier(a)))]))])")
def test_057(): check("void main(){ +a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PrefixOp(+Identifier(a)))]))])")
def test_058(): check("void main(){ ++a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PrefixOp(++Identifier(a)))]))])")
def test_059(): check("void main(){ --a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PrefixOp(--Identifier(a)))]))])")
def test_060(): check("void main(){ a++; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PostfixOp(Identifier(a)++))]))])")
def test_061(): check("void main(){ a--; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PostfixOp(Identifier(a)--))]))])")
def test_062(): check("void main(){ ++a++; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PrefixOp(++PostfixOp(Identifier(a)++)))]))])")
def test_063(): check("void main(){ !-a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PrefixOp(!PrefixOp(-Identifier(a))))]))])")

# ============================================================================
# GROUP 9: Control Flows - Return, Break, Continue, If, While (064-072)
# ============================================================================
def test_064(): check("void main(){ return; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ReturnStmt(return)]))])")
def test_065(): check("void main(){ return 1; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ReturnStmt(return IntLiteral(1))]))])")
def test_066(): check("void main(){ break; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([BreakStmt()]))])")
def test_067(): check("void main(){ continue; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ContinueStmt()]))])")
def test_068(): check("void main(){ if (a) b; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(a) then ExprStmt(Identifier(b)))]))])")
def test_069(): check("void main(){ if (a) b; else c; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(a) then ExprStmt(Identifier(b)), else ExprStmt(Identifier(c)))]))])")
def test_070(): check("void main(){ if (a) { b; } }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(a) then BlockStmt([ExprStmt(Identifier(b))]))]))])")
def test_071(): check("void main(){ while (a) b; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while Identifier(a) do ExprStmt(Identifier(b)))]))])")
def test_072(): check("void main(){ while (a) { b; } }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while Identifier(a) do BlockStmt([ExprStmt(Identifier(b))]))]))])")

# ============================================================================
# GROUP 10: Control Flows - For Loop Combinations (073-080)
# ============================================================================
def test_073(): check("void main(){ for(;;) a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for None; None; None do ExprStmt(Identifier(a)))]))])")
def test_074(): check("void main(){ for(int i=0;;) a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); None; None do ExprStmt(Identifier(a)))]))])")
def test_075(): check("void main(){ for(auto i=0;;) a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(auto, i = IntLiteral(0)); None; None do ExprStmt(Identifier(a)))]))])")
def test_076(): check("void main(){ for(i=0;;) a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for ExprStmt(AssignExpr(Identifier(i) = IntLiteral(0))); None; None do ExprStmt(Identifier(a)))]))])")
def test_077(): check("void main(){ for(;i<1;) a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for None; BinaryOp(Identifier(i), <, IntLiteral(1)); None do ExprStmt(Identifier(a)))]))])")
def test_078(): check("void main(){ for(;;i++) a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for None; None; PostfixOp(Identifier(i)++) do ExprStmt(Identifier(a)))]))])")
def test_079(): check("void main(){ for(;;++i) a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for None; None; PrefixOp(++Identifier(i)) do ExprStmt(Identifier(a)))]))])")
def test_080(): check("void main(){ for(;;i=i+1) a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for None; None; AssignExpr(Identifier(i) = BinaryOp(Identifier(i), +, IntLiteral(1))) do ExprStmt(Identifier(a)))]))])")

# ============================================================================
# GROUP 11: Control Flows - Switch Case (081-086)
# ============================================================================
def test_081(): check("void main(){ switch(a) {} }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(a) cases [])]))])")
def test_082(): check("void main(){ switch(a) { case 1: b; } }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(a) cases [CaseStmt(case IntLiteral(1): [ExprStmt(Identifier(b))])])]))])")
def test_083(): check("void main(){ switch(a) { default: b; } }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(a) cases [], default DefaultStmt(default: [ExprStmt(Identifier(b))]))]))])")
def test_084(): check("void main(){ switch(a) { case 1: b; case 2: c; } }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(a) cases [CaseStmt(case IntLiteral(1): [ExprStmt(Identifier(b))]), CaseStmt(case IntLiteral(2): [ExprStmt(Identifier(c))])])]))])")
def test_085(): check("void main(){ switch(a) { case 1: b; default: c; } }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(a) cases [CaseStmt(case IntLiteral(1): [ExprStmt(Identifier(b))])], default DefaultStmt(default: [ExprStmt(Identifier(c))]))]))])")
def test_086(): check("void main(){ switch(a) { default: c; case 1: b; } }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(a) cases [CaseStmt(case IntLiteral(1): [ExprStmt(Identifier(b))])], default DefaultStmt(default: [ExprStmt(Identifier(c))]))]))])")

# ============================================================================
# GROUP 12: Blocks & Complex Nested AST structures (087-100)
# ============================================================================
def test_087(): check("void main(){ {} }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([BlockStmt([])]))])")
def test_088(): check("void main(){ { a; } }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([BlockStmt([ExprStmt(Identifier(a))])]))])")
def test_089(): check("void main(){ a == b == c; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(BinaryOp(BinaryOp(Identifier(a), ==, Identifier(b)), ==, Identifier(c)))]))])")
def test_090(): check("void main(){ a = b = c = 1; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(a) = AssignExpr(Identifier(b) = AssignExpr(Identifier(c) = IntLiteral(1)))))]))])")
def test_091(): check("void main(){ f().a.b; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(MemberAccess(MemberAccess(FuncCall(f, []).a).b))]))])")
def test_092(): check("void main(){ {1, 2}.a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(MemberAccess(StructLiteral({IntLiteral(1), IntLiteral(2)}).a))]))])")
def test_093(): check("void main(){ ++--a; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PrefixOp(++PrefixOp(--Identifier(a))))]))])")
def test_094(): check("void main(){ a++--; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PostfixOp(PostfixOp(Identifier(a)++)--))]))])")
def test_095(): check("void main(){ a.b++; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PostfixOp(MemberAccess(Identifier(a).b)++))]))])")
def test_096(): check("void main(){ ++a.b; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PrefixOp(++MemberAccess(Identifier(a).b)))]))])")
def test_097(): check("void main(){ (a); }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(Identifier(a))]))])")
def test_098(): check("void main(){ f(1+2, a=3); }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(FuncCall(f, [BinaryOp(IntLiteral(1), +, IntLiteral(2)), AssignExpr(Identifier(a) = IntLiteral(3))]))]))])")
def test_099(): check("void main(){ if (a) if (b) c; else d; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(a) then IfStmt(if Identifier(b) then ExprStmt(Identifier(c)), else ExprStmt(Identifier(d))))]))])")
def test_100(): check("void main(){ a = \"hcmut\"; }", "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(a) = StringLiteral('hcmut')))]))])")