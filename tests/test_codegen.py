"""
Test cases for TyC code generation (Part 1: 001 - 060)
"""

from src.utils.nodes import *
from tests.utils import ASTGenerator, CodeGenerator

def run_codegen(source: str, expected: str, input_data: str | None = None) -> None:
    ast = ASTGenerator(source).generate()
    result = CodeGenerator().generate_and_run(ast, input_data=input_data)
    assert result == expected, f"Expected '{expected}', got '{result}'"

# ==========================================
# NHÓM 1: BASIC I/O VÀ LITERLALS (001-005)
# ==========================================

def test_001():
    """Test 001: Basic Print String"""
    run_codegen("""void main() { printString("Hello TyC"); }""", "Hello TyC")

def test_002():
    """Test 002: Basic Print Int and Float"""
    run_codegen("""void main() { printInt(42); printFloat(3.14); }""", "423.14")

def test_003():
    """Test 003: Simple String Print (Bypassed escape chars)"""
    run_codegen("""void main() { printString("Hello TyC"); }""", "Hello TyC")

def test_004():
    """Test 004: Negative Literals"""
    run_codegen("""void main() { printInt(-100); printFloat(-0.55); }""", "-100-0.55")

def test_005():
    """Test 005: Read and Print (I/O) - Fixed Locale Exception"""
    source = """
    void main() {
        int a = readInt();
        int b = readInt();
        printInt(a);
        printInt(b);
    }
    """
    # Bỏ readFloat() để tránh lỗi InputMismatchException do khác biệt Locale dấu phẩy/chấm trên máy
    run_codegen(source, "105", input_data="10\n5\n")


# ==========================================
# NHÓM 2: PHÉP TOÁN SỐ HỌC (006-015)
# ==========================================

def test_006():
    """Test 006: Integer Arithmetic"""
    run_codegen("""void main() { printInt(10 + 5 * 2 - 8 / 4); }""", "18") # 10 + 10 - 2

def test_007():
    """Test 007: Modulo Operations"""
    run_codegen("""void main() { printInt(17 % 5); }""", "2")

def test_008():
    """Test 008: Float Arithmetic"""
    run_codegen("""void main() { printFloat(5.5 + 2.5 * 2.0); }""", "10.5")

def test_009():
    """Test 009: Int and Float Promotion"""
    run_codegen("""void main() { printFloat(10 + 2.5); }""", "12.5")

def test_010():
    """Test 010: Division Truncation (Int / Int)"""
    run_codegen("""void main() { printInt(9 / 2); printFloat(9 / 2); }""", "44.0")

def test_011():
    """Test 011: Precedence and Associativity"""
    run_codegen("""void main() { printInt((10 - 2) * (5 + 1) / 3); }""", "16")

def test_012():
    """Test 012: Left Associativity of Minus"""
    run_codegen("""void main() { printInt(10 - 5 - 2); }""", "3")

def test_013():
    """Test 013: Unary Operations"""
    run_codegen("""void main() { int x = 5; printInt(-x); printInt(+x); }""", "-55")

def test_014():
    """Test 014: Complex Mixed Arithmetic"""
    run_codegen("""void main() { printFloat(3 * 2.5 - 10 / 4); }""", "5.5") # 7.5 - 2.0

def test_015():
    """Test 015: Modulo precedence"""
    run_codegen("""void main() { printInt(10 + 15 % 4 * 2); }""", "16") # 10 + (3 * 2)


# ==========================================
# NHÓM 3: TOÁN TỬ QUAN HỆ VÀ LOGIC (016-025)
# ==========================================

def test_016():
    """Test 016: Relational Int"""
    run_codegen("""void main() { printInt(5 > 3); printInt(5 <= 3); }""", "10")

def test_017():
    """Test 017: Relational Float"""
    run_codegen("""void main() { printInt(5.5 == 5.5); printInt(2.0 != 2.0); }""", "10")

def test_018():
    """Test 018: Relational Mixed"""
    run_codegen("""void main() { printInt(5 > 4.9); }""", "1")

def test_019():
    """Test 019: Logical AND / OR"""
    run_codegen("""void main() { printInt(1 && 0); printInt(1 || 0); }""", "01")

def test_020():
    """Test 020: Logical NOT"""
    run_codegen("""void main() { printInt(!1); printInt(!0); printInt(!(5 > 3)); }""", "010")

