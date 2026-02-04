import pytest
from tests.utils import Tokenizer

# ========== BASIC TOKENS (1–20) ==========

def test_01_empty_input():
    assert Tokenizer("").get_tokens_as_string() == "<EOF>"


def test_02_whitespace_only():
    assert Tokenizer("   \n\t ").get_tokens_as_string() == "<EOF>"


def test_03_identifier_simple():
    assert Tokenizer("abc").get_tokens_as_string() == "abc,<EOF>"


def test_04_identifier_with_digits():
    assert Tokenizer("a1b2").get_tokens_as_string() == "a1b2,<EOF>"


def test_05_identifier_with_underscore():
    assert Tokenizer("_abc_").get_tokens_as_string() == "_abc_,<EOF>"


def test_06_keyword_int():
    assert Tokenizer("int").get_tokens_as_string() == "int,<EOF>"


def test_07_keyword_struct():
    assert Tokenizer("struct").get_tokens_as_string() == "struct,<EOF>"


def test_08_integer_literal():
    assert Tokenizer("123").get_tokens_as_string() == "123,<EOF>"


def test_09_integer_leading_zero():
    assert Tokenizer("000123").get_tokens_as_string() == "000123,<EOF>"


def test_10_float_literal():
    assert Tokenizer("3.14").get_tokens_as_string() == "3.14,<EOF>"


def test_11_string_literal_simple():
    assert Tokenizer('"abc"').get_tokens_as_string() == "abc,<EOF>"


def test_12_string_with_space():
    assert Tokenizer('"hello world"').get_tokens_as_string() == "hello world,<EOF>"


def test_13_boolean_like_int():
    assert Tokenizer("1 0").get_tokens_as_string() == "1,0,<EOF>"


def test_14_operator_plus():
    assert Tokenizer("+").get_tokens_as_string() == "+,<EOF>"


def test_15_operator_minus():
    assert Tokenizer("-").get_tokens_as_string() == "-,<EOF>"


def test_16_operator_mul():
    assert Tokenizer("*").get_tokens_as_string() == "*,<EOF>"


def test_17_operator_div():
    assert Tokenizer("/").get_tokens_as_string() == "/,<EOF>"


def test_18_operator_mod():
    assert Tokenizer("%").get_tokens_as_string() == "%,<EOF>"


def test_19_operator_assign():
    assert Tokenizer("=").get_tokens_as_string() == "=,<EOF>"


def test_20_operator_equal():
    assert Tokenizer("==").get_tokens_as_string() == "==,<EOF>"


# ========== SEPARATORS & DELIMITERS (21–35) ==========

def test_21_semicolon():
    assert Tokenizer(";").get_tokens_as_string() == ";,<EOF>"


def test_22_comma():
    assert Tokenizer(",").get_tokens_as_string() == ",,<EOF>"


def test_23_parentheses():
    assert Tokenizer("( )").get_tokens_as_string() == "(,),<EOF>"


def test_24_braces():
    assert Tokenizer("{ }").get_tokens_as_string() == "{,},<EOF>"


def test_25_brackets():
    assert Tokenizer("[ ]").get_tokens_as_string() == "[,],<EOF>"


def test_26_mixed_delimiters():
    assert Tokenizer("(){},;").get_tokens_as_string() == "(,),{,},,,;,<EOF>"


def test_27_dot_operator():
    assert Tokenizer(".").get_tokens_as_string() == ".,<EOF>"


def test_28_relational_ops():
    assert Tokenizer("< > <= >=").get_tokens_as_string() == "<,>,<=,>=,<EOF>"


def test_29_logical_ops():
    assert Tokenizer("&& || !").get_tokens_as_string() == "&&,||,!,<EOF>"


def test_30_increment_decrement():
    assert Tokenizer("++ --").get_tokens_as_string() == "++,--,<EOF>"



# ========== COMMENTS (36–50) ==========

def test_36_line_comment():
    assert Tokenizer("// comment").get_tokens_as_string() == "<EOF>"


def test_37_line_comment_after_code():
    assert Tokenizer("int x; // comment").get_tokens_as_string() == "int,x,;,<EOF>"


def test_38_block_comment():
    assert Tokenizer("/* comment */").get_tokens_as_string() == "<EOF>"


def test_39_block_comment_between_code():
    assert Tokenizer("int /* c */ x;").get_tokens_as_string() == "int,x,;,<EOF>"


def test_40_block_comment_not_nested():
    assert Tokenizer("/* a /* b */ c */").get_tokens_as_string() == "c,*,/,<EOF>"


