import pytest
from tests.utils import Tokenizer


def test_001_empty():
    assert Tokenizer("").get_tokens_as_string() == "EOF"

def test_002_spaces():
    assert Tokenizer("   \t\n").get_tokens_as_string() == "EOF"

def test_003_line_comment():
    assert Tokenizer("// comment").get_tokens_as_string() == "EOF"

def test_004_block_comment():
    assert Tokenizer("/* comment */").get_tokens_as_string() == "EOF"

def test_005_comment_and_code():
    assert Tokenizer("// cmt\nx").get_tokens_as_string() == "IDENTIFIER,x,EOF"

def test_006_block_comment_multiline():
    assert Tokenizer("/* a\nb\nc */ x").get_tokens_as_string() == "IDENTIFIER,x,EOF"

def test_007_leading_whitespace():
    assert Tokenizer("   x").get_tokens_as_string() == "IDENTIFIER,x,EOF"

def test_008_trailing_whitespace():
    assert Tokenizer("x   ").get_tokens_as_string() == "IDENTIFIER,x,EOF"

def test_009_between_whitespace():
    assert Tokenizer("x   y").get_tokens_as_string() == "IDENTIFIER,x,IDENTIFIER,y,EOF"

def test_010_comment_between():
    assert Tokenizer("x/*c*/y").get_tokens_as_string() == "IDENTIFIER,x,IDENTIFIER,y,EOF"

def test_011_auto():
    assert Tokenizer("auto").get_tokens_as_string() == "AUTO,auto,EOF"

def test_012_int():
    assert Tokenizer("int").get_tokens_as_string() == "INT,int,EOF"

def test_013_float():
    assert Tokenizer("float").get_tokens_as_string() == "FLOAT,float,EOF"

def test_014_string():
    assert Tokenizer("string").get_tokens_as_string() == "STRING,string,EOF"

def test_015_void():
    assert Tokenizer("void").get_tokens_as_string() == "VOID,void,EOF"

def test_016_if():
    assert Tokenizer("if").get_tokens_as_string() == "IF,if,EOF"

def test_017_else():
    assert Tokenizer("else").get_tokens_as_string() == "ELSE,else,EOF"

def test_018_for():
    assert Tokenizer("for").get_tokens_as_string() == "FOR,for,EOF"

def test_019_while():
    assert Tokenizer("while").get_tokens_as_string() == "WHILE,while,EOF"

def test_020_return():
    assert Tokenizer("return").get_tokens_as_string() == "RETURN,return,EOF"

def test_021_break():
    assert Tokenizer("break").get_tokens_as_string() == "BREAK,break,EOF"

def test_022_continue():
    assert Tokenizer("continue").get_tokens_as_string() == "CONTINUE,continue,EOF"

def test_023_switch():
    assert Tokenizer("switch").get_tokens_as_string() == "SWITCH,switch,EOF"

def test_024_case():
    assert Tokenizer("case").get_tokens_as_string() == "CASE,case,EOF"

def test_025_default():
    assert Tokenizer("default").get_tokens_as_string() == "DEFAULT,default,EOF"

def test_026_identifier_simple():
    assert Tokenizer("x").get_tokens_as_string() == "IDENTIFIER,x,EOF"

def test_027_identifier_upper():
    assert Tokenizer("ABC").get_tokens_as_string() == "IDENTIFIER,ABC,EOF"

def test_028_identifier_mixed():
    assert Tokenizer("a1_b2").get_tokens_as_string() == "IDENTIFIER,a1_b2,EOF"

def test_029_identifier_keyword_like():
    assert Tokenizer("intx").get_tokens_as_string() == "IDENTIFIER,intx,EOF"

def test_030_identifier_underscore():
    assert Tokenizer("_temp").get_tokens_as_string() == "IDENTIFIER,_temp,EOF"

def test_031_identifier_many():
    assert Tokenizer("a b c").get_tokens_as_string() == \
        "IDENTIFIER,a,IDENTIFIER,b,IDENTIFIER,c,EOF"

def test_032_int_zero():
    assert Tokenizer("0").get_tokens_as_string() == "INTLIT,0,EOF"

