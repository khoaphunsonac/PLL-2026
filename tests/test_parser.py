import pytest
from tests.utils import Parser


def test_01():
    assert Parser("").parse() == "success"

def test_02():
    assert Parser("void main() {}").parse() == "success"

def test_03():
    source = """
    void f() {}
    void g() {}
    void main() {}
    """
    assert Parser(source).parse() == "success"

def test_04():
    source = "void main() {}"
    Parser(source).parse() == "success"

def test_05():
    source = "void main( {}"
    assert Parser(source).parse().startswith("Error")

def test_06():
    source = "void main) {}"
    assert Parser(source).parse().startswith("Error")

def test_07():
    source = "void main() {"
    assert Parser(source).parse().startswith("Error")

def test_08():
    source = "void main() }"
    assert Parser(source).parse().startswith("Error")

def test_09():
    source = "void main();"
    assert Parser(source).parse().startswith("Error")

def test_10():
    source = "main() {}"
    assert Parser(source).parse() == "success"

def test_11():
    source = """
    void main() {
        int x;
        float y;
        string s;
    }
    """
    assert Parser(source).parse() == "success"

def test_12():
    source = """
    void main() {
        int x = 10;
        float y = 3.14;
        string s = "hi";
    }
    """
    assert Parser(source).parse() == "success"

def test_13():
    source = """
    void main() {
        auto x = 10;
        auto y = 3.14;
        auto s = "hi";
    }
    """
    assert Parser(source).parse() == "success"

def test_14():
    source = """
    void main() {
        auto x;
    }
    """
    assert Parser(source).parse() == "success"

