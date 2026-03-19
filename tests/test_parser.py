import pytest
from tests.utils import Parser

# ----------------------------------------------------
# 001-004: Empty and basic programs
# ----------------------------------------------------
def test_001():
    source = ""
    expected = "success"
    assert Parser(source).parse() == expected

def test_002():
    source = "void main() {}"
    expected = "success"
    assert Parser(source).parse() == expected

def test_003():
    source = """
/* block */
// line
void main() {}
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_004():
    source = """
struct A {}
void f() {}
struct B { int a; }
void main() {}
"""
    expected = "success"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 005-009: Struct declarations
# ----------------------------------------------------
def test_005():
    source = "struct Empty {};"
    expected = "success"
    assert Parser(source).parse() == expected

def test_006():
    source = """
struct Point { int x; int y; }
struct Line { Point p1; Point p2; }
"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_007():
    source = "struct Node { Node next; };"
    expected = "success"
    assert Parser(source).parse() == expected

def test_008():
    source = """
struct Error {
    auto x;
};
"""
    expected = "Error on line 3 col 4: auto"
    assert Parser(source).parse() == expected

def test_009():
    source = """
struct Error {
    int x = 1;
};
"""
    expected = "Error on line 3 col 10: ="
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 010-018: Function declarations
# ----------------------------------------------------
def test_010():
    source = "void f() {}"
    expected = "success"
    assert Parser(source).parse() == expected

def test_011():
    source = "int f(int a, float b) {}"
    expected = "success"
    assert Parser(source).parse() == expected

def test_012():
    source = "f() {}"
    expected = "success"
    assert Parser(source).parse() == expected

def test_013():
    source = "Point f(Point p) {}"
    expected = "success"
    assert Parser(source).parse() == expected

def test_014():
    source = """
auto f() {}
"""
    expected = "Error on line 2 col 0: auto"
    assert Parser(source).parse() == expected

def test_015():
    source = """
void f(auto a) {}
"""
    expected = "Error on line 2 col 7: auto"
    assert Parser(source).parse() == expected

def test_016():
    source = """
void f(int a,) {}
"""
    expected = "Error on line 2 col 13: )"
    assert Parser(source).parse() == expected

def test_017():
    source = """
void f();
"""
    expected = "Error on line 2 col 8: ;"
    assert Parser(source).parse() == expected

def test_018():
    source = "void main(string s) {}"
    expected = "success"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 019-024: Variable declarations
# ----------------------------------------------------
def test_019():
    source = 'void main() { int a; float b = 1.0; string c = "hcmut"; }'
    expected = "success"
    assert Parser(source).parse() == expected

def test_020():
    source = "void main() { auto a; auto b = 1; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_021():
    source = "void main() { Point p; Point p2 = {1, 2}; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_022():
    source = "void main() { Line l = {{1,2}, {3,4}}; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_023():
    source = "void main() { auto l = {{1}, 2}; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_024():
    source = """
int global_var = 1;
"""
    expected = "Error on line 2 col 15: ="
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 025-030: Expressions — arithmetic
# ----------------------------------------------------
def test_025():
    source = "void main() { +1; -2; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_026():
    source = "void main() { -+!-+1; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_027():
    source = 'void main() { "a" + "b"; }'
    expected = "success"
    assert Parser(source).parse() == expected

def test_028():
    source = "void main() { (1+2)*(3-4); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_029():
    source = "void main() { 1+2*3/4%5-6; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_030():
    source = "void main() { a + b - c * d / e % f; }"
    expected = "success"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 031-032: Expressions — relational
# ----------------------------------------------------
def test_031():
    source = "void main() { a < b; c > d; e <= f; g >= h; i == j; k != l; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_032():
    source = "void main() { a < b > c == d != e <= f >= g; }"
    expected = "success"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 033-037: Expressions — logical
# ----------------------------------------------------
def test_033():
    source = "void main() { a && b || c; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_034():
    source = "void main() { !a && !b || !c; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_035():
    source = "void main() { a < b && c > d || e == f; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_036():
    source = "void main() { a || b && c; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_037():
    source = "void main() { (a || b) && c; }"
    expected = "success"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 038: Expressions — increment/decrement
# ----------------------------------------------------
def test_038():
    source = "void main() { ++a; a++; --b; b--; ++a.b; a.b++; }"
    expected = "success"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 039-041: Expressions — assignment
# ----------------------------------------------------
def test_039():
    source = "void main() { a = b = c = 1; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_040():
    source = "void main() { a = (b = 1) + 2; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_041():
    source = "void main() { a.b = c.d = 1; }"
    expected = "success"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 042-046: Expressions — member access
# ----------------------------------------------------
def test_042():
    source = "void main() { a.b; a.b.c; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_043():
    source = "void main() { a.b.c.d; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_044():
    source = "void main() { a.b++; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_045():
    source = "void main() { a + b.c * d; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_046():
    source = "void main() { f().a.b; }"
    expected = "success"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 047-048: Expressions — function calls
# ----------------------------------------------------
def test_047():
    source = "void main() { f(); f(1); f(1, 2); f(g(1), 2); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_048():
    source = "void main() { f({1, 2}, 3); }"
    expected = "success"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 049-050: Expressions — precedence
# ----------------------------------------------------
def test_049():
    source = "void main() { a = b || c && d == e < f + g * h; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_050():
    source = "void main() { f1() + f2(a) * f3(b,c); }"
    expected = "success"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 051-052: Statements — if
# ----------------------------------------------------
def test_051():
    source = "void main() { if (1) a; if (1) a; else b; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_052():
    source = "void main() { if (1) if (2) a; else b; else c; }"
    expected = "success"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 053: Statements — while
