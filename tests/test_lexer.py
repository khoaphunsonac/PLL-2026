import pytest
from tests.utils import Tokenizer

import pytest
from tests.utils import Tokenizer

# ========== 001 KEYWORDS ==========

def test_001_all_keywords():
    source = "int float string bool void auto struct if else for while do break continue return switch case default"
    expected = "int,float,string,bool,void,auto,struct,if,else,for,while,do,break,continue,return,switch,case,default,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected


# ========== 002 OPERATORS & SEPARATORS ==========

def test_002_all_operators_and_separators():
    source = "+ - * / % == != < > <= >= || && ! ++ -- = . { } ( ) ; , :"
    expected = "+,-,*,/,%,==,!=,<,>,<=,>=,||,&&,!,++,--,=,.,{,},(,),;,,,:,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected


# ========== 003–009 IDENTIFIERS ==========

def test_003_identifier_letters_digits():
    assert Tokenizer("abc123").get_tokens_as_string() == "abc123,<EOF>"


def test_004_identifier_leading_underscore():
    assert Tokenizer("_abc").get_tokens_as_string() == "_abc,<EOF>"


def test_005_identifier_only_underscore():
    assert Tokenizer("_").get_tokens_as_string() == "_,<EOF>"


def test_006_identifier_uppercase():
    assert Tokenizer("ABC").get_tokens_as_string() == "ABC,<EOF>"


def test_007_identifier_mixed_case():
    assert Tokenizer("AbCde").get_tokens_as_string() == "AbCde,<EOF>"


def test_008_identifier_double_underscore():
    assert Tokenizer("__name__").get_tokens_as_string() == "__name__,<EOF>"


def test_009_case_sensitive_keyword():
    # If and ELSE are identifiers, not keywords
    assert Tokenizer("If ELSE").get_tokens_as_string() == "If,ELSE,<EOF>"


# ========== 010–015 INTEGER LITERALS ==========

def test_010_single_digit_integer():
    assert Tokenizer("5").get_tokens_as_string() == "5,<EOF>"


def test_011_multi_digit_integer():
    assert Tokenizer("12345").get_tokens_as_string() == "12345,<EOF>"


def test_012_leading_zero_integer():
    assert Tokenizer("007").get_tokens_as_string() == "007,<EOF>"


def test_013_minus_is_separate_operator():
    assert Tokenizer("-5").get_tokens_as_string() == "-,5,<EOF>"


def test_014_plus_is_separate_operator():
    assert Tokenizer("+10").get_tokens_as_string() == "+,10,<EOF>"


def test_015_integer_adjacent_operator():
    assert Tokenizer("5+10").get_tokens_as_string() == "5,+,10,<EOF>"


# ========== 016–033 FLOAT LITERALS ==========

def test_016_float_decimal():
    assert Tokenizer("3.14").get_tokens_as_string() == "3.14,<EOF>"


def test_017_float_zero():
    assert Tokenizer("0.0").get_tokens_as_string() == "0.0,<EOF>"


def test_018_float_trailing_dot():
    assert Tokenizer("1.").get_tokens_as_string() == "1.,<EOF>"


def test_019_float_leading_dot():
    assert Tokenizer(".5").get_tokens_as_string() == ".5,<EOF>"


def test_020_float_exponent_lower():
    assert Tokenizer("1e4").get_tokens_as_string() == "1e4,<EOF>"


def test_021_float_exponent_upper():
    assert Tokenizer("1E4").get_tokens_as_string() == "1E4,<EOF>"


def test_022_float_decimal_exponent():
    assert Tokenizer("1.23e4").get_tokens_as_string() == "1.23e4,<EOF>"


def test_023_float_exponent_negative():
    assert Tokenizer("5.67E-2").get_tokens_as_string() == "5.67E-2,<EOF>"


def test_024_float_exponent_positive():
    assert Tokenizer("1e+5").get_tokens_as_string() == "1e+5,<EOF>"


def test_025_invalid_exponent_no_digit():
    # 1e → INT + ID
    assert Tokenizer("1e").get_tokens_as_string() == "1,e,<EOF>"


def test_026_invalid_exponent_sign_no_digit():
    # 1e+ → INT + ID + +
    assert Tokenizer("1e+").get_tokens_as_string() == "1,e,+,<EOF>"


def test_027_multiple_dots():
    # 1.2.3 → float then . then int
    assert Tokenizer("1.2.3").get_tokens_as_string() == "1.2,.3,<EOF>"


def test_028_dot_after_identifier():
    assert Tokenizer("a.5").get_tokens_as_string() == "a,.5,<EOF>"


def test_029_minus_before_float():
    assert Tokenizer("-3.14").get_tokens_as_string() == "-,3.14,<EOF>"


def test_030_plus_before_float():
    assert Tokenizer("+2.5").get_tokens_as_string() == "+,2.5,<EOF>"


def test_031_float_adjacent_operator():
    assert Tokenizer("3.5+2.1").get_tokens_as_string() == "3.5,+,2.1,<EOF>"


def test_032_float_only_dot_error():
    # Single dot is operator
    assert Tokenizer(".").get_tokens_as_string() == ".,<EOF>"


def test_033_complex_float_chain():
    assert Tokenizer("1e2+3.4E-1").get_tokens_as_string() == "1e2,+,3.4E-1,<EOF>"

# ========== 034–044 STRING LITERALS ==========

def test_034_empty_string():
    assert Tokenizer('""').get_tokens_as_string() == ',<EOF>'


def test_035_string_with_space():
    assert Tokenizer('"hello world"').get_tokens_as_string() == 'hello world,<EOF>'


def test_036_string_with_tab():
    assert Tokenizer('"a\\tb"').get_tokens_as_string() == "a\tb,<EOF>"


def test_037_string_with_newline_escape():
    assert Tokenizer('"a\\nb"').get_tokens_as_string() == "a\nb,<EOF>"


def test_038_string_with_quote_escape():
    assert Tokenizer('"a\\"b"').get_tokens_as_string() == 'a"b,<EOF>'


def test_039_string_with_backslash():
    assert Tokenizer('"a\\\\b"').get_tokens_as_string() == 'a\\b,<EOF>'


def test_040_string_with_backspace():
    assert Tokenizer('"a\\bb"').get_tokens_as_string() == "a\bb,<EOF>"


def test_041_string_with_formfeed():
    assert Tokenizer('"a\\fb"').get_tokens_as_string() == "a\fb,<EOF>"


def test_042_string_with_carriage_return():
    assert Tokenizer('"a\\rb"').get_tokens_as_string() == "a\rb,<EOF>"


def test_043_string_digits_special_chars():
    assert Tokenizer('"123!@#"').get_tokens_as_string() == '123!@#,<EOF>'


def test_044_string_with_comment_symbols():
    # // and /* inside string are normal text
    assert Tokenizer('"// not comment /* ok */"').get_tokens_as_string() == '// not comment /* ok */,<EOF>'

# ========== 045–052 COMMENTS ==========

def test_045_line_comment_only():
    assert Tokenizer("// comment").get_tokens_as_string() == "<EOF>"


def test_046_line_comment_with_code():
    assert Tokenizer("int x; // comment").get_tokens_as_string() == "int,x,;,<EOF>"


def test_047_block_comment_only():
    assert Tokenizer("/* comment */").get_tokens_as_string() == "<EOF>"


def test_048_block_comment_with_code():
    assert Tokenizer("int x; /* comment */").get_tokens_as_string() == "int,x,;,<EOF>"


def test_049_multiline_block_comment():
    assert Tokenizer("/* line1\nline2 */").get_tokens_as_string() == "<EOF>"


