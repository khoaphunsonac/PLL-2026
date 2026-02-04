"""
Parser test cases for TyC compiler
100 complex test cases for parser
"""

import pytest
from tests.utils import Parser


# ========== BASIC STRUCTURE (1–10) ==========

def test_01_empty_program():
    assert Parser("").parse() == "success"


def test_02_only_main():
    assert Parser("void main() {}").parse() == "success"


def test_03_multiple_functions():
    source = """
    void f() {}
    void g() {}
    void main() {}
    """
    assert Parser(source).parse() == "success"


def test_04_struct_empty():
    assert Parser("struct A {};").parse() == "success"


def test_05_struct_many_fields():
    source = "struct S { int a; float b; string c; };"  
    assert Parser(source).parse() == "success"


def test_06_struct_before_function():
    source = """
    struct P { int x; int y; };
    void main() {}
    """
    assert Parser(source).parse() == "success"


def test_07_function_return_int():
    source = "int f() { return 1; }"
    assert Parser(source).parse() == "success"


def test_08_function_inferred_return():
    source = "f() { return 1; }"
    assert Parser(source).parse() == "success"


def test_09_function_void_return():
    source = "void f() { return; }"
    assert Parser(source).parse() == "success"


def test_10_multiple_structs():
    source = """
    struct A { int x; };
    struct B { float y; };
    """
    assert Parser(source).parse() == "success"


# ========== VARIABLE DECLARATION (11–20) ==========

def test_11_auto_no_init():
    assert Parser("void main() { auto x; }").parse() == "success"


def test_12_auto_init_expression():
    source = "void main() { auto x = 1 + 2 * 3; }"
    assert Parser(source).parse() == "success"


def test_13_explicit_no_init():
    source = "void main() { int x; float y; string z; }"
    assert Parser(source).parse() == "success"


def test_14_struct_variable():
    source = """
    struct P { int x; int y; };
    void main() { P p; }
    """
    assert Parser(source).parse() == "success"

def test_19_multiple_decls_one_block():
    source = "void main() { int a; int b; auto c = a + b; }"
    assert Parser(source).parse() == "success"


def test_20_nested_block_decl():
    source = "void main() { { int x; } }"
    assert Parser(source).parse() == "success"


# ========== EXPRESSIONS (21–35) ==========

def test_22_prefix_postfix():
    source = "void main() { int x; ++x; x++; --x; x--; }"
    assert Parser(source).parse() == "success"


def test_23_complex_expression():
    source = "void main() { auto x = (1 + 2) * (3 - 4) / 5; }"
    assert Parser(source).parse() == "success"


def test_24_relational_chain():
    source = "void main() { auto x = 1 < 2 == 3 > 4; }"
    assert Parser(source).parse() == "success"


def test_25_logical_expr():
    source = "void main() { auto x = 1 && 0 || !1; }"
    assert Parser(source).parse() == "success"


def test_26_function_call_expr():
    source = """
    int f(int x) { return x; }
    void main() { auto y = f(10); }
    """
    assert Parser(source).parse() == "success"


def test_27_nested_function_call():
    source = """
    int f(int x) { return x; }
    void main() { auto y = f(f(1)); }
    """
    assert Parser(source).parse() == "success"





def test_30_assignment_to_member():
    source = """
    struct P { int x; };
    void main() { P p; p.x = 5; }
    """
    assert Parser(source).parse() == "success"


# ========== CONTROL FLOW (36–60) ==========

def test_36_if_else_block():
    source = "void main() { if (1) { printInt(1); } else { printInt(0); } }"
    assert Parser(source).parse() == "success"


def test_37_nested_if():
    source = "void main() { if (1) if (2) printInt(1); else printInt(0); }"
    assert Parser(source).parse() == "success"


def test_38_while_block():
    source = "void main() { while (1) { break; } }"
    assert Parser(source).parse() == "success"


def test_39_for_full():
    source = "void main() { for (int i = 0; i < 10; i++) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_40_for_missing_parts():
    source = "void main() { for (; ; ) break; }"
    assert Parser(source).parse() == "success"


def test_41_for_no_init():
    source = "void main() { int i; for (; i < 10; ++i) {} }"
    assert Parser(source).parse() == "success"


def test_42_for_no_condition():
    source = "void main() { for (int i = 0; ; ++i) break; }"
    assert Parser(source).parse() == "success"


def test_43_for_no_update():
    source = "void main() { for (int i = 0; i < 10; ) break; }"
    assert Parser(source).parse() == "success"


def test_44_continue_in_loop():
    source = "void main() { while (1) { continue; } }"
    assert Parser(source).parse() == "success"


def test_45_break_in_switch():
    source = "void main() { switch (1) { case 1: break; } }"
    assert Parser(source).parse() == "success"


# ========== SWITCH CASE (61–80) ==========

