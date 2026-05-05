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

def test_019():
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                ForStmt(
                    ExprStmt(AssignExpr(Identifier("i"), IntLiteral(0))),
                    BinaryOp(Identifier("i"), "<=", IntLiteral(10)),
                    PostfixOp("++", Identifier("i")),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")]))
                    ])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("i")]))
            ])
        )
    ])
    expected = "01234567891011"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_020():
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
                        CaseStmt(IntLiteral(1), [
                            ExprStmt(FuncCall("printInt", [IntLiteral(1)]))
                        ]),
                        CaseStmt(IntLiteral(3), [
                            ExprStmt(FuncCall("printInt", [IntLiteral(3)]))
                        ]),
                        CaseStmt(IntLiteral(5), [
                            ExprStmt(FuncCall("printInt", [IntLiteral(5)]))
                        ])
                    ],
                    DefaultStmt([
                        ExprStmt(FuncCall("printInt", [IntLiteral(7)]))
                    ])
                )
            ])
        )
    ])
    expected = "357"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_034():
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "x", FuncCall("readInt", [])),
                VarDecl(None, "y", FuncCall("readFloat", [])),
                VarDecl(None, "name", FuncCall("readString", [])),
                VarDecl(None, "sum"),
                ExprStmt(AssignExpr(
                    Identifier("sum"),
                    BinaryOp(Identifier("x"), "+", Identifier("y"))
                )),
                VarDecl(IntType(), "count", IntLiteral(0)),
                VarDecl(FloatType(), "total", FloatLiteral(0.0)),
                VarDecl(StringType(), "greeting", StringLiteral("Hello, ")),
                VarDecl(IntType(), "i"),
                VarDecl(FloatType(), "f"),
                ExprStmt(AssignExpr(Identifier("i"), FuncCall("readInt", []))),
                ExprStmt(AssignExpr(Identifier("f"), FuncCall("readFloat", []))),
                ExprStmt(FuncCall("printFloat", [Identifier("sum")])),
                ExprStmt(FuncCall("printString", [Identifier("greeting")])),
                ExprStmt(FuncCall("printString", [Identifier("name")]))
            ])
        )
    ])
    expected = "4.2Hello, votien"
    input_data = "3\n1.2\nvotien\n7\n2.5\n"
    result = CodeGenerator().generate_and_run(ast, input_data=input_data)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_031():
    ast = Program([
        FuncDecl(
            IntType(),
            "foo",
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
                VarDecl(None, "a"),
                VarDecl(None, "b"),
                ExprStmt(FuncCall("printInt", [
                    FuncCall("foo", [Identifier("a"), Identifier("b")])
                ]))
            ])
        )
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_081():
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
                        ExprStmt(AssignExpr(
                            Identifier("i"),
                            BinaryOp(Identifier("i"), "+", IntLiteral(1))
                        )),
                        SwitchStmt(
                            Identifier("i"),
                            [
                                CaseStmt(IntLiteral(2), [ContinueStmt()]),
                                CaseStmt(IntLiteral(4), [BreakStmt()])
                            ],
                            DefaultStmt([
                                ExprStmt(FuncCall("printInt", [Identifier("i")]))
                            ])
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("i")]))
                    ])
                )
            ])
        )
    ])
    expected = "1133455"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_084():
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(2)),
                SwitchStmt(
                    Identifier("i"),
                    [],
                    DefaultStmt([
                        VarDecl(IntType(), "i", IntLiteral(3))
                    ])
                ),
                ExprStmt(FuncCall("printInt", [Identifier("i")]))
            ])
        )
    ])
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_131():
    ast = Program([
        StructDecl("Point", [
            MemberDecl(IntType(), "x"),
            MemberDecl(IntType(), "y")
        ]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Point"), "p1"),
                VarDecl(StructType("Point"), "p2"),
                ExprStmt(AssignExpr(
                    MemberAccess(Identifier("p2"), "x"),
                    IntLiteral(10)
                )),
                ExprStmt(AssignExpr(
                    MemberAccess(Identifier("p2"), "y"),
                    IntLiteral(20)
                )),
                ExprStmt(AssignExpr(Identifier("p1"), Identifier("p2"))),
                ExprStmt(AssignExpr(
                    MemberAccess(Identifier("p2"), "x"),
                    IntLiteral(99)
                )),
                ExprStmt(AssignExpr(
                    MemberAccess(Identifier("p2"), "y"),
                    IntLiteral(88)
                )),
                ExprStmt(FuncCall("printInt", [
                    MemberAccess(Identifier("p1"), "x")
                ])),
                ExprStmt(FuncCall("printInt", [
                    MemberAccess(Identifier("p1"), "y")
                ])),
                ExprStmt(FuncCall("printInt", [
                    MemberAccess(Identifier("p2"), "x")
                ])),
                ExprStmt(FuncCall("printInt", [
                    MemberAccess(Identifier("p2"), "y")
                ]))
            ])
        )
    ])
    expected = "99889988"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_134():
    ast = Program([
        StructDecl("Point", [
            MemberDecl(IntType(), "x"),
            MemberDecl(IntType(), "y")
        ]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Point"), "a"),
                VarDecl(StructType("Point"), "b"),
                ExprStmt(AssignExpr(
                    Identifier("a"),
                    AssignExpr(
                        Identifier("b"),
                        StructLiteral([IntLiteral(1), IntLiteral(2)])
                    )
                )),
                ExprStmt(FuncCall("printInt", [
                    MemberAccess(Identifier("a"), "x")
                ])),
                ExprStmt(FuncCall("printInt", [
                    MemberAccess(Identifier("a"), "y")
                ])),
                ExprStmt(FuncCall("printInt", [
                    MemberAccess(Identifier("b"), "x")
                ])),
                ExprStmt(FuncCall("printInt", [
                    MemberAccess(Identifier("b"), "y")
                ]))
            ])
        )
    ])
    expected = "1212"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"