# ----------------------------------------------------
def test_053():
    source = "void main() { while (1) a; while(1) while(2) b; }"
    expected = "success"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 054-062: Statements — for
# ----------------------------------------------------
def test_054():
    source = "void main() { for (int i = 0; i < 1; i++) a; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_055():
    source = "void main() { for (auto i = 0; i < 1; i = i + 1) a; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_056():
    source = "void main() { for (i = 0; i < 1; i++) a; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_057():
    source = "void main() { for (;;) a; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_058():
    source = "void main() { for (int i = 0;;) a; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_059():
    source = "void main() { for (; i < 1;) a; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_060():
    source = "void main() { for (;;i++) a; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_061():
    source = "void main() { for (int i;;++i) a; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_062():
    source = """
void main() {
    for (3; 1; 2) a;
}
"""
    expected = "Error on line 3 col 10: ;"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 063-069: Statements — switch
# ----------------------------------------------------
def test_063():
    source = "void main() { switch (x) {} }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_064():
    source = "void main() { switch (x) { case 1: break; } }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_065():
    source = "void main() { switch (x) { case 1: a; case 2: b; default: c; } }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_066():
    source = "void main() { switch (x) { case 1+2: a; case (4*2): b; case -1: c; } }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_067():
    source = "void main() { switch (x) { default: a; } }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_068():
    source = """
void main() {
    switch (x) { case 1 break; }
}
"""
    expected = "Error on line 3 col 24: break"
    assert Parser(source).parse() == expected

def test_069():
    source = """
void main() {
    switch(x) { default: a; default: b; }
}
"""
    expected = "Error on line 3 col 28: default"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 070-071: Statements — break, continue, return
# ----------------------------------------------------
def test_070():
    source = "void main() { while(1) { break; continue; } }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_071():
    source = "void main() { return; return 1; return a+b; }"
    expected = "success"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 072-073: Statements — block
# ----------------------------------------------------
def test_072():
    source = "void main() { {{{}}} }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_073():
    source = "void main() { {a;} {b;} }"
    expected = "success"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 074-075: Expression statements
# ----------------------------------------------------
def test_074():
    source = "void main() { f(); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_075():
    source = "void main() { i++; }"
    expected = "success"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 076-080: Unsupported / parser errors
# ----------------------------------------------------
def test_076():
    source = """
void main() {
    ;
}
"""
    expected = "Error on line 3 col 4: ;"
    assert Parser(source).parse() == expected

def test_077():
    source = """
void main() {
    int arr[10];
}
"""
    expected = "Error Token ["
    assert Parser(source).parse() == expected

def test_078():
    source = """
void main() {
    int a, b;
}
"""
    expected = "Error on line 3 col 9: ,"
    assert Parser(source).parse() == expected

def test_079():
    source = """
void main() {
    void a;
}
"""
    expected = "Error on line 3 col 4: void"
    assert Parser(source).parse() == expected

def test_080():
    source = """
void main() {
    struct A{};
}
"""
    expected = "Error on line 3 col 4: struct"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 081-089: Tricky / edge cases
# ----------------------------------------------------
def test_081():
    source = """
void main() {
    switch(x) { case 1: a; default: b; case 2: c; default: d; }
}
"""
    expected = "Error on line 3 col 50: default"
    assert Parser(source).parse() == expected

def test_082():
    source = """
void main() {
    for(;;)
}
"""
    expected = "Error on line 4 col 0: }"
    assert Parser(source).parse() == expected

def test_083():
    source = """
void main() {
    a < b = 1;
}
"""
    expected = "Error on line 3 col 10: ="
    assert Parser(source).parse() == expected

def test_084():
    source = """
void main() {
    1 = 2;
}
"""
    expected = "Error on line 3 col 6: ="
    assert Parser(source).parse() == expected

def test_085():
    source = """
void main() {
    (1+2;
}
"""
    expected = "Error on line 3 col 8: ;"
    assert Parser(source).parse() == expected

def test_086():
    source = "void main() { switch(x) { case a: b; case 1.5: c; } }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_087():
    source = """
void main() {
    {1, 2} = 3;
}
"""
    expected = "Error on line 3 col 11: ="
    assert Parser(source).parse() == expected

def test_088():
    source = """
void main() {
    for (i || 1; ;) a;
}
"""
    expected = "Error on line 3 col 11: ||"
    assert Parser(source).parse() == expected

def test_089():
    source = """
void main() {
    a.++b;
}
"""
    expected = "Error on line 3 col 6: ++"
    assert Parser(source).parse() == expected

# ----------------------------------------------------
# 090-100: Complex programs and edges
# ----------------------------------------------------
def test_090():
    source = "struct Point { int x; int y; } Point create() { return {0,0}; } void main(){}"
    expected = "success"
    assert Parser(source).parse() == expected

def test_091():
    source = "void main() { a.b.c = d.e.f = 1; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_092():
    source = "void main() { 1.2.a.b; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_093():
    source = "void main() { f().a = g().b = 1; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_094():
    source = "void main() { return { {1,2}, 3 }; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_095():
    source = 'void main() { "s"++; }'
    expected = "success"
    assert Parser(source).parse() == expected

def test_096():
    source = "void main() { ++f(); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_097():
    source = "void main() { return f(); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_098():
    source = "void main() { {1} < {2}; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_099():
    source = "void main() { ++--a++--; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_100():
    source = """
void main() {
    a = (b) = 2;
}
"""
    expected = "Error on line 3 col 12: ="
    assert Parser(source).parse() == expected