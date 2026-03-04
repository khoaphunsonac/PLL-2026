import pytest
from tests.utils import Parser


# =============================
# 001–004 Empty & Basic
# =============================
def test_001(): assert Parser("").parse() == "success"

def test_002(): assert Parser("void main() {}").parse() == "success"

def test_003():
    src = "void f(){} struct A{}; void main(){}"
    assert Parser(src).parse() == "success"

def test_004():
    src = "//c\n/*b*/\nvoid main(){}"
    assert Parser(src).parse() == "success"
# =============================
# 005–009 Struct
# =============================
def test_005(): assert Parser("struct A{}; void main(){}").parse()=="success"

def test_006():
    src="struct B{int x;}; struct A{B b;}; void main(){}"
    assert Parser(src).parse()=="success"

def test_007():
    src="struct A{A a;}; void main(){}"
    assert Parser(src).parse()=="success"

def test_008():
    src="struct A{auto x;}; void main(){}"
    assert Parser(src).parse().startswith("Error")

def test_009():
    src="struct A{int x=1;}; void main(){}"
    assert Parser(src).parse().startswith("Error")
# =============================
# 010–018 Function
# =============================
def test_010(): assert Parser("int f(){return 1;}").parse()=="success"

def test_011(): assert Parser("int f(int a,float b){return 1;}").parse()=="success"

def test_012(): assert Parser("f(){return 1;}").parse()=="success"

def test_013():
    src="struct A{int x;}; A f(){A a; return a;}"
    assert Parser(src).parse()=="success"

def test_014(): assert Parser("auto f(){return 1;}").parse().startswith("Error")

def test_015(): assert Parser("int f(auto a){return 1;}").parse().startswith("Error")

def test_016(): assert Parser("int f(int a,){return 1;}").parse().startswith("Error")

def test_017(): assert Parser("int f();").parse().startswith("Error")

def test_018(): assert Parser("void f(){} void main(){}").parse()=="success"
# =============================
# 019–024 Variables
# =============================
def test_019(): assert Parser("void main(){int x;}").parse()=="success"

def test_020(): assert Parser("void main(){int x=1;}").parse()=="success"

def test_021(): assert Parser("void main(){auto x=1;}").parse()=="success"

def test_022():
    src="struct A{int x;}; void main(){A a={1};}"
    assert Parser(src).parse()=="success"

def test_023():
    src="struct A{int x;}; void main(){A a={{1}};}"
    assert Parser(src).parse()=="success"

def test_024(): assert Parser("int x;").parse().startswith("Error")

# =============================
# 025–030 Expressions — arithmetic
# =============================
def test_025():
    assert Parser("void main(){int x; x = -1;}").parse() == "success"

def test_026():
    assert Parser("void main(){int x; x = + - + 1;}").parse() == "success"

def test_027():
    assert Parser("void main(){int x; x = (1 + 2) * 3;}").parse() == "success"

def test_028():
    assert Parser("void main(){int x; x = 1 + 2 * 3 - 4 / 5 % 6;}").parse() == "success"

def test_029():
    assert Parser("void main(){int x; x = 1 + 2 + 3 + 4 + 5;}").parse() == "success"

def test_030():
    assert Parser("void main(){int x; x = 1 + ;}").parse().startswith("Error")
# =============================
# 031–032 Relational
# =============================
def test_031():
    assert Parser("void main(){int x; x = 1 < 2 > 3 <= 4 >= 5 == 6 != 7;}").parse() == "success"

def test_032():
    assert Parser("void main(){int x; x = 1 < 2 < 3;}").parse() == "success"
# =============================
# 033–037 Logical
# =============================
def test_033():
    assert Parser("void main(){int x; x = 1 && 2;}").parse() == "success"

def test_034():
    assert Parser("void main(){int x; x = 1 || 2;}").parse() == "success"

def test_035():
    assert Parser("void main(){int x; x = !1;}").parse() == "success"

def test_036():
    assert Parser("void main(){int x; x = 1 || 2 && 3;}").parse() == "success"

def test_037():
    assert Parser("void main(){int x; x = (1 < 2) && (3 > 4);}").parse() == "success"