def test_033_int_positive():
    assert Tokenizer("123").get_tokens_as_string() == "INTLIT,123,EOF"

def test_034_int_many():
    assert Tokenizer("1 2 3").get_tokens_as_string() == \
        "INTLIT,1,INTLIT,2,INTLIT,3,EOF"

def test_035_float_basic():
    assert Tokenizer("1.5").get_tokens_as_string() == "FLOATLIT,1.5,EOF"

def test_036_float_dot():
    assert Tokenizer("1.").get_tokens_as_string() == "FLOATLIT,1.,EOF"

def test_037_float_leading_dot():
    assert Tokenizer(".5").get_tokens_as_string() == "FLOATLIT,.5,EOF"

def test_038_float_exp():
    assert Tokenizer("1e3").get_tokens_as_string() == "FLOATLIT,1e3,EOF"

def test_039_float_exp_signed():
    assert Tokenizer("1E-2").get_tokens_as_string() == "FLOATLIT,1E-2,EOF"

def test_040_string_empty():
    assert Tokenizer('""').get_tokens_as_string() == 'STRINGLIT,,EOF'

def test_041_string_simple():
    assert Tokenizer('"abc"').get_tokens_as_string() == 'STRINGLIT,abc,EOF'

def test_042_string_space():
    assert Tokenizer('"a b"').get_tokens_as_string() == 'STRINGLIT,a b,EOF'

def test_043_string_escape():
    assert Tokenizer('"a\\n"').get_tokens_as_string() == 'STRINGLIT,a\\n,EOF'

def test_044_string_quote():
    assert Tokenizer('"a\\""').get_tokens_as_string() == 'STRINGLIT,a\\",EOF'

def test_045_add():
    assert Tokenizer("+").get_tokens_as_string() == "ADD,+,EOF"

def test_046_equal():
    assert Tokenizer("==").get_tokens_as_string() == "EQUAL,==,EOF"

def test_047_assign():
    assert Tokenizer("=").get_tokens_as_string() == "ASSIGNMENT,=,EOF"

def test_048_and():
    assert Tokenizer("&&").get_tokens_as_string() == "AND,&&,EOF"

def test_049_or():
    assert Tokenizer("||").get_tokens_as_string() == "OR,||,EOF"

def test_050_not():
    assert Tokenizer("!").get_tokens_as_string() == "NOT,!,EOF"
def test_051_inc():
    assert Tokenizer("++").get_tokens_as_string() == "INCREMENT,++,EOF"

def test_052_dec():
    assert Tokenizer("--").get_tokens_as_string() == "DECREMENT,--,EOF"

def test_053_lparen():
    assert Tokenizer("(").get_tokens_as_string() == "LPAREN,(,EOF"

def test_054_rparen():
    assert Tokenizer(")").get_tokens_as_string() == "RPAREN,),EOF"
def test_055_semi():
    assert Tokenizer(";").get_tokens_as_string() == "SEMI,;,EOF"

def test_056_comma():
    assert Tokenizer(",").get_tokens_as_string() == "COMMA,,,EOF"

def test_057_lsb():
    assert Tokenizer("[").get_tokens_as_string() == "LBRACK,[,EOF"

def test_058_rsb():
    assert Tokenizer("]").get_tokens_as_string() == "RBRACK,],EOF"
def test_059_lbrace():
    assert Tokenizer("{").get_tokens_as_string() == "LBRACE,{,EOF"

def test_060_rbrace():
    assert Tokenizer("}").get_tokens_as_string() == "RBRACE,},EOF"

def test_061_less():
    assert Tokenizer("<").get_tokens_as_string() == "LT,<,EOF"

def test_062_LE():
    assert Tokenizer("<=").get_tokens_as_string() == "LE,<=,EOF"
def test_063_greater():
    assert Tokenizer(">").get_tokens_as_string() == "GT,>,EOF"

def test_064_GE():
    assert Tokenizer(">=").get_tokens_as_string() == "GE,>=,EOF"

def test_065_DOT():
    assert Tokenizer(".").get_tokens_as_string() == "DOT,.,EOF"