def test_41_multiple_comments():
    assert Tokenizer("//a\n/*b*/").get_tokens_as_string() == "<EOF>"


def test_42_comment_and_string():
    assert Tokenizer('"// not comment"').get_tokens_as_string() == "// not comment,<EOF>"


def test_43_comment_and_operator():
    assert Tokenizer("/* */ +").get_tokens_as_string() == "+,<EOF>"


def test_44_unclosed_block_comment():
    assert Tokenizer("/* abc").get_tokens_as_string() == "/,*,abc,<EOF>"


def test_45_comment_only():
    assert Tokenizer("/* test */ // test").get_tokens_as_string() == "<EOF>"


# ========== STRING ERRORS (51–65) ==========

def test_51_unclosed_string():
    assert Tokenizer('"abc').get_tokens_as_string().startswith("Unclosed String")


def test_52_string_with_newline():
    assert Tokenizer('"abc\n"').get_tokens_as_string().startswith("Unclosed String")


def test_53_string_escape_valid():
    assert Tokenizer('"a\\n"').get_tokens_as_string() == "a\\n,<EOF>"


def test_54_string_escape_tab():
    assert Tokenizer('"a\\t"').get_tokens_as_string() == "a\\t,<EOF>"


def test_55_string_escape_quote():
    assert Tokenizer('"a\\""').get_tokens_as_string() == 'a\\",<EOF>'


def test_56_string_escape_backslash():
    assert Tokenizer('"a\\\\"').get_tokens_as_string() == "a\\\\,<EOF>"


def test_57_illegal_escape():
    assert Tokenizer('"a\\x"').get_tokens_as_string().startswith("Illegal Escape")


def test_58_illegal_escape_number():
    assert Tokenizer('"a\\1"').get_tokens_as_string().startswith("Illegal Escape")


def test_59_empty_string():
    assert Tokenizer('""').get_tokens_as_string() == ",<EOF>"


def test_60_string_only_space():
    assert Tokenizer('"   "').get_tokens_as_string() == "   ,<EOF>"


# ========== INVALID TOKENS (61–80) ==========

def test_61_error_char_at():
    assert Tokenizer("@").get_tokens_as_string().startswith("Error Token")


def test_62_error_char_dollar():
    assert Tokenizer("$").get_tokens_as_string().startswith("Error Token")


def test_63_error_char_backtick():
    assert Tokenizer("`").get_tokens_as_string().startswith("Error Token")


def test_64_error_char_unicode():
    assert Tokenizer("α").get_tokens_as_string().startswith("Error Token")


def test_65_error_char_mix():
    assert "Error Token @" in Tokenizer("int @ x").get_tokens_as_string()


def test_66_identifier_start_digit_invalid():
    assert Tokenizer("1abc").get_tokens_as_string() == "1,abc,<EOF>"


def test_67_float_missing_decimal_part():
    assert Tokenizer("1.").get_tokens_as_string() == "1.,<EOF>"


def test_68_float_missing_int_part():
    assert Tokenizer(".5").get_tokens_as_string() == ".5,<EOF>"


def test_69_multiple_dots():
    assert Tokenizer("1.2.3").get_tokens_as_string() == "1.2,.3,<EOF>"

def test_70_float_no_exponent():
    assert Tokenizer("1e10").get_tokens_as_string() == "1e10,<EOF>"


# ========== EDGE CASES (81–100) ==========

def test_81_long_identifier():
    assert Tokenizer("a" * 100).get_tokens_as_string().endswith("<EOF>")


def test_82_long_integer():
    assert Tokenizer("9" * 100).get_tokens_as_string().endswith("<EOF>")


def test_83_many_operators():
    assert Tokenizer("+-*/").get_tokens_as_string() == "+,-,*,/,<EOF>"


def test_84_many_semicolons():
    assert Tokenizer(";;;").get_tokens_as_string() == ";,;,;,<EOF>"


def test_85_nested_parentheses():
    assert Tokenizer("((()))").get_tokens_as_string() == "(,(,(,),),),<EOF>"


def test_86_adjacent_identifiers():
    assert Tokenizer("abcxyz").get_tokens_as_string() == "abcxyz,<EOF>"


def test_87_keyword_as_prefix():
    assert Tokenizer("intx").get_tokens_as_string() == "intx,<EOF>"


def test_88_identifier_keyword_mix():
    assert Tokenizer("main1").get_tokens_as_string() == "main1,<EOF>"


def test_89_number_and_identifier():
    assert Tokenizer("123abc").get_tokens_as_string() == "123,abc,<EOF>"


