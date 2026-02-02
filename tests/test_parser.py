"""
Parser test cases for TyC compiler
Temporary test cases for Assignment 2
"""

import pytest
from tests.utils import Parser


def test_001_empty_program():
    source = ""
    Parser(source)


def test_002_single_empty_main():
    source = """
    void main() {
    }
    """
    Parser(source)


def test_003_multiple_functions():
    source = """
    int foo() { return 1; }
    float bar() { return 1.0; }
    void main() {}
    """
    Parser(source)


def test_004_auto_var_decl():
    source = """
    void main() {
        auto x = 10;
    }
    """
    Parser(source)


def test_005_explicit_var_decl():
    source = """
    void main() {
        int x;
        float y = 3.14;
        string s = "hello";
    }
    """
    Parser(source)


def test_006_assignment_stmt():
    source = """
    void main() {
        int x;
        x = 5;
    }
    """
    Parser(source)


def test_007_simple_if():
    source = """
    void main() {
        if (1) x = 1;
    }
    """
    Parser(source)


def test_008_if_else():
    source = """
    void main() {
        if (1) x = 1;
        else x = 2;
    }
    """
    Parser(source)


def test_009_while_loop():
    source = """
    void main() {
        auto i = 0;
        while (i < 10) {
            ++i;
        }
    }
    """
    Parser(source)


def test_010_for_loop():
    source = """
    void main() {
        for (auto i = 0; i < 10; ++i) {
            printInt(i);
        }
    }
    """
    Parser(source)


def test_011_function_call():
    source = """
    int add(int a, int b) {
        return a + b;
    }
    void main() {
        auto x = add(1, 2);
    }
    """
    Parser(source)


def test_012_return_stmt():
    source = """
    int foo() {
        return 10;
    }
    """
    Parser(source)


def test_013_void_return():
    source = """
    void main() {
        return;
    }
    """
    Parser(source)


def test_014_arithmetic_expr():
    source = """
    void main() {
        auto x = 1 + 2 * 3;
    }
    """
    Parser(source)


def test_015_logical_expr():
    source = """
    void main() {
        auto x = 1 && 0 || 1;
    }
    """
    Parser(source)


def test_016_struct_decl():
    source = """
    struct Point {
        int x;
        int y;
    };
    void main() {}
    """
    Parser(source)


def test_017_struct_var_decl():
    source = """
    struct Point {
        int x;
        int y;
    };
    void main() {
        Point p;
    }
    """
    Parser(source)


def test_018_struct_init():
    source = """
    struct Point {
        int x;
        int y;
    };
    void main() {
        Point p = {1, 2};
    }
    """
    Parser(source)


def test_019_struct_member_access():
    source = """
    struct Point {
        int x;
        int y;
    };
    void main() {
        Point p;
        p.x = 10;
    }
    """
    Parser(source)


def test_020_switch_stmt():
    source = """
    void main() {
        auto x = 1;
        switch (x) {
            case 1:
                printInt(1);
                break;
            default:
                printInt(0);
        }
    }
    """
    Parser(source)

def test_021_nested_block():
    source = """
    void main() {
        {
            int x;
            {
                x = 10;
            }
        }
    }
    """
    Parser(source)


def test_022_multiple_var_decl_same_block():
    source = """
    void main() {
        int a;
        int b;
        int c;
    }
    """
    Parser(source)


def test_023_var_decl_with_expr_init():
    source = """
    void main() {
        int x = 1 + 2 * 3;
    }
    """
    Parser(source)


def test_024_multiple_assignment():
    source = """
    void main() {
        int x;
        x = 1;
        x = x + 1;
        x = x * 2;
    }
    """
    Parser(source)


def test_025_nested_if():
    source = """
    void main() {
        if (1)
            if (0)
                x = 1;
            else
                x = 2;
    }
    """
    Parser(source)


def test_026_if_with_block():
    source = """
    void main() {
        if (1) {
            int x;
            x = 10;
        }
    }
    """
    Parser(source)


def test_027_if_else_block():
    source = """
    void main() {
        if (1) {
            x = 1;
        } else {
            x = 2;
        }
    }
    """
    Parser(source)


def test_028_while_simple():
    source = """
    void main() {
        int i = 0;
        while (i < 5)
            i = i + 1;
    }
    """
    Parser(source)


def test_029_while_block():
    source = """
    void main() {
        int i = 0;
        while (i < 5) {
            i = i + 1;
        }
    }
    """
    Parser(source)


def test_030_for_no_init():
    source = """
    void main() {
        int i = 0;
        for (; i < 10; i = i + 1)
            i = i;
    }
    """
    Parser(source)


def test_031_for_no_cond():
    source = """
    void main() {
        int i = 0;
        for (i = 0; ; i = i + 1)
            break;
    }
    """
    Parser(source)


def test_032_for_no_update():
    source = """
    void main() {
        int i = 0;
        for (i = 0; i < 10; )
            i = i + 1;
    }
    """
    Parser(source)


def test_033_for_full_block():
    source = """
    void main() {
        for (int i = 0; i < 5; i = i + 1) {
            printInt(i);
        }
    }
    """
    Parser(source)


def test_034_break_stmt():
    source = """
    void main() {
        while (1) {
            break;
        }
    }
    """
    Parser(source)


def test_035_continue_stmt():
    source = """
    void main() {
        while (1) {
            continue;
        }
    }
    """
    Parser(source)


def test_036_return_expr():
    source = """
    int foo() {
        return 1 + 2;
    }
    """
    Parser(source)


def test_037_return_no_expr():
    source = """
    void main() {
        return;
    }
    """
    Parser(source)


def test_038_function_no_param():
    source = """
    int foo() {
        return 10;
    }
    """
    Parser(source)


def test_039_function_multiple_param():
    source = """
    int sum(int a, int b, int c) {
        return a + b + c;
    }
    """
    Parser(source)


def test_040_function_call_no_arg():
    source = """
    void foo() {}
    void main() {
        foo();
    }
    """
    Parser(source)


def test_041_function_call_multi_arg():
    source = """
    int sum(int a, int b) {
        return a + b;
    }
    void main() {
        int x = sum(1, 2);
    }
    """
    Parser(source)


def test_042_nested_function_call():
    source = """
    int f(int x) { return x; }
    void main() {
        int a = f(f(10));
    }
    """
    Parser(source)


def test_043_expression_parentheses():
    source = """
    void main() {
        int x = (1 + 2) * 3;
    }
    """
    Parser(source)


def test_044_unary_minus():
    source = """
    void main() {
        int x = -1;
    }
    """
    Parser(source)


def test_045_logical_not():
    source = """
    void main() {
        int x = !0;
    }
    """
    Parser(source)


def test_046_relational_chain():
    source = """
    void main() {
        int x = 1 < 2;
    }
    """
    Parser(source)


def test_047_equality_expr():
    source = """
    void main() {
        int x = 1 == 1;
    }
    """
    Parser(source)


def test_048_and_or_expr():
    source = """
    void main() {
        int x = 1 && 0 || 1;
    }
    """
    Parser(source)


def test_049_struct_only():
    source = """
    struct A {
        int x;
    };
    """
    Parser(source)


def test_050_struct_multiple_member():
    source = """
    struct B {
        int x;
        int y;
        int z;
    };
    """
    Parser(source)


def test_051_struct_and_main():
    source = """
    struct C {
        int x;
    };
    void main() {}
    """
    Parser(source)


def test_052_struct_var_in_block():
    source = """
    struct P {
        int x;
    };
    void main() {
        P p;
    }
    """
    Parser(source)


def test_053_struct_member_assign():
    source = """
    struct P {
        int x;
    };
    void main() {
        P p;
        p.x = 10;
    }
    """
    Parser(source)


def test_054_struct_nested_access():
    source = """
    struct A { int x; };
    struct B { A a; };
    void main() {
        B b;
        b.a.x = 1;
    }
    """
    Parser(source)


def test_055_switch_simple():
    source = """
    void main() {
        int x = 1;
        switch (x) {
            case 1:
                break;
        }
    }
    """
    Parser(source)


def test_056_switch_multiple_case():
    source = """
    void main() {
        int x = 2;
        switch (x) {
            case 1:
                break;
            case 2:
                break;
        }
    }
    """
    Parser(source)


def test_057_switch_default_only():
    source = """
    void main() {
        int x = 0;
        switch (x) {
            default:
                break;
        }
    }
    """
    Parser(source)


def test_058_switch_case_default():
    source = """
    void main() {
        int x = 3;
        switch (x) {
            case 1:
                break;
            default:
                break;
        }
    }
    """
    Parser(source)


def test_059_nested_switch():
    source = """
    void main() {
        int x = 1;
        switch (x) {
            case 1:
                switch (x) {
                    case 1:
                        break;
                }
        }
    }
    """
    Parser(source)


def test_060_deep_nested_blocks():
    source = """
    void main() {
        {{{{{ int x; }}}}}
    }
    """
    Parser(source)


def test_061_long_expression():
    source = """
    void main() {
        int x = 1 + 2 + 3 + 4 + 5;
    }
    """
    Parser(source)


def test_062_multiple_functions_no_main():
    source = """
    int a() { return 1; }
    int b() { return 2; }
    """
    Parser(source)


def test_063_auto_decl_no_init():
    source = """
    void main() {
        auto x;
    }
    """
    Parser(source)


def test_064_assignment_with_call():
    source = """
    int f() { return 1; }
    void main() {
        int x;
        x = f();
    }
    """
    Parser(source)


def test_065_expr_stmt_call():
    source = """
    void foo() {}
    void main() {
        foo();
    }
    """
    Parser(source)


def test_066_expr_stmt_arithmetic():
    source = """
    void main() {
        1 + 2;
    }
    """
    Parser(source)


def test_067_multiple_expr_stmt():
    source = """
    void main() {
        1 + 2;
        3 * 4;
    }
    """
    Parser(source)


def test_068_unary_chain():
    source = """
    void main() {
        int x = ---1;
    }
    """
    Parser(source)


def test_069_post_increment():
    source = """
    void main() {
        int x = 1;
        x++;
    }
    """
    Parser(source)