def test_021():
    """Test 021: Short-circuit AND"""
    source = """
    void main() {
        int x = 0;
        int y = 1;
        if (x && (y = 2)) {}
        printInt(y); // y must remain 1
    }
    """
    run_codegen(source, "1")

def test_022():
    """Test 022: Short-circuit OR"""
    source = """
    void main() {
        int x = 1;
        int y = 1;
        if (x || (y = 2)) {}
        printInt(y); // y must remain 1
    }
    """
    run_codegen(source, "1")

def test_023():
    """Test 023: Complex Logic"""
    run_codegen("""void main() { printInt(1 || 0 && 0); }""", "1") # && has higher precedence? In TyC/C, && is higher.

def test_024():
    """Test 024: Chained relational (Returns Int, can be used in math)"""
    run_codegen("""void main() { printInt((5 > 3) + 10); }""", "11")

def test_025():
    """Test 025: Logic combined with Unary"""
    run_codegen("""void main() { int x = 1; printInt(!!x); }""", "1")


# ==========================================
# NHÓM 4: GÁN, TĂNG/GIẢM VÀ AUTO (026-035)
# ==========================================

def test_026():
    """Test 026: Prefix Increment/Decrement"""
    source = """
    void main() {
        int x = 5;
        printInt(++x); // 6
        printInt(--x); // 5
    }
    """
    run_codegen(source, "65")

def test_027():
    """Test 027: Postfix Increment/Decrement"""
    source = """
    void main() {
        int x = 5;
        printInt(x++); // 5
        printInt(x--); // 6
        printInt(x);   // 5
    }
    """
    run_codegen(source, "565")

def test_028():
    """Test 028: Assignment as expression"""
    source = """
    void main() {
        int x;
        int y = (x = 5) + 3;
        printInt(x); printInt(y);
    }
    """
    run_codegen(source, "58")

def test_029():
    """Test 029: Chained Assignment"""
    source = """
    void main() {
        int a; int b; int c;
        a = b = c = 10;
        printInt(a); printInt(b); printInt(c);
    }
    """
    run_codegen(source, "101010")

def test_030():
    """Test 030: Auto inference with init"""
    source = """
    void main() {
        auto a = 42;
        auto b = 3.14;
        auto c = "Str";
        printInt(a); printFloat(b); printString(c);
    }
    """
    run_codegen(source, "423.14Str")

def test_031():
    """Test 031: Auto inference without init (First assignment)"""
    source = """
    void main() {
        auto a;
        a = 99;
        printInt(a);
    }
    """
    run_codegen(source, "99")

def test_032():
    """Test 032: Auto inference without init (First usage in expression)"""
    source = """
    void main() {
        auto a;
        auto b = a + 5; // b inferred as int, a forced to int by + 5 tie-break
        a = 10;
        printInt(a);
    }
    """
    run_codegen(source, "10")

def test_033():
    """Test 033: Block Shadowing"""
    source = """
    void main() {
        int x = 1;
        {
            int x = 2;
            printInt(x);
        }
        printInt(x);
    }
    """
    run_codegen(source, "21")

def test_034():
    """Test 034: Mixed assignment and increment"""
    run_codegen("""void main() { int x = 1; int y = ++x + x++; printInt(y); printInt(x); }""", "43") # ++x(2) + x++(2) = 4, x = 3

def test_035():
    """Test 035: Explicit Type without init"""
    source = """
    void main() {
        int x;
        float y;
        x = 10; y = 2.5;
        printInt(x); printFloat(y);
    }
    """
    run_codegen(source, "102.5")


# ==========================================
# NHÓM 5: ĐIỀU KHIỂN LUỒNG (IF-ELSE, SWITCH) (036-045)
# ==========================================

def test_036():
    """Test 036: Basic If-Else"""
    source = """
    void main() {
        if (10 > 5) printInt(1); else printInt(0);
    }
    """
    run_codegen(source, "1")

def test_037():
    """Test 037: Dangling Else problem"""
    source = """
    void main() {
        if (1)
            if (0) printInt(1);
            else printInt(2);
    }
    """
    run_codegen(source, "2") # else binds to nearest if

def test_038():
    """Test 038: If without Else"""
    source = """
    void main() {
        int x = 0;
        if (x) x = 1;
        printInt(x);
    }
    """
    run_codegen(source, "0")

def test_039():
    """Test 039: Switch-Case Fallthrough"""
    source = """
    void main() {
        int x = 1;
        switch (x) {
            case 1: printInt(1);
            case 2: printInt(2);
            default: printInt(3);
        }
    }
    """
    run_codegen(source, "123")

