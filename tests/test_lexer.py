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