def test_050_comment_between_tokens():
    assert Tokenizer("int/*c*/x").get_tokens_as_string() == "int,x,<EOF>"


def test_051_line_inside_block_comment():
    assert Tokenizer("/* // still comment */").get_tokens_as_string() == "<EOF>"


def test_052_block_not_nested():
    # Block comments do not nest
    assert Tokenizer("/* /* x */ */").get_tokens_as_string() == "*,/,<EOF>"

# ========== 053–059 ILLEGAL ESCAPE ==========

def test_053_illegal_escape_unknown_char():
    assert "Illegal" in Tokenizer('"abc\\q"').get_tokens_as_string()

def test_054_illegal_escape_x():
    assert "Illegal" in Tokenizer('"abc\\x"').get_tokens_as_string()


def test_055_illegal_escape_a():
    assert "Illegal" in Tokenizer('"abc\\a"').get_tokens_as_string()


def test_056_illegal_escape_q():
    assert "Illegal" in Tokenizer('"abc\\q"').get_tokens_as_string()


def test_057_illegal_escape_number():
    assert "Illegal" in Tokenizer('"abc\\8"').get_tokens_as_string()


def test_058_stop_at_first_illegal_escape():
    # first illegal escape is \x, \q should not be processed
    assert "Illegal" in Tokenizer('"a\\x b\\q"').get_tokens_as_string()


def test_059_illegal_escape_before_valid_escape():
    assert "Illegal" in Tokenizer('"a\\x\\n"').get_tokens_as_string()

# ========== 060–069 UNCLOSED STRING ==========

def test_060_unclosed_string_eof():
    assert "Unclosed" in Tokenizer('"abc').get_tokens_as_string()


def test_061_unclosed_string_with_escape():
    assert "Unclosed" in Tokenizer('"abc\\n').get_tokens_as_string()


def test_062_unclosed_string_newline_terminates():
    assert "Unclosed" in Tokenizer('"abc\n').get_tokens_as_string()


def test_063_unclosed_string_carriage_return():
    assert "Unclosed" in Tokenizer('"abc\r').get_tokens_as_string()


def test_064_just_open_quote():
    assert "Unclosed" in Tokenizer('"').get_tokens_as_string()


def test_065_escaped_quote_still_unclosed():
    assert "Unclosed" in Tokenizer('"abc\\"').get_tokens_as_string()


def test_066_long_unclosed_string():
    assert "Unclosed" in Tokenizer('"this is a very long string without end').get_tokens_as_string()


def test_067_unclosed_vs_illegal_priority():
    # illegal escape should be detected before unclosed
    result = Tokenizer('"abc\\x').get_tokens_as_string()
    assert "Illegal" in result


def test_068_unclosed_after_valid_escape():
    assert "Unclosed" in Tokenizer('"abc\\nxyz').get_tokens_as_string()


def test_069_unclosed_empty_content():
    assert "Unclosed" in Tokenizer('"').get_tokens_as_string()

# ========== 070–077 ERROR TOKEN ==========

def test_070_invalid_dollar():
    assert "Error" in Tokenizer("$").get_tokens_as_string()


def test_071_invalid_at():
    assert "Error" in Tokenizer("@").get_tokens_as_string()


def test_072_invalid_hash():
    assert "Error" in Tokenizer("#").get_tokens_as_string()


def test_073_single_ampersand():
    assert "Error" in Tokenizer("&").get_tokens_as_string()


def test_074_single_pipe():
    assert "Error" in Tokenizer("|").get_tokens_as_string()


def test_075_invalid_bracket():
    assert "Error" in Tokenizer("[").get_tokens_as_string()


def test_076_error_after_valid_token():
    assert "Error" in Tokenizer("int $").get_tokens_as_string()


def test_077_only_first_error_reported():
    result = Tokenizer("$@#").get_tokens_as_string()
    assert result.count("Error") == 1

# ========== 078–083 OPERATOR DISAMBIGUATION ==========

