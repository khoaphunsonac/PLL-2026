import pytest
from tests.utils import Tokenizer

# ----------------------------------------------------
# 001: Keywords
# ----------------------------------------------------
def test_001():
    source = "auto break case continue default else float for if int return string struct switch void while"
    expected = "auto,break,case,continue,default,else,float,for,if,int,return,string,struct,switch,void,while,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

# ----------------------------------------------------
# 002: Operators and separators
# ----------------------------------------------------
def test_002():
    source = "+ - * / % == != < > <= >= || && ! ++ -- = . { } ( ) ; , :"
    expected = "+,-,*,/,%,==,!=,<,>,<=,>=,||,&&,!,++,--,=,.,{,},(,),;,,,:,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

# ----------------------------------------------------
# 003-009: Identifiers
# ----------------------------------------------------
def test_003():
    source = "a a1 abc123"
    expected = "a,a1,abc123,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_004():
    source = "_a _123 _abc"
    expected = "_a,_123,_abc,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_005():
    source = "_ __ ___"
    expected = "_,__,___,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_006():
    source = "A ABC HCMUT"
    expected = "A,ABC,HCMUT,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_007():
    source = "aBc AbC"
    expected = "aBc,AbC,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_008():
    source = "a__b c___d"
    expected = "a__b,c___d,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_009():
    source = "If ELSE For While"
    expected = "If,ELSE,For,While,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

# ----------------------------------------------------
# 010-015: Integer literals
# ----------------------------------------------------
def test_010():
    source = "0 5 9"
    expected = "0,5,9,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_011():
    source = "10 255 9999"
    expected = "10,255,9999,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_012():
    source = "00 0123 005"
    expected = "00,0123,005,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_013():
    source = "-1 -0 -99"
    expected = "-,1,-,0,-,99,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_014():
    source = "+1 +0"
    expected = "+,1,+,0,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_015():
    source = "5+10 3*2"
    expected = "5,+,10,3,*,2,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

# ----------------------------------------------------
# 016-033: Float literals
# ----------------------------------------------------
def test_016():
    source = "3.14 0.0"
    expected = "3.14,0.0,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_017():
    source = "1. 99."
    expected = "1.,99.,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_018():
    source = ".5 .001"
    expected = ".5,.001,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_019():
    source = "1e4 1E4"
    expected = "1e4,1E4,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_020():
    source = "1.23e4 3.14E5"
    expected = "1.23e4,3.14E5,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_021():
    source = "5.67e-2 9.1E-5"
    expected = "5.67e-2,9.1E-5,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_022():
    source = "1e+5 .2E+3"
    expected = "1e+5,.2E+3,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_023():
    source = "1.e+5 0.e-2"
    expected = "1.e+5,0.e-2,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_024():
    source = "0e0 1.E-0"
    expected = "0e0,1.E-0,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_025():
    source = "1e"
    expected = "1,e,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_026():
    source = "1.2E"
    expected = "1.2,E,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_027():
    source = ".5e+"
    expected = ".5,e,+,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_028():
    source = "1.2.3"
    expected = "1.2,.3,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_029():
    source = "..5"
    expected = ".,.5,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_030():
    source = "-1.23 -5e-2"
    expected = "-,1.23,-,5e-2,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_031():
    source = "+3.14 +.5"
    expected = "+,3.14,+,.5,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_032():
    source = "001.23 00.5"
    expected = "001.23,00.5,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_033():
    source = "0.00e00"
    expected = "0.00e00,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

# ----------------------------------------------------
# 034-044: String literals
# ----------------------------------------------------
def test_034():
    source = '""'
    expected = ",<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_035():
    source = '"a b c"'
    expected = "a b c,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_036():
    source = '"a\\tb"'
    expected = 'a\\tb,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_037():
    source = '"a\\nb"'
    expected = 'a\\nb,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_038():
    source = '"a\\"b"'
    expected = 'a\\"b,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_039():
    source = '"a\\\\b"'
    expected = 'a\\\\b,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_040():
    source = '"\\b\\f\\r"'
    expected = '\\b\\f\\r,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_041():
    source = '"123"'
    expected = "123,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_042():
    source = '"!@#$%^&*()"'
    expected = "!@#$%^&*(),<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_043():
    source = '"Hello\\nWorld\\t!"'
    expected = 'Hello\\nWorld\\t!,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_044():
    source = '" "'
    expected = ' ,<EOF>'
    assert Tokenizer(source).get_tokens_as_string() == expected

# ----------------------------------------------------
# 045-052: Comments
# ----------------------------------------------------
def test_045():
    source = "// this is a comment"
    expected = "<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_046():
    source = "/* comment */"
    expected = "<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_047():
    source = "/* multi\nline */"
    expected = "<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_048():
    source = "1 /* comment */ 2"
    expected = "1,2,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_049():
    source = "/* // inside */"
    expected = "<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_050():
    source = "// /* inside"
    expected = "<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_051():
    source = "/* /* x */ */"
    expected = "*,/,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_052():
    source = "// comment\nint x"
    expected = "int,x,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