def test_070_post_decrement():
    source = """
    void main() {
        int x = 1;
        x--;
    }
    """
    Parser(source)


def test_071_multiple_postfix():
    source = """
    void main() {
        int x = 1;
        x+++++;
    }
    """
    Parser(source)


def test_072_for_with_expr_update():
    source = """
    void main() {
        int i = 0;
        for (i = 0; i < 10; i = i + 1)
            i;
    }
    """
    Parser(source)


def test_073_complex_for():
    source = """
    void main() {
        for (int i = 0; i < 10; i = i + 1)
            for (int j = 0; j < 5; j = j + 1)
                j;
    }
    """
    Parser(source)


def test_074_return_expr_complex():
    source = """
    int f(int a, int b) {
        return (a + b) * (a - b);
    }
    """
    Parser(source)


def test_075_struct_many_access():
    source = """
    struct A { int x; };
    void main() {
        A a;
        a.x = a.x;
    }
    """
    Parser(source)


def test_076_chained_call_expr():
    source = """
    int f(int x) { return x; }
    void main() {
        f(1 + f(2));
    }
    """
    Parser(source)


def test_077_empty_block_stmt():
    source = """
    void main() {
        {}
    }
    """
    Parser(source)


def test_078_block_in_if():
    source = """
    void main() {
        if (1) {}
    }
    """
    Parser(source)


def test_079_block_in_while():
    source = """
    void main() {
        while (1) {}
    }
    """
    Parser(source)


def test_080_complex_program():
    source = """
    struct P { int x; };
    int f(int a) {
        if (a) return a;
        else return a + 1;
    }
    void main() {
        P p;
        p.x = f(10);
        while (p.x > 0) {
            p.x--;
        }   
    }
    """
    Parser(source)

def test_081_nested_block():
    source = """
    void main() {
        {
            {
                auto x = 10;
            }
        }
    }
    """
    Parser(source)


def test_082_multiple_var_decl_same_block():
    source = """
    void main() {
        int a;
        int b;
        int c;
    }
    """
    Parser(source)


def test_083_complex_arithmetic_expr():
    source = """
    void main() {
        auto x = (1 + 2) * (3 - 4) / 5;
    }
    """
    Parser(source)


def test_084_prefix_and_postfix_inc():
    source = """
    void main() {
        auto x = 0;
        ++x;
        x++;
    }
    """
    Parser(source)


def test_085_nested_if_else():
    source = """
    void main() {
        if (1)
            if (0)
                x = 1;
            else
                x = 2;
    }
    """
    Parser(source)


def test_086_while_with_expr_stmt():
    source = """
    void main() {
        auto i = 0;
        while (i < 5)
            i = i + 1;
    }
    """
    Parser(source)


def test_087_for_without_init():
    source = """
    void main() {
        auto i = 0;
        for (; i < 10; ++i) {
            printInt(i);
        }
    }
    """
    Parser(source)


def test_088_for_without_condition():
    source = """
    void main() {
        auto i = 0;
        for (i = 0; ; ++i) {
            break;
        }
    }
    """
    Parser(source)


def test_089_for_without_update():
    source = """
    void main() {
        auto i = 0;
        for (i = 0; i < 10; ) {
            i = i + 1;
        }
    }
    """
    Parser(source)


def test_090_switch_multiple_cases():
    source = """
    void main() {
        auto x = 2;
        switch (x) {
            case 1:
                printInt(1);
                break;
            case 2:
                printInt(2);
                break;
            case 3:
                printInt(3);
                break;
        }
    }
    """
    Parser(source)


def test_091_switch_fallthrough():
    source = """
    void main() {
        auto x = 1;
        switch (x) {
            case 1:
            case 2:
                printInt(1);
                break;
        }
    }
    """
    Parser(source)


def test_092_function_no_return_void():
    source = """
    void foo() {
        auto x = 10;
    }
    void main() {}
    """
    Parser(source)


def test_093_function_nested_call():
    source = """
    int add(int a, int b) {
        return a + b;
    }
    void main() {
        auto x = add(add(1, 2), 3);
    }
    """
    Parser(source)


def test_094_function_call_as_stmt():
    source = """
    void main() {
        printInt(10);
    }
    """
    Parser(source)


def test_095_struct_multiple_decl():
    source = """
    struct A {
        int x;
    };
    struct B {
        float y;
    };
    void main() {}
    """
    Parser(source)


def test_096_struct_member_chain():
    source = """
    struct A {
        int x;
    };
    struct B {
        A a;
    };
    void main() {
        B b;
        b.a.x = 10;
    }
    """
    Parser(source)


def test_097_assignment_with_expr():
    source = """
    void main() {
        auto x = 0;
        x = x + 1 * 2;
    }
    """
    Parser(source)


def test_098_return_expr_complex():
    source = """
    int foo(int x) {
        return x * (x + 1);
    }
    """
    Parser(source)


def test_099_struct():
    source = """
    struct Point { int x; int y; };
    """
    Parser(source)


def test_100_break_in_switch():
    source = """
    void main() { int x = ; }
    """
    Parser(source)