def test_078_triple_equal():
    # === → == then =
    assert Tokenizer("===").get_tokens_as_string() == "==,=,<EOF>"


def test_079_a_triple_plus_b():
    # a+++b → a, ++, +, b
    assert Tokenizer("a+++b").get_tokens_as_string() == "a,++,+,b,<EOF>"


def test_080_a_decrement_gt_b():
    # a-->b → a, --, >, b
    assert Tokenizer("a-->b").get_tokens_as_string() == "a,--,>,b,<EOF>"


def test_081_equal_plus_equal_equal_increment():
    # =+==++ → =, +, ==, ++
    assert Tokenizer("=+==++").get_tokens_as_string() == "=,+,==,++,<EOF>"


def test_082_left_shift_split():
    # << → <, <
    assert Tokenizer("<<").get_tokens_as_string() == "<,<,<EOF>"


def test_083_right_shift_split():
    # >> → >, >
    assert Tokenizer(">>").get_tokens_as_string() == ">,>,<EOF>"

# ========== 084–087 EDGE CASES ==========

def test_084_keyword_followed_by_letter():
    # intx → identifier
    assert Tokenizer("intx").get_tokens_as_string() == "intx,<EOF>"


def test_085_number_then_identifier_split():
    # 123abc → 123 , abc
    assert Tokenizer("123abc").get_tokens_as_string() == "123,abc,<EOF>"


def test_086_dot_float_member_cases():
    source = "a.b 1.23 .5 a."
    expected = "a,.,b,1.23,.5,a,.,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_087_string_with_comment_symbols():
    assert Tokenizer('"// test /* ok */"').get_tokens_as_string() == '// test /* ok */,<EOF>'

# ========== 088–091 C/C++ NOT IN TyC ==========

def test_088_plus_equal():
    # += → + , =
    assert Tokenizer("+=").get_tokens_as_string() == "+,=,<EOF>"


def test_089_arrow_operator():
    # -> → - , >
    assert Tokenizer("->").get_tokens_as_string() == "-,>,<EOF>"


def test_090_scope_resolution():
    # :: → : , :
    assert Tokenizer("::").get_tokens_as_string() == ":,:,<EOF>"


def test_091_ellipsis():
    # ... → . , . , .
    assert Tokenizer("...").get_tokens_as_string() == ".,.,.,<EOF>"

# ========== 092–100 COMPLEX / REAL CODE ==========

def test_092_auto_declaration():
    assert Tokenizer("auto x = 5;").get_tokens_as_string() == \
           "auto,x,=,5,;,<EOF>"


def test_093_function_declaration():
    source = "int foo(int a) { return a; }"
    expected = "int,foo,(,int,a,),{,return,a,;,},<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_094_multiple_declarations():
    source = "int a; float b;"
    expected = "int,a,;,float,b,;,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_095_struct_declaration():
    source = "struct S { int x; };"
    expected = "struct,S,{,int,x,;,},;,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_096_if_else_logical():
    source = "if(a && b || !c) { x = 1; } else { x = 2; }"
    expected = "if,(,a,&&,b,||,!,c,),{,x,=,1,;,},else,{,x,=,2,;,},<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_097_for_loop():
    source = "for(i=0;i<10;i++){x=x+1;}"
    expected = "for,(,i,=,0,;,i,<,10,;,i,++,),{,x,=,x,+,1,;,},<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_098_switch_case():
    source = "switch(x){case 1: break; default: break;}"
    expected = "switch,(,x,),{,case,1,:,break,;,default,:,break,;,},<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_099_member_access_chain():
    source = "a.b.c = 5;"
    expected = "a,.,b,.,c,=,5,;,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_100_mixed_tokens_with_error():
    source = "int x = 5; @"
    result = Tokenizer(source).get_tokens_as_string()
    assert result.startswith("int,x,=,5,;,")
    assert "Error" in result