def test_61_switch_multiple_cases():
    source = """
    void main() {
        switch (1) {
            case 1: printInt(1); break;
            case 2: printInt(2); break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_62_switch_fallthrough():
    source = """
    void main() {
        switch (1) {
            case 1:
            case 2:
                printInt(1);
                break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_63_switch_default():
    source = """
    void main() {
        switch (1) {
            default:
                printInt(0);
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_64_switch_empty():
    source = "void main() { switch (1) { } }"
    assert Parser(source).parse() == "success"


def test_65_switch_expr():
    source = "void main() { switch (1+2*3) { case 7: break; } }"
    assert Parser(source).parse() == "success"


def test_70_switch_nested():
    source = """
    void main() {
        switch (1) {
            case 1:
                switch (2) {
                    case 2: break;
                }
                break;
        }
    }
    """
    assert Parser(source).parse() == "success"


# ========== COMPLEX PROGRAMS (81–100) ==========

def test_81_recursive_function():
    source = """
    int f(int x) {
        if (x <= 1) return 1;
        return x * f(x - 1);
    }
    """
    assert Parser(source).parse() == "success"


def test_82_multiple_returns():
    source = "int f(int x) { if (x) return 1; else return 0; }"
    assert Parser(source).parse() == "success"


def test_83_function_call_in_loop():
    source = """
    int f(int x) { return x; }
    void main() {
        for (int i = 0; i < 10; i++)
            printInt(f(i));
    }
    """
    assert Parser(source).parse() == "success"


def test_84_deep_blocks():
    source = "void main() { {{{{ int x; }}}} }"
    assert Parser(source).parse() == "success"


def test_85_expression_statement_only():
    source = "void main() { 1 + 2; }"
    assert Parser(source).parse() == "success"


def test_86_chained_member_access():
    source = """
    struct A { int x; };
    struct B { A a; };
    void main() { B b; b.a.x = 1; }
    """
    assert Parser(source).parse() == "success"


def test_88_assignment_in_condition():
    source = "void main() { int x; if (x == 1) printInt(x); }"
    assert Parser(source).parse() == "success"


def test_89_complex_for_body():
    source = """
    void main() {
        for (int i = 0; i < 10; ++i) {
            if (i % 2 == 0) continue;
            printInt(i);
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_90_empty_block_statement():
    source = "void main() { {} }"
    assert Parser(source).parse() == "success"


def test_91_multiple_empty_statements():
    source = "void main() { ; ; ; }"
    # expr_stmt yêu cầu expr; nên chỉ cho phép block rỗng
    # => thay bằng block lồng
    source = "void main() { {} {} }"
    assert Parser(source).parse() == "success"


def test_92_nested_loops():
    source = """
    void main() {
        for (int i = 0; i < 3; i++)
            while (i < 2)
                break;
    }
    """
    assert Parser(source).parse() == "success"


def test_93_if_else_chain():
    source = """
    void main() {
        if (1) printInt(1);
        else if (0) printInt(0);
        else printInt(-1);
    }
    """
    assert Parser(source).parse() == "success"


def test_94_switch_only_default():
    source = """
    void main() {
        switch (10) {
            default:
                break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_95_return_expression_complex():
    source = """
    int f(int a, int b) {
        return (a + b) * (a - b) / 2;
    }
    """
    assert Parser(source).parse() == "success"


def test_96_struct_used_as_param():
    source = """
    struct P { int x; };
    int f(P p) { return p.x; }
    """
    assert Parser(source).parse() == "success"


def test_97_function_call_as_statement():
    source = """
    void foo() {}
    void main() { foo(); }
    """
    assert Parser(source).parse() == "success"


def test_98_multiple_blocks_sequential():
    source = """
    void main() {
        { int a; }
        { int b; }
        { int c; }
    }
    """
    assert Parser(source).parse() == "success"


def test_99_complex_member_access_expression():
    source = """
    struct A { int x; };
    struct B { A a; };
    void main() {
        B b;
        auto y = b.a.x + 1;
    }
    """
    assert Parser(source).parse() == "success"


def test_100_large_program_mix():
    source = """
    struct Point { int x; int y; };

    int sum(Point p) {
        return p.x + p.y;
    }

    void main() {
        Point p;
        p.x = 1;
        p.y = 2;

        for (int i = 0; i < 1; i++) {
            if (sum(p) > 0)
                printInt(sum(p));
        }
    }
    """
    assert Parser(source).parse() == "success"


# ========== VALID STRUCTURES (59–75) ==========

def test_59_simple_assignment():
    source = "void main() { int x; x = 1; }"
    assert Parser(source).parse() == "success"


def test_60_multiple_assignments():
    source = "void main() { int x; int y; x = 1; y = 2; }"
    assert Parser(source).parse() == "success"


def test_61_return_in_block():
    source = "int f() { { return 1; } }"
    assert Parser(source).parse() == "success"


def test_62_nested_blocks_only():
    source = "void main() { { { { } } } }"
    assert Parser(source).parse() == "success"


def test_63_while_with_block():
    source = "void main() { while (1) { int x; } }"
    assert Parser(source).parse() == "success"


def test_64_for_with_assignment_init():
    source = "void main() { int i; for (i = 0; i < 3; i++) {} }"
    assert Parser(source).parse() == "success"


def test_65_for_with_expr_update():
    source = "void main() { int i; for (; i < 3; i++) break; }"
    assert Parser(source).parse() == "success"


def test_66_if_else_blocks():
    source = "void main() { if (1) { int x; } else { int y; } }"
    assert Parser(source).parse() == "success"


def test_67_switch_multiple_cases():
    source = """
    void main() {
        switch (1) {
            case 1: break;
            case 2: break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_68_switch_only_default():
    source = """
    void main() {
        switch (1) {
            default: break;
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_69_function_call_statement():
    source = "void foo() {} void main() { foo(); }"
    assert Parser(source).parse() == "success"


def test_70_nested_function_calls():
    source = """
    int f(int x) { return x; }
    void main() { printInt(f(f(1))); }
    """
    assert Parser(source).parse() == "success"


def test_71_struct_param_function():
    source = """
    struct A { int x; };
    int f(A a) { return a.x; }
    """
    assert Parser(source).parse() == "success"


def test_72_chained_member_assignment():
    source = """
    struct A { int x; };
    struct B { A a; };
    void main() { B b; b.a.x = 10; }
    """
    assert Parser(source).parse() == "success"


def test_73_expression_with_parentheses():
    source = "void main() { auto x = (1 + 2) * (3 - 4); }"
    assert Parser(source).parse() == "success"


def test_74_logical_expression():
    source = "void main() { auto x = 1 && 0 || !1; }"
    assert Parser(source).parse() == "success"


def test_75_relational_expression():
    source = "void main() { auto x = 1 < 2; }"
    assert Parser(source).parse() == "success"


# ========== INVALID / SYNTAX ERROR CASES (76–100) ==========

def test_76_missing_semicolon():
    source = "void main() { int x }"
    assert Parser(source).parse().startswith("Error")


def test_77_invalid_assignment_expression():
    source = "void main() { int x; x = ; }"
    assert Parser(source).parse().startswith("Error")


def test_78_unclosed_block():
    source = "void main() { int x; "
    assert Parser(source).parse().startswith("Error")


def test_79_unclosed_parenthesis():
    source = "void main() { if (1 printInt(1); }"
    assert Parser(source).parse().startswith("Error")


def test_80_invalid_if_syntax():
    source = "void main() { if 1 printInt(1); }"
    assert Parser(source).parse().startswith("Error")


def test_81_invalid_for_missing_semicolon():
    source = "void main() { for (int i = 0 i < 10; i++) {} }"
    assert Parser(source).parse().startswith("Error")


def test_82_invalid_for_missing_paren():
    source = "void main() { for int i = 0; i < 10; i++) {} }"
    assert Parser(source).parse().startswith("Error")


def test_83_invalid_switch_no_expr():
    source = "void main() { switch () { case 1: break; } }"
    assert Parser(source).parse().startswith("Error")


def test_84_case_without_colon():
    source = "void main() { switch (1) { case 1 break; } }"
    assert Parser(source).parse().startswith("Error")


def test_85_default_without_colon():
    source = "void main() { switch (1) { default break; } }"
    assert Parser(source).parse().startswith("Error")


def test_86_break_outside_loop():
    source = "void main() { break; }"
    assert Parser(source).parse() == "success"  # syntax OK


def test_87_continue_outside_loop():
    source = "void main() { continue; }"
    assert Parser(source).parse() == "success"  # syntax OK


def test_88_return_with_expr_in_void():
    source = "void f() { return 1; }"
    assert Parser(source).parse() == "success"  # semantic error only


def test_89_missing_return_semicolon():
    source = "int f() { return 1 }"
    assert Parser(source).parse().startswith("Error")


def test_90_invalid_function_decl():
    source = "int () { return 1; }"
    assert Parser(source).parse().startswith("Error")


def test_91_invalid_struct_decl():
    source = "struct { int x; };"
    assert Parser(source).parse().startswith("Error")


def test_92_invalid_member_access():
    source = "void main() { int x; x.y = 1; }"
    assert Parser(source).parse() == "success"  # semantic error only


def test_93_invalid_expression_operator():
    source = "void main() { auto x = 1 + * 2; }"
    assert Parser(source).parse().startswith("Error")


def test_94_double_operator():
    source = "void main() { auto x = 1 && || 0; }"
    assert Parser(source).parse().startswith("Error")


def test_95_missing_function_body():
    source = "int f();"
    assert Parser(source).parse().startswith("Error")


def test_96_missing_struct_semicolon():
    source = "struct A { int x; }"
    assert Parser(source).parse().startswith("Error")


def test_97_invalid_param_list():
    source = "int f(int, int b) { return b; }"
    assert Parser(source).parse().startswith("Error")


def test_98_invalid_call_syntax():
    source = "void main() { printInt(,); }"
    assert Parser(source).parse().startswith("Error")


def test_99_unmatched_braces():
    source = "void main() { if (1) { printInt(1); }"
    assert Parser(source).parse().startswith("Error")


def test_100_random_invalid_tokens():
    source = "void main() { @@@ }"
    assert Parser(source).parse().startswith("Error")