# =============================
# 038 Increment / Decrement
# =============================
def test_038():
    assert Parser("void main(){int x; x++; ++x; x--; --x;}").parse() == "success"
# =============================
# 039–041 Assignment
# =============================
def test_039():
    assert Parser("void main(){int a; int b; a = b = 1;}").parse() == "success"

def test_040():
    assert Parser("void main(){int a; int b; a = (b = 1);}").parse() == "success"

def test_041():
    src = "struct A{int x;}; void main(){A a; a.x = 1;}"
    assert Parser(src).parse() == "success"
# =============================
# 042–046 Member Access
# =============================
def test_042():
    assert Parser("void main(){int x; x = a.b;}").parse() == "success"

def test_043():
    assert Parser("void main(){int x; x = a.b.c;}").parse() == "success"

def test_044():
    assert Parser("void main(){a.b++;}").parse() == "success"

def test_045():
    assert Parser("void main(){int x; x = a.b + 1;}").parse() == "success"

def test_046():
    assert Parser("void main(){int x; x = f().x;}").parse() == "success"
# =============================
# 047–048 Function Calls
# =============================
def test_047():
    assert Parser("void main(){f(); g(1,2,f(3));}").parse() == "success"

def test_048():
    assert Parser("void main(){struct A{int x;}; f({1});}").parse() == "success"
# =============================
# 049–050 Precedence
# =============================
def test_049():
    assert Parser("void main(){int x; x = 1 + 2 * 3 < 4 && 5;}").parse() == "success"

def test_050():
    assert Parser("void main(){int x; x = f(1) + g(2) * h(3);}").parse() == "success"
# =============================
# 051–052 If
# =============================
def test_051():
    assert Parser("void main(){if(1) if(2){} else{} }").parse() == "success"

def test_052():
    assert Parser("void main(){if(1){} else if(2){} else{} }").parse() == "success"
# =============================
# 053 While
# =============================
def test_053():
    assert Parser("void main(){while(1){} while(2){while(3){}}}").parse() == "success"
# =============================
# 054–062 For
# =============================
def test_054():
    assert Parser("void main(){for(int i=0;i<10;i++){} }").parse() == "success"

def test_055():
    assert Parser("void main(){int i; for(i=0;i<10;i++){} }").parse() == "success"

def test_056():
    assert Parser("void main(){for(;i<10;i++){} }").parse() == "success"

def test_057():
    assert Parser("void main(){for(;;){} }").parse() == "success"

def test_058():
    assert Parser("void main(){for(int i=0;;){} }").parse() == "success"

def test_059():
    assert Parser("void main(){for(;i<10;){} }").parse() == "success"

def test_060():
    assert Parser("void main(){for(;;i++){} }").parse() == "success"

def test_061():
    assert Parser("void main(){for(i=0;i<10;i++){} }").parse() == "success"

def test_062():
    assert Parser("void main(){for(3;1;){} }").parse().startswith("Error")
# =============================
# 063–069 Switch
# =============================
def test_063():
    assert Parser("void main(){switch(1){} }").parse() == "success"

def test_064():
    assert Parser("void main(){switch(1){case 1: break;} }").parse() == "success"

def test_065():
    assert Parser("void main(){switch(1){case 1: break; default: break;} }").parse() == "success"

def test_066():
    assert Parser("void main(){switch(1){case 1+2: break;} }").parse() == "success"

def test_067():
    assert Parser("void main(){switch(1){default: break;} }").parse() == "success"

def test_068():
    assert Parser("void main(){switch(1){case 1 break;} }").parse().startswith("Error")

def test_069():
    assert Parser("void main(){switch(1){default: break; default: break;} }").parse().startswith("Error")
# =============================
# 070–071 break/continue/return
# =============================
def test_070():
    assert Parser("void main(){while(1){break; continue;} }").parse() == "success"

def test_071():
    assert Parser("void main(){return; return 1;}").parse() == "success"
# =============================
# 072–073 Blocks
# =============================
def test_072():
    assert Parser("void main(){{{{}}}}").parse() == "success"

def test_073():
    assert Parser("void main(){} {}").parse() == "success"
# =============================
# 074–075 Expression statements
# =============================
def test_074():
    assert Parser("void main(){f();}").parse() == "success"