def test_066_simple_declaration():
    source = "int x;"
    assert Tokenizer(source).get_tokens_as_string() == \
        "INT,int,IDENTIFIER,x,SEMI,;,EOF"

def test_067_assignment():
    source = "x = 5"
    assert Tokenizer(source).get_tokens_as_string() == \
        "IDENTIFIER,x,ASSIGNMENT,=,INTLIT,5,EOF"

def test_068_expression():
    source = "a + b * 2"
    assert Tokenizer(source).get_tokens_as_string() == \
        "IDENTIFIER,a,ADD,+,IDENTIFIER,b,MUL,*,INTLIT,2,EOF"

def test_069_logical_expression():
    source = "a && b || !c"
    assert Tokenizer(source).get_tokens_as_string() == \
        "IDENTIFIER,a,AND,&&,IDENTIFIER,b,OR,||,NOT,!,IDENTIFIER,c,EOF"

def test_070_function_like():
    source = "foo(bar, 2)"
    assert Tokenizer(source).get_tokens_as_string() == \
        "IDENTIFIER,foo,LPAREN,(,IDENTIFIER,bar,COMMA,,,INTLIT,2,RPAREN,),EOF"

def test_071_struct_declaration():
    source = "struct Point { int x; }"
    assert Tokenizer(source).get_tokens_as_string() == \
        "STRUCT,struct,IDENTIFIER,Point,LBRACE,{,INT,int,IDENTIFIER,x,SEMI,;,RBRACE,},EOF"

def test_072_comparison_operators():
    source = "< <= > >="
    assert Tokenizer(source).get_tokens_as_string() == \
        "LT,<,LE,<=,GT,>,GE,>=,EOF"

def test_073_float_scientific():
    source = "1.5e-3"
    assert Tokenizer(source).get_tokens_as_string() == \
        "FLOATLIT,1.5e-3,EOF"

def test_074_switch_case_default():
    source = "switch case default break"
    assert Tokenizer(source).get_tokens_as_string() == \
        "SWITCH,switch,CASE,case,DEFAULT,default,BREAK,break,EOF"

def test_075_string_with_tab_escape():
    source = r'"hello\tworld"'
    assert Tokenizer(source).get_tokens_as_string() == \
        r'STRINGLIT,hello\tworld,EOF'

def test_076_member_DOT_chain():
    source = "p.x"
    assert Tokenizer(source).get_tokens_as_string() == \
        "IDENTIFIER,p,DOT,.,IDENTIFIER,x,EOF"

def test_077_assignment_expression():
    source = "x = 5"
    assert Tokenizer(source).get_tokens_as_string() == \
        "IDENTIFIER,x,ASSIGNMENT,=,INTLIT,5,EOF"

def test_078_return_statement():
    source = "return 42"
    assert Tokenizer(source).get_tokens_as_string() == \
        "RETURN,return,INTLIT,42,EOF"

def test_079_while_loop():
    source = "while (i < 10)"
    assert Tokenizer(source).get_tokens_as_string() == \
        "WHILE,while,LPAREN,(,IDENTIFIER,i,LT,<,INTLIT,10,RPAREN,),EOF"

def test_080_for_loop():
    source = "for (i = 0; i < 5; ++i)"
    assert Tokenizer(source).get_tokens_as_string() == \
        "FOR,for,LPAREN,(,IDENTIFIER,i,ASSIGNMENT,=,INTLIT,0,SEMI,;,IDENTIFIER,i,LT,<,INTLIT,5,SEMI,;,INCREMENT,++,IDENTIFIER,i,RPAREN,),EOF"

def test_081_if_else():
    source = "if (x > 0) else"
    assert Tokenizer(source).get_tokens_as_string() == \
        "IF,if,LPAREN,(,IDENTIFIER,x,GT,>,INTLIT,0,RPAREN,),ELSE,else,EOF"

def test_082_only_operator_sequence():
    source = "+++"
    assert Tokenizer(source).get_tokens_as_string() == \
        "INCREMENT,++,ADD,+,EOF"