def test_90_many_whitespace():
    assert Tokenizer(" \n\t int \n ").get_tokens_as_string() == "int,<EOF>"


def test_91_operator_without_space():
    assert Tokenizer("a+b").get_tokens_as_string() == "a,+,b,<EOF>"


def test_92_multiple_strings():
    assert Tokenizer('"a" "b"').get_tokens_as_string() == "a,b,<EOF>"


def test_93_string_after_code():
    assert Tokenizer('x="a"').get_tokens_as_string() == "x,=,a,<EOF>"


def test_94_comment_after_string():
    assert Tokenizer('"a"//c').get_tokens_as_string() == "a,<EOF>"


def test_95_block_comment_after_string():
    assert Tokenizer('"a"/*c*/').get_tokens_as_string() == "a,<EOF>"


def test_96_string_with_slash():
    assert Tokenizer('"a/b"').get_tokens_as_string() == "a/b,<EOF>"


def test_97_string_with_star():
    assert Tokenizer('"a*b"').get_tokens_as_string() == "a*b,<EOF>"


def test_98_string_with_percent():
    assert Tokenizer('"a%b"').get_tokens_as_string() == "a%b,<EOF>"


def test_99_only_eof():
    assert Tokenizer("").get_tokens_as_string() == "<EOF>"


def test_100_mix_everything():
    source = 'int x=1; //c\n"x" /*c*/'
    assert Tokenizer(source).get_tokens_as_string() == "int,x,=,1,;,x,<EOF>"


def test_81_integer_zero():
    assert Tokenizer("0").get_tokens_as_string() == "0,<EOF>"


def test_82_integer_many_zeros():
    assert Tokenizer("0000").get_tokens_as_string() == "0000,<EOF>"


def test_83_float_simple():
    assert Tokenizer("12.34").get_tokens_as_string() == "12.34,<EOF>"


def test_84_float_leading_zero():
    assert Tokenizer("000012.67").get_tokens_as_string() == "000012.67,<EOF>"


def test_85_float_only_fraction():
    assert Tokenizer(".75").get_tokens_as_string() == ".75,<EOF>"


def test_86_float_with_exponent_lower():
    assert Tokenizer("1e10").get_tokens_as_string() == "1e10,<EOF>"


def test_87_float_with_exponent_upper():
    assert Tokenizer("2E-3").get_tokens_as_string() == "2E-3,<EOF>"


def test_88_string_simple():
    assert Tokenizer("\"hello\"").get_tokens_as_string() == "hello,<EOF>"


def test_89_string_with_escape_newline():
    assert Tokenizer("\"a\\nb\"").get_tokens_as_string() == "a\\nb,<EOF>"


def test_90_string_with_escape_quote():
    assert Tokenizer("\"\\\"abc\\\"\"").get_tokens_as_string() == "\\\"abc\\\",<EOF>"


def test_91_string_with_escape_tab():
    assert Tokenizer("\"a\\tb\"").get_tokens_as_string() == "a\\tb,<EOF>"


def test_92_empty_string():
    assert Tokenizer("\"\"").get_tokens_as_string() == ",<EOF>"


def test_93_string_with_backslash():
    assert Tokenizer("\"a\\\\b\"").get_tokens_as_string() == "a\\\\b,<EOF>"


def test_94_string_with_spaces():
    assert Tokenizer("\"hello world\"").get_tokens_as_string() == "hello world,<EOF>"


def test_95_all_arithmetic_ops():
    source = "+ - * / %"
    assert Tokenizer(source).get_tokens_as_string() == "+,-,*,/,%,<EOF>"


def test_96_all_relational_ops():
    source = "< <= > >= == !="
    assert Tokenizer(source).get_tokens_as_string() == "<,<=,>,>=,==,!=,<EOF>"


def test_97_logical_ops():
    source = "&& || !"
    assert Tokenizer(source).get_tokens_as_string() == "&&,||,!,<EOF>"


def test_98_increment_decrement():
    source = "++ --"
    assert Tokenizer(source).get_tokens_as_string() == "++,--,<EOF>"


def test_99_keywords_and_identifiers_mix():
    source = "int x float y string s"
    assert Tokenizer(source).get_tokens_as_string() == "int,x,float,y,string,s,<EOF>"


def test_100_comments_are_skipped():
    source = """
    // this is a line comment
    int x; /* block comment */ float y;
    """
    assert Tokenizer(source).get_tokens_as_string() == "int,x,;,float,y,;,<EOF>"