def test_075():
    assert Parser("void main(){int x; x++;}").parse() == "success"
# =============================
# 076–080 Unsupported / Errors
# =============================
def test_076():
    assert Parser("void main(){;}").parse().startswith("Error")

def test_077():
    assert Parser("void main(){int arr[10];}").parse().startswith("Error")

def test_078():
    assert Parser("void main(){int a,b,c;}").parse().startswith("Error")

def test_079():
    assert Parser("void main(){void x;}").parse().startswith("Error")

def test_080():
    assert Parser("void main(){struct A{int x;};}").parse().startswith("Error")

# =============================
# 081–089 Tricky / Edge cases
# =============================
# 081 Multiple default in switch (reject)
def test_081():
    src = "void main(){switch(1){default: break; default: break;}}"
    assert Parser(src).parse().startswith("Error")


# 082 for(;; missing ) (reject)
def test_082():
    src = "void main(){for(;;{} }"
    assert Parser(src).parse().startswith("Error")


# 083 relational on LHS of assignment (parser may accept)
def test_083():
    src = "void main(){int x; (1<2) = 3;}"
    assert Parser(src).parse() == "success"


# 084 assignment to literal (parser may accept)
def test_084():
    src = "void main(){ 1 = 2; }"
    assert Parser(src).parse() == "success"


# 085 unmatched parentheses (reject)
def test_085():
    src = "void main(){ int x; x = (1 + 2; }"
    assert Parser(src).parse().startswith("Error")


# 086 case with identifier or float (parser may accept)
def test_086():
    src = "void main(){switch(1){case x: break; case 1.5: break;}}"
    assert Parser(src).parse() == "success"


# 087 struct literal on LHS of assignment (parser may accept)
def test_087():
    src = "void main(){ {1} = a; }"
    assert Parser(src).parse() == "success"


# 088 for init with invalid expression e.g. i || 1 (reject)
def test_088():
    src = "void main(){for(i || 1; i<10; i++){} }"
    assert Parser(src).parse().startswith("Error")


# 089 unmatched brace (reject)
def test_089():
    src = "void main(){ if(1) { }"
    assert Parser(src).parse().startswith("Error")
# =============================
# 090–100 Complex Programs & Edge
# =============================
# 090 Structs + functions (createPoint, distance style)
def test_090():
    src = """
    struct Point { int x; int y; };
    Point createPoint(int a, int b){
        Point p = {a,b};
        return p;
    }
    void main(){}
    """
    assert Parser(src).parse() == "success"


# 091 Full program: struct + control flow + switch + member
def test_091():
    src = """
    struct A{int x;};
    void main(){
        A a = {1};
        switch(a.x){
            case 1: break;
            default: break;
        }
    }
    """
    assert Parser(src).parse() == "success"


# 092 Mixed types in one expression
def test_092():
    src = "void main(){int x; x = 1 + 2.0 * 3 < 4 && 5;}"
    assert Parser(src).parse() == "success"


# 093 Chained member and assignment
def test_093():
    src = "void main(){int x; a.b.c = d.e.f = 1;}"
    assert Parser(src).parse() == "success"


# 094 Float literal with member access
def test_094():
    src = "void main(){int x; x = 1.5.x;}"
    assert Parser(src).parse() == "success"


# 095 Nested calls and chained assignment
def test_095():
    src = "void main(){int x; x = f(g(1),h(2)) = 3;}"
    assert Parser(src).parse() == "success"


# 096 Nested struct literals as statement
def test_096():
    src = "void main(){ {{1,2},{3,4}}; }"
    assert Parser(src).parse() == "success"


# 097 Postfix on string literal
def test_097():
    src = 'void main(){ "abc"++; }'
    assert Parser(src).parse() == "success"


# 098 Prefix/postfix on function call
def test_098():
    src = "void main(){ ++f(); g()++; }"
    assert Parser(src).parse() == "success"


# 099 return f();;
def test_099():
    src = "void main(){ return f();; }"
    assert Parser(src).parse().startswith("Error")


# 100 Struct literal in comparison
def test_100():
    src = """
    struct A{int x;};
    void main(){
        if({1} == {2}){}
    }
    """
    assert Parser(src).parse() == "success"