def test_15():
    source = """
    void main() {
        int x = ;
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_16():
    source = """
    void main() {
        auto = 10;
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_17():
    source = """
    void main() {
        int;
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_18():
    source = """
    void main() {
        string "abc";
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_19():
    source = """
    void main() {
        int x y;
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_20():
    source = """
    void main() {
        float = 1.2;
    }
    """
    assert Parser(source).parse().startswith("Error")



def test_21():
    source = """
    void main() {
        int x;
        x = 1 + 2 * 3;
    }
    """
    assert Parser(source).parse() == "success"

def test_22():
    source = """
    void main() {
        int x;
        x = (1 + 2) * 3;
    }
    """
    assert Parser(source).parse() == "success"

def test_23():
    source = """
    void main() {
        float y;
        y = 1.0 + 2 / 3 * 4;
    }
    """
    assert Parser(source).parse() == "success"

def test_24():
    source = """
    void main() {
        int x;
        x = -1 + +2;
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_25():
    source = """
    void main() {
        int x;
        x = 1 + ;
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_26():
    source = """
    void main() {
        int x;
        x = * 3;
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_27():
    source = """
    void main() {
        int x;
        x = (1 + 2;
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_28():
    source = """
    void main() {
        int x;
        x = 1 2;
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_29():
    source = """
    void main() {
        int x;
        x = 10;
    }
    """
    assert Parser(source).parse() == "success"

def test_30():
    source = """
    void main() {
        int x;
        x = ;
    }
    """
    assert Parser(source).parse().startswith("Error")



def test_31():
    source = """
    void main() {
        if (1) {}
    }
    """
    assert Parser(source).parse() == "success"

def test_32():
    source = """
    void main() {
        if (1) {} else {}
    }
    """
    assert Parser(source).parse() == "success"

def test_33():
    source = """
    void main() {
        while (1) {}
    }
    """
    assert Parser(source).parse() == "success"

def test_34():
    source = """
    void main() {
        for (int i = 0; i < 10; i = i + 1) {}
    }
    """
    assert Parser(source).parse() == "success"

def test_35():
    source = """
    void main() {
        for (;;) {}
    }
    """
    assert Parser(source).parse() == "success"

def test_36():
    source = """
    void main() {
        if () {}
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_37():
    source = """
    void main() {
        while () {}
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_38():
    source = """
    void main() {
        for (int i = 0 i < 10; i = i + 1) {}
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_39():
    source = """
    void main() {
        else {}
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_40():
    source = """
    void main() {
        if 1 {}
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_41():
    source = """
    void main() {
        for (int i = 0; i < 10 i = i + 1) {}
    }
    """
    assert Parser(source).parse().startswith("Error")
def test_42():
    source = """
    void main() {
        return;
    }
    """
    assert Parser(source).parse() == "success"
def test_43():
    source = """
    void main() {
        return 1;
    }
    """
    assert Parser(source).parse() == "success"
def test_44():
    source = """
    void main() {
        return ;
    }
    """
    assert Parser(source).parse() == "success"
def test_45():
    source = """
    void main() {
        return 1 + 2 * 3;
    }
    """
    assert Parser(source).parse() == "success"      
def test_46():
    source = """
    void main() {
        return 1 + ;
    }
    """
    assert Parser(source).parse().startswith("Error")
def test_47():
    source = """
    void main() {
        return * 3;
    }
    """
    assert Parser(source).parse().startswith("Error")
def test_48():
    source = """
    void main() {
        return (1 + 2;
    }
    """
    assert Parser(source).parse().startswith("Error")
def test_49():
    source = """
    void main() {
        return 1 2;
    }
    """
    assert Parser(source).parse().startswith("Error")
def test_50():
    source = """
    void main() {
        return 10;
    }
    """
    assert Parser(source).parse() == "success"
def test_51():
    source = """
    void main() {
        return ;
    }
    """
    assert Parser(source).parse() == "success"
def test_52():
    source = """
    void main() {
        return
    }
    """
    assert Parser(source).parse().startswith("Error")
def test_53():
    source = """
    void main() {
        switch (1) {
            case 1:
                break;
            default:
                break;
        }
    }
    """
    assert Parser(source).parse() == "success"
def test_54():
    source = """
    void main() {
        switch (1) {
            case 1:
                printInt(0);
        }
    }
    """
    assert Parser(source).parse() == "success"


def test_55():
    source = """
    void main() {
        switch (1) {
            case 1:
                break;
        }
    }
    """
    assert Parser(source).parse() == "success"

def test_56():
    source = """
    void main() {
        switch (1) {}
    }
    """
    assert Parser(source).parse() == "success"

def test_57():
    source = """
    void main() {
        switch (1) {
            case 1:
                break;
            default:
                break;
        }
    }
    """
    assert Parser(source).parse() == "success"

def test_58():
    source = """
    void main() {
        switch (1) {
            case 1+2:
                break;
            case (3*4):
                break;
        }
    }
    """
    assert Parser(source).parse() == "success"

def test_59():
    source = """
    void main() {
        switch (1) {
            default:
                break;
        }
    }
    """
    assert Parser(source).parse() == "success"

def test_60():
    source = """
    void main() {
        switch (1) {
            case :
                break;
        }
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_61():
    source = """
    void main() {
        switch (1) {
            case 1
                break;
        }
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_62():
    source = """
    void main() {
        switch 1 {
            case 1:
                break;
        }
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_63():
    source = """
    void main() {
        switch (1) {
            case 1:
        }
    }
    """
    assert Parser(source).parse() == "success"

def test_64():
    source = """
    void main() {
        switch (1) {
            case 1:
                case 2:
                    break;
        }
    }
    """
    assert Parser(source).parse() == "success"

def test_65():
    source = """
    void main() {
        switch (1) {
            default:
            default:
                break;
        }
    }
    """
    assert Parser(source).parse() == "success"

def test_66():
    source = """
    void main() {
        switch (1) {
            case 1:
                break;
            default:
                break;
        }
    }
    """
    assert Parser(source).parse() == "success"

def test_67():
    source = """
    void main() {
        switch (1) {
            case 1:
                break;
            default:
                break;
            case 2:
                break;
        }   
    }
    """
    assert Parser(source).parse() == "success"

def test_68():
    source = """
    void main() {
        switch (1) {
            case 1:
                break;
            case 2:
                break;
            default:
                break;
        }   
    }
    """
    assert Parser(source).parse() == "success"
def test_69():
    source = """
    void main() {
        struct A {
            int x;
        };
    }
    """
    assert Parser(source).parse().startswith("Error")
def test_70():
    source = """
    struct A {
        int x;
        float y;
        string s;
    };
    void main() {}
    """
    assert Parser(source).parse() == "success"
def test_71():
    source = """
    struct A {
        int x;
        float y;
        string s;
    };
    void main() {
        A a;
        a.x = 10;
        a.y = 3.14;
        a.s = "hi";
    }
    """
    assert Parser(source).parse() == "success"
def test_72():
    source = """
    struct A {
        int x;
        float y;
        string s;
    };
    void main() {
        A a = {10, 3.14, "hi"};
    }
    """
    assert Parser(source).parse() == "success"
def test_73():
    source = """
    struct A {
        int x;
        float y;
        string s;
    };
    void main() {
        A a = {10, 3.14};
    }
    """
    assert Parser(source).parse() == "success"
def test_74():
    source = """
    struct C {
        int v;
    };

    void main() {
        C c = {0};
        for (int i = 0; i < 3; i = i + 1) {
            c.v = i;
        }
    }

    """
    assert Parser(source).parse() == "success"

def test_75():
    source = """
    void main() {
        switch (1 * 3 / 4) {
            case (1 + 2) * 3:
                printInt(0);
                break;
            default:
                printInt(1);
        }
    }

    """
    assert Parser(source).parse() == "success"
    
def test_76():
    source = """
    struct Point {
        int x;
        int y;
    };
    void main() {}
    """
    assert Parser(source).parse() == "success"

def test_77():
    source = """
    struct A {
    int x;
};

struct B {
    float y;
};

void main() {
    A a = {10};
    auto c = a;
    printInt(c.x);
}

    """
    assert Parser(source).parse() == "success"

def test_78():
    source = """
    struct Point {
    int x;
    int y;
};

void main() {
    Point a = {1, 2};
    Point b;
    b = a;
    printInt(b.y);
}

    """
    assert Parser(source).parse() == "success"

def test_79():
    source = """
    void main() {
        return;
    }
    """
    assert Parser(source).parse() == "success"

def test_80():
    source = """
    int f() {
        return 1;
    }
    """
    assert Parser(source).parse() == "success"

def test_81():
    source = """
    void main() {
        return 1;
    }
    """
    assert Parser(source).parse() == "success"

def test_82():
    source = """
    int f() {
        return;
    }
    """
    assert Parser(source).parse() == "success"

def test_83():
    source = """
    void main() {
        break;
    }
    """
    assert Parser(source).parse() == "success"

def test_84():
    source = """
    void main() {
        continue;
    }
    """
    assert Parser(source).parse() == "success"

def test_85():
    source = """
    void main() {
        return
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_86():
    source = """
    void main() {
        break
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_87():
    source = """
    void main() {
        continue
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_88():
    source = """
    struct A {
        int x;
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_89():
    source = """
    struct {
        int x;
    };
    """
    assert Parser(source).parse().startswith("Error")

def test_90():
    source = """
    void main() {
        struct A {
            int x;
        };
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_91():
    source = """
    struct Point {
    int x;
    int y;
};

void main() {
    Point p;
    p.x = 1;
    p.y = 2;
    printInt(p.x);
}

    """
    assert Parser(source).parse() == "success"

def test_92():
    source = """
    void main() {
        printInt(1);
        printFloat(1.2);
        printString("a");
    }
    """
    assert Parser(source).parse() == "success"

def test_93():
    source = """
    void main() {
        printInt();
    }
    """
    assert Parser(source).parse() == "success"

def test_94():
    source = """
    void main() {
        readInt(1);
    }
    """
    assert Parser(source).parse() == "success"

def test_95():
    source = """
    void main() {
        foo(1,2);
    }
    """
    assert Parser(source).parse() == "success"

def test_96():
    source = """
    void main() {
        foo(1,);
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_97():
    source = """
    void main() {
        foo();
    }
    """
    assert Parser(source).parse() == "success"

def test_98():
    source = """
    void main() {
        ;
    }
    """
    assert Parser(source).parse().startswith("Error")

def test_99():
    source = """
    void main() {
    switch (1 * 3 / 4) {
        case (1 + 2) * 3:
            printInt(0);
            break;
        default:
            printInt(1);
        }
    }
    """
    assert Parser(source).parse() == "success"

def test_100():
    source = """
    void main() {
        ,;
    }
    """
    assert Parser(source).parse().startswith("Error")