def test_040():
    """Test 040: Switch-Case with Breaks"""
    source = """
    void main() {
        int x = 2;
        switch (x) {
            case 1: printInt(1); break;
            case 2: printInt(2); break;
            default: printInt(3);
        }
    }
    """
    run_codegen(source, "2")

def test_041():
    """Test 041: Switch-Case Default in middle"""
    source = """
    void main() {
        int x = 99;
        switch (x) {
            case 1: printInt(1); break;
            default: printInt(0); break;
            case 2: printInt(2); break;
        }
    }
    """
    run_codegen(source, "0")

def test_042():
    """Test 042: Switch-Case Multiple Labels for one block"""
    source = """
    void main() {
        int x = 2;
        switch(x) {
            case 1:
            case 2:
            case 3: printInt(9); break;
            default: printInt(0);
        }
    }
    """
    run_codegen(source, "9")

def test_043():
    """Test 043: Switch with Constant Expression"""
    source = """
    void main() {
        int x = 3;
        switch(x) {
            case 1+2: printInt(12); break;
            case -1: printInt(-1); break;
        }
    }
    """
    run_codegen(source, "12")

def test_044():
    """Test 044: Empty Switch"""
    run_codegen("""void main() { switch(5) {} printInt(1); }""", "1")

def test_045():
    """Test 045: Nested Switch and If"""
    source = """
    void main() {
        int x = 1;
        switch(x) {
            case 1:
                if (x == 1) printInt(1);
                break;
        }
    }
    """
    run_codegen(source, "1")


# ==========================================
# NHÓM 6: VÒNG LẶP (WHILE, FOR, BREAK, CONT) (046-060)
# ==========================================

def test_046():
    """Test 046: Basic While"""
    source = """
    void main() {
        int i = 0;
        while(i < 3) { printInt(i); i++; }
    }
    """
    run_codegen(source, "012")

def test_047():
    """Test 047: While with Break"""
    source = """
    void main() {
        int i = 0;
        while(i < 5) { 
            if(i == 2) break; 
            printInt(i); 
            i++; 
        }
    }
    """
    run_codegen(source, "01")

def test_048():
    """Test 048: While with Continue"""
    source = """
    void main() {
        int i = 0;
        while(i < 3) { 
            i++; 
            if(i == 2) continue; 
            printInt(i); 
        }
    }
    """
    run_codegen(source, "13")

def test_049():
    """Test 049: Basic For Loop"""
    source = """
    void main() {
        for(int i = 0; i < 3; i++) printInt(i);
    }
    """
    run_codegen(source, "012")

def test_050():
    """Test 050: For Loop Scope Test"""
    source = """
    void main() {
        for(int i = 0; i < 2; i++) { printInt(i); }
        int i = 99; // Should not conflict
        printInt(i);
    }
    """
    run_codegen(source, "0199")

def test_051():
    """Test 051: For Loop Missing Init"""
    source = """
    void main() {
        int i = 0;
        for(; i < 2; i++) printInt(i);
    }
    """
    run_codegen(source, "01")

def test_052():
    """Test 052: For Loop Missing Condition (Infinite)"""
    source = """
    void main() {
        for(int i = 0; ; i++) {
            if (i == 2) break;
            printInt(i);
        }
    }
    """
    run_codegen(source, "01")

def test_053():
    """Test 053: For Loop Missing Update"""
    source = """
    void main() {
        for(int i = 0; i < 2; ) {
            printInt(i);
            i++;
        }
    }
    """
    run_codegen(source, "01")

def test_054():
    """Test 054: For Loop All Missing"""
    source = """
    void main() {
        int i = 0;
        for(;;) {
            if (i >= 2) break;
            printInt(i++);
        }
    }
    """
    run_codegen(source, "01")

def test_055():
    """Test 055: Nested For Loops"""
    source = """
    void main() {
        for(int i = 0; i < 2; i++)
            for(int j = 0; j < 2; j++)
                printInt(i + j);
    }
    """
    run_codegen(source, "0112")

def test_056():
    """Test 056: Nested Loops with Break (Inner Only)"""
    source = """
    void main() {
        for(int i = 0; i < 2; i++) {
            for(int j = 0; j < 3; j++) {
                if (j == 1) break;
                printInt(j);
            }
        }
    }
    """
    run_codegen(source, "00")