# ----------------------------------------------------
# 053: Whitespace
# ----------------------------------------------------
def test_053():
    source = " \t\n\r\f"
    expected = "<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

# ----------------------------------------------------
# 054-059: Illegal escape in string
# ----------------------------------------------------
def test_054():
    source = '"\\x"'
    expected = "Illegal Escape In String: \\x"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_055():
    source = '"\\a"'
    expected = "Illegal Escape In String: \\a"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_056():
    source = '"\\q"'
    expected = "Illegal Escape In String: \\q"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_057():
    source = '"\\\'"'
    expected = "Illegal Escape In String: \\'"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_058():
    source = '"abc\\kdef"'
    expected = "Illegal Escape In String: abc\\k"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_059():
    source = '"\\p\\q"'
    expected = "Illegal Escape In String: \\p"
    assert Tokenizer(source).get_tokens_as_string() == expected

# ----------------------------------------------------
# 060-069: Unclosed string
# ----------------------------------------------------
def test_060():
    source = '"abc'
    expected = "Unclosed String: abc"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_061():
    source = '"abc\n"'
    expected = "Unclosed String: abc"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_062():
    source = '"abc\r"'
    expected = "Unclosed String: abc"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_063():
    source = '"'
    expected = "Unclosed String: "
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_064():
    source = '"abc\\"'
    expected = 'Unclosed String: abc\\"'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_065():
    source = '"this is a very long unclosed string'
    expected = "Unclosed String: this is a very long unclosed string"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_066():
    source = '"abc\\x\n'
    expected = "Illegal Escape In String: abc\\x"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_067():
    source = '"abc\n def"'
    expected = "Unclosed String: abc"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_068():
    source = '"a\r\n"'
    expected = "Unclosed String: a"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_069():
    source = '"abc" "def'
    expected = "abc,Unclosed String: def"
    assert Tokenizer(source).get_tokens_as_string() == expected

# ----------------------------------------------------
# 070-077: Error token
# ----------------------------------------------------
def test_070():
    source = "$"
    expected = "Error Token $"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_071():
    source = "@"
    expected = "Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_072():
    source = "#"
    expected = "Error Token #"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_073():
    source = "&"
    expected = "Error Token &"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_074():
    source = "|"
    expected = "Error Token |"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_075():
    source = "["
    expected = "Error Token ["
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_076():
    source = "int @"
    expected = "int,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_077():
    source = "@#$"
    expected = "Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected

# ----------------------------------------------------
# 078-083: Operator disambiguation
# ----------------------------------------------------
def test_078():
    source = "==="
    expected = "==,=,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_079():
    source = "a+++b"
    expected = "a,++,+,b,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_080():
    source = "a-->b"
    expected = "a,--,>,b,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_081():
    source = "=+==++"
    expected = "=,+,==,++,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_082():
    source = "<<"
    expected = "<,<,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_083():
    source = ">>"
    expected = ">,>,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

# ----------------------------------------------------
# 084-087: Edge cases
# ----------------------------------------------------
def test_084():
    source = "intx"
    expected = "intx,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_085():
    source = "123abc"
    expected = "123,abc,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_086():
    source = "a.b 1.23 .5 a."
    expected = "a,.,b,1.23,.5,a,.,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_087():
    source = '"// not comment /* neither */"'
    expected = "// not comment /* neither */,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

# ----------------------------------------------------
# 088-091: C/C++ not in TyC
# ----------------------------------------------------
def test_088():
    source = "+="
    expected = "+,=,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_089():
    source = "->"
    expected = "-,>,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_090():
    source = "::"
    expected = ":,:,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_091():
    source = "..."
    expected = ".,.,.,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

# ----------------------------------------------------
# 092-100: Complex / real code
# ----------------------------------------------------
def test_092():
    source = "auto x = 5;"
    expected = "auto,x,=,5,;,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_093():
    source = "int main() {}"
    expected = "int,main,(,),{,},<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_094():
    source = "struct Point { int x; };"
    expected = "struct,Point,{,int,x,;,},;,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_095():
    source = "if (x == 1) x++; else x--;"
    expected = "if,(,x,==,1,),x,++,;,else,x,--,;,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_096():
    source = "for (auto i = 0; i < 10; ++i) {}"
    expected = "for,(,auto,i,=,0,;,i,<,10,;,++,i,),{,},<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_097():
    source = "switch (x) { case 1: break; default: }"
    expected = "switch,(,x,),{,case,1,:,break,;,default,:,},<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_098():
    source = "p1.x = p2.y + 1;"
    expected = "p1,.,x,=,p2,.,y,+,1,;,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_099():
    source = "int a, b; float c;"
    expected = "int,a,,,b,;,float,c,;,<EOF>"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_100():
    source = "void main() { int a = 10; @ }"
    expected = "void,main,(,),{,int,a,=,10,;,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected