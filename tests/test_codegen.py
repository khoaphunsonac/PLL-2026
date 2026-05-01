"""
Test cases for TyC code generation.
"""

from src.utils.nodes import *
from tests.utils import CodeGenerator


def test_001():
    """Test 1: Hello World - print string"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("Hello World")]))
            ])
        )
    ])
    expected = "Hello World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_002():
    """Test 2: Print integer"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [IntLiteral(42)]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_003():
    """Test 3: Print float"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printFloat", [FloatLiteral(3.14)]))
            ])
        )
    ])
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_004():
    """Test 4: Variable declaration and assignment"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_005():
    """Test 5: Binary operation - addition"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(IntLiteral(5), "+", IntLiteral(3))
                ]))
            ])
        )
    ])
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_006():
    """Test 6: Binary operation - multiplication"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(IntLiteral(6), "*", IntLiteral(7))
                ]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_007():
    """Test 7: If statement"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(1), "<", IntLiteral(2)),
                    ExprStmt(FuncCall("printString", [StringLiteral("yes")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("no")]))
                )
            ])
        )
    ])
    expected = "yes"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_008():
    """Test 8: While loop"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(AssignExpr(
                            Identifier("i"),
                            BinaryOp(Identifier("i"), "+", IntLiteral(1))
                        ))
                    ])
                )
            ])
        )
    ])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_009():
    """Test 9: Function call with return value"""
    ast = Program([
        FuncDecl(
            IntType(),
            "add",
            [Param(IntType(), "a"), Param(IntType(), "b")],
            BlockStmt([
                ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    FuncCall("add", [IntLiteral(20), IntLiteral(22)])
                ]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_010():
    """Test 10: Multiple statements - arithmetic operations"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                VarDecl(IntType(), "y", IntLiteral(20)),
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(Identifier("x"), "+", Identifier("y"))
                ]))
            ])
        )
    ])
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_011():
    """Test 11: Modulo operation"""
    # % operates on int only and returns int[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(IntLiteral(10), "%", IntLiteral(3))
                ]))
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_012():
    """Test 12: Logical AND with Short-circuit evaluation"""
    # If LHS is false (0), RHS should not be evaluated[cite: 3]
    ast = Program([
        FuncDecl(
            IntType(),
            "side_effect",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("evaluated")])),
                ReturnStmt(IntLiteral(1))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(0), "&&", FuncCall("side_effect", [])),
                    ExprStmt(FuncCall("printString", [StringLiteral("true")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("false")]))
                )
            ])
        )
    ])
    expected = "false" # "evaluated" should not be printed due to short-circuit[cite: 3]
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_013():
    """Test 13: Logical OR with Short-circuit evaluation"""
    ast = Program([
        FuncDecl(
            IntType(),
            "side_effect",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("evaluated")])),
                ReturnStmt(IntLiteral(1))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(1), "||", FuncCall("side_effect", [])),
                    ExprStmt(FuncCall("printString", [StringLiteral("true")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("false")]))
                )
            ])
        )
    ])
    expected = "true" # "evaluated" should not be printed
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_014():
    """Test 14: Unary operators (! and -)"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", PrefixOp("-", IntLiteral(5))),
                VarDecl(IntType(), "y", PrefixOp("!", IntLiteral(0))),
                ExprStmt(FuncCall("printInt", [Identifier("x")])),
                ExprStmt(FuncCall("printInt", [Identifier("y")]))
            ])
        )
    ])
    expected = "-51"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_015():
    """Test 15: For loop basic execution"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(0)),
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")]))
                    ])
                )
            ])
        )
    ])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_016():
    """Test 16: Switch-case basic with break"""
    # switch statements follow C-style fall-through behavior[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "day", IntLiteral(2)),
                SwitchStmt(
                    Identifier("day"),
                    [
                        CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printInt", [IntLiteral(10)])), BreakStmt()]),
                        CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printInt", [IntLiteral(20)])), BreakStmt()]),
                    ],
                    DefaultStmt([ExprStmt(FuncCall("printInt", [IntLiteral(0)])), BreakStmt()])
                )
            ])
        )
    ])
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_017():
    """Test 17: Switch-case with fall-through behavior"""
    # Execution will fall through to subsequent cases unless terminated with a break[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(1)),
                SwitchStmt(
                    Identifier("x"),
                    [
                        CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printInt", [IntLiteral(1)]) )]), # No break
                        CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printInt", [IntLiteral(2)]) ), BreakStmt()]),
                    ],
                    None
                )
            ])
        )
    ])
    expected = "12"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_018():
    """Test 18: Recursion (Factorial)"""
    ast = Program([
        FuncDecl(
            IntType(),
            "factorial",
            [Param(IntType(), "n")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("n"), "<=", IntLiteral(1)),
                    ReturnStmt(IntLiteral(1)),
                    ReturnStmt(BinaryOp(Identifier("n"), "*", FuncCall("factorial", [BinaryOp(Identifier("n"), "-", IntLiteral(1))])))
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("factorial", [IntLiteral(5)])]))
            ])
        )
    ])
    expected = "120"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_019():
    """Test 19: Struct creation and member access"""
    # Struct members are accessed using the dot (.) operator[cite: 3]
    ast = Program([
        StructDecl("Point", [
            VarDecl(IntType(), "x", None),
            VarDecl(IntType(), "y", None)
        ]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Point"), "p", StructLiteral([IntLiteral(10), IntLiteral(20)])),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p"), "x")])),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p"), "y")]))
            ])
        )
    ])
    expected = "1020"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_020():
    """Test 20: Struct Assignment"""
    # Assignment copies all member values[cite: 3]
    ast = Program([
        StructDecl("Point", [
            VarDecl(IntType(), "x", None),
            VarDecl(IntType(), "y", None)
        ]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Point"), "p1", StructLiteral([IntLiteral(5), IntLiteral(15)])),
                VarDecl(StructType("Point"), "p2", None),
                ExprStmt(AssignExpr(Identifier("p2"), Identifier("p1"))),
                ExprStmt(AssignExpr(MemberAccess(Identifier("p2"), "x"), IntLiteral(99))),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p1"), "x")])), # p1.x should remain 5
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p2"), "x")]))  # p2.x should be 99
            ])
        )
    ])
    expected = "599"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_021():
    """Test 21: Break statement in while loop"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(5)),
                    BlockStmt([
                        IfStmt(
                            BinaryOp(Identifier("i"), "==", IntLiteral(2)),
                            BreakStmt(),
                            None
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                    ])
                )
            ])
        )
    ])
    expected = "01"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_022():
    """Test 22: Continue statement in for loop"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(0)),
                    BinaryOp(Identifier("i"), "<", IntLiteral(4)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        IfStmt(
                            BinaryOp(Identifier("i"), "==", IntLiteral(2)),
                            ContinueStmt(),
                            None
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("i")]))
                    ])
                )
            ])
        )
    ])
    expected = "013"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_023():
    """Test 23: Chained Assignment"""
    # Assignment expression is right-associative[cite: 3, 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", None),
                VarDecl(IntType(), "y", None),
                VarDecl(IntType(), "z", None),
                ExprStmt(AssignExpr(Identifier("x"), AssignExpr(Identifier("y"), AssignExpr(Identifier("z"), IntLiteral(7))))),
                ExprStmt(FuncCall("printInt", [Identifier("x")])),
                ExprStmt(FuncCall("printInt", [Identifier("y")])),
                ExprStmt(FuncCall("printInt", [Identifier("z")]))
            ])
        )
    ])
    expected = "777"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_024():
    """Test 24: Postfix Increment"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(5)),
                VarDecl(IntType(), "y", PostfixOp("++", Identifier("x"))),
                ExprStmt(FuncCall("printInt", [Identifier("y")])), # y gets original value (5)
                ExprStmt(FuncCall("printInt", [Identifier("x")]))  # x is incremented (6)
            ])
        )
    ])
    expected = "56"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_025():
    """Test 25: Local scope shadowing"""
    # Variables in nested blocks shadow variables with the same name in outer scopes[cite: 3, 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                BlockStmt([
                    VarDecl(IntType(), "x", IntLiteral(20)),
                    ExprStmt(FuncCall("printInt", [Identifier("x")]))
                ]),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "2010"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_026():
    """Test 26: Float arithmetic operations"""
    # Các phép toán số học hỗ trợ float và trả về float[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printFloat", [
                    BinaryOp(FloatLiteral(5.5), "-", FloatLiteral(2.25))
                ]))
            ])
        )
    ])
    expected = "3.25"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_027():
    """Test 27: Float relational operations"""
    # Các phép so sánh số thực luôn trả về kiểu int (0 hoặc 1)[cite: 3, 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(FloatLiteral(3.14), ">=", FloatLiteral(3.0))
                ]))
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_028():
    """Test 28: Prefix Increment as expression"""
    # Prefix increment (++) hoạt động trên kiểu int và trả về giá trị sau khi tăng[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(5)),
                VarDecl(IntType(), "y", PrefixOp("++", Identifier("x"))),
                ExprStmt(FuncCall("printInt", [Identifier("y")])),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "66"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_029():
    """Test 29: Prefix Decrement as expression"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                VarDecl(IntType(), "y", PrefixOp("--", Identifier("x"))),
                ExprStmt(FuncCall("printInt", [Identifier("y")])),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_030():
    """Test 30: Nested If-Else statements"""
    # Else luôn gắn với If gần nhất (innermost)[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(1), "==", IntLiteral(1)),
                    IfStmt(
                        BinaryOp(IntLiteral(2), "<", IntLiteral(1)),
                        ExprStmt(FuncCall("printInt", [IntLiteral(1)])),
                        ExprStmt(FuncCall("printInt", [IntLiteral(2)])) # Else này thuộc về If bên trong
                    ),
                    ExprStmt(FuncCall("printInt", [IntLiteral(3)]))
                )
            ])
        )
    ])
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_031():
    """Test 31: Nested While loops"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                VarDecl(IntType(), "count", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(2)),
                    BlockStmt([
                        VarDecl(IntType(), "j", IntLiteral(0)),
                        WhileStmt(
                            BinaryOp(Identifier("j"), "<", IntLiteral(3)),
                            BlockStmt([
                                ExprStmt(AssignExpr(Identifier("count"), BinaryOp(Identifier("count"), "+", IntLiteral(1)))),
                                ExprStmt(AssignExpr(Identifier("j"), BinaryOp(Identifier("j"), "+", IntLiteral(1))))
                            ])
                        ),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                    ])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("count")]))
            ])
        )
    ])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_032():
    """Test 32: Break in nested loop"""
    # Break chỉ thoát khỏi vòng lặp gần nhất (inner loop)[cite: 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                VarDecl(IntType(), "count", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(2)),
                    BlockStmt([
                        VarDecl(IntType(), "j", IntLiteral(0)),
                        WhileStmt(
                            BinaryOp(Identifier("j"), "<", IntLiteral(3)),
                            BlockStmt([
                                IfStmt(
                                    BinaryOp(Identifier("j"), "==", IntLiteral(1)),
                                    BreakStmt(),
                                    None
                                ),
                                ExprStmt(AssignExpr(Identifier("count"), BinaryOp(Identifier("count"), "+", IntLiteral(1)))),
                                ExprStmt(AssignExpr(Identifier("j"), BinaryOp(Identifier("j"), "+", IntLiteral(1))))
                            ])
                        ),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                    ])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("count")]))
            ])
        )
    ])
    expected = "2" # Inner loop chạy 1 lần (j=0) trước khi break, outer chạy 2 lần -> 1 * 2 = 2
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_033():
    """Test 33: Void function with early return"""
    # Hàm void sử dụng return;[cite: 3, 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "early_return",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [IntLiteral(1)])),
                ReturnStmt(None),
                ExprStmt(FuncCall("printInt", [IntLiteral(2)])) # Code này không bao giờ được chạy
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("early_return", []))
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_034():
    """Test 34: Function with multiple parameters"""
    ast = Program([
        FuncDecl(
            IntType(),
            "sum3",
            [Param(IntType(), "a"), Param(IntType(), "b"), Param(IntType(), "c")],
            BlockStmt([
                ReturnStmt(BinaryOp(Identifier("a"), "+", BinaryOp(Identifier("b"), "+", Identifier("c"))))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("sum3", [IntLiteral(10), IntLiteral(20), IntLiteral(30)])]))
            ])
        )
    ])
    expected = "60"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_035():
    """Test 35: Switch statement with only default"""
    # Default có thể đứng một mình hoặc đứng bất kỳ đâu nhưng chỉ có tối đa 1[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(99)),
                SwitchStmt(
                    Identifier("x"),
                    [],
                    DefaultStmt([ExprStmt(FuncCall("printInt", [IntLiteral(0)])), BreakStmt()])
                )
            ])
        )
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_036():
    """Test 36: Logical NOT operator"""
    # ! operand trả về int (đảo ngược logic)[cite: 3, 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "flag", IntLiteral(0)),
                IfStmt(
                    PrefixOp("!", Identifier("flag")),
                    ExprStmt(FuncCall("printInt", [IntLiteral(1)])),
                    ExprStmt(FuncCall("printInt", [IntLiteral(0)]))
                )
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_037():
    """Test 37: Chained Assignment in Expression context"""
    # Phép gán trong ngữ cảnh biểu thức trả về giá trị sau khi gán[cite: 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", None),
                VarDecl(IntType(), "y", None),
                ExprStmt(AssignExpr(
                    Identifier("y"), 
                    BinaryOp(AssignExpr(Identifier("x"), IntLiteral(5)), "+", IntLiteral(10))
                )),
                ExprStmt(FuncCall("printInt", [Identifier("y")])),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "155" # y = 15, x = 5
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_038():
    """Test 38: Struct member chained assignment"""
    ast = Program([
        StructDecl("Point", [
            VarDecl(IntType(), "x", None),
            VarDecl(IntType(), "y", None)
        ]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Point"), "p1", StructLiteral([IntLiteral(0), IntLiteral(0)])),
                VarDecl(StructType("Point"), "p2", StructLiteral([IntLiteral(0), IntLiteral(0)])),
                ExprStmt(AssignExpr(
                    MemberAccess(Identifier("p1"), "x"), 
                    AssignExpr(MemberAccess(Identifier("p2"), "x"), IntLiteral(42))
                )),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p1"), "x")])),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p2"), "x")]))
            ])
        )
    ])
    expected = "4242"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_039():
    """Test 39: Multiple Return Paths"""
    # Kiểm tra khả năng sinh mã nhánh return đa đường của máy ảo JVM
    ast = Program([
        FuncDecl(
            IntType(),
            "max",
            [Param(IntType(), "a"), Param(IntType(), "b")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("a"), ">", Identifier("b")),
                    ReturnStmt(Identifier("a")),
                    ReturnStmt(Identifier("b"))
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("max", [IntLiteral(10), IntLiteral(20)])]))
            ])
        )
    ])
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_040():
    """Test 40: Left-to-Right associative evaluation in Arithmetic"""
    # 10 - 4 - 2 nên được phân tích là (10 - 4) - 2 = 4, thay vì 10 - (4 - 2) = 8[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(
                        BinaryOp(IntLiteral(10), "-", IntLiteral(4)), 
                        "-", 
                        IntLiteral(2)
                    )
                ]))
            ])
        )
    ])
    expected = "4"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_041():
    """Test 41: Empty Return in Void Function"""
    # Hàm void sử dụng return;[cite: 3, 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [IntLiteral(1)])),
                ReturnStmt(None),
                ExprStmt(FuncCall("printInt", [IntLiteral(2)]))
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_042():
    """Test 42: For loop without init and update"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                ForStmt(
                    None,
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    None,
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                    ])
                )
            ])
        )
    ])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_043():
    """Test 43: Switch with complex case expressions"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(5)),
                SwitchStmt(
                    Identifier("x"),
                    [
                        CaseStmt(BinaryOp(IntLiteral(2), "+", IntLiteral(3)), [ExprStmt(FuncCall("printInt", [IntLiteral(1)])), BreakStmt()]),
                        CaseStmt(IntLiteral(6), [ExprStmt(FuncCall("printInt", [IntLiteral(2)])), BreakStmt()])
                    ],
                    None
                )
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_044():
    """Test 44: Struct passed to function"""
    ast = Program([
        StructDecl("Point", [
            VarDecl(IntType(), "x", None),
            VarDecl(IntType(), "y", None)
        ]),
        FuncDecl(
            IntType(),
            "sumPoint",
            [Param(StructType("Point"), "p")],
            BlockStmt([
                ReturnStmt(BinaryOp(MemberAccess(Identifier("p"), "x"), "+", MemberAccess(Identifier("p"), "y")))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Point"), "pt", StructLiteral([IntLiteral(10), IntLiteral(20)])),
                ExprStmt(FuncCall("printInt", [FuncCall("sumPoint", [Identifier("pt")])]))
            ])
        )
    ])
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_045():
    """Test 45: Function returning struct"""
    ast = Program([
        StructDecl("Point", [
            VarDecl(IntType(), "x", None),
            VarDecl(IntType(), "y", None)
        ]),
        FuncDecl(
            StructType("Point"),
            "createPoint",
            [Param(IntType(), "x"), Param(IntType(), "y")],
            BlockStmt([
                ReturnStmt(StructLiteral([Identifier("x"), Identifier("y")]))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Point"), "pt", FuncCall("createPoint", [IntLiteral(5), IntLiteral(15)])),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("pt"), "x")])),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("pt"), "y")]))
            ])
        )
    ])
    expected = "515"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_046():
    """Test 46: Complex logical expression"""
    # Kết hợp &&, || và ![cite: 3, 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "a", IntLiteral(1)),
                VarDecl(IntType(), "b", IntLiteral(0)),
                VarDecl(IntType(), "c", IntLiteral(1)),
                IfStmt(
                    BinaryOp(BinaryOp(Identifier("a"), "||", Identifier("b")), "&&", PrefixOp("!", Identifier("b"))),
                    ExprStmt(FuncCall("printInt", [IntLiteral(1)])),
                    ExprStmt(FuncCall("printInt", [IntLiteral(0)]))
                )
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_047():
    """Test 47: Unary minus on expression"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                VarDecl(IntType(), "y", PrefixOp("-", BinaryOp(Identifier("x"), "-", IntLiteral(5)))),
                ExprStmt(FuncCall("printInt", [Identifier("y")]))
            ])
        )
    ])
    expected = "-5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_048():
    """Test 48: Nested struct member access"""
    ast = Program([
        StructDecl("Point", [
            VarDecl(IntType(), "x", None),
            VarDecl(IntType(), "y", None)
        ]),
        StructDecl("Line", [
            VarDecl(StructType("Point"), "start", None),
            VarDecl(StructType("Point"), "end", None)
        ]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Line"), "l", StructLiteral([
                    StructLiteral([IntLiteral(1), IntLiteral(2)]),
                    StructLiteral([IntLiteral(3), IntLiteral(4)])
                ])),
                ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(Identifier("l"), "start"), "x")])),
                ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(Identifier("l"), "end"), "y")]))
            ])
        )
    ])
    expected = "14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_049():
    """Test 49: Assignment as side effect in if condition"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(0)),
                IfStmt(
                    AssignExpr(Identifier("x"), IntLiteral(1)),
                    ExprStmt(FuncCall("printInt", [Identifier("x")])),
                    ExprStmt(FuncCall("printInt", [IntLiteral(0)]))
                )
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_050():
    """Test 50: Complex arithmetic with mixed types"""
    # Kết hợp int và float, ép kiểu ngầm định khi gọi in[cite: 3, 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(FloatType(), "f", BinaryOp(IntLiteral(10), "+", FloatLiteral(2.5))),
                VarDecl(FloatType(), "g", BinaryOp(Identifier("f"), "*", IntLiteral(2))),
                ExprStmt(FuncCall("printFloat", [Identifier("g")]))
            ])
        )
    ])
    expected = "25.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_051():
    """Test 51: Nested function calls as arguments"""
    ast = Program([
        FuncDecl(
            IntType(),
            "double_val",
            [Param(IntType(), "n")],
            BlockStmt([
                ReturnStmt(BinaryOp(Identifier("n"), "*", IntLiteral(2)))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    FuncCall("double_val", [FuncCall("double_val", [IntLiteral(5)])])
                ]))
            ])
        )
    ])
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_052():
    """Test 52: Multiple local variable declarations in one block"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "a", IntLiteral(1)),
                VarDecl(IntType(), "b", IntLiteral(2)),
                VarDecl(IntType(), "c", IntLiteral(3)),
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(Identifier("a"), "+", BinaryOp(Identifier("b"), "+", Identifier("c")))
                ]))
            ])
        )
    ])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_053():
    """Test 53: Loop condition evaluation order"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(AssignExpr(Identifier("x"), BinaryOp(Identifier("x"), "+", IntLiteral(1))), "<", IntLiteral(4)),
                    ExprStmt(FuncCall("printInt", [Identifier("x")]))
                )
            ])
        )
    ])
    expected = "123"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_054():
    """Test 54: Function returning boolean logic"""
    ast = Program([
        FuncDecl(
            IntType(),
            "is_even",
            [Param(IntType(), "n")],
            BlockStmt([
                ReturnStmt(BinaryOp(BinaryOp(Identifier("n"), "%", IntLiteral(2)), "==", IntLiteral(0)))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("is_even", [IntLiteral(4)])])),
                ExprStmt(FuncCall("printInt", [FuncCall("is_even", [IntLiteral(5)])]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_055():
    """Test 55: Floating point comparison and logic"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(FloatType(), "f1", FloatLiteral(2.5)),
                VarDecl(FloatType(), "f2", FloatLiteral(2.5)),
                IfStmt(
                    BinaryOp(Identifier("f1"), "==", Identifier("f2")),
                    ExprStmt(FuncCall("printString", [StringLiteral("equal")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("not_equal")]))
                )
            ])
        )
    ])
    expected = "equal"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_056():
    """Test 56: Short-circuiting avoiding division by zero"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "a", IntLiteral(0)),
                IfStmt(
                    BinaryOp(BinaryOp(Identifier("a"), "!=", IntLiteral(0)), "&&", BinaryOp(BinaryOp(IntLiteral(10), "/", Identifier("a")), ">", IntLiteral(1))),
                    ExprStmt(FuncCall("printString", [StringLiteral("safe")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("zero")]))
                )
            ])
        )
    ])
    expected = "zero"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_057():
    """Test 57: Fall-through in Switch with intermediate break"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "val", IntLiteral(1)),
                SwitchStmt(
                    Identifier("val"),
                    [
                        CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printInt", [IntLiteral(1)]))]),
                        CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printInt", [IntLiteral(2)])), BreakStmt()]),
                        CaseStmt(IntLiteral(3), [ExprStmt(FuncCall("printInt", [IntLiteral(3)]))])
                    ],
                    None
                )
            ])
        )
    ])
    expected = "12"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_058():
    """Test 58: Repeated String concatenation (Print sequence)"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("A")])),
                ExprStmt(FuncCall("printString", [StringLiteral("B")])),
                ExprStmt(FuncCall("printString", [StringLiteral("C")]))
            ])
        )
    ])
    expected = "ABC"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_059():
    """Test 59: Unary plus on arithmetic result"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "res", PrefixOp("+", BinaryOp(IntLiteral(5), "-", IntLiteral(10)))),
                ExprStmt(FuncCall("printInt", [Identifier("res")]))
            ])
        )
    ])
    expected = "-5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_060():
    """Test 60: Postfix decrement on local variable"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "cnt", IntLiteral(5)),
                WhileStmt(
                    BinaryOp(PostfixOp("--", Identifier("cnt")), ">", IntLiteral(0)),
                    ExprStmt(FuncCall("printInt", [Identifier("cnt")]))
                )
            ])
        )
    ])
    expected = "43210"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_061():
    """Test 61: For loop without condition (Infinite loop with break)"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                ForStmt(
                    None,
                    None, # Missing condition -> always true
                    None,
                    BlockStmt([
                        IfStmt(
                            BinaryOp(Identifier("i"), "==", IntLiteral(3)),
                            BreakStmt(),
                            None
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                    ])
                )
            ])
        )
    ])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_062():
    """Test 62: Auto type inference in declarations"""
    # Trình sinh mã phải cấp phát đúng slot biến với kiểu int/float được suy diễn[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "x", IntLiteral(10)), # auto x = 10
                VarDecl(None, "y", FloatLiteral(3.5)), # auto y = 3.5
                ExprStmt(FuncCall("printInt", [Identifier("x")])),
                ExprStmt(FuncCall("printFloat", [Identifier("y")]))
            ])
        )
    ])
    expected = "103.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_063():
    """Test 63: Integer Division vs Float Division"""
    # int / int -> int, float / int -> float[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(10), "/", IntLiteral(3))])),
                ExprStmt(FuncCall("printFloat", [BinaryOp(FloatLiteral(10.0), "/", IntLiteral(4))]))
            ])
        )
    ])
    expected = "32.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_064():
    """Test 64: Chained Relational Operators"""
    # (a < b) < c -> (0 | 1) < c[cite: 3, 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(BinaryOp(IntLiteral(5), "<", IntLiteral(10)), "<", IntLiteral(2))
                ])) # (5 < 10) is 1. Then 1 < 2 is 1 (True)
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_065():
    """Test 65: Multiple cases falling to same block"""
    # Case 1 và Case 2 đều không có break, sẽ rớt xuống in ra 1, 2, 3[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(1)),
                SwitchStmt(
                    Identifier("x"),
                    [
                        CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printInt", [IntLiteral(1)]))]),
                        CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printInt", [IntLiteral(2)]))]),
                        CaseStmt(IntLiteral(3), [ExprStmt(FuncCall("printInt", [IntLiteral(3)])), BreakStmt()])
                    ],
                    None
                )
            ])
        )
    ])
    expected = "123"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_066():
    """Test 66: Negative Modulo Arithmetic"""
    # -10 % 3 = -1 trong JVM[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [BinaryOp(PrefixOp("-", IntLiteral(10)), "%", IntLiteral(3))]))
            ])
        )
    ])
    expected = "-1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_067():
    """Test 67: Unary NOT (!) combined with relational"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    PrefixOp("!", BinaryOp(IntLiteral(5), ">", IntLiteral(10))),
                    ExprStmt(FuncCall("printInt", [IntLiteral(1)])), # !(False) -> True
                    ExprStmt(FuncCall("printInt", [IntLiteral(0)]))
                )
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_068():
    """Test 68: Mutual Recursion"""
    # Hàm is_even gọi is_odd và ngược lại
    ast = Program([
        FuncDecl(
            IntType(),
            "is_odd",
            [Param(IntType(), "n")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("n"), "==", IntLiteral(0)),
                    ReturnStmt(IntLiteral(0)),
                    ReturnStmt(FuncCall("is_even", [BinaryOp(Identifier("n"), "-", IntLiteral(1))]))
                )
            ])
        ),
        FuncDecl(
            IntType(),
            "is_even",
            [Param(IntType(), "n")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("n"), "==", IntLiteral(0)),
                    ReturnStmt(IntLiteral(1)),
                    ReturnStmt(FuncCall("is_odd", [BinaryOp(Identifier("n"), "-", IntLiteral(1))]))
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("is_even", [IntLiteral(4)])]))
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_069():
    """Test 69: While loop that never executes"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                WhileStmt(
                    BinaryOp(Identifier("x"), "<", IntLiteral(5)),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [IntLiteral(99)]))
                    ])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_070():
    """Test 70: Struct variable shadowing"""
    # Biến struct cùng tên che khuất ở block con[cite: 3, 4]
    ast = Program([
        StructDecl("S", [VarDecl(IntType(), "v", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("S"), "obj", StructLiteral([IntLiteral(1)])),
                BlockStmt([
                    VarDecl(StructType("S"), "obj", StructLiteral([IntLiteral(2)])),
                    ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("obj"), "v")]))
                ]),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("obj"), "v")]))
            ])
        )
    ])
    expected = "21"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_071():
    """Test 71: Assignment returns LHS value (nested assignment)"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "a", IntLiteral(0)),
                VarDecl(IntType(), "b", IntLiteral(0)),
                ExprStmt(AssignExpr(Identifier("a"), BinaryOp(AssignExpr(Identifier("b"), IntLiteral(5)), "*", IntLiteral(2)))),
                ExprStmt(FuncCall("printInt", [Identifier("a")])),
                ExprStmt(FuncCall("printInt", [Identifier("b")]))
            ])
        )
    ])
    expected = "105"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_072():
    """Test 72: Short-circuit OR RHS not executed"""
    ast = Program([
        FuncDecl(
            IntType(),
            "mutate",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [IntLiteral(99)])),
                ReturnStmt(IntLiteral(1))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(1), "||", FuncCall("mutate", [])),
                    ExprStmt(FuncCall("printInt", [IntLiteral(1)])),
                    None
                )
            ])
        )
    ])
    expected = "1" # 99 không được in ra do short-circuit của OR[cite: 3]
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_073():
    """Test 73: Prefix Increment with Arithmetic Expression"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(2)),
                ExprStmt(FuncCall("printInt", [BinaryOp(PrefixOp("++", Identifier("x")), "*", IntLiteral(3))])) # ++x * 3 = 3 * 3 = 9
            ])
        )
    ])
    expected = "9"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_074():
    """Test 74: Empty block {} execution"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [IntLiteral(1)])),
                BlockStmt([]),
                ExprStmt(FuncCall("printInt", [IntLiteral(2)]))
            ])
        )
    ])
    expected = "12"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_075():
    """Test 75: Continue skips the rest of the loop block"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    BlockStmt([
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1)))),
                        IfStmt(
                            BinaryOp(Identifier("i"), "==", IntLiteral(2)),
                            ContinueStmt(),
                            None
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("i")]))
                    ])
                )
            ])
        )
    ])
    expected = "13"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_076():
    """Test 76: Nested unary operations"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(5)),
                ExprStmt(FuncCall("printInt", [PrefixOp("-", PrefixOp("-", Identifier("x")))])) # -(-x) = 5
            ])
        )
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_077():
    """Test 77: Complex boolean logic inside loop condition"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(0)),
                VarDecl(IntType(), "y", IntLiteral(2)),
                WhileStmt(
                    BinaryOp(BinaryOp(Identifier("x"), "<", IntLiteral(3)), "&&", BinaryOp(Identifier("y"), ">", IntLiteral(0))),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("x")])),
                        ExprStmt(AssignExpr(Identifier("x"), BinaryOp(Identifier("x"), "+", IntLiteral(1)))),
                        ExprStmt(AssignExpr(Identifier("y"), BinaryOp(Identifier("y"), "-", IntLiteral(1))))
                    ])
                )
            ])
        )
    ])
    expected = "01" # Chạy 2 lần vì y sẽ giảm về 0
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_078():
    """Test 78: Deeply nested struct"""
    ast = Program([
        StructDecl("A", [VarDecl(IntType(), "val", None)]),
        StructDecl("B", [VarDecl(StructType("A"), "innerA", None)]),
        StructDecl("C", [VarDecl(StructType("B"), "innerB", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("C"), "obj", StructLiteral([StructLiteral([StructLiteral([IntLiteral(99)])])])),
                ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(MemberAccess(Identifier("obj"), "innerB"), "innerA"), "val")]))
            ])
        )
    ])
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_079():
    """Test 79: Multiple function calls in an expression"""
    ast = Program([
        FuncDecl(IntType(), "f1", [], BlockStmt([ReturnStmt(IntLiteral(1))])),
        FuncDecl(IntType(), "f2", [], BlockStmt([ReturnStmt(IntLiteral(2))])),
        FuncDecl(IntType(), "f3", [], BlockStmt([ReturnStmt(IntLiteral(3))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(BinaryOp(FuncCall("f1", []), "+", FuncCall("f2", [])), "*", FuncCall("f3", []))
                ])) # (1 + 2) * 3 = 9
            ])
        )
    ])
    expected = "9"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_080():
    """Test 80: Re-assigning Struct Variables"""
    # Struct assignment copies all member values[cite: 3]
    ast = Program([
        StructDecl("Point", [
            VarDecl(IntType(), "x", None),
            VarDecl(IntType(), "y", None)
        ]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Point"), "p1", StructLiteral([IntLiteral(10), IntLiteral(20)])),
                VarDecl(StructType("Point"), "p2", StructLiteral([IntLiteral(0), IntLiteral(0)])),
                ExprStmt(AssignExpr(Identifier("p2"), Identifier("p1"))),
                ExprStmt(AssignExpr(MemberAccess(Identifier("p2"), "y"), IntLiteral(99))),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p1"), "y")])), # Vẫn là 20 (Truyền trị / Pass by value)
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p2"), "y")]))  # Đổi thành 99
            ])
        )
    ])
    expected = "2099"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_081():
    """Test 81: Nested If inside While loop"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(5)),
                    BlockStmt([
                        IfStmt(
                            BinaryOp(BinaryOp(Identifier("i"), "%", IntLiteral(2)), "==", IntLiteral(0)),
                            ExprStmt(FuncCall("printInt", [Identifier("i")])),
                            None
                        ),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                    ])
                )
            ])
        )
    ])
    expected = "024" # In ra các số chẵn
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_082():
    """Test 82: Complex For loop with assignment in init and update"""
    # init có thể là phép gán, update có thể là phép gán phức tạp[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", None),
                ForStmt(
                    ExprStmt(AssignExpr(Identifier("i"), IntLiteral(1))),
                    BinaryOp(Identifier("i"), "<", IntLiteral(10)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "*", IntLiteral(2))),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")]))
                    ])
                )
            ])
        )
    ])
    expected = "1248"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_083():
    """Test 83: Return inside a While loop (Early exit)"""
    ast = Program([
        FuncDecl(
            IntType(),
            "find_first_even",
            [Param(IntType(), "start")],
            BlockStmt([
                VarDecl(IntType(), "i", Identifier("start")),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(10)),
                    BlockStmt([
                        IfStmt(
                            BinaryOp(BinaryOp(Identifier("i"), "%", IntLiteral(2)), "==", IntLiteral(0)),
                            ReturnStmt(Identifier("i")),
                            None
                        ),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                    ])
                ),
                ReturnStmt(PrefixOp("-", IntLiteral(1)))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("find_first_even", [IntLiteral(3)])]))
            ])
        )
    ])
    expected = "4"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_084():
    """Test 84: Accessing struct member directly from function return"""
    # getPoint().x hợp lệ nếu hàm trả về kiểu struct[cite: 3, 4]
    ast = Program([
        StructDecl("Point", [
            VarDecl(IntType(), "x", None),
            VarDecl(IntType(), "y", None)
        ]),
        FuncDecl(
            StructType("Point"),
            "getPoint",
            [],
            BlockStmt([
                ReturnStmt(StructLiteral([IntLiteral(77), IntLiteral(88)]))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [MemberAccess(FuncCall("getPoint", []), "x")]))
            ])
        )
    ])
    expected = "77"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_085():
    """Test 85: Logical NOT double negation !(!x)"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(0)),
                IfStmt(
                    PrefixOp("!", PrefixOp("!", Identifier("x"))),
                    ExprStmt(FuncCall("printInt", [IntLiteral(1)])),
                    ExprStmt(FuncCall("printInt", [IntLiteral(0)]))
                )
            ])
        )
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_086():
    """Test 86: Passing struct returned from function directly to another function"""
    ast = Program([
        StructDecl("Box", [VarDecl(IntType(), "val", None)]),
        FuncDecl(StructType("Box"), "createBox", [Param(IntType(), "v")], BlockStmt([ReturnStmt(StructLiteral([Identifier("v")]))])),
        FuncDecl(VoidType(), "printBox", [Param(StructType("Box"), "b")], BlockStmt([ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("b"), "val")]))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printBox", [FuncCall("createBox", [IntLiteral(123)])]))
            ])
        )
    ])
    expected = "123"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_087():
    """Test 87: Complex Precedence: Arithmetic + Relational + Logical"""
    # a + b > c && x == y[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(
                        BinaryOp(BinaryOp(IntLiteral(1), "+", IntLiteral(2)), ">", IntLiteral(2)), 
                        "&&", 
                        BinaryOp(IntLiteral(3), "==", IntLiteral(3))
                    ),
                    ExprStmt(FuncCall("printInt", [IntLiteral(1)])),
                    ExprStmt(FuncCall("printInt", [IntLiteral(0)]))
                )
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_088():
    """Test 88: Recursion (Fibonacci Sequence)"""
    ast = Program([
        FuncDecl(
            IntType(),
            "fib",
            [Param(IntType(), "n")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("n"), "<=", IntLiteral(1)),
                    ReturnStmt(Identifier("n")),
                    ReturnStmt(BinaryOp(FuncCall("fib", [BinaryOp(Identifier("n"), "-", IntLiteral(1))]), "+", FuncCall("fib", [BinaryOp(Identifier("n"), "-", IntLiteral(2))])))
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("fib", [IntLiteral(6)])]))
            ])
        )
    ])
    expected = "8" # fib(6) = 8
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_089():
    """Test 89: Struct Literal directly in member access"""
    # {10, 20}.x (mặc dù ít dùng nhưng hợp lệ về mặt AST nếu được parse)
    # Trong CodeGen, đẩy literal lên stack rồi truy cập field.
    ast = Program([
        StructDecl("Point", [VarDecl(IntType(), "x", None), VarDecl(IntType(), "y", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                # Tuy TyC specification không explicitly nói `{10, 20}.x`, ta có thể test gián tiếp qua biến tạm
                VarDecl(StructType("Point"), "p", StructLiteral([IntLiteral(10), IntLiteral(20)])),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p"), "x")]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_090():
    """Test 90: Modifying loop counter inside the loop body"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(0)),
                    BinaryOp(Identifier("i"), "<", IntLiteral(10)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(2)))) # Skip 2 numbers
                    ])
                )
            ])
        )
    ])
    expected = "0369"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_091():
    """Test 91: Nested Switch Statements"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "out", IntLiteral(1)),
                VarDecl(IntType(), "in", IntLiteral(2)),
                SwitchStmt(
                    Identifier("out"),
                    [
                        CaseStmt(IntLiteral(1), [
                            SwitchStmt(
                                Identifier("in"),
                                [
                                    CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printInt", [IntLiteral(22)])), BreakStmt()])
                                ],
                                None
                            ),
                            BreakStmt()
                        ])
                    ],
                    None
                )
            ])
        )
    ])
    expected = "22"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_092():
    """Test 92: Mixed Assign and Arithmetic Associativity"""
    # a = b + c * d
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "a", None),
                VarDecl(IntType(), "b", IntLiteral(2)),
                VarDecl(IntType(), "c", IntLiteral(3)),
                VarDecl(IntType(), "d", IntLiteral(4)),
                ExprStmt(AssignExpr(Identifier("a"), BinaryOp(Identifier("b"), "+", BinaryOp(Identifier("c"), "*", Identifier("d"))))),
                ExprStmt(FuncCall("printInt", [Identifier("a")]))
            ])
        )
    ])
    expected = "14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_093():
    """Test 93: Left-to-Right evaluation in function arguments"""
    ast = Program([
        FuncDecl(IntType(), "f1", [], BlockStmt([ExprStmt(FuncCall("printInt", [IntLiteral(1)])), ReturnStmt(IntLiteral(1))])),
        FuncDecl(IntType(), "f2", [], BlockStmt([ExprStmt(FuncCall("printInt", [IntLiteral(2)])), ReturnStmt(IntLiteral(2))])),
        FuncDecl(VoidType(), "consume", [Param(IntType(), "a"), Param(IntType(), "b")], BlockStmt([])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("consume", [FuncCall("f1", []), FuncCall("f2", [])]))
            ])
        )
    ])
    expected = "12" # f1 executes before f2[cite: 3]
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_094():
    """Test 94: Chained member access assignment"""
    ast = Program([
        StructDecl("Inner", [VarDecl(IntType(), "val", None)]),
        StructDecl("Outer", [VarDecl(StructType("Inner"), "inn", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Outer"), "o", StructLiteral([StructLiteral([IntLiteral(0)])])),
                ExprStmt(AssignExpr(MemberAccess(MemberAccess(Identifier("o"), "inn"), "val"), IntLiteral(999))),
                ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(Identifier("o"), "inn"), "val")]))
            ])
        )
    ])
    expected = "999"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_095():
    """Test 95: Switch case fall-through to default"""
    # Nếu một case không có break nằm kề default, nó sẽ chạy tràn xuống default[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(1)),
                SwitchStmt(
                    Identifier("x"),
                    [
                        CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printInt", [IntLiteral(1)]))])
                    ],
                    DefaultStmt([ExprStmt(FuncCall("printInt", [IntLiteral(0)])), BreakStmt()])
                )
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_096():
    """Test 96: Local variable in nested block"""
    # Dùng tên khác để tránh vi phạm quy tắc không cho che khuất tham số[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "test_shadow",
            [Param(IntType(), "x")],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [Identifier("x")])),
                BlockStmt([
                    VarDecl(IntType(), "y", IntLiteral(99)),
                    ExprStmt(FuncCall("printInt", [Identifier("y")]))
                ]),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("test_shadow", [IntLiteral(10)]))
            ])
        )
    ])
    expected = "109910"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_097():
    """Test 97: Short-circuit combined with Assignment Expression"""
    # Mặc dù gán có side effect, nhưng nếu bị short-circuit thì biến không bị thay đổi[cite: 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "a", IntLiteral(0)),
                IfStmt(
                    BinaryOp(IntLiteral(0), "&&", AssignExpr(Identifier("a"), IntLiteral(1))),
                    BlockStmt([]),
                    BlockStmt([])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("a")]))
            ])
        )
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_098():
    """Test 98: Modulo precedence and left-associativity"""
    # 10 % 4 % 2 -> (10 % 4) % 2 = 2 % 2 = 0[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [BinaryOp(BinaryOp(IntLiteral(10), "%", IntLiteral(4)), "%", IntLiteral(2))]))
            ])
        )
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_099():
    """Test 99: Logical NOT with Relational (Evaluating to Int)"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "res", PrefixOp("!", BinaryOp(IntLiteral(5), "==", IntLiteral(5)))),
                ExprStmt(FuncCall("printInt", [Identifier("res")])) # !1 = 0
            ])
        )
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_100():
    """Test 100: Comprehensive Integration Test"""
    # Tính tổng bình phương các số lẻ trong mảng giả lập bằng loop và condition[cite: 3]
    ast = Program([
        FuncDecl(
            IntType(),
            "square",
            [Param(IntType(), "x")],
            BlockStmt([ReturnStmt(BinaryOp(Identifier("x"), "*", Identifier("x")))])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "sum", IntLiteral(0)),
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(1)),
                    BinaryOp(Identifier("i"), "<=", IntLiteral(5)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        IfStmt(
                            BinaryOp(BinaryOp(Identifier("i"), "%", IntLiteral(2)), "==", IntLiteral(0)),
                            ContinueStmt(),
                            None
                        ),
                        ExprStmt(AssignExpr(Identifier("sum"), BinaryOp(Identifier("sum"), "+", FuncCall("square", [Identifier("i")]))))
                    ])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("sum")])) # 1^2 + 3^2 + 5^2 = 1 + 9 + 25 = 35
            ])
        )
    ])
    expected = "35"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_101():
    """Test 101: Auto type inference cascading"""
    # Suy diễn kiểu liên hoàn: int -> int -> float -> float[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "a", IntLiteral(5)),           # auto a = 5
                VarDecl(None, "b", Identifier("a")),         # auto b = a
                VarDecl(None, "c", FloatLiteral(2.5)),       # auto c = 2.5
                VarDecl(None, "d", BinaryOp(Identifier("b"), "+", Identifier("c"))), # auto d = b + c (float)
                ExprStmt(FuncCall("printFloat", [Identifier("d")]))
            ])
        )
    ])
    expected = "7.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_102():
    """Test 102: Postfix operation in complex arithmetic"""
    # x++ * 2 + ++y -> (3 * 2) + 5 = 11. Sau đó x = 4.[cite: 3, 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(3)),
                VarDecl(IntType(), "y", IntLiteral(4)),
                VarDecl(IntType(), "res", BinaryOp(
                    BinaryOp(PostfixOp("++", Identifier("x")), "*", IntLiteral(2)),
                    "+",
                    PrefixOp("++", Identifier("y"))
                )),
                ExprStmt(FuncCall("printInt", [Identifier("res")])),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "114"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_103():
    """Test 103: Extreme Variable Shadowing (4 levels deep)"""
    # Kiểm tra symbol table phân giải đúng offset biến trong các frame lồng nhau[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "val", IntLiteral(1)),
                BlockStmt([
                    VarDecl(IntType(), "val", IntLiteral(2)),
                    BlockStmt([
                        VarDecl(IntType(), "val", IntLiteral(3)),
                        BlockStmt([
                            VarDecl(IntType(), "val", IntLiteral(4)),
                            ExprStmt(FuncCall("printInt", [Identifier("val")]))
                        ]),
                        ExprStmt(FuncCall("printInt", [Identifier("val")]))
                    ]),
                    ExprStmt(FuncCall("printInt", [Identifier("val")]))
                ]),
                ExprStmt(FuncCall("printInt", [Identifier("val")]))
            ])
        )
    ])
    expected = "4321"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_104():
    """Test 104: Break statement escaping only the Switch, not the Loop"""
    # Break trong switch chỉ thoát switch, vòng lặp while vẫn tiếp tục[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    BlockStmt([
                        SwitchStmt(
                            Identifier("i"),
                            [
                                CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printInt", [IntLiteral(99)])), BreakStmt()])
                            ],
                            DefaultStmt([ExprStmt(FuncCall("printInt", [Identifier("i")])), BreakStmt()])
                        ),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                    ])
                )
            ])
        )
    ])
    expected = "0992"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_105():
    """Test 105: Double Short-circuit (&& and || combined)"""
    # (0 && f1()) || f2() -> f1() bị bypass do &&, f2() chạy do || cần đánh giá[cite: 3]
    ast = Program([
        FuncDecl(IntType(), "f1", [], BlockStmt([ExprStmt(FuncCall("printInt", [IntLiteral(1)])), ReturnStmt(IntLiteral(1))])),
        FuncDecl(IntType(), "f2", [], BlockStmt([ExprStmt(FuncCall("printInt", [IntLiteral(2)])), ReturnStmt(IntLiteral(1))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(
                        BinaryOp(IntLiteral(0), "&&", FuncCall("f1", [])),
                        "||",
                        FuncCall("f2", [])
                    ),
                    ExprStmt(FuncCall("printString", [StringLiteral("T")])),
                    None
                )
            ])
        )
    ])
    expected = "2T" # f1 không chạy, f2 chạy in ra 2, kết quả || là true nên in ra T
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_106():
    """Test 106: Struct returned from function assigned to auto variable"""
    ast = Program([
        StructDecl("Vec2", [VarDecl(FloatType(), "x", None), VarDecl(FloatType(), "y", None)]),
        FuncDecl(StructType("Vec2"), "get_vec", [], BlockStmt([ReturnStmt(StructLiteral([FloatLiteral(1.5), FloatLiteral(2.5)]))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "v", FuncCall("get_vec", [])),
                ExprStmt(FuncCall("printFloat", [MemberAccess(Identifier("v"), "x")])),
                ExprStmt(FuncCall("printFloat", [MemberAccess(Identifier("v"), "y")]))
            ])
        )
    ])
    expected = "1.52.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_107():
    """Test 107: Relational operators on Floats returning Int"""
    # JVM sinh lệnh fcmpl/fcmpg, sau đó đẩy 0 hoặc 1[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(FloatType(), "f1", FloatLiteral(10.5)),
                VarDecl(FloatType(), "f2", FloatLiteral(10.5)),
                VarDecl(IntType(), "res", BinaryOp(Identifier("f1"), ">=", Identifier("f2"))),
                ExprStmt(FuncCall("printInt", [Identifier("res")]))
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_108():
    """Test 108: Function with no parameters but inferred return type"""
    # Hàm auto suy diễn kiểu trả về từ return statement đầu tiên[cite: 3]
    ast = Program([
        FuncDecl(
            None, # Inferred return type
            "get_magic",
            [],
            BlockStmt([
                ReturnStmt(IntLiteral(42))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("get_magic", [])]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_109():
    """Test 109: Continue skips update? No, for loop always executes update"""
    # Trong for loop, continue sẽ bỏ qua phần còn lại của block nhưng VẪN PHẢI chạy update expression[cite: 3, 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(0)),
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(1)), ContinueStmt(), None),
                        ExprStmt(FuncCall("printInt", [Identifier("i")]))
                    ])
                )
            ])
        )
    ])
    expected = "02" # 1 bị bỏ qua khối in, nhưng i vẫn được tăng lên 2
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_110():
    """Test 110: Nested Assignment as Function Argument"""
    ast = Program([
        FuncDecl(VoidType(), "display", [Param(IntType(), "x")], BlockStmt([ExprStmt(FuncCall("printInt", [Identifier("x")]))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "a", IntLiteral(0)),
                ExprStmt(FuncCall("display", [AssignExpr(Identifier("a"), IntLiteral(88))])),
                ExprStmt(FuncCall("display", [Identifier("a")]))
            ])
        )
    ])
    expected = "8888"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_111():
    """Test 111: Empty string literal"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("A")])),
                ExprStmt(FuncCall("printString", [StringLiteral("")])), # Empty string
                ExprStmt(FuncCall("printString", [StringLiteral("B")]))
            ])
        )
    ])
    expected = "AB"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_112():
    """Test 112: If statement with implicit float to int condition? Error in TyC"""
    # Tuy nhiên trình sinh mã giả định AST đã pass Static Check (kiểu if phải là int).
    # Test này kiểm tra logic: nếu ExprStmt là assignment thì nó trả về kết quả RHS để gọi function.
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(0)),
                IfStmt(
                    BinaryOp(AssignExpr(Identifier("x"), IntLiteral(1)), "==", IntLiteral(1)),
                    ExprStmt(FuncCall("printInt", [Identifier("x")])),
                    None
                )
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_113():
    """Test 113: Deeply nested Binary Operations to test stack size handling"""
    # Trình sinh mã phải đảm bảo không bị lỗi tràn operand stack khi biểu thức dài[cite: 1, 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(
                        BinaryOp(BinaryOp(IntLiteral(1), "+", IntLiteral(1)), "+", IntLiteral(1)),
                        "+",
                        BinaryOp(BinaryOp(IntLiteral(1), "+", IntLiteral(1)), "+", IntLiteral(1))
                    )
                ]))
            ])
        )
    ])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_114():
    """Test 114: Switch Fall-through executing multiple variable assignments"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "state", IntLiteral(1)),
                VarDecl(IntType(), "counter", IntLiteral(0)),
                SwitchStmt(
                    Identifier("state"),
                    [
                        CaseStmt(IntLiteral(1), [ExprStmt(AssignExpr(Identifier("counter"), BinaryOp(Identifier("counter"), "+", IntLiteral(1))))]),
                        CaseStmt(IntLiteral(2), [ExprStmt(AssignExpr(Identifier("counter"), BinaryOp(Identifier("counter"), "+", IntLiteral(10))))]),
                        CaseStmt(IntLiteral(3), [ExprStmt(AssignExpr(Identifier("counter"), BinaryOp(Identifier("counter"), "+", IntLiteral(100)))), BreakStmt()])
                    ],
                    None
                ),
                ExprStmt(FuncCall("printInt", [Identifier("counter")]))
            ])
        )
    ])
    expected = "111" # 0 + 1 + 10 + 100 = 111 (Fall-through từ 1 -> 2 -> 3)
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_115():
    """Test 115: Multiple Default in logic? No, static checker blocks it. Test Single Default."""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "val", IntLiteral(99)),
                SwitchStmt(
                    Identifier("val"),
                    [
                        CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printInt", [IntLiteral(1)])), BreakStmt()])
                    ],
                    DefaultStmt([ExprStmt(FuncCall("printInt", [IntLiteral(0)])), BreakStmt()])
                )
            ])
        )
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_116():
    """Test 116: Unary minus on float literal vs integer literal"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(FloatType(), "f", PrefixOp("-", FloatLiteral(3.5))),
                VarDecl(IntType(), "i", PrefixOp("-", IntLiteral(3))),
                ExprStmt(FuncCall("printFloat", [Identifier("f")])),
                ExprStmt(FuncCall("printInt", [Identifier("i")]))
            ])
        )
    ])
    expected = "-3.5-3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_117():
    """Test 117: Struct passing as argument (Pass by Value verification)"""
    # Struct trong TyC truyền bằng trị (copy content), đổi trong hàm không ảnh hưởng ngoài[cite: 3]
    ast = Program([
        StructDecl("Data", [VarDecl(IntType(), "v", None)]),
        FuncDecl(
            VoidType(),
            "modify",
            [Param(StructType("Data"), "d")],
            BlockStmt([
                ExprStmt(AssignExpr(MemberAccess(Identifier("d"), "v"), IntLiteral(99)))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Data"), "my_data", StructLiteral([IntLiteral(10)])),
                ExprStmt(FuncCall("modify", [Identifier("my_data")])),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("my_data"), "v")]))
            ])
        )
    ])
    expected = "10" # Vẫn là 10
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_118():
    """Test 118: Implicit Float promotion in BinaryOp"""
    # int + float -> float[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(5)),
                VarDecl(FloatType(), "f", FloatLiteral(2.5)),
                VarDecl(FloatType(), "res", BinaryOp(Identifier("i"), "-", Identifier("f"))),
                ExprStmt(FuncCall("printFloat", [Identifier("res")]))
            ])
        )
    ])
    expected = "2.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_119():
    """Test 119: Boolean NOT reversing Relational expression"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    PrefixOp("!", BinaryOp(IntLiteral(10), "<=", IntLiteral(5))), # !(10 <= 5) -> !(False) -> True
                    ExprStmt(FuncCall("printString", [StringLiteral("True")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("False")]))
                )
            ])
        )
    ])
    expected = "True"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_120():
    """Test 120: Recursive function returning Struct"""
    ast = Program([
        StructDecl("Counter", [VarDecl(IntType(), "count", None)]),
        FuncDecl(
            StructType("Counter"),
            "increment_struct",
            [Param(StructType("Counter"), "c"), Param(IntType(), "times")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("times"), "==", IntLiteral(0)),
                    ReturnStmt(Identifier("c")),
                    BlockStmt([
                        ExprStmt(AssignExpr(MemberAccess(Identifier("c"), "count"), BinaryOp(MemberAccess(Identifier("c"), "count"), "+", IntLiteral(1)))),
                        ReturnStmt(FuncCall("increment_struct", [Identifier("c"), BinaryOp(Identifier("times"), "-", IntLiteral(1))]))
                    ])
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Counter"), "init", StructLiteral([IntLiteral(0)])),
                VarDecl(StructType("Counter"), "final", FuncCall("increment_struct", [Identifier("init"), IntLiteral(5)])),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("final"), "count")]))
            ])
        )
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_121():
    """Test 121: Continue inside Switch inside While loop"""
    # Lệnh continue không hợp lệ trong switch độc lập, nhưng hợp lệ nếu switch nằm trong loop.
    # Lệnh continue này sẽ nhảy tới cuối vòng lặp while (update/condition)[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    BlockStmt([
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1)))),
                        SwitchStmt(
                            Identifier("i"),
                            [
                                CaseStmt(IntLiteral(2), [ContinueStmt()]) # Nếu là 2, bỏ qua lệnh printInt bên dưới
                            ],
                            None
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("i")]))
                    ])
                )
            ])
        )
    ])
    expected = "13"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_122():
    """Test 122: Double Unary Minus"""
    # -(-x) = x[cite: 3, 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(42)),
                ExprStmt(FuncCall("printInt", [PrefixOp("-", PrefixOp("-", Identifier("x")))]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_123():
    """Test 123: Nested Relational Equivalence"""
    # (a < b) == (c > d) -> (1 == 0) -> 0[cite: 3, 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(
                        BinaryOp(IntLiteral(1), "<", IntLiteral(5)),
                        "==",
                        BinaryOp(IntLiteral(2), ">", IntLiteral(8))
                    )
                ]))
            ])
        )
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_124():
    """Test 124: Nested While Loops with Break and Continue"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    BlockStmt([
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1)))),
                        VarDecl(IntType(), "j", IntLiteral(0)),
                        WhileStmt(
                            BinaryOp(Identifier("j"), "<", IntLiteral(3)),
                            BlockStmt([
                                ExprStmt(AssignExpr(Identifier("j"), BinaryOp(Identifier("j"), "+", IntLiteral(1)))),
                                IfStmt(
                                    BinaryOp(Identifier("j"), "==", IntLiteral(2)),
                                    ContinueStmt(),
                                    None
                                ),
                                ExprStmt(FuncCall("printInt", [Identifier("j")]))
                            ])
                        )
                    ])
                )
            ])
        )
    ])
    expected = "131313" # Với mỗi i (1,2,3), j in ra 1, 3 (bỏ qua 2)
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_125():
    """Test 125: De Morgan's Laws Validation"""
    # !(a || b) == (!a && !b)[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "a", IntLiteral(1)), # True
                VarDecl(IntType(), "b", IntLiteral(0)), # False
                VarDecl(IntType(), "left", PrefixOp("!", BinaryOp(Identifier("a"), "||", Identifier("b")))),
                VarDecl(IntType(), "right", BinaryOp(PrefixOp("!", Identifier("a")), "&&", PrefixOp("!", Identifier("b")))),
                IfStmt(
                    BinaryOp(Identifier("left"), "==", Identifier("right")),
                    ExprStmt(FuncCall("printString", [StringLiteral("Eq")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("Neq")]))
                )
            ])
        )
    ])
    expected = "Eq"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_126():
    """Test 126: For loop with auto and complex update"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ForStmt(
                    VarDecl(None, "i", IntLiteral(1)), # auto i = 1
                    BinaryOp(Identifier("i"), "<", IntLiteral(100)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "*", IntLiteral(5))),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")]))
                    ])
                )
            ])
        )
    ])
    expected = "1525"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_127():
    """Test 127: Struct member assignment evaluating to value"""
    # a = (p.x = 5)[cite: 3, 4]
    ast = Program([
        StructDecl("Point", [VarDecl(IntType(), "x", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Point"), "p", StructLiteral([IntLiteral(0)])),
                VarDecl(IntType(), "a", None),
                ExprStmt(AssignExpr(Identifier("a"), AssignExpr(MemberAccess(Identifier("p"), "x"), IntLiteral(42)))),
                ExprStmt(FuncCall("printInt", [Identifier("a")])),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p"), "x")]))
            ])
        )
    ])
    expected = "4242"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_128():
    """Test 128: Return deeply nested in If-Else"""
    ast = Program([
        FuncDecl(
            IntType(),
            "find_val",
            [Param(IntType(), "code")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("code"), "==", IntLiteral(1)),
                    ReturnStmt(IntLiteral(100)),
                    IfStmt(
                        BinaryOp(Identifier("code"), "==", IntLiteral(2)),
                        ReturnStmt(IntLiteral(200)),
                        ReturnStmt(IntLiteral(300))
                    )
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("find_val", [IntLiteral(2)])]))
            ])
        )
    ])
    expected = "200"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_129():
    """Test 129: Uninitialized variables with explicit type"""
    # Các biến cục bộ chưa khởi tạo có giá trị undefined, nhưng trong môi trường này ta khởi tạo sau đó[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", None),
                VarDecl(FloatType(), "y", None),
                ExprStmt(AssignExpr(Identifier("x"), IntLiteral(7))),
                ExprStmt(AssignExpr(Identifier("y"), FloatLiteral(2.2))),
                ExprStmt(FuncCall("printInt", [Identifier("x")])),
                ExprStmt(FuncCall("printFloat", [Identifier("y")]))
            ])
        )
    ])
    expected = "72.2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_130():
    """Test 130: Complex sequence of arithmetic and assignment"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "a", IntLiteral(2)),
                VarDecl(IntType(), "b", IntLiteral(3)),
                VarDecl(IntType(), "c", IntLiteral(4)),
                ExprStmt(AssignExpr(Identifier("a"), BinaryOp(Identifier("a"), "+", BinaryOp(Identifier("b"), "*", Identifier("c"))))),
                ExprStmt(FuncCall("printInt", [Identifier("a")]))
            ])
        )
    ])
    expected = "14" # 2 + (3 * 4) = 14
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_131():
    """Test 131: Nested For Loops"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(1)),
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        ForStmt(
                            VarDecl(IntType(), "j", IntLiteral(1)),
                            BinaryOp(Identifier("j"), "<=", IntLiteral(2)),
                            AssignExpr(Identifier("j"), BinaryOp(Identifier("j"), "+", IntLiteral(1))),
                            BlockStmt([
                                ExprStmt(FuncCall("printInt", [Identifier("i")])),
                                ExprStmt(FuncCall("printInt", [Identifier("j")]))
                            ])
                        )
                    ])
                )
            ])
        )
    ])
    expected = "11122122" # i=1,j=1 -> 11; i=1,j=2 -> 12; i=2,j=1 -> 21; i=2,j=2 -> 22
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_132():
    """Test 132: Recursive Sum to N"""
    ast = Program([
        FuncDecl(
            IntType(),
            "sumTo",
            [Param(IntType(), "n")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("n"), "<=", IntLiteral(0)),
                    ReturnStmt(IntLiteral(0)),
                    ReturnStmt(BinaryOp(Identifier("n"), "+", FuncCall("sumTo", [BinaryOp(Identifier("n"), "-", IntLiteral(1))])))
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("sumTo", [IntLiteral(5)])])) # 5+4+3+2+1=15
            ])
        )
    ])
    expected = "15"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_133():
    """Test 133: Short-circuiting with function calls mutating state"""
    # Nếu || short-circuit, hàm có side effect sẽ không được gọi[cite: 3]
    ast = Program([
        FuncDecl(
            IntType(),
            "mutate",
            [Param(IntType(), "v")],
            BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("M")])),
                ReturnStmt(Identifier("v"))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(1), "||", FuncCall("mutate", [IntLiteral(0)])),
                    ExprStmt(FuncCall("printString", [StringLiteral("True")])),
                    None
                )
            ])
        )
    ])
    expected = "True" # 'M' không được in
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_134():
    """Test 134: Switch Case with Constant Expression"""
    # Switch nhận case là biểu thức hằng (Constant expression)[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "val", IntLiteral(5)),
                SwitchStmt(
                    Identifier("val"),
                    [
                        CaseStmt(BinaryOp(IntLiteral(2), "+", IntLiteral(3)), [ExprStmt(FuncCall("printString", [StringLiteral("Five")])), BreakStmt()])
                    ],
                    None
                )
            ])
        )
    ])
    expected = "Five"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_135():
    """Test 135: Default clause placed in the middle of Switch"""
    # Default có thể đứng giữa các case[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(99)),
                SwitchStmt(
                    Identifier("x"),
                    [
                        CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printInt", [IntLiteral(1)])), BreakStmt()]),
                        CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printInt", [IntLiteral(2)])), BreakStmt()])
                    ],
                    DefaultStmt([ExprStmt(FuncCall("printInt", [IntLiteral(0)])), BreakStmt()])
                )
            ])
        )
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_136():
    """Test 136: Assigning a function returning a struct to a struct variable"""
    ast = Program([
        StructDecl("Data", [VarDecl(IntType(), "id", None)]),
        FuncDecl(StructType("Data"), "make_data", [], BlockStmt([ReturnStmt(StructLiteral([IntLiteral(101)]))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Data"), "d", None),
                ExprStmt(AssignExpr(Identifier("d"), FuncCall("make_data", []))),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("d"), "id")]))
            ])
        )
    ])
    expected = "101"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_137():
    """Test 137: Boolean variable from Relational Operator used in Condition"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "a", IntLiteral(10)),
                VarDecl(IntType(), "b", IntLiteral(20)),
                VarDecl(IntType(), "isLess", BinaryOp(Identifier("a"), "<", Identifier("b"))),
                IfStmt(
                    Identifier("isLess"),
                    ExprStmt(FuncCall("printString", [StringLiteral("Yes")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("No")]))
                )
            ])
        )
    ])
    expected = "Yes"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_138():
    """Test 138: Shadowing within For Loop block"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "v", IntLiteral(0)),
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(0)),
                    BinaryOp(Identifier("i"), "<", IntLiteral(1)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        VarDecl(IntType(), "v", IntLiteral(99)),
                        ExprStmt(FuncCall("printInt", [Identifier("v")]))
                    ])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("v")]))
            ])
        )
    ])
    expected = "990"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_139():
    """Test 139: String variable passed to function"""
    # String có thể truyền như tham số bình thường[cite: 3]
    ast = Program([
        FuncDecl(VoidType(), "greet", [Param(StringType(), "msg")], BlockStmt([ExprStmt(FuncCall("printString", [Identifier("msg")]))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StringType(), "hello", StringLiteral("XinChao")),
                ExprStmt(FuncCall("greet", [Identifier("hello")]))
            ])
        )
    ])
    expected = "XinChao"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_140():
    """Test 140: Comprehensive test - Check Prime Number"""
    ast = Program([
        FuncDecl(
            IntType(),
            "isPrime",
            [Param(IntType(), "n")],
            BlockStmt([
                IfStmt(BinaryOp(Identifier("n"), "<=", IntLiteral(1)), ReturnStmt(IntLiteral(0)), None),
                VarDecl(IntType(), "i", IntLiteral(2)),
                WhileStmt(
                    BinaryOp(BinaryOp(Identifier("i"), "*", Identifier("i")), "<=", Identifier("n")),
                    BlockStmt([
                        IfStmt(
                            BinaryOp(BinaryOp(Identifier("n"), "%", Identifier("i")), "==", IntLiteral(0)),
                            ReturnStmt(IntLiteral(0)),
                            None
                        ),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                    ])
                ),
                ReturnStmt(IntLiteral(1))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    FuncCall("isPrime", [IntLiteral(7)]),
                    ExprStmt(FuncCall("printString", [StringLiteral("Prime")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("NotPrime")]))
                )
            ])
        )
    ])
    expected = "Prime"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_141():
    """Test 141: Modulo with negative dividend"""
    # Trong JVM, phép % giữ dấu của số bị chia (dividend)[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [BinaryOp(PrefixOp("-", IntLiteral(14)), "%", IntLiteral(3))])) # -14 % 3 = -2
            ])
        )
    ])
    expected = "-2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_142():
    """Test 142: For loop with initially false condition"""
    # Vòng lặp không được thực thi lần nào[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "flag", IntLiteral(0)),
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(0)),
                    BinaryOp(Identifier("i"), ">", IntLiteral(5)), # False ngay từ đầu
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        ExprStmt(AssignExpr(Identifier("flag"), IntLiteral(1)))
                    ])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("flag")]))
            ])
        )
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_143():
    """Test 143: While loop with initially false condition"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "count", IntLiteral(99)),
                WhileStmt(
                    BinaryOp(IntLiteral(1), "==", IntLiteral(0)),
                    BlockStmt([
                        ExprStmt(AssignExpr(Identifier("count"), IntLiteral(0)))
                    ])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("count")]))
            ])
        )
    ])
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_144():
    """Test 144: Complex Short-circuiting with && and ||"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(
                        BinaryOp(IntLiteral(0), "&&", IntLiteral(1)),
                        "||",
                        BinaryOp(IntLiteral(1), "&&", IntLiteral(1))
                    ),
                    ExprStmt(FuncCall("printString", [StringLiteral("Pass")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("Fail")]))
                )
            ])
        )
    ])
    expected = "Pass"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_145():
    """Test 145: Triple Unary Minus"""
    # -(-(-x)) = -x[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(5)),
                ExprStmt(FuncCall("printInt", [PrefixOp("-", PrefixOp("-", PrefixOp("-", Identifier("x"))))]))
            ])
        )
    ])
    expected = "-5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_146():
    """Test 146: Prefix Increment embedded in Assignment"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(0)),
                VarDecl(IntType(), "y", IntLiteral(10)),
                ExprStmt(AssignExpr(Identifier("x"), PrefixOp("++", Identifier("y")))),
                ExprStmt(FuncCall("printInt", [Identifier("x")])),
                ExprStmt(FuncCall("printInt", [Identifier("y")]))
            ])
        )
    ])
    expected = "1111"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_147():
    """Test 147: Variable mutation inside nested block without shadowing"""
    # Không khai báo lại, chỉ thay đổi giá trị biến ở block ngoài[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "v", IntLiteral(10)),
                BlockStmt([
                    ExprStmt(AssignExpr(Identifier("v"), IntLiteral(20))),
                    BlockStmt([
                        ExprStmt(AssignExpr(Identifier("v"), IntLiteral(30)))
                    ])
                ]),
                ExprStmt(FuncCall("printInt", [Identifier("v")]))
            ])
        )
    ])
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_148():
    """Test 148: Switch statement with completely empty body"""
    # Switch rỗng hợp lệ và luồng điều khiển nhảy thẳng qua[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(5)),
                SwitchStmt(Identifier("x"), [], None),
                ExprStmt(FuncCall("printString", [StringLiteral("Done")]))
            ])
        )
    ])
    expected = "Done"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_149():
    """Test 149: Switch statement evaluating an arithmetic expression"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "a", IntLiteral(2)),
                VarDecl(IntType(), "b", IntLiteral(3)),
                SwitchStmt(
                    BinaryOp(Identifier("a"), "*", Identifier("b")), # evaluates to 6
                    [
                        CaseStmt(IntLiteral(5), [ExprStmt(FuncCall("printInt", [IntLiteral(5)])), BreakStmt()]),
                        CaseStmt(IntLiteral(6), [ExprStmt(FuncCall("printInt", [IntLiteral(6)])), BreakStmt()])
                    ],
                    None
                )
            ])
        )
    ])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_150():
    """Test 150: Assigning multiple struct variables"""
    ast = Program([
        StructDecl("Pair", [VarDecl(IntType(), "a", None), VarDecl(IntType(), "b", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Pair"), "p1", StructLiteral([IntLiteral(1), IntLiteral(2)])),
                VarDecl(StructType("Pair"), "p2", StructLiteral([IntLiteral(0), IntLiteral(0)])),
                VarDecl(StructType("Pair"), "p3", StructLiteral([IntLiteral(0), IntLiteral(0)])),
                ExprStmt(AssignExpr(Identifier("p3"), AssignExpr(Identifier("p2"), Identifier("p1")))),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p3"), "b")]))
            ])
        )
    ])
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_151():
    """Test 151: Auto type inferred from another inferred variable"""
    # Suy diễn kiểu dây chuyền: a (int) -> b (int) -> c (int)[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "a", IntLiteral(42)),
                VarDecl(None, "b", Identifier("a")),
                VarDecl(None, "c", Identifier("b")),
                ExprStmt(FuncCall("printInt", [Identifier("c")]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_152():
    """Test 152: If-Else with ExprStmt directly (no BlockStmt)"""
    # Kiểm tra mã sinh ra có nhảy đúng nhãn khi thân if/else chỉ là 1 lệnh đơn
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(10), ">", IntLiteral(20)),
                    ExprStmt(FuncCall("printString", [StringLiteral("A")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("B")]))
                )
            ])
        )
    ])
    expected = "B"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_153():
    """Test 153: Function returning float assigned to auto"""
    ast = Program([
        FuncDecl(FloatType(), "get_pi", [], BlockStmt([ReturnStmt(FloatLiteral(3.14))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "pi", FuncCall("get_pi", [])),
                ExprStmt(FuncCall("printFloat", [Identifier("pi")]))
            ])
        )
    ])
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_154():
    """Test 154: Right-associativity of assignment in complex expression"""
    # x = y = 5 + 2 -> x = (y = 7)[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", None),
                VarDecl(IntType(), "y", None),
                ExprStmt(AssignExpr(Identifier("x"), AssignExpr(Identifier("y"), BinaryOp(IntLiteral(5), "+", IntLiteral(2))))),
                ExprStmt(FuncCall("printInt", [Identifier("x")])),
                ExprStmt(FuncCall("printInt", [Identifier("y")]))
            ])
        )
    ])
    expected = "77"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_155():
    """Test 155: Boolean logic inside function return statement"""
    ast = Program([
        FuncDecl(
            IntType(),
            "is_valid",
            [Param(IntType(), "val")],
            BlockStmt([
                ReturnStmt(BinaryOp(BinaryOp(Identifier("val"), ">", IntLiteral(0)), "&&", BinaryOp(Identifier("val"), "<", IntLiteral(10))))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("is_valid", [IntLiteral(5)])])),
                ExprStmt(FuncCall("printInt", [FuncCall("is_valid", [IntLiteral(15)])]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_156():
    """Test 156: Deeply nested function calls f(g(h(x)))"""
    ast = Program([
        FuncDecl(IntType(), "add1", [Param(IntType(), "n")], BlockStmt([ReturnStmt(BinaryOp(Identifier("n"), "+", IntLiteral(1)))])),
        FuncDecl(IntType(), "mul2", [Param(IntType(), "n")], BlockStmt([ReturnStmt(BinaryOp(Identifier("n"), "*", IntLiteral(2)))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    FuncCall("add1", [
                        FuncCall("mul2", [
                            FuncCall("add1", [IntLiteral(3)]) # (3+1)*2 + 1 = 9
                        ])
                    ])
                ]))
            ])
        )
    ])
    expected = "9"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_157():
    """Test 157: Loop condition controlled by Boolean NOT"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "flag", IntLiteral(0)),
                VarDecl(IntType(), "count", IntLiteral(0)),
                WhileStmt(
                    PrefixOp("!", Identifier("flag")),
                    BlockStmt([
                        ExprStmt(AssignExpr(Identifier("count"), BinaryOp(Identifier("count"), "+", IntLiteral(1)))),
                        IfStmt(
                            BinaryOp(Identifier("count"), "==", IntLiteral(3)),
                            ExprStmt(AssignExpr(Identifier("flag"), IntLiteral(1))),
                            None
                        )
                    ])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("count")]))
            ])
        )
    ])
    expected = "3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_158():
    """Test 158: Arithmetic with logical operators (TyC treats them as strict Int operations)"""
    # (1 && 1) + (1 || 0) -> 1 + 1 = 2[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(
                        BinaryOp(IntLiteral(1), "&&", IntLiteral(1)),
                        "+",
                        BinaryOp(IntLiteral(1), "||", IntLiteral(0))
                    )
                ]))
            ])
        )
    ])
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_159():
    """Test 159: Struct member used in loop condition"""
    ast = Program([
        StructDecl("Limit", [VarDecl(IntType(), "max", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Limit"), "lim", StructLiteral([IntLiteral(3)])),
                VarDecl(IntType(), "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", MemberAccess(Identifier("lim"), "max")),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                    ])
                )
            ])
        )
    ])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_160():
    """Test 160: Comprehensive Algorithm - Greatest Common Divisor (GCD)"""
    ast = Program([
        FuncDecl(
            IntType(),
            "gcd",
            [Param(IntType(), "a"), Param(IntType(), "b")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("b"), "==", IntLiteral(0)),
                    ReturnStmt(Identifier("a")),
                    ReturnStmt(FuncCall("gcd", [Identifier("b"), BinaryOp(Identifier("a"), "%", Identifier("b"))]))
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("gcd", [IntLiteral(48), IntLiteral(18)])])) # GCD(48, 18) = 6
            ])
        )
    ])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_161():
    """Test 161: Left-associativity of Division and Multiplication"""
    # a / b * c -> (a / b) * c[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "res", BinaryOp(BinaryOp(IntLiteral(20), "/", IntLiteral(4)), "*", IntLiteral(2))),
                ExprStmt(FuncCall("printInt", [Identifier("res")])) # (20 / 4) * 2 = 10
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_162():
    """Test 162: Nested Struct Literal Initialization"""
    ast = Program([
        StructDecl("Point", [VarDecl(IntType(), "x", None), VarDecl(IntType(), "y", None)]),
        StructDecl("Rect", [VarDecl(StructType("Point"), "top_left", None), VarDecl(StructType("Point"), "bottom_right", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Rect"), "r", StructLiteral([
                    StructLiteral([IntLiteral(0), IntLiteral(10)]),
                    StructLiteral([IntLiteral(10), IntLiteral(0)])
                ])),
                ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(Identifier("r"), "bottom_right"), "x")]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_163():
    """Test 163: Logical Precedence && over || without parenthesis"""
    # 0 || 1 && 0 -> 0 || (1 && 0) -> 0 || 0 -> 0[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(0), "||", BinaryOp(IntLiteral(1), "&&", IntLiteral(0))),
                    ExprStmt(FuncCall("printString", [StringLiteral("True")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("False")]))
                )
            ])
        )
    ])
    expected = "False"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_164():
    """Test 164: Postfix decrement in while condition"""
    # x-- > 0 sẽ đánh giá x > 0 trước, sau đó x giảm đi 1[cite: 3, 4]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(3)),
                WhileStmt(
                    BinaryOp(PostfixOp("--", Identifier("x")), ">", IntLiteral(0)),
                    ExprStmt(FuncCall("printInt", [Identifier("x")]))
                )
            ])
        )
    ])
    expected = "210" # Lần 1: 3>0(T), x=2, in 2. Lần 2: 2>0(T), x=1, in 1. Lần 3: 1>0(T), x=0, in 0. Lần 4: 0>0(F), dừng.
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_165():
    """Test 165: Cascading If-Else If-Else"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "score", IntLiteral(75)),
                IfStmt(
                    BinaryOp(Identifier("score"), ">=", IntLiteral(90)),
                    ExprStmt(FuncCall("printString", [StringLiteral("A")])),
                    IfStmt(
                        BinaryOp(Identifier("score"), ">=", IntLiteral(80)),
                        ExprStmt(FuncCall("printString", [StringLiteral("B")])),
                        IfStmt(
                            BinaryOp(Identifier("score"), ">=", IntLiteral(70)),
                            ExprStmt(FuncCall("printString", [StringLiteral("C")])),
                            ExprStmt(FuncCall("printString", [StringLiteral("D")]))
                        )
                    )
                )
            ])
        )
    ])
    expected = "C"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_166():
    """Test 166: Integer division truncation"""
    # Phép chia số nguyên trong máy ảo JVM sẽ chặt bỏ phần thập phân[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(14), "/", IntLiteral(5))])), # 14 / 5 = 2
                ExprStmt(FuncCall("printInt", [BinaryOp(PrefixOp("-", IntLiteral(14)), "/", IntLiteral(5))])) # -14 / 5 = -2
            ])
        )
    ])
    expected = "2-2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_167():
    """Test 167: Auto variable initialized with Struct"""
    # auto suy diễn kiểu Struct và copy giá trị[cite: 3]
    ast = Program([
        StructDecl("Data", [VarDecl(IntType(), "val", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Data"), "d1", StructLiteral([IntLiteral(99)])),
                VarDecl(None, "d2", Identifier("d1")),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("d2"), "val")]))
            ])
        )
    ])
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_168():
    """Test 168: Passing expressions as function arguments"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "print_sum",
            [Param(IntType(), "a"), Param(IntType(), "b")],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [BinaryOp(Identifier("a"), "+", Identifier("b"))]))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("print_sum", [
                    BinaryOp(IntLiteral(10), "*", IntLiteral(2)), # 20
                    BinaryOp(IntLiteral(30), "/", IntLiteral(3))  # 10
                ]))
            ])
        )
    ])
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_169():
    """Test 169: Complex condition with Negation and Parentheses"""
    # !(a == b) equivalent to a != b[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "a", IntLiteral(5)),
                VarDecl(IntType(), "b", IntLiteral(5)),
                IfStmt(
                    PrefixOp("!", BinaryOp(Identifier("a"), "==", Identifier("b"))),
                    ExprStmt(FuncCall("printString", [StringLiteral("Diff")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("Same")]))
                )
            ])
        )
    ])
    expected = "Same"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_170():
    """Test 170: Switch with negative case labels"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "val", PrefixOp("-", IntLiteral(2))),
                SwitchStmt(
                    Identifier("val"),
                    [
                        CaseStmt(PrefixOp("-", IntLiteral(1)), [ExprStmt(FuncCall("printString", [StringLiteral("Neg1")])), BreakStmt()]),
                        CaseStmt(PrefixOp("-", IntLiteral(2)), [ExprStmt(FuncCall("printString", [StringLiteral("Neg2")])), BreakStmt()]),
                    ],
                    None
                )
            ])
        )
    ])
    expected = "Neg2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_171():
    """Test 171: Modifying parameter does not affect caller argument"""
    # Pass by value (truyền tham trị) cho kiểu nguyên thủy[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "try_modify",
            [Param(IntType(), "x")],
            BlockStmt([
                ExprStmt(AssignExpr(Identifier("x"), IntLiteral(999)))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "val", IntLiteral(10)),
                ExprStmt(FuncCall("try_modify", [Identifier("val")])),
                ExprStmt(FuncCall("printInt", [Identifier("val")]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_172():
    """Test 172: Nested loop break and continue combo"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(0)),
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        ForStmt(
                            VarDecl(IntType(), "j", IntLiteral(0)),
                            BinaryOp(Identifier("j"), "<", IntLiteral(3)),
                            AssignExpr(Identifier("j"), BinaryOp(Identifier("j"), "+", IntLiteral(1))),
                            BlockStmt([
                                IfStmt(BinaryOp(Identifier("j"), "==", IntLiteral(1)), ContinueStmt(), None),
                                IfStmt(BinaryOp(Identifier("j"), "==", IntLiteral(2)), BreakStmt(), None),
                                ExprStmt(FuncCall("printInt", [Identifier("j")]))
                            ])
                        )
                    ])
                )
            ])
        )
    ])
    expected = "000" # Mỗi vòng lặp i, j chỉ in 0, 1 bị continue, 2 bị break
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_173():
    """Test 173: Return inside For loop"""
    ast = Program([
        FuncDecl(
            IntType(),
            "search",
            [Param(IntType(), "target")],
            BlockStmt([
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(1)),
                    BinaryOp(Identifier("i"), "<=", IntLiteral(5)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        IfStmt(
                            BinaryOp(Identifier("i"), "==", Identifier("target")),
                            ReturnStmt(Identifier("i")),
                            None
                        )
                    ])
                ),
                ReturnStmt(PrefixOp("-", IntLiteral(1)))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("search", [IntLiteral(3)])])),
                ExprStmt(FuncCall("printInt", [FuncCall("search", [IntLiteral(9)])]))
            ])
        )
    ])
    expected = "3-1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_174():
    """Test 174: Assignment chain with Struct member"""
    ast = Program([
        StructDecl("Box", [VarDecl(IntType(), "v", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Box"), "b1", StructLiteral([IntLiteral(0)])),
                VarDecl(IntType(), "x", IntLiteral(0)),
                VarDecl(IntType(), "y", IntLiteral(0)),
                ExprStmt(AssignExpr(Identifier("x"), AssignExpr(Identifier("y"), AssignExpr(MemberAccess(Identifier("b1"), "v"), IntLiteral(42))))),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_175():
    """Test 175: Inferred Return Type implicitly converted to Void if empty"""
    # Trình biên dịch TyC sẽ coi hàm không có return hoặc chỉ có return; là VoidType[cite: 3]
    ast = Program([
        FuncDecl(
            None,
            "do_nothing",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("Done")])),
                ReturnStmt(None)
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("do_nothing", []))
            ])
        )
    ])
    expected = "Done"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_176():
    """Test 176: Variable declarations interspersed with statements"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "a", IntLiteral(1)),
                ExprStmt(FuncCall("printInt", [Identifier("a")])),
                VarDecl(IntType(), "b", IntLiteral(2)),
                ExprStmt(FuncCall("printInt", [Identifier("b")]))
            ])
        )
    ])
    expected = "12"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_177():
    """Test 177: Arithmetic precedence forcing early evaluation"""
    # (a + b) * (c - d) -> 5 * 10 = 50[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(
                        BinaryOp(IntLiteral(2), "+", IntLiteral(3)),
                        "*",
                        BinaryOp(IntLiteral(15), "-", IntLiteral(5))
                    )
                ]))
            ])
        )
    ])
    expected = "50"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_178():
    """Test 178: Prefix Increment embedded in complex logic"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(0)),
                IfStmt(
                    BinaryOp(PrefixOp("++", Identifier("x")), "==", IntLiteral(1)),
                    ExprStmt(FuncCall("printString", [StringLiteral("Inc")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("Fail")]))
                )
            ])
        )
    ])
    expected = "Inc"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_179():
    """Test 179: Multiple Case statements sharing same block explicitly"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(3)),
                SwitchStmt(
                    Identifier("x"),
                    [
                        CaseStmt(IntLiteral(1), []),
                        CaseStmt(IntLiteral(2), []),
                        CaseStmt(IntLiteral(3), [ExprStmt(FuncCall("printString", [StringLiteral("Found")])), BreakStmt()])
                    ],
                    None
                )
            ])
        )
    ])
    expected = "Found"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_180():
    """Test 180: Comprehensive Algorithm - Iterative Fibonacci"""
    ast = Program([
        FuncDecl(
            IntType(),
            "fib_iter",
            [Param(IntType(), "n")],
            BlockStmt([
                IfStmt(BinaryOp(Identifier("n"), "<=", IntLiteral(1)), ReturnStmt(Identifier("n")), None),
                VarDecl(IntType(), "a", IntLiteral(0)),
                VarDecl(IntType(), "b", IntLiteral(1)),
                VarDecl(IntType(), "c", IntLiteral(0)),
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(2)),
                    BinaryOp(Identifier("i"), "<=", Identifier("n")),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        ExprStmt(AssignExpr(Identifier("c"), BinaryOp(Identifier("a"), "+", Identifier("b")))),
                        ExprStmt(AssignExpr(Identifier("a"), Identifier("b"))),
                        ExprStmt(AssignExpr(Identifier("b"), Identifier("c")))
                    ])
                ),
                ReturnStmt(Identifier("b"))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("fib_iter", [IntLiteral(7)])])) # Fib(7) = 13
            ])
        )
    ])
    expected = "13"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_181():
    """Test 181: Return statement inside Switch case"""
    ast = Program([
        FuncDecl(
            IntType(),
            "get_code",
            [Param(IntType(), "val")],
            BlockStmt([
                SwitchStmt(
                    Identifier("val"),
                    [
                        CaseStmt(IntLiteral(1), [ReturnStmt(IntLiteral(100))]),
                        CaseStmt(IntLiteral(2), [ReturnStmt(IntLiteral(200))])
                    ],
                    DefaultStmt([ReturnStmt(IntLiteral(404))])
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("get_code", [IntLiteral(2)])]))
            ])
        )
    ])
    expected = "200"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_182():
    """Test 182: Postfix increment on a struct member"""
    # p.x++ -> truy cập struct member sau đó áp dụng phép toán hậu tố[cite: 3]
    ast = Program([
        StructDecl("Point", [VarDecl(IntType(), "x", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Point"), "p", StructLiteral([IntLiteral(10)])),
                VarDecl(IntType(), "y", PostfixOp("++", MemberAccess(Identifier("p"), "x"))),
                ExprStmt(FuncCall("printInt", [Identifier("y")])), # y nhận giá trị cũ 10
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p"), "x")])) # p.x tăng lên 11
            ])
        )
    ])
    expected = "1011"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_183():
    """Test 183: Infinite For Loop `for(;;)` with internal break"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                ForStmt(
                    None, None, None, # for (;;)
                    BlockStmt([
                        IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(3)), BreakStmt(), None),
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                    ])
                )
            ])
        )
    ])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_184():
    """Test 184: Logical AND/OR mixed precedence without parentheses"""
    # a || b && c -> a || (b && c)[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(1), "||", BinaryOp(IntLiteral(0), "&&", IntLiteral(1))),
                    ExprStmt(FuncCall("printString", [StringLiteral("T")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("F")]))
                )
            ])
        )
    ])
    expected = "T"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_185():
    """Test 185: Left-Associativity of Subtraction"""
    # 10 - 5 - 2 = (10 - 5) - 2 = 3[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(BinaryOp(IntLiteral(10), "-", IntLiteral(5)), "-", IntLiteral(2))
                ]))
            ])
        )
    ])
    expected = "3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_186():
    """Test 186: Nested prefix and postfix mixed in arithmetic"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(5)),
                VarDecl(IntType(), "y", IntLiteral(10)),
                VarDecl(IntType(), "res", BinaryOp(PrefixOp("++", Identifier("x")), "+", PostfixOp("--", Identifier("y")))),
                ExprStmt(FuncCall("printInt", [Identifier("res")])) # (++x) + (y--) -> 6 + 10 = 16
            ])
        )
    ])
    expected = "16"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_187():
    """Test 187: Accessing Struct field immediately from function call"""
    # get_data().id -> Hợp lệ và phải thao tác stack kỹ lưỡng[cite: 3, 4]
    ast = Program([
        StructDecl("Data", [VarDecl(IntType(), "id", None)]),
        FuncDecl(StructType("Data"), "get_data", [], BlockStmt([ReturnStmt(StructLiteral([IntLiteral(777)]))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [MemberAccess(FuncCall("get_data", []), "id")]))
            ])
        )
    ])
    expected = "777"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_188():
    """Test 188: Dangling Else problem explicitly verified via indentation"""
    # Else bind to nearest If[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(0)),
                IfStmt(
                    BinaryOp(Identifier("x"), "==", IntLiteral(0)),
                    IfStmt(
                        BinaryOp(Identifier("x"), "==", IntLiteral(1)),
                        ExprStmt(FuncCall("printString", [StringLiteral("A")])),
                        ExprStmt(FuncCall("printString", [StringLiteral("B")])) # Nearest Else
                    ),
                    ExprStmt(FuncCall("printString", [StringLiteral("C")]))
                )
            ])
        )
    ])
    expected = "B"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_189():
    """Test 189: String variable reassignment"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StringType(), "msg", StringLiteral("Hello")),
                ExprStmt(AssignExpr(Identifier("msg"), StringLiteral("World"))),
                ExprStmt(FuncCall("printString", [Identifier("msg")]))
            ])
        )
    ])
    expected = "World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_190():
    """Test 190: Auto inference from float and int arithmetic causing Float result"""
    # auto a = 5 + 3.14 -> a is Float[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "res", BinaryOp(IntLiteral(5), "+", FloatLiteral(2.5))),
                ExprStmt(FuncCall("printFloat", [Identifier("res")]))
            ])
        )
    ])
    expected = "7.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_191():
    """Test 191: Short-circuit protecting against modulo by zero"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(0)),
                IfStmt(
                    BinaryOp(BinaryOp(Identifier("x"), "!=", IntLiteral(0)), "&&", BinaryOp(BinaryOp(IntLiteral(10), "%", Identifier("x")), "==", IntLiteral(0))),
                    ExprStmt(FuncCall("printString", [StringLiteral("Divisible")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("Safe")]))
                )
            ])
        )
    ])
    expected = "Safe"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_192():
    """Test 192: Implicit conversion of Relational Result inside PrintInt"""
    # (a > b) -> JVM push 0 or 1[cite: 3]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(10), ">", IntLiteral(5))])),
                ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(10), "<", IntLiteral(5))]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_193():
    """Test 193: Nested Blocks Shadowing Function Parameters"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "func",
            [Param(IntType(), "p")],
            BlockStmt([
                BlockStmt([
                    VarDecl(IntType(), "p", IntLiteral(99)),
                    ExprStmt(FuncCall("printInt", [Identifier("p")]))
                ]),
                ExprStmt(FuncCall("printInt", [Identifier("p")]))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("func", [IntLiteral(10)]))
            ])
        )
    ])
    expected = "9910"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_194():
    """Test 194: Void function implicit return handling"""
    ast = Program([
        FuncDecl(VoidType(), "empty_func", [], BlockStmt([])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("empty_func", [])),
                ExprStmt(FuncCall("printString", [StringLiteral("Done")]))
            ])
        )
    ])
    expected = "Done"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_195():
    """Test 195: Float unary minus chaining"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(FloatType(), "f", FloatLiteral(3.14)),
                ExprStmt(FuncCall("printFloat", [PrefixOp("-", PrefixOp("-", Identifier("f")))]))
            ])
        )
    ])
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_196():
    """Test 196: Struct assignments returning right-hand side value"""
    # Assignment biểu thức Struct trả về Struct[cite: 3, 4]
    ast = Program([
        StructDecl("S", [VarDecl(IntType(), "v", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("S"), "s1", StructLiteral([IntLiteral(10)])),
                VarDecl(StructType("S"), "s2", StructLiteral([IntLiteral(0)])),
                VarDecl(StructType("S"), "s3", None),
                ExprStmt(AssignExpr(Identifier("s3"), AssignExpr(Identifier("s2"), Identifier("s1")))),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("s3"), "v")]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_197():
    """Test 197: Complex Fall-through Switch-Case with Variable Assignments"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "flag", IntLiteral(2)),
                VarDecl(IntType(), "res", IntLiteral(0)),
                SwitchStmt(
                    Identifier("flag"),
                    [
                        CaseStmt(IntLiteral(1), [ExprStmt(AssignExpr(Identifier("res"), BinaryOp(Identifier("res"), "+", IntLiteral(1))))]),
                        CaseStmt(IntLiteral(2), [ExprStmt(AssignExpr(Identifier("res"), BinaryOp(Identifier("res"), "+", IntLiteral(10))))]),
                        CaseStmt(IntLiteral(3), [ExprStmt(AssignExpr(Identifier("res"), BinaryOp(Identifier("res"), "+", IntLiteral(100))))])
                    ],
                    None
                ),
                ExprStmt(FuncCall("printInt", [Identifier("res")]))
            ])
        )
    ])
    expected = "110" # flag = 2 -> chạy case 2 (+10) -> rớt xuống case 3 (+100) = 110
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_198():
    """Test 198: Multiple function calls in print sequence maintaining evaluation order"""
    ast = Program([
        FuncDecl(IntType(), "p1", [], BlockStmt([ExprStmt(FuncCall("printInt", [IntLiteral(1)])), ReturnStmt(IntLiteral(0))])),
        FuncDecl(IntType(), "p2", [], BlockStmt([ExprStmt(FuncCall("printInt", [IntLiteral(2)])), ReturnStmt(IntLiteral(0))])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(BinaryOp(FuncCall("p1", []), "+", FuncCall("p2", [])))
        ]))
    ])
    expected = "12"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_199():
    """Test 199: Local Variable declarations separated by assignments"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(1)),
                ExprStmt(AssignExpr(Identifier("x"), BinaryOp(Identifier("x"), "+", IntLiteral(1)))),
                VarDecl(IntType(), "y", Identifier("x")),
                ExprStmt(FuncCall("printInt", [Identifier("y")]))
            ])
        )
    ])
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_200():
    """Test 200: Ultimate Integration Algorithm - Sum of Digits"""
    ast = Program([
        FuncDecl(
            IntType(),
            "sum_of_digits",
            [Param(IntType(), "n")],
            BlockStmt([
                VarDecl(IntType(), "sum", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("n"), ">", IntLiteral(0)),
                    BlockStmt([
                        ExprStmt(AssignExpr(Identifier("sum"), BinaryOp(Identifier("sum"), "+", BinaryOp(Identifier("n"), "%", IntLiteral(10))))),
                        ExprStmt(AssignExpr(Identifier("n"), BinaryOp(Identifier("n"), "/", IntLiteral(10))))
                    ])
                ),
                ReturnStmt(Identifier("sum"))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("sum_of_digits", [IntLiteral(12345)])])) # 1+2+3+4+5 = 15
            ])
        )
    ])
    expected = "15"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_201():
    """Test 201: Short-circuit && avoiding division by zero in While loop"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(5)),
                WhileStmt(
                    BinaryOp(BinaryOp(Identifier("x"), ">", IntLiteral(0)), "&&", BinaryOp(BinaryOp(IntLiteral(10), "/", Identifier("x")), ">", IntLiteral(0))),
                    BlockStmt([
                        ExprStmt(AssignExpr(Identifier("x"), BinaryOp(Identifier("x"), "-", IntLiteral(1))))
                    ])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_202():
    """Test 202: Struct reassignment and member modification isolation"""
    ast = Program([
        StructDecl("Config", [VarDecl(IntType(), "timeout", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Config"), "c1", StructLiteral([IntLiteral(30)])),
                VarDecl(StructType("Config"), "c2", StructLiteral([IntLiteral(0)])),
                ExprStmt(AssignExpr(Identifier("c2"), Identifier("c1"))),
                ExprStmt(AssignExpr(MemberAccess(Identifier("c2"), "timeout"), IntLiteral(60))),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("c1"), "timeout")])),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("c2"), "timeout")]))
            ])
        )
    ])
    expected = "3060"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_203():
    """Test 203: Switch-case with positive and negative constant expressions"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "v", PrefixOp("-", IntLiteral(3))),
                SwitchStmt(
                    Identifier("v"),
                    [
                        CaseStmt(BinaryOp(IntLiteral(1), "-", IntLiteral(4)), [ExprStmt(FuncCall("printString", [StringLiteral("Minus3")])), BreakStmt()]),
                        CaseStmt(IntLiteral(3), [ExprStmt(FuncCall("printString", [StringLiteral("Plus3")])), BreakStmt()])
                    ],
                    DefaultStmt([ExprStmt(FuncCall("printString", [StringLiteral("None")])), BreakStmt()])
                )
            ])
        )
    ])
    expected = "Minus3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_204():
    """Test 204: Auto variable storing result of complex logic expression"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "is_valid", BinaryOp(BinaryOp(IntLiteral(10), ">", IntLiteral(5)), "||", BinaryOp(IntLiteral(5), "<", IntLiteral(2)))),
                ExprStmt(FuncCall("printInt", [Identifier("is_valid")]))
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_205():
    """Test 205: Nested While loop inside an Else block"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "flag", IntLiteral(0)),
                IfStmt(
                    BinaryOp(Identifier("flag"), "==", IntLiteral(1)),
                    ExprStmt(FuncCall("printString", [StringLiteral("True")])),
                    BlockStmt([
                        VarDecl(IntType(), "i", IntLiteral(0)),
                        WhileStmt(
                            BinaryOp(Identifier("i"), "<", IntLiteral(2)),
                            BlockStmt([
                                ExprStmt(FuncCall("printInt", [Identifier("i")])),
                                ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                            ])
                        )
                    ])
                )
            ])
        )
    ])
    expected = "01"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_206():
    """Test 206: Logical NOT applied to a relational expression inside assignment"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "res", IntLiteral(0)),
                ExprStmt(AssignExpr(Identifier("res"), PrefixOp("!", BinaryOp(IntLiteral(10), "==", IntLiteral(10))))),
                ExprStmt(FuncCall("printInt", [Identifier("res")]))
            ])
        )
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_207():
    """Test 207: For loop breaking based on an internal condition without loop condition"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "sum", IntLiteral(0)),
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(1)),
                    None,
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        IfStmt(BinaryOp(Identifier("i"), ">", IntLiteral(3)), BreakStmt(), None),
                        ExprStmt(AssignExpr(Identifier("sum"), BinaryOp(Identifier("sum"), "+", Identifier("i"))))
                    ])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("sum")]))
            ])
        )
    ])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_208():
    """Test 208: Break inside While inside Switch"""
    # Break inside while should only break the while, not the switch[cite: 6]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "val", IntLiteral(1)),
                SwitchStmt(
                    Identifier("val"),
                    [
                        CaseStmt(IntLiteral(1), [
                            BlockStmt([
                                VarDecl(IntType(), "i", IntLiteral(0)),
                                WhileStmt(
                                    BinaryOp(Identifier("i"), "<", IntLiteral(5)),
                                    BlockStmt([
                                        IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(1)), BreakStmt(), None),
                                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                                    ])
                                ),
                                ExprStmt(FuncCall("printInt", [Identifier("i")]))
                            ]),
                            BreakStmt()
                        ])
                    ],
                    None
                )
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_209():
    """Test 209: Returning and passing String types"""
    ast = Program([
        FuncDecl(StringType(), "get_msg", [], BlockStmt([ReturnStmt(StringLiteral("Hello"))])),
        FuncDecl(VoidType(), "print_msg", [Param(StringType(), "m")], BlockStmt([ExprStmt(FuncCall("printString", [Identifier("m")]))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("print_msg", [FuncCall("get_msg", [])]))
            ])
        )
    ])
    expected = "Hello"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_210():
    """Test 210: Modulo with negative dividend and negative divisor"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(PrefixOp("-", IntLiteral(10)), "%", PrefixOp("-", IntLiteral(3)))
                ]))
            ])
        )
    ])
    expected = "-1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_211():
    """Test 211: Successive unary operations + - + -"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(5)),
                ExprStmt(FuncCall("printInt", [
                    PrefixOp("+", PrefixOp("-", PrefixOp("+", PrefixOp("-", Identifier("x")))))
                ]))
            ])
        )
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_212():
    """Test 212: Function parameters evaluated strictly Left-to-Right"""
    ast = Program([
        FuncDecl(IntType(), "a", [], BlockStmt([ExprStmt(FuncCall("printString", [StringLiteral("A")])), ReturnStmt(IntLiteral(1))])),
        FuncDecl(IntType(), "b", [], BlockStmt([ExprStmt(FuncCall("printString", [StringLiteral("B")])), ReturnStmt(IntLiteral(2))])),
        FuncDecl(VoidType(), "c", [Param(IntType(), "x"), Param(IntType(), "y")], BlockStmt([])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("c", [FuncCall("a", []), FuncCall("b", [])]))
            ])
        )
    ])
    expected = "AB"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_213():
    """Test 213: Prefix operator inside function arguments"""
    ast = Program([
        FuncDecl(VoidType(), "display", [Param(IntType(), "val")], BlockStmt([ExprStmt(FuncCall("printInt", [Identifier("val")]))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                ExprStmt(FuncCall("display", [PrefixOp("++", Identifier("x"))])),
                ExprStmt(FuncCall("display", [Identifier("x")]))
            ])
        )
    ])
    expected = "1111"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_214():
    """Test 214: Multiple Return inside Switch Cases"""
    ast = Program([
        FuncDecl(
            IntType(),
            "check",
            [Param(IntType(), "val")],
            BlockStmt([
                SwitchStmt(
                    Identifier("val"),
                    [
                        CaseStmt(IntLiteral(1), [ReturnStmt(IntLiteral(10))]),
                        CaseStmt(IntLiteral(2), [ReturnStmt(IntLiteral(20))])
                    ],
                    DefaultStmt([ReturnStmt(IntLiteral(30))])
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("check", [IntLiteral(2)])])),
                ExprStmt(FuncCall("printInt", [FuncCall("check", [IntLiteral(99)])]))
            ])
        )
    ])
    expected = "2030"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_215():
    """Test 215: For loop re-assigning an outer variable in init"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(99)),
                ForStmt(
                    AssignExpr(Identifier("i"), IntLiteral(0)),
                    BinaryOp(Identifier("i"), "<", IntLiteral(2)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")]))
                    ])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("i")]))
            ])
        )
    ])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_216():
    """Test 216: Shadowing function parameter and returning its original value? No, returns shadow."""
    ast = Program([
        FuncDecl(
            IntType(),
            "shadow_param",
            [Param(IntType(), "p")],
            BlockStmt([
                BlockStmt([
                    VarDecl(IntType(), "p", IntLiteral(42)),
                    ExprStmt(FuncCall("printInt", [Identifier("p")]))
                ]),
                ReturnStmt(Identifier("p"))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("shadow_param", [IntLiteral(10)])]))
            ])
        )
    ])
    expected = "4210" # In 42 ở trong block, ra ngoài block lấy lại p của tham số là 10[cite: 6].
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_217():
    """Test 217: Associativity of Subtraction and Addition (a - b + c - d)"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "res", BinaryOp(BinaryOp(BinaryOp(IntLiteral(10), "-", IntLiteral(5)), "+", IntLiteral(2)), "-", IntLiteral(3))),
                ExprStmt(FuncCall("printInt", [Identifier("res")]))
            ])
        )
    ])
    expected = "4" # ((10 - 5) + 2) - 3 = 4
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_218():
    """Test 218: Nested Structs value updates"""
    ast = Program([
        StructDecl("Inner", [VarDecl(IntType(), "val", None)]),
        StructDecl("Outer", [VarDecl(StructType("Inner"), "in1", None), VarDecl(StructType("Inner"), "in2", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Outer"), "obj", StructLiteral([StructLiteral([IntLiteral(1)]), StructLiteral([IntLiteral(2)])])),
                ExprStmt(AssignExpr(MemberAccess(MemberAccess(Identifier("obj"), "in1"), "val"), IntLiteral(99))),
                ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(Identifier("obj"), "in1"), "val")])),
                ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(Identifier("obj"), "in2"), "val")]))
            ])
        )
    ])
    expected = "992"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_219():
    """Test 219: Simple Recursive Factorial with early return validation"""
    ast = Program([
        FuncDecl(
            IntType(),
            "fact",
            [Param(IntType(), "n")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("n"), "==", IntLiteral(0)),
                    ReturnStmt(IntLiteral(1)),
                    None
                ),
                ReturnStmt(BinaryOp(Identifier("n"), "*", FuncCall("fact", [BinaryOp(Identifier("n"), "-", IntLiteral(1))])))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("fact", [IntLiteral(4)])]))
            ])
        )
    ])
    expected = "24"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_220():
    """Test 220: Void return interrupting loop evaluation"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "loop_and_exit",
            [],
            BlockStmt([
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(0)),
                    BinaryOp(Identifier("i"), "<", IntLiteral(10)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(2)), ReturnStmt(None), None)
                    ])
                ),
                ExprStmt(FuncCall("printString", [StringLiteral("Unreachable")]))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("loop_and_exit", []))
            ])
        )
    ])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_221():
    """Test 221: Break statement in nested For loop"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(0)),
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        ForStmt(
                            VarDecl(IntType(), "j", IntLiteral(0)),
                            BinaryOp(Identifier("j"), "<", IntLiteral(3)),
                            AssignExpr(Identifier("j"), BinaryOp(Identifier("j"), "+", IntLiteral(1))),
                            BlockStmt([
                                IfStmt(BinaryOp(Identifier("j"), "==", IntLiteral(1)), BreakStmt(), None),
                                ExprStmt(FuncCall("printInt", [Identifier("j")]))
                            ])
                        )
                    ])
                )
            ])
        )
    ])
    expected = "000" # Mỗi vòng lặp i, j chỉ in 0 rồi break
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_222():
    """Test 222: Complex boolean condition in If statement"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(5)),
                VarDecl(IntType(), "y", IntLiteral(10)),
                IfStmt(
                    BinaryOp(
                        BinaryOp(Identifier("x"), ">", IntLiteral(0)),
                        "&&",
                        PrefixOp("!", BinaryOp(Identifier("y"), "<", IntLiteral(5)))
                    ),
                    ExprStmt(FuncCall("printString", [StringLiteral("Valid")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("Invalid")]))
                )
            ])
        )
    ])
    expected = "Valid"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_223():
    """Test 223: Returning struct from nested if blocks"""
    ast = Program([
        StructDecl("Data", [VarDecl(IntType(), "value", None)]),
        FuncDecl(
            StructType("Data"),
            "process",
            [Param(IntType(), "code")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("code"), "==", IntLiteral(1)),
                    ReturnStmt(StructLiteral([IntLiteral(100)])),
                    IfStmt(
                        BinaryOp(Identifier("code"), "==", IntLiteral(2)),
                        ReturnStmt(StructLiteral([IntLiteral(200)])),
                        ReturnStmt(StructLiteral([IntLiteral(300)]))
                    )
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Data"), "res", FuncCall("process", [IntLiteral(2)])),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("res"), "value")]))
            ])
        )
    ])
    expected = "200"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_224():
    """Test 224: Floating point arithmetic with negative numbers"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(FloatType(), "a", FloatLiteral(-2.5)),
                VarDecl(FloatType(), "b", FloatLiteral(1.5)),
                ExprStmt(FuncCall("printFloat", [BinaryOp(Identifier("a"), "*", Identifier("b"))]))
            ])
        )
    ])
    expected = "-3.75"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_225():
    """Test 225: While loop with multiple conditions"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                VarDecl(IntType(), "j", IntLiteral(5)),
                WhileStmt(
                    BinaryOp(
                        BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                        "&&",
                        BinaryOp(Identifier("j"), ">", IntLiteral(0))
                    ),
                    BlockStmt([
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1)))),
                        ExprStmt(AssignExpr(Identifier("j"), BinaryOp(Identifier("j"), "-", IntLiteral(1))))
                    ])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("i")])),
                ExprStmt(FuncCall("printInt", [Identifier("j")]))
            ])
        )
    ])
    expected = "32"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_226():
    """Test 226: Switch statement with break inside nested if"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(1)),
                SwitchStmt(
                    Identifier("x"),
                    [
                        CaseStmt(IntLiteral(1), [
                            IfStmt(
                                BinaryOp(Identifier("x"), "==", IntLiteral(1)),
                                BreakStmt(),
                                None
                            ),
                            ExprStmt(FuncCall("printString", [StringLiteral("Unreachable")]))
                        ])
                    ],
                    None
                ),
                ExprStmt(FuncCall("printString", [StringLiteral("Done")]))
            ])
        )
    ])
    expected = "Done"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_227():
    """Test 227: Function call inside logical expression (Short-circuit test)"""
    ast = Program([
        FuncDecl(
            IntType(),
            "side_effect",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("Called")])),
                ReturnStmt(IntLiteral(1))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(1), "||", FuncCall("side_effect", [])),
                    ExprStmt(FuncCall("printString", [StringLiteral("True")])),
                    None
                )
            ])
        )
    ])
    expected = "True" # 'Called' is not printed due to short-circuit[cite: 6]
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_228():
    """Test 228: Struct assignment chaining"""
    ast = Program([
        StructDecl("Point", [VarDecl(IntType(), "x", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Point"), "p1", StructLiteral([IntLiteral(10)])),
                VarDecl(StructType("Point"), "p2", StructLiteral([IntLiteral(20)])),
                VarDecl(StructType("Point"), "p3", None),
                ExprStmt(AssignExpr(Identifier("p3"), AssignExpr(Identifier("p2"), Identifier("p1")))),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p3"), "x")]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_229():
    """Test 229: Unary operators sequence"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(5)),
                ExprStmt(FuncCall("printInt", [PrefixOp("-", PrefixOp("!", PrefixOp("!", Identifier("x"))))]))
            ])
        )
    ])
    expected = "-1" # !(!5) = !0 = 1, then -1
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_230():
    """Test 230: Nested ternary-like behavior using if-else and assignment"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                VarDecl(IntType(), "y", None),
                IfStmt(
                    BinaryOp(Identifier("x"), ">", IntLiteral(5)),
                    ExprStmt(AssignExpr(Identifier("y"), IntLiteral(1))),
                    ExprStmt(AssignExpr(Identifier("y"), IntLiteral(0)))
                ),
                ExprStmt(FuncCall("printInt", [Identifier("y")]))
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_231():
    """Test 231: Function returning string passed to printString"""
    ast = Program([
        FuncDecl(
            StringType(),
            "get_message",
            [],
            BlockStmt([
                ReturnStmt(StringLiteral("TestMessage"))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printString", [FuncCall("get_message", [])]))
            ])
        )
    ])
    expected = "TestMessage"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_232():
    """Test 232: Modulo operation with zero dividend"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(0), "%", IntLiteral(5))]))
            ])
        )
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_233():
    """Test 233: Logical AND sequence"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(BinaryOp(IntLiteral(1), "&&", IntLiteral(1)), "&&", IntLiteral(1)),
                    ExprStmt(FuncCall("printString", [StringLiteral("AllTrue")])),
                    None
                )
            ])
        )
    ])
    expected = "AllTrue"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_234():
    """Test 234: Re-declaring variable in inner scope"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                BlockStmt([
                    VarDecl(IntType(), "x", IntLiteral(20)),
                    ExprStmt(FuncCall("printInt", [Identifier("x")]))
                ]),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "2010"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_235():
    """Test 235: Fall-through behavior in switch statement"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(1)),
                SwitchStmt(
                    Identifier("x"),
                    [
                        CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printString", [StringLiteral("A")]))]),
                        CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printString", [StringLiteral("B")])), BreakStmt()])
                    ],
                    None
                )
            ])
        )
    ])
    expected = "AB" # Fall-through
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_236():
    """Test 236: Returning a value from a recursive struct parameter update"""
    ast = Program([
        StructDecl("Counter", [VarDecl(IntType(), "val", None)]),
        FuncDecl(
            IntType(),
            "increment",
            [Param(StructType("Counter"), "c"), Param(IntType(), "n")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("n"), "==", IntLiteral(0)),
                    ReturnStmt(MemberAccess(Identifier("c"), "val")),
                    BlockStmt([
                        ExprStmt(AssignExpr(MemberAccess(Identifier("c"), "val"), BinaryOp(MemberAccess(Identifier("c"), "val"), "+", IntLiteral(1)))),
                        ReturnStmt(FuncCall("increment", [Identifier("c"), BinaryOp(Identifier("n"), "-", IntLiteral(1))]))
                    ])
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Counter"), "my_counter", StructLiteral([IntLiteral(0)])),
                ExprStmt(FuncCall("printInt", [FuncCall("increment", [Identifier("my_counter"), IntLiteral(3)])]))
            ])
        )
    ])
    expected = "3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_237():
    """Test 237: Multiple nested unary minus operators"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", PrefixOp("-", PrefixOp("-", PrefixOp("-", IntLiteral(5))))),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "-5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_238():
    """Test 238: Switch statement with constant expression case"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(5)),
                SwitchStmt(
                    Identifier("x"),
                    [
                        CaseStmt(BinaryOp(IntLiteral(2), "+", IntLiteral(3)), [ExprStmt(FuncCall("printString", [StringLiteral("Match")])), BreakStmt()])
                    ],
                    None
                )
            ])
        )
    ])
    expected = "Match"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_239():
    """Test 239: Auto type inference for floating point operations"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "x", BinaryOp(FloatLiteral(5.0), "/", FloatLiteral(2.0))),
                ExprStmt(FuncCall("printFloat", [Identifier("x")]))
            ])
        )
    ])
    expected = "2.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_240():
    """Test 240: Comprehensive algorithm - Factorial (Iterative)"""
    ast = Program([
        FuncDecl(
            IntType(),
            "fact_iter",
            [Param(IntType(), "n")],
            BlockStmt([
                VarDecl(IntType(), "result", IntLiteral(1)),
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(1)),
                    BinaryOp(Identifier("i"), "<=", Identifier("n")),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        ExprStmt(AssignExpr(Identifier("result"), BinaryOp(Identifier("result"), "*", Identifier("i"))))
                    ])
                ),
                ReturnStmt(Identifier("result"))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("fact_iter", [IntLiteral(5)])])) # 5! = 120
            ])
        )
    ])
    expected = "120"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_241():
    """Test 241: Nested switch cases with break testing"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(1)),
                VarDecl(IntType(), "y", IntLiteral(2)),
                SwitchStmt(
                    Identifier("x"),
                    [
                        CaseStmt(IntLiteral(1), [
                            SwitchStmt(
                                Identifier("y"),
                                [
                                    CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printString", [StringLiteral("Nested Match")])), BreakStmt()])
                                ],
                                None
                            ),
                            BreakStmt()
                        ])
                    ],
                    None
                )
            ])
        )
    ])
    expected = "Nested Match"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_242():
    """Test 242: Division by a variable and assignment"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                VarDecl(IntType(), "y", IntLiteral(2)),
                ExprStmt(AssignExpr(Identifier("x"), BinaryOp(Identifier("x"), "/", Identifier("y")))),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_243():
    """Test 243: Function returning inferred variable"""
    ast = Program([
        FuncDecl(
            IntType(),
            "get_val",
            [],
            BlockStmt([
                VarDecl(None, "v", IntLiteral(42)),
                ReturnStmt(Identifier("v"))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("get_val", [])]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_244():
    """Test 244: Chained boolean expressions returning int values"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(
                        BinaryOp(IntLiteral(5), ">", IntLiteral(3)),
                        "==",
                        BinaryOp(IntLiteral(2), "<", IntLiteral(4))
                    )
                ])) # 1 == 1 -> 1
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_245():
    """Test 245: Prefix increment within an expression"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(5)),
                ExprStmt(FuncCall("printInt", [BinaryOp(PrefixOp("++", Identifier("x")), "+", IntLiteral(4))])) # 6 + 4 = 10
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_246():
    """Test 246: Accessing deeply nested struct members"""
    ast = Program([
        StructDecl("Level1", [VarDecl(IntType(), "val", None)]),
        StructDecl("Level2", [VarDecl(StructType("Level1"), "l1", None)]),
        StructDecl("Level3", [VarDecl(StructType("Level2"), "l2", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Level3"), "obj", StructLiteral([StructLiteral([StructLiteral([IntLiteral(99)])])])),
                ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(MemberAccess(Identifier("obj"), "l2"), "l1"), "val")]))
            ])
        )
    ])
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_247():
    """Test 247: Multiple logical NOT operations"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(0)),
                IfStmt(
                    PrefixOp("!", PrefixOp("!", PrefixOp("!", Identifier("x")))), # !(!(!0)) = !(!1) = !0 = 1
                    ExprStmt(FuncCall("printString", [StringLiteral("T")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("F")]))
                )
            ])
        )
    ])
    expected = "T"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_248():
    """Test 248: Assigning a logical result to a variable"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "res", BinaryOp(IntLiteral(10), "==", IntLiteral(10))),
                ExprStmt(FuncCall("printInt", [Identifier("res")]))
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_249():
    """Test 249: Testing auto variable with negative float literal"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "neg_f", PrefixOp("-", FloatLiteral(5.5))),
                ExprStmt(FuncCall("printFloat", [Identifier("neg_f")]))
            ])
        )
    ])
    expected = "-5.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_250():
    """Test 250: Comprehensive Algorithm - Fibonacci (Recursive)"""
    ast = Program([
        FuncDecl(
            IntType(),
            "fib_rec",
            [Param(IntType(), "n")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("n"), "<=", IntLiteral(1)),
                    ReturnStmt(Identifier("n")),
                    ReturnStmt(
                        BinaryOp(
                            FuncCall("fib_rec", [BinaryOp(Identifier("n"), "-", IntLiteral(1))]),
                            "+",
                            FuncCall("fib_rec", [BinaryOp(Identifier("n"), "-", IntLiteral(2))])
                        )
                    )
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("fib_rec", [IntLiteral(6)])])) # fib(6) = 8
            ])
        )
    ])
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_251():
    """Test 251: Struct initialization using function calls"""
    # Khởi tạo struct bằng kết quả trả về từ các hàm[cite: 6]
    ast = Program([
        StructDecl("Point", [VarDecl(IntType(), "x", None), VarDecl(IntType(), "y", None)]),
        FuncDecl(IntType(), "get_x", [], BlockStmt([ReturnStmt(IntLiteral(10))])),
        FuncDecl(IntType(), "get_y", [], BlockStmt([ReturnStmt(IntLiteral(20))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Point"), "p", StructLiteral([FuncCall("get_x", []), FuncCall("get_y", [])])),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p"), "x")])),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("p"), "y")]))
            ])
        )
    ])
    expected = "1020"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_252():
    """Test 252: Auto inference from struct member access"""
    # Suy diễn kiểu tự động từ một trường của struct[cite: 6]
    ast = Program([
        StructDecl("Data", [VarDecl(FloatType(), "val", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Data"), "d", StructLiteral([FloatLiteral(3.14)])),
                VarDecl(None, "inferred_val", MemberAccess(Identifier("d"), "val")),
                ExprStmt(FuncCall("printFloat", [Identifier("inferred_val")]))
            ])
        )
    ])
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_253():
    """Test 253: For loop with Continue inside a Switch Case"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(0)),
                    BinaryOp(Identifier("i"), "<", IntLiteral(4)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        SwitchStmt(
                            Identifier("i"),
                            [
                                CaseStmt(IntLiteral(2), [ContinueStmt()]) # Bỏ qua printInt khi i == 2
                            ],
                            None
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("i")]))
                    ])
                )
            ])
        )
    ])
    expected = "013"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_254():
    """Test 254: Nested Switch statements with independent breaks"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "outer", IntLiteral(1)),
                VarDecl(IntType(), "inner", IntLiteral(1)),
                SwitchStmt(
                    Identifier("outer"),
                    [
                        CaseStmt(IntLiteral(1), [
                            SwitchStmt(
                                Identifier("inner"),
                                [
                                    CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printString", [StringLiteral("In1")])), BreakStmt()]),
                                    CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printString", [StringLiteral("In2")])), BreakStmt()])
                                ],
                                None
                            ),
                            ExprStmt(FuncCall("printString", [StringLiteral("Out1")])),
                            BreakStmt()
                        ])
                    ],
                    None
                )
            ])
        )
    ])
    expected = "In1Out1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_255():
    """Test 255: If condition using chained assignment"""
    # if ((x = y) == 5)[cite: 6]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(0)),
                VarDecl(IntType(), "y", IntLiteral(5)),
                IfStmt(
                    BinaryOp(AssignExpr(Identifier("x"), Identifier("y")), "==", IntLiteral(5)),
                    ExprStmt(FuncCall("printString", [StringLiteral("Yes")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("No")]))
                )
            ])
        )
    ])
    expected = "Yes"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_256():
    """Test 256: While condition using Postfix operation"""
    # while (x-- > 0)[cite: 6]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(2)),
                WhileStmt(
                    BinaryOp(PostfixOp("--", Identifier("x")), ">", IntLiteral(0)),
                    ExprStmt(FuncCall("printInt", [Identifier("x")]))
                )
            ])
        )
    ])
    expected = "10" # Lần 1: 2 > 0 -> x = 1 -> In 1. Lần 2: 1 > 0 -> x = 0 -> In 0. Lần 3: 0 > 0 (False).
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_257():
    """Test 257: Logical AND short-circuit skipping function call that returns struct"""
    ast = Program([
        StructDecl("Dummy", [VarDecl(IntType(), "v", None)]),
        FuncDecl(
            StructType("Dummy"),
            "side_effect",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("Mutated")])),
                ReturnStmt(StructLiteral([IntLiteral(1)]))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(0), "&&", MemberAccess(FuncCall("side_effect", []), "v")),
                    ExprStmt(FuncCall("printString", [StringLiteral("T")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("F")]))
                )
            ])
        )
    ])
    expected = "F" # 'Mutated' không được in do ngắt mạch
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_258():
    """Test 258: Evaluating function parameters left to right with state mutation"""
    ast = Program([
        FuncDecl(
            IntType(),
            "modify",
            [Param(IntType(), "x")],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [Identifier("x")])),
                ReturnStmt(Identifier("x"))
            ])
        ),
        FuncDecl(VoidType(), "consume", [Param(IntType(), "a"), Param(IntType(), "b")], BlockStmt([])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("consume", [FuncCall("modify", [IntLiteral(1)]), FuncCall("modify", [IntLiteral(2)])]))
            ])
        )
    ])
    expected = "12"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_259():
    """Test 259: Recursive algorithm - Power calculation"""
    ast = Program([
        FuncDecl(
            IntType(),
            "power",
            [Param(IntType(), "base"), Param(IntType(), "exp")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("exp"), "==", IntLiteral(0)),
                    ReturnStmt(IntLiteral(1)),
                    ReturnStmt(BinaryOp(Identifier("base"), "*", FuncCall("power", [Identifier("base"), BinaryOp(Identifier("exp"), "-", IntLiteral(1))])))
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("power", [IntLiteral(2), IntLiteral(5)])])) # 2^5 = 32
            ])
        )
    ])
    expected = "32"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_260():
    """Test 260: Deeply nested member access and assignment"""
    ast = Program([
        StructDecl("L1", [VarDecl(IntType(), "a", None)]),
        StructDecl("L2", [VarDecl(StructType("L1"), "b", None)]),
        StructDecl("L3", [VarDecl(StructType("L2"), "c", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("L3"), "obj", StructLiteral([StructLiteral([StructLiteral([IntLiteral(0)])])])),
                ExprStmt(AssignExpr(MemberAccess(MemberAccess(MemberAccess(Identifier("obj"), "c"), "b"), "a"), IntLiteral(888))),
                ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(MemberAccess(Identifier("obj"), "c"), "b"), "a")]))
            ])
        )
    ])
    expected = "888"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_261():
    """Test 261: Modulo combinations with negatives"""
    # 10 % -3 = 1 (Trong Java, dấu của phép % lấy theo số bị chia)[cite: 6]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(10), "%", PrefixOp("-", IntLiteral(3)))]))
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_262():
    """Test 262: Mix of Relational >= and <="""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(BinaryOp(IntLiteral(5), ">=", IntLiteral(5)), "&&", BinaryOp(IntLiteral(4), "<=", IntLiteral(6))),
                    ExprStmt(FuncCall("printString", [StringLiteral("Pass")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("Fail")]))
                )
            ])
        )
    ])
    expected = "Pass"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_263():
    """Test 263: Function Call modifying external variable simulated with struct passing"""
    ast = Program([
        StructDecl("Wrapper", [VarDecl(IntType(), "val", None)]),
        FuncDecl(
            IntType(),
            "process",
            [Param(StructType("Wrapper"), "w")],
            BlockStmt([
                ReturnStmt(BinaryOp(MemberAccess(Identifier("w"), "val"), "*", IntLiteral(2)))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Wrapper"), "my_w", StructLiteral([IntLiteral(10)])),
                ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(5), "+", FuncCall("process", [Identifier("my_w")]))]))
            ])
        )
    ])
    expected = "25"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_264():
    """Test 264: Shadowing outer Struct variable with local Int variable"""
    ast = Program([
        StructDecl("A", [VarDecl(IntType(), "v", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("A"), "x", StructLiteral([IntLiteral(1)])),
                BlockStmt([
                    VarDecl(IntType(), "x", IntLiteral(99)),
                    ExprStmt(FuncCall("printInt", [Identifier("x")]))
                ]),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("x"), "v")]))
            ])
        )
    ])
    expected = "991"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_265():
    """Test 265: Prefix Increment on struct member"""
    ast = Program([
        StructDecl("Counter", [VarDecl(IntType(), "ticks", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Counter"), "c", StructLiteral([IntLiteral(0)])),
                ExprStmt(FuncCall("printInt", [PrefixOp("++", MemberAccess(Identifier("c"), "ticks"))])),
                ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("c"), "ticks")]))
            ])
        )
    ])
    expected = "11"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_266():
    """Test 266: Unary NOT (!) applied directly to an integer literal"""
    # !0 = 1, !5 = 0[cite: 6]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [PrefixOp("!", IntLiteral(0))])),
                ExprStmt(FuncCall("printInt", [PrefixOp("!", IntLiteral(5))]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_267():
    """Test 267: Complex arithmetic involving modulo and division"""
    # (a * b) / (c % d) + e = (10 * 2) / (7 % 4) + 1 = 20 / 3 + 1 = 6 + 1 = 7
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(
                        BinaryOp(
                            BinaryOp(IntLiteral(10), "*", IntLiteral(2)),
                            "/",
                            BinaryOp(IntLiteral(7), "%", IntLiteral(4))
                        ),
                        "+",
                        IntLiteral(1)
                    )
                ]))
            ])
        )
    ])
    expected = "7"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_268():
    """Test 268: Return inside an infinite For loop with complex condition inside"""
    ast = Program([
        FuncDecl(
            IntType(),
            "search_inf",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                ForStmt(
                    None, None, None,
                    BlockStmt([
                        IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(5)), ReturnStmt(Identifier("i")), None),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                    ])
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("search_inf", [])]))
            ])
        )
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_269():
    """Test 269: Nested If-Else returning different struct types? Not valid in TyC. Testing same struct type."""
    ast = Program([
        StructDecl("Val", [VarDecl(IntType(), "v", None)]),
        FuncDecl(
            StructType("Val"),
            "gen",
            [Param(IntType(), "flag")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("flag"), "==", IntLiteral(1)),
                    ReturnStmt(StructLiteral([IntLiteral(10)])),
                    ReturnStmt(StructLiteral([IntLiteral(20)]))
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [MemberAccess(FuncCall("gen", [IntLiteral(1)]), "v")])),
                ExprStmt(FuncCall("printInt", [MemberAccess(FuncCall("gen", [IntLiteral(0)]), "v")]))
            ])
        )
    ])
    expected = "1020"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_270():
    """Test 270: Relational operator combining Arithmetic"""
    # 5 + 2 > 3 * 2 -> 7 > 6 -> 1[cite: 6]
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(
                        BinaryOp(IntLiteral(5), "+", IntLiteral(2)),
                        ">",
                        BinaryOp(IntLiteral(3), "*", IntLiteral(2))
                    )
                ]))
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_271():
    """Test 271: Void function without explicit return at the end of block"""
    # CodeGen JVM tự động sinh lệnh return ở cuối hàm VoidType[cite: 6]
    ast = Program([
        FuncDecl(
            VoidType(),
            "no_return_func",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("AutoReturn")]))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("no_return_func", []))
            ])
        )
    ])
    expected = "AutoReturn"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_272():
    """Test 272: Floating point assignment cascading"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(FloatType(), "f1", None),
                VarDecl(FloatType(), "f2", None),
                ExprStmt(AssignExpr(Identifier("f1"), AssignExpr(Identifier("f2"), FloatLiteral(3.14)))),
                ExprStmt(FuncCall("printFloat", [Identifier("f1")]))
            ])
        )
    ])
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_273():
    """Test 273: Unary minus combined with parenthesis expression"""
    # -(10 - 20) = 10
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [PrefixOp("-", BinaryOp(IntLiteral(10), "-", IntLiteral(20)))]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_274():
    """Test 274: For loop ignoring the init block entirely"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(2)),
                ForStmt(
                    None,
                    BinaryOp(Identifier("i"), "<", IntLiteral(4)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")]))
                    ])
                )
            ])
        )
    ])
    expected = "23"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_275():
    """Test 275: Recursive string printing (Simulating string loops)"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "print_n_times",
            [Param(IntType(), "n")],
            BlockStmt([
                IfStmt(BinaryOp(Identifier("n"), "<=", IntLiteral(0)), ReturnStmt(None), None),
                ExprStmt(FuncCall("printString", [StringLiteral("*")])),
                ExprStmt(FuncCall("print_n_times", [BinaryOp(Identifier("n"), "-", IntLiteral(1))]))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("print_n_times", [IntLiteral(3)]))
            ])
        )
    ])
    expected = "***"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_276():
    """Test 276: Postfix increment inside If condition"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(0)),
                IfStmt(
                    BinaryOp(PostfixOp("++", Identifier("x")), "==", IntLiteral(0)),
                    ExprStmt(FuncCall("printString", [StringLiteral("ZeroFirst")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("OneFirst")]))
                ),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "ZeroFirst1" # So sánh x == 0 (True), sau đó x mới tăng lên 1
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_277():
    """Test 277: Assigning struct literal directly to a struct member"""
    ast = Program([
        StructDecl("Inner", [VarDecl(IntType(), "val", None)]),
        StructDecl("Outer", [VarDecl(StructType("Inner"), "inn", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Outer"), "o", StructLiteral([StructLiteral([IntLiteral(0)])])),
                ExprStmt(AssignExpr(MemberAccess(Identifier("o"), "inn"), StructLiteral([IntLiteral(99)]))),
                ExprStmt(FuncCall("printInt", [MemberAccess(MemberAccess(Identifier("o"), "inn"), "val")]))
            ])
        )
    ])
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_278():
    """Test 278: Short-circuit OR skipping multiple subsequent operands"""
    ast = Program([
        FuncDecl(IntType(), "f1", [], BlockStmt([ExprStmt(FuncCall("printString", [StringLiteral("1")])), ReturnStmt(IntLiteral(1))])),
        FuncDecl(IntType(), "f2", [], BlockStmt([ExprStmt(FuncCall("printString", [StringLiteral("2")])), ReturnStmt(IntLiteral(1))])),
        FuncDecl(IntType(), "f3", [], BlockStmt([ExprStmt(FuncCall("printString", [StringLiteral("3")])), ReturnStmt(IntLiteral(1))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(BinaryOp(FuncCall("f1", []), "||", FuncCall("f2", [])), "||", FuncCall("f3", [])),
                    ExprStmt(FuncCall("printString", [StringLiteral("T")])),
                    None
                )
            ])
        )
    ])
    expected = "1T" # Chỉ f1 được chạy vì f1 trả về 1 (True), các hàm sau bị ngắt mạch toàn bộ[cite: 6]
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_279():
    """Test 279: Prefix decrement inside while condition"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(3)),
                WhileStmt(
                    BinaryOp(PrefixOp("--", Identifier("x")), ">", IntLiteral(0)),
                    ExprStmt(FuncCall("printInt", [Identifier("x")]))
                )
            ])
        )
    ])
    expected = "21" # 2 > 0 -> In 2. 1 > 0 -> In 1. 0 > 0 (False) -> Dừng.
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_280():
    """Test 280: Return from deep inside a switch-case inside a while loop"""
    ast = Program([
        FuncDecl(
            IntType(),
            "find_magic",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(10)),
                    BlockStmt([
                        SwitchStmt(
                            Identifier("i"),
                            [
                                CaseStmt(IntLiteral(3), [ReturnStmt(IntLiteral(333))])
                            ],
                            None
                        ),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                    ])
                ),
                ReturnStmt(IntLiteral(0))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("find_magic", [])]))
            ])
        )
    ])
    expected = "333"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_281():
    """Test 281: Nested loops shadowing with same loop variable name"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ForStmt(
                    VarDecl(IntType(), "i", IntLiteral(1)),
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                    BlockStmt([
                        ForStmt(
                            VarDecl(IntType(), "i", IntLiteral(9)), # Shadowing biến i ở vòng lặp ngoài
                            BinaryOp(Identifier("i"), "<", IntLiteral(11)),
                            AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))),
                            BlockStmt([
                                ExprStmt(FuncCall("printInt", [Identifier("i")]))
                            ])
                        )
                    ])
                )
            ])
        )
    ])
    expected = "910910"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_282():
    """Test 282: Float Relational combinations"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(FloatType(), "f1", FloatLiteral(1.5)),
                VarDecl(FloatType(), "f2", FloatLiteral(2.5)),
                ExprStmt(FuncCall("printInt", [BinaryOp(Identifier("f1"), "<", Identifier("f2"))])),
                ExprStmt(FuncCall("printInt", [BinaryOp(Identifier("f1"), ">", Identifier("f2"))])),
                ExprStmt(FuncCall("printInt", [BinaryOp(Identifier("f1"), "<=", FloatLiteral(1.5))])),
                ExprStmt(FuncCall("printInt", [BinaryOp(Identifier("f2"), ">=", FloatLiteral(2.5))]))
            ])
        )
    ])
    expected = "1011"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_283():
    """Test 283: Deeply chained logical NOT !!!!x"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(1)),
                ExprStmt(FuncCall("printInt", [PrefixOp("!", PrefixOp("!", PrefixOp("!", PrefixOp("!", Identifier("x")))))]))
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_284():
    """Test 284: Returning an expression containing assignment"""
    # return (x = 5); -> Trả về 5[cite: 6]
    ast = Program([
        FuncDecl(
            IntType(),
            "assign_and_ret",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(0)),
                ReturnStmt(AssignExpr(Identifier("x"), IntLiteral(42)))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("assign_and_ret", [])]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_285():
    """Test 285: Sequence of Float and Int Prints to test stack alignment"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [IntLiteral(1)])),
                ExprStmt(FuncCall("printFloat", [FloatLiteral(2.2)])),
                ExprStmt(FuncCall("printInt", [IntLiteral(3)])),
                ExprStmt(FuncCall("printFloat", [FloatLiteral(4.4)]))
            ])
        )
    ])
    expected = "12.234.4"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_286():
    """Test 286: For loop with missing init and missing update"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                ForStmt(
                    None,
                    BinaryOp(Identifier("i"), "<", IntLiteral(2)),
                    None,
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1)))) # Update thủ công
                    ])
                )
            ])
        )
    ])
    expected = "01"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_287():
    """Test 287: Relational chaining logic equivalence: (a < b) == (c < d)"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(
                        BinaryOp(IntLiteral(1), "<", IntLiteral(2)), # True (1)
                        "==",
                        BinaryOp(IntLiteral(3), "<", IntLiteral(4))  # True (1)
                    ),
                    ExprStmt(FuncCall("printString", [StringLiteral("Equal")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("NotEqual")]))
                )
            ])
        )
    ])
    expected = "Equal"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_288():
    """Test 288: Evaluating struct literal directly in print parameter (Implicit auto mapping)"""
    ast = Program([
        StructDecl("S", [VarDecl(IntType(), "v", None)]),
        FuncDecl(IntType(), "extract", [Param(StructType("S"), "obj")], BlockStmt([ReturnStmt(MemberAccess(Identifier("obj"), "v"))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("extract", [StructLiteral([IntLiteral(123)])])]))
            ])
        )
    ])
    expected = "123"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_289():
    """Test 289: Multiple assignment from function return"""
    ast = Program([
        FuncDecl(IntType(), "get_five", [], BlockStmt([ReturnStmt(IntLiteral(5))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "a", None),
                VarDecl(IntType(), "b", None),
                ExprStmt(AssignExpr(Identifier("a"), AssignExpr(Identifier("b"), FuncCall("get_five", [])))),
                ExprStmt(FuncCall("printInt", [BinaryOp(Identifier("a"), "+", Identifier("b"))]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_290():
    """Test 290: Complex condition: Leap Year Check"""
    ast = Program([
        FuncDecl(
            IntType(),
            "is_leap",
            [Param(IntType(), "year")],
            BlockStmt([
                IfStmt(
                    BinaryOp(
                        BinaryOp(BinaryOp(Identifier("year"), "%", IntLiteral(4)), "==", IntLiteral(0)),
                        "&&",
                        BinaryOp(
                            BinaryOp(BinaryOp(Identifier("year"), "%", IntLiteral(100)), "!=", IntLiteral(0)),
                            "||",
                            BinaryOp(BinaryOp(Identifier("year"), "%", IntLiteral(400)), "==", IntLiteral(0))
                        )
                    ),
                    ReturnStmt(IntLiteral(1)),
                    ReturnStmt(IntLiteral(0))
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("is_leap", [IntLiteral(2024)])])), # 1
                ExprStmt(FuncCall("printInt", [FuncCall("is_leap", [IntLiteral(2100)])])), # 0
                ExprStmt(FuncCall("printInt", [FuncCall("is_leap", [IntLiteral(2101)])]))  # 0
            ])
        )
    ])
    expected = "100"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_291():
    """Test 291: Function returning Void but having return statement"""
    # Lệnh return; hợp lệ trong hàm Void[cite: 6]
    ast = Program([
        FuncDecl(
            VoidType(),
            "test_void",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("Before")])),
                ReturnStmt(None),
                ExprStmt(FuncCall("printString", [StringLiteral("After")]))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("test_void", []))
            ])
        )
    ])
    expected = "Before"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_292():
    """Test 292: Complex Algorithm - Check if number is Power of 2"""
    ast = Program([
        FuncDecl(
            IntType(),
            "is_pow_2",
            [Param(IntType(), "n")],
            BlockStmt([
                IfStmt(BinaryOp(Identifier("n"), "==", IntLiteral(0)), ReturnStmt(IntLiteral(0)), None),
                WhileStmt(
                    BinaryOp(Identifier("n"), "!=", IntLiteral(1)),
                    BlockStmt([
                        IfStmt(BinaryOp(BinaryOp(Identifier("n"), "%", IntLiteral(2)), "!=", IntLiteral(0)), ReturnStmt(IntLiteral(0)), None),
                        ExprStmt(AssignExpr(Identifier("n"), BinaryOp(Identifier("n"), "/", IntLiteral(2))))
                    ])
                ),
                ReturnStmt(IntLiteral(1))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("is_pow_2", [IntLiteral(16)])])), # 1
                ExprStmt(FuncCall("printInt", [FuncCall("is_pow_2", [IntLiteral(18)])]))  # 0
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_293():
    """Test 293: Complex Algorithm - Reversing a Number Matematically"""
    ast = Program([
        FuncDecl(
            IntType(),
            "reverse",
            [Param(IntType(), "n")],
            BlockStmt([
                VarDecl(IntType(), "rev", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("n"), ">", IntLiteral(0)),
                    BlockStmt([
                        ExprStmt(AssignExpr(Identifier("rev"), BinaryOp(BinaryOp(Identifier("rev"), "*", IntLiteral(10)), "+", BinaryOp(Identifier("n"), "%", IntLiteral(10))))),
                        ExprStmt(AssignExpr(Identifier("n"), BinaryOp(Identifier("n"), "/", IntLiteral(10))))
                    ])
                ),
                ReturnStmt(Identifier("rev"))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [FuncCall("reverse", [IntLiteral(12345)])]))
            ])
        )
    ])
    expected = "54321"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_294():
    """Test 294: Chained member accesses mixed with prefix operators"""
    ast = Program([
        StructDecl("Node", [VarDecl(IntType(), "v", None)]),
        StructDecl("Wrap", [VarDecl(StructType("Node"), "n", None)]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Wrap"), "w", StructLiteral([StructLiteral([IntLiteral(5)])])),
                ExprStmt(FuncCall("printInt", [PrefixOp("++", MemberAccess(MemberAccess(Identifier("w"), "n"), "v"))]))
            ])
        )
    ])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_295():
    """Test 295: Deep recursion reaching stack limits (Simple Counter)"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "recurse",
            [Param(IntType(), "n")],
            BlockStmt([
                IfStmt(BinaryOp(Identifier("n"), "==", IntLiteral(0)), ReturnStmt(None), None),
                ExprStmt(FuncCall("printString", [StringLiteral("R")])),
                ExprStmt(FuncCall("recurse", [BinaryOp(Identifier("n"), "-", IntLiteral(1))]))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("recurse", [IntLiteral(5)]))
            ])
        )
    ])
    expected = "RRRRR"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_296():
    """Test 296: Double Break interacting with Switch and While combined"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(5)),
                    BlockStmt([
                        SwitchStmt(
                            Identifier("i"),
                            [
                                CaseStmt(IntLiteral(2), [BreakStmt()]) # Chỉ break switch, không break while
                            ],
                            None
                        ),
                        IfStmt(BinaryOp(Identifier("i"), "==", IntLiteral(4)), BreakStmt(), None), # Break while
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(AssignExpr(Identifier("i"), BinaryOp(Identifier("i"), "+", IntLiteral(1))))
                    ])
                )
            ])
        )
    ])
    expected = "0123"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_297():
    """Test 297: Modulo sequence simulating random logic"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [BinaryOp(BinaryOp(IntLiteral(100), "%", IntLiteral(30)), "%", IntLiteral(7))])) # 100 % 30 = 10, 10 % 7 = 3
            ])
        )
    ])
    expected = "3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_298():
    """Test 298: Floating point cascading relational with logic AND"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(FloatType(), "f", FloatLiteral(5.5)),
                IfStmt(
                    BinaryOp(BinaryOp(Identifier("f"), ">", FloatLiteral(0.0)), "&&", BinaryOp(Identifier("f"), "<", FloatLiteral(10.0))),
                    ExprStmt(FuncCall("printString", [StringLiteral("InBounds")])),
                    None
                )
            ])
        )
    ])
    expected = "InBounds"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_299():
    """Test 299: String printing embedded directly in boolean logic side effects"""
    ast = Program([
        FuncDecl(IntType(), "log", [], BlockStmt([ExprStmt(FuncCall("printString", [StringLiteral("Log")])), ReturnStmt(IntLiteral(1))])),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(1), "&&", FuncCall("log", [])),
                    ExprStmt(FuncCall("printString", [StringLiteral("Done")])),
                    None
                )
            ])
        )
    ])
    expected = "LogDone"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_300():
    """Test 300: Ultimate Integration Algorithm - Hailstone Sequence (Collatz Conjecture)"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "collatz",
            [Param(IntType(), "n")],
            BlockStmt([
                WhileStmt(
                    BinaryOp(Identifier("n"), "!=", IntLiteral(1)),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("n")])),
                        IfStmt(
                            BinaryOp(BinaryOp(Identifier("n"), "%", IntLiteral(2)), "==", IntLiteral(0)),
                            ExprStmt(AssignExpr(Identifier("n"), BinaryOp(Identifier("n"), "/", IntLiteral(2)))),
                            ExprStmt(AssignExpr(Identifier("n"), BinaryOp(BinaryOp(Identifier("n"), "*", IntLiteral(3)), "+", IntLiteral(1))))
                        )
                    ])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("n")])) # Print 1 at the end
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("collatz", [IntLiteral(6)])) # 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
            ])
        )
    ])
    expected = "63105168421"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"