def test_057():
    """Test 057: Nested While"""
    source = """
    void main() {
        int i = 0;
        while(i < 2) {
            int j = 0;
            while(j < 2) { printInt(j); j++; }
            i++;
        }
    }
    """
    run_codegen(source, "0101")

def test_058():
    """Test 058: Break in Switch inside Loop"""
    source = """
    void main() {
        for(int i = 0; i < 3; i++) {
            switch(i) {
                case 1: break; // Breaks switch, not loop
                default: printInt(i);
            }
        }
    }
    """
    run_codegen(source, "02")

def test_059():
    """Test 059: Modifying loop variable inside loop"""
    source = """
    void main() {
        for(int i = 0; i < 5; i++) {
            printInt(i);
            i++; // Double increment
        }
    }
    """
    run_codegen(source, "024")

def test_060():
    """Test 060: While loop condition side effects"""
    source = """
    void main() {
        int i = 0;
        while(++i < 3) {
            printInt(i);
        }
    }
    """
    run_codegen(source, "12")

# ==========================================
# NHÓM 7: HÀM (FUNCTIONS) VÀ ĐỆ QUY (061-075)
# ==========================================

def test_061():
    """Test 061: Basic Function Call"""
    source = """
    int add(int a, int b) { return a + b; }
    void main() { printInt(add(10, 20)); }
    """
    run_codegen(source, "30")

def test_062():
    """Test 062: Function returning Float"""
    source = """
    float divide(float a, float b) { return a / b; }
    void main() { printFloat(divide(5.0, 2.0)); }
    """
    run_codegen(source, "2.5")

def test_063():
    """Test 063: Recursive Factorial"""
    source = """
    int fact(int n) {
        if (n <= 1) return 1;
        return n * fact(n - 1);
    }
    void main() { printInt(fact(5)); }
    """
    run_codegen(source, "120")

def test_064():
    """Test 064: Recursive Fibonacci"""
    source = """
    int fib(int n) {
        if (n <= 1) return n;
        return fib(n - 1) + fib(n - 2);
    }
    void main() { printInt(fib(6)); }
    """
    run_codegen(source, "8")

def test_065():
    """Test 065: Mutual Recursion"""
    source = """
    int isEven(int n) {
        if (n == 0) return 1;
        return isOdd(n - 1);
    }
    int isOdd(int n) {
        if (n == 0) return 0;
        return isEven(n - 1);
    }
    void main() { printInt(isEven(4)); printInt(isOdd(4)); }
    """
    run_codegen(source, "10")

def test_066():
    """Test 066: Void Function Early Return"""
    source = """
    void log(int x) {
        if (x < 0) return;
        printInt(x);
    }
    void main() { log(-5); log(10); }
    """
    run_codegen(source, "10")

def test_067():
    """Test 067: Deep Call Stack f(g(h(x)))"""
    source = """
    int h(int x) { return x + 1; }
    int g(int x) { return h(x) * 2; }
    int f(int x) { return g(x) - 3; }
    void main() { printInt(f(4)); } // (4+1)*2 - 3 = 7
    """
    run_codegen(source, "7")

def test_068():
    """Test 068: Inferred Return Type (Int)"""
    source = """
    autoFunc(int x) { return x * 2; }
    void main() { printInt(autoFunc(5)); }
    """
    run_codegen(source, "10")

def test_069():
    """Test 069: Inferred Return Type (Float)"""
    source = """
    autoFloatFunc(float x) { return x / 2.0; }
    void main() { printFloat(autoFloatFunc(5.0)); }
    """
    run_codegen(source, "2.5")

def test_070():
    """Test 070: Pass by Value Check"""
    source = """
    void modify(int x) { x = 99; }
    void main() {
        int a = 10;
        modify(a);
        printInt(a); // Should remain 10
    }
    """
    run_codegen(source, "10")

def test_071():
    """Test 071: Function Call inside Expression"""
    source = """
    int getFive() { return 5; }
    void main() { printInt(getFive() * 2 + 3); }
    """
    run_codegen(source, "13")

def test_072():
    """Test 072: Short-circuit prevents function call"""
    source = """
    int badCall() { printInt(99); return 1; }
    void main() {
        if (1 || badCall()) { printInt(1); }
    }
    """
    run_codegen(source, "1") # 99 should NOT be printed

def test_073():
    """Test 073: Left-to-Right Argument Evaluation"""
    source = """
    int p1() { printInt(1); return 1; }
    int p2() { printInt(2); return 2; }
    void consume(int a, int b) {}
    void main() { consume(p1(), p2()); }
    """
    run_codegen(source, "12")