def test_083_minus_sequence():
    source = "---"
    assert Tokenizer(source).get_tokens_as_string() == \
        "DECREMENT,--,SUB,-,EOF"

def test_084_dot_and_number():
    source = ".1"
    assert Tokenizer(source).get_tokens_as_string() == \
        "FLOATLIT,.1,EOF"

def test_085_number_then_dot():
    source = "1."
    assert Tokenizer(source).get_tokens_as_string() == \
        "FLOATLIT,1.,EOF"

def test_086_only_eof():
    assert Tokenizer("").get_tokens_as_string() == "EOF"

def test_087_multiple_lines():
    source = "int\nx\n=\n10"
    assert Tokenizer(source).get_tokens_as_string() == \
        "INT,int,IDENTIFIER,x,ASSIGNMENT,=,INTLIT,10,EOF"

def test_088_long_input():
    source = "int a; float b; string c;"
    assert Tokenizer(source).get_tokens_as_string() == \
        "INT,int,IDENTIFIER,a,SEMI,;,FLOAT,float,IDENTIFIER,b,SEMI,;,STRING,string,IDENTIFIER,c,SEMI,;,EOF"

def test_089_trailing_comment():
    source = "x /* end */"
    assert Tokenizer(source).get_tokens_as_string() == \
        "IDENTIFIER,x,EOF"

def test_090_leading_whitespace():
    source = "   x"
    assert Tokenizer(source).get_tokens_as_string() == \
        "IDENTIFIER,x,EOF"
def test_091_trailing_whitespace():
    source = "x   "
    assert Tokenizer(source).get_tokens_as_string() == \
        "IDENTIFIER,x,EOF" 
def test_092_between_whitespace():
    source = "x   y"
    assert Tokenizer(source).get_tokens_as_string() == \
        "IDENTIFIER,x,IDENTIFIER,y,EOF" 
def test_093_comment_between():
    source = "x/*c*/y"
    assert Tokenizer(source).get_tokens_as_string() == \
        "IDENTIFIER,x,IDENTIFIER,y,EOF" 
def test_094_equal_vs_assign():
    source = "== ="
    assert Tokenizer(source).get_tokens_as_string() == \
        "EQUAL,==,ASSIGNMENT,=,EOF"

def test_095_less_vs_LE():
    source = "< <="
    assert Tokenizer(source).get_tokens_as_string() == \
        "LT,<,LE,<=,EOF"

def test_096_plus_vs_increment():
    source = "+ ++"
    assert Tokenizer(source).get_tokens_as_string() == \
        "ADD,+,INCREMENT,++,EOF"

def test_097_minus_vs_decrement():
    source = "- --"
    assert Tokenizer(source).get_tokens_as_string() == \
        "SUB,-,DECREMENT,--,EOF"

def test_098_int_then_dot_identifier():
    source = "1.a"
    assert Tokenizer(source).get_tokens_as_string() == \
        "FLOATLIT,1.,IDENTIFIER,a,EOF"

def test_099_dot_identifier():
    source = ".a"
    assert Tokenizer(source).get_tokens_as_string() == \
        "DOT,.,IDENTIFIER,a,EOF"

def test_100_int_exp_only():
    source = "10e2"
    assert Tokenizer(source).get_tokens_as_string() == \
        "FLOATLIT,10e2,EOF"

def test_101_int_then_identifier():
    source = "10abc"
    assert Tokenizer(source).get_tokens_as_string() == \
        "INTLIT,10,IDENTIFIER,abc,EOF"

def test_102_string_with_backslash():
    source = r'"a\\b"'
    assert Tokenizer(source).get_tokens_as_string() == \
        r'STRINGLIT,a\\b,EOF'

def test_103_string_with_multiple_escapes():
    source = r'"a\n\t\b\f\r"'
    assert Tokenizer(source).get_tokens_as_string() == \
        r'STRINGLIT,a\n\t\b\f\r,EOF'

def test_104_string_with_space_and_tab():
    source = '"a b\tc"'
    assert Tokenizer(source).get_tokens_as_string() == \
        "STRINGLIT,a b\tc,EOF"