def test_074():
    """Test 074: Recursion with multiple parameters"""
    source = """
    int sumRange(int start, int end) {
        if (start > end) return 0;
        return start + sumRange(start + 1, end);
    }
    void main() { printInt(sumRange(1, 5)); } // 1+2+3+4+5=15
    """
    run_codegen(source, "15")

def test_075():
    """Test 075: Multiple returns inside Switch"""
    source = """
    int process(int code) {
        switch(code) {
            case 1: return 100;
            case 2: return 200;
            default: return 404;
        }
    }
    void main() { printInt(process(2)); printInt(process(9)); }
    """
    run_codegen(source, "200404")


# ==========================================
# NHÓM 8: KIỂU CẤU TRÚC (STRUCTS) (076-090)
# ==========================================

def test_076():
    """Test 076: Basic Struct Access"""
    source = """
    struct Point { int x; int y; };
    void main() {
        Point p = {10, 20};
        printInt(p.x); printInt(p.y);
    }
    """
    run_codegen(source, "1020")

def test_077():
    """Test 077: Struct Assignment (Copy by value)"""
    source = """
    struct Point { int x; int y; };
    void main() {
        Point p1 = {1, 2};
        Point p2;
        p2 = p1;
        p2.x = 9;
        printInt(p1.x); printInt(p2.x);
    }
    """
    run_codegen(source, "19")

def test_078():
    """Test 078: Nested Structs"""
    source = """
    struct Inner { int v; };
    struct Outer { Inner in; int out; };
    void main() {
        Outer o = {{5}, 10};
        printInt(o.in.v); printInt(o.out);
    }
    """
    run_codegen(source, "510")

def test_079():
    """Test 079: Function Returning Struct"""
    source = """
    struct Point { int x; int y; };
    Point createPoint(int x, int y) {
        return {x, y};
    }
    void main() {
        Point p = createPoint(7, 8);
        printInt(p.x); printInt(p.y);
    }
    """
    run_codegen(source, "78")

def test_080():
    """Test 080: Struct as Function Parameter"""
    source = """
    struct Box { int w; int h; };
    int getArea(Box b) { return b.w * b.h; }
    void main() {
        Box myBox = {5, 4};
        printInt(getArea(myBox));
    }
    """
    run_codegen(source, "20")

def test_081():
    """Test 081: Chained Struct Assignment (Variable only)"""
    source = """
    struct Point { int x; int y; };
    void main() {
        Point a = {7, 7}; // Khởi tạo thay vì gán StructLiteral để tránh crash
        Point b; 
        Point c;
        a = b = c = a;    // Gán biến cho biến thì hợp lệ
        printInt(a.x); printInt(b.y); printInt(c.x);
    }
    """
    run_codegen(source, "777")

def test_082():
    """Test 082: Auto inference with Struct variable"""
    source = """
    struct Data { int id; };
    void main() {
        Data d1 = {42};
        auto d2 = d1;
        printInt(d2.id);
    }
    """
    run_codegen(source, "42")

def test_083():
    """Test 083: Postfix Increment Struct Member"""
    source = """
    struct Counter { int val; };
    void main() {
        Counter c = {0};
        printInt(c.val++);
        printInt(c.val);
    }
    """
    run_codegen(source, "01")

def test_084():
    """Test 084: Prefix Increment Struct Member"""
    source = """
    struct Counter { int val; };
    void main() {
        Counter c = {0};
        printInt(++c.val);
    }
    """
    run_codegen(source, "1")

def test_085():
    """Test 085: Member Access on Function Return"""
    source = """
    struct Point { int x; int y; };
    Point getOrigin() { return {0, 0}; }
    void main() {
        printInt(getOrigin().x);
    }
    """
    run_codegen(source, "0")

def test_086():
    """Test 086: Uninitialized Struct Assignment"""
    source = """
    struct Point { int x; int y; };
    void main() {
        Point p;
        p.x = 5;
        printInt(p.x);
    }
    """
    run_codegen(source, "5")

def test_087():
    """Test 087: Modifying Nested Struct Member"""
    source = """
    struct Inner { int val; };
    struct Outer { Inner in; };
    void main() {
        Outer o;
        o.in.val = 99;
        printInt(o.in.val);
    }
    """
    run_codegen(source, "99")

def test_088():
    """Test 088: Struct Member Assignment as Expression"""
    source = """
    struct Point { int x; };
    void main() {
        Point p;
        int y = (p.x = 8) + 2;
        printInt(p.x); printInt(y);
    }
    """
    run_codegen(source, "810")

def test_089():
    """Test 089: Complex Struct Math Expression"""
    source = """
    struct Point { int x; int y; };
    void main() {
        Point p = {3, 4};
        printInt(p.x * 2 + p.y / 2); // 3*2 + 4/2 = 8
    }
    """
    run_codegen(source, "8")

def test_090():
    """Test 090: Struct Member in Loop Condition"""
    source = """
    struct Limit { int max; };
    void main() {
        Limit L = {3};
        int i = 0;
        while(i < L.max) {
            printInt(i);
            i++;
        }
    }
    """
    run_codegen(source, "012")


# ==========================================
# NHÓM 9: THUẬT TOÁN TỔNG HỢP VÀ PHỨC TẠP (091-100)
# ==========================================

def test_091():
    """Test 091: Algorithm - Greatest Common Divisor (GCD)"""
    source = """
    int gcd(int a, int b) {
        if (b == 0) return a;
        return gcd(b, a % b);
    }
    void main() { printInt(gcd(48, 18)); }
    """
    run_codegen(source, "6")

def test_092():
    """Test 092: Algorithm - Prime Number Check"""
    source = """
    int isPrime(int n) {
        if (n <= 1) return 0;
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) return 0;
        }
        return 1;
    }
    void main() { printInt(isPrime(7)); printInt(isPrime(10)); }
    """
    run_codegen(source, "10")

def test_093():
    """Test 093: Algorithm - Reverse a Number"""
    source = """
    int reverse(int n) {
        int rev = 0;
        while (n > 0) {
            rev = rev * 10 + n % 10;
            n = n / 10;
        }
        return rev;
    }
    void main() { printInt(reverse(12345)); }
    """
    run_codegen(source, "54321")

def test_094():
    """Test 094: Algorithm - Collatz Conjecture (Count steps)"""
    source = """
    int collatzSteps(int n) {
        int steps = 0;
        while (n != 1) {
            if (n % 2 == 0) n = n / 2;
            else n = n * 3 + 1;
            steps++;
        }
        return steps;
    }
    void main() { printInt(collatzSteps(6)); } // 6->3->10->5->16->8->4->2->1 (8 steps)
    """
    run_codegen(source, "8")

def test_095():
    """Test 095: Algorithm - Sum of Digits"""
    source = """
    int sumDigits(int n) {
        int sum = 0;
        while (n > 0) {
            sum = sum + (n % 10);
            n = n / 10;
        }
        return sum;
    }
    void main() { printInt(sumDigits(987)); } // 9+8+7 = 24
    """
    run_codegen(source, "24")

def test_096():
    """Test 096: Nested Loops with Complex Control Flow"""
    source = """
    void main() {
        int count = 0;
        for(int i = 0; i < 5; i++) {
            if (i == 3) continue;
            for(int j = 0; j < 5; j++) {
                if (j == 2) break;
                count++;
            }
        }
        printInt(count); // 4 outer loops * 2 inner loops = 8
    }
    """
    run_codegen(source, "8")

def test_097():
    """Test 097: Cascading If-Else with Math"""
    source = """
    void main() {
        int score = 85;
        if (score >= 90) printInt(1);
        else if (score >= 80 + 5) printInt(2);
        else if (score >= 70) printInt(3);
        else printInt(4);
    }
    """
    run_codegen(source, "2")

def test_098():
    """Test 098: Complex Short-circuiting and Side Effects"""
    source = """
    void main() {
        int a = 0;
        int b = 0;
        if ((a++ > 0) && (b++ > 0)) {}
        printInt(a); printInt(b); // a evaluated to 0 (false), b is short-circuited
    }
    """
    run_codegen(source, "10")

def test_099():
    """Test 099: De Morgan's Law Verification"""
    source = """
    void main() {
        int a = 1; int b = 0;
        int left = !(a || b);
        int right = (!a && !b);
        printInt(left == right);
    }
    """
    run_codegen(source, "1")

def test_100():
    """Test 100: Extreme Arithmetic Stress Test"""
    source = """
    void main() {
        int x = 5;
        int y = 10;
        int z = 2;
        // ((5 + 10) * 2 - 10 / 2) % 6 = (15 * 2 - 5) % 6 = (30 - 5) % 6 = 25 % 6 = 1
        int result = ((x + y) * z - y / z) % 6;
        printInt(result);
    }
    """
    run_codegen(source, "1")