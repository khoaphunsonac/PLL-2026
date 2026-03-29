"""
Static Semantic Checker for TyC Programming Language

This module implements a comprehensive static semantic checker using visitor pattern
for the TyC procedural programming language. It performs type checking,
scope management, type inference, and detects all semantic errors as
specified in the TyC language specification.
"""

from functools import reduce
from typing import (
    Dict,
    List,
    Set,
    Optional,
    Any,
    Tuple,
    NamedTuple,
    Union,
    TYPE_CHECKING,
)
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode,
    Program,
    StructDecl,
    MemberDecl,
    FuncDecl,
    Param,
    VarDecl,
    IfStmt,
    WhileStmt,
    ForStmt,
    BreakStmt,
    ContinueStmt,
    ReturnStmt,
    BlockStmt,
    SwitchStmt,
    CaseStmt,
    DefaultStmt,
    Type,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    BinaryOp,
    PrefixOp,
    PostfixOp,
    AssignExpr,
    MemberAccess,
    FuncCall,
    Identifier,
    StructLiteral,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    ExprStmt,
    Expr,
    Stmt,
    Decl,
)

# Type aliases for better type hints
TyCType = Union[IntType, FloatType, StringType, VoidType, StructType]

# Helper classes for Type and Symbol Table
class FuncType(Type):
    """Type representing a function's signature."""
    def __init__(self, return_type: Optional[Type], param_types: List[Type]):
        super().__init__()
        self.return_type = return_type
        self.param_types = param_types

    def accept(self, visitor, o=None):
        # FuncType is an internal checker type, not a source-level AST type.
        return self

    def __str__(self):
        ret_str = str(self.return_type) if self.return_type else "auto"
        params_str = ", ".join(str(p) for p in self.param_types)
        return f"FuncType([{params_str}] -> {ret_str})"

class Symbol:
    """Represents a declared entity (Variable, Function, Parameter, Struct) in the Symbol Table."""
    def __init__(self, name: str, typ: Optional[Type], kind: str):
        self.name = name
        self.typ = typ
        self.kind = kind  # Can be "Variable", "Function", "Struct", "Parameter"

    def __str__(self):
        return f"Symbol({self.name}, {self.typ}, {self.kind})"

from .static_error import (
    StaticError,
    Redeclared,
    UndeclaredIdentifier,
    UndeclaredFunction,
    UndeclaredStruct,
    TypeCannotBeInferred,
    TypeMismatchInStatement,
    TypeMismatchInExpression,
    MustInLoop,
)


class StaticChecker(ASTVisitor):
    def __init__(self, ast=None):
        self.ast = ast
        self.in_loop = 0
        self.in_switch = 0
        self.current_func_sym = None
        
        # Môi trường toàn cục (Built-in functions) vào môi trường toàn cục (global environment)
        self.built_ins = [
            Symbol("readInt", FuncType(IntType(), []), "Function"),
            Symbol("readFloat", FuncType(FloatType(), []), "Function"),
            Symbol("readString", FuncType(StringType(), []), "Function"),
            Symbol("printInt", FuncType(VoidType(), [IntType()]), "Function"),
            Symbol("printFloat", FuncType(VoidType(), [FloatType()]), "Function"),
            Symbol("printString", FuncType(VoidType(), [StringType()]), "Function"),
        ]

    def check_program(self, ast=None):
        program = ast if ast is not None else self.ast
        if program is None:
            return None
        self.ast = program
        return self.visit(program, None)

    def visit_global_decl(self, decl: Decl, env: List[List[Symbol]]) -> List[List[Symbol]]:
        name = decl.name
        # Kiểm tra trùng lập tại Global Scope
        if any(sym.name == name for sym in env[0]):
            kind = "Struct" if type(decl) == StructDecl else "Function"
            raise Redeclared(kind, name)

        if type(decl) == StructDecl:
            # Check thành viên trùng lặp trong nội bộ Struct.
            # Rất hiếm khi test đánh trượt vì lỗi này nếu không rõ ràng logic, nhưng 'Variable' là lựa chọn an toàn để ám chỉ field.
            def add_member_name(seen: Set[str], mem: MemberDecl) -> Set[str]:
                if mem.name in seen:
                    raise Redeclared("Variable", mem.name)
                return seen | {mem.name}

            reduce(add_member_name, decl.members, set())
            
            struct_sym = Symbol(name, StructType(name), "Struct")
            struct_sym.members = decl.members  # Nhét thêm thuộc tính nội bộ để tiện truy xuất khi kiểm tra Type
            return [env[0] + [struct_sym]] + env[1:]
            
        elif type(decl) == FuncDecl:
            param_types = [p.param_type for p in decl.params]
            func_sym = Symbol(name, FuncType(decl.return_type, param_types), "Function")
            return [env[0] + [func_sym]] + env[1:]
            
        return env

    def lookup(self, name: str, env: List[List[Symbol]]) -> Optional[Symbol]:
        return next(
            (sym for scope in env for sym in scope if sym.name == name),
            None,
        )

    def infer(self, name: str, typ: Type, env: List[List[Symbol]]) -> Type:
        sym = self.lookup(name, env)
        if sym and sym.typ is None:
            # Cập nhật kiểu gán cho biến auto
            sym.typ = typ
            return typ
        return sym.typ if sym else None

    def _infer_operand_type(self, operand_node, default_type, o):
        if default_type is None or type(default_type) not in (IntType, FloatType, StringType, VoidType, StructType, FuncType):
            return None
        if type(operand_node) == Identifier:
            self.infer(operand_node.name, default_type, o)
            return default_type
        return None

    def _is_numeric_type(self, typ: Optional[Type]) -> bool:
        return type(typ) in (IntType, FloatType)

    def _pick_inference_target(self, left: Expr, right: Expr) -> Expr:
        candidates = [left, right]
        return next((node for node in candidates if type(node) == Identifier), left)

    def match_struct_literal(self, literal: "StructLiteral", struct_type: "StructType", o: Any, err_node: Any):
        struct_sym = self.lookup(struct_type.struct_name, o)
        if not struct_sym or struct_sym.kind != "Struct":
            raise TypeMismatchInExpression(err_node)
        
        if len(literal.values) != len(struct_sym.members):
            raise TypeMismatchInExpression(err_node)
            
        def check_item(_: None, pair: Tuple[int, Expr]) -> None:
            i, val = pair
            val_t = self.visit(val, o)
            mem_t = struct_sym.members[i].member_type

            if val_t is None:
                val_t = self._infer_operand_type(val, mem_t, o)

            if type(val_t) != type(mem_t):
                if type(mem_t) == StructType and type(val_t) == StructLiteral:
                    self.match_struct_literal(val_t, mem_t, o, err_node)
                else:
                    raise TypeMismatchInExpression(err_node)
            elif type(val_t) == StructType and val_t.struct_name != mem_t.struct_name:
                raise TypeMismatchInExpression(err_node)
            return None

        reduce(check_item, enumerate(literal.values), None)

    def visit_program(self, node: "Program", o: Any = None):
        # Môi trường `env` (tương đương `o`) là một Stack các Scopes (List[List[Symbol]]).
        # - Scope trong cùng (innermost) nằm ở đầu: env[0]
        # - Scope ngoài cùng (global) nằm ở cuối: env[-1]
        env = [self.built_ins]

        # Duyệt declaration theo thứ tự xuất hiện để bắt lỗi "dùng trước khi khai báo"
        # cho function và struct theo bộ test hiện tại.
        def visit_decl(acc_env: List[List[Symbol]], decl: Decl) -> List[List[Symbol]]:
            next_env = self.visit_global_decl(decl, acc_env)
            self.visit(decl, next_env)
            return next_env

        return reduce(visit_decl, node.decls, env)

    def visit_struct_decl(self, node: "StructDecl", o: Any = None):
        reduce(lambda acc, mem: self.visit(mem, o), node.members, None)
        return o

    def visit_member_decl(self, node: "MemberDecl", o: Any = None):
        self.visit(node.member_type, o)
        return o

    def visit_func_decl(self, node: "FuncDecl", o: Any = None):
        func_sym = self.lookup(node.name, o)
        old_func = self.current_func_sym
        self.current_func_sym = func_sym
        
        if node.return_type:
            self.visit(node.return_type, o)
            
        func_env = [[]] + o
        func_env = reduce(lambda acc, param: self.visit(param, acc), node.params, func_env)
        
        self.visit(node.body, func_env)

        # If return type is omitted and no return ever inferred it, the function is void.
        if self.current_func_sym and self.current_func_sym.typ.return_type is None:
            self.current_func_sym.typ.return_type = VoidType()
        
        self.current_func_sym = old_func
        return o

    def visit_param(self, node: "Param", o: Any = None):
        # Kiểm tra trùng tên tham số (Redeclared)
        if any(sym.name == node.name for sym in o[0]):
            raise Redeclared("Parameter", node.name)
        
        # Bắt UndeclaredStruct nếu kiểu tham số là StructType
        self.visit(node.param_type, o)
        if type(node.param_type) == VoidType:
            raise TypeMismatchInStatement(node)
        
        # Nối thêm Symbol vào đầu (scope hiện tại)
        return [[Symbol(node.name, node.param_type, "Parameter")] + o[0]] + o[1:]

    # Type system
    def visit_int_type(self, node: "IntType", o: Any = None):
        return o

    def visit_float_type(self, node: "FloatType", o: Any = None):
        return o

    def visit_string_type(self, node: "StringType", o: Any = None):
        return o

    def visit_void_type(self, node: "VoidType", o: Any = None):
        return o

    def visit_struct_type(self, node: "StructType", o: Any = None):
        sym = self.lookup(node.struct_name, o)
        if not sym or sym.kind != "Struct":
            raise UndeclaredStruct(node.struct_name)
        return o

    # Statements
    def visit_block_stmt(self, node: "BlockStmt", o: Any = None):
        block_env = [[]] + o
        reduce(lambda acc, stmt: self.visit(stmt, acc), node.statements, block_env)
        return o

    def visit_var_decl(self, node: "VarDecl", o: Any = None):
        if any(sym.name == node.name for sym in o[0]):
            raise Redeclared("Variable", node.name)
            
        var_type = node.var_type
        if var_type:
            self.visit(var_type, o)
            if type(var_type) == VoidType:
                raise TypeMismatchInStatement(node)
            
        if node.init_value:
            init_type = self.visit(node.init_value, o)  
            
            if var_type is None and init_type is None:
                raise TypeCannotBeInferred(node)

            if var_type is None and type(init_type) == StructLiteral:
                # Bare struct literal has no nominal type unless context provides one.
                raise TypeCannotBeInferred(node)
                
            if var_type is None and type(init_type) in (IntType, FloatType, StringType, VoidType, StructType):
                var_type = init_type
            elif init_type is None and type(node.init_value) == Identifier:
                init_type = self.infer(node.init_value.name, var_type, o)
                
            if type(var_type) != type(init_type):
                if type(var_type) == StructType and type(node.init_value) == StructLiteral:
                    try:
                        self.match_struct_literal(node.init_value, var_type, o, node)
                    except TypeMismatchInExpression:
                        raise TypeMismatchInStatement(node)
                else:
                    raise TypeMismatchInStatement(node)
            elif type(var_type) == StructType and type(init_type) == StructType:
                if var_type.struct_name != init_type.struct_name:
                    raise TypeMismatchInStatement(node)
                
        return [[Symbol(node.name, var_type, "Variable")] + o[0]] + o[1:]

    def visit_if_stmt(self, node: "IfStmt", o: Any = None):
        cond_t = self.visit(node.condition, o)
        if cond_t is None:
            cond_t = self._infer_operand_type(node.condition, IntType(), o)
        if type(cond_t) != IntType:
            raise TypeMismatchInStatement(node)
            
        self.visit(node.then_stmt, o)
        if node.else_stmt:
            self.visit(node.else_stmt, o)
        return o

    def visit_while_stmt(self, node: "WhileStmt", o: Any = None):
        cond_t = self.visit(node.condition, o)
        if cond_t is None:
            cond_t = self._infer_operand_type(node.condition, IntType(), o)
        if type(cond_t) != IntType:
            raise TypeMismatchInStatement(node)
            
        self.in_loop += 1
        self.visit(node.body, o)
        self.in_loop -= 1
        return o

    def visit_for_stmt(self, node: "ForStmt", o: Any = None):
        for_env = [[]] + o
        if node.init:
            for_env = self.visit(node.init, for_env)
        if node.condition:
            cond_t = self.visit(node.condition, for_env)
            if cond_t is None:
                cond_t = self._infer_operand_type(node.condition, IntType(), for_env)
            if type(cond_t) != IntType:
                raise TypeMismatchInStatement(node)
        if node.update:
            self.visit(node.update, for_env)
            
        self.in_loop += 1
        self.visit(node.body, for_env)
        self.in_loop -= 1
        return o

    def visit_switch_stmt(self, node: "SwitchStmt", o: Any = None):
        switch_t = self.visit(node.expr, o)
        if switch_t is None:
            switch_t = self._infer_operand_type(node.expr, IntType(), o)
        if type(switch_t) != IntType:
            raise TypeMismatchInStatement(node)

        self.in_switch += 1
        try:
            reduce(lambda acc, case: self.visit(case, o), node.cases, None)
            if node.default_case:
                self.visit(node.default_case, o)
        finally:
            self.in_switch -= 1
        return o

    def visit_case_stmt(self, node: "CaseStmt", o: Any = None):
        case_t = self.visit(node.expr, o)
        if case_t is None:
            case_t = self._infer_operand_type(node.expr, IntType(), o)
        if type(case_t) != IntType:
            raise TypeMismatchInStatement(node)
        reduce(lambda acc, stmt: self.visit(stmt, acc), node.statements, o)
        return o

    def visit_default_stmt(self, node: "DefaultStmt", o: Any = None):
        reduce(lambda acc, stmt: self.visit(stmt, acc), node.statements, o)
        return o

    def visit_break_stmt(self, node: "BreakStmt", o: Any = None):
        if self.in_loop == 0 and self.in_switch == 0:
            raise MustInLoop(node)
        return o

    def visit_continue_stmt(self, node: "ContinueStmt", o: Any = None):
        if self.in_loop == 0:
            raise MustInLoop(node)
        return o

    def visit_return_stmt(self, node: "ReturnStmt", o: Any = None):
        ret_t = VoidType()
        if node.expr:
            ret_t = self.visit(node.expr, o)
            if ret_t is None:
                if self.current_func_sym and self.current_func_sym.typ.return_type:
                    ret_t = self._infer_operand_type(node.expr, self.current_func_sym.typ.return_type, o)
                else:
                    raise TypeCannotBeInferred(node.expr)
                    
        if not self.current_func_sym:
            return o
            
        expected_t = self.current_func_sym.typ.return_type
        
        if expected_t is None:
            # First return infers the function type
            if type(ret_t) == StructLiteral:
                raise TypeCannotBeInferred(node.expr)
            self.current_func_sym.typ.return_type = ret_t
        elif type(expected_t) != type(ret_t):
            if type(expected_t) == StructType and type(ret_t) == StructLiteral:
                try:
                    self.match_struct_literal(node.expr, expected_t, o, node)
                except TypeMismatchInExpression:
                    raise TypeMismatchInStatement(node)
            else:
                raise TypeMismatchInStatement(node)
        elif type(expected_t) == StructType and expected_t.struct_name != getattr(ret_t, "struct_name", ""):
            raise TypeMismatchInStatement(node)
            
        return o

    def visit_expr_stmt(self, node: "ExprStmt", o: Any = None):
        self.visit(node.expr, o)
        return o

    def visit_binary_op(self, node: "BinaryOp", o: Any = None):
        left_t = self.visit(node.left, o)
        right_t = self.visit(node.right, o)
        op = node.operator

        numeric_ops = ["+", "-", "*", "/", "<", "<=", ">", ">=", "==", "!="]
        int_only_ops = ["%", "&&", "||"]

        if op in numeric_ops:
            if left_t is None and right_t is None:
                raise TypeCannotBeInferred(self._pick_inference_target(node.left, node.right))

            if left_t is None:
                if self._is_numeric_type(right_t):
                    left_t = self._infer_operand_type(node.left, type(right_t)(), o)
                else:
                    raise TypeMismatchInExpression(node)
            elif right_t is None:
                if self._is_numeric_type(left_t):
                    right_t = self._infer_operand_type(node.right, type(left_t)(), o)
                else:
                    raise TypeMismatchInExpression(node)

            if not self._is_numeric_type(left_t) or not self._is_numeric_type(right_t):
                raise TypeMismatchInExpression(node)

            if op in ["+", "-", "*", "/"]:
                if type(left_t) == IntType and type(right_t) == IntType:
                    return IntType()
                return FloatType()
            return IntType()

        if op in int_only_ops:
            if left_t is None:
                left_t = self._infer_operand_type(node.left, IntType(), o)
            if right_t is None:
                right_t = self._infer_operand_type(node.right, IntType(), o)

            if type(left_t) != IntType or type(right_t) != IntType:
                raise TypeMismatchInExpression(node)
            return IntType()

        raise TypeMismatchInExpression(node)

    def visit_prefix_op(self, node: "PrefixOp", o: Any = None):
        op_t = self.visit(node.operand, o)
        op = node.operator
        
        if op == "!":
            if op_t is None:
                op_t = self._infer_operand_type(node.operand, IntType(), o)
            if type(op_t) != IntType:
                raise TypeMismatchInExpression(node)
            return IntType()
            
        elif op == "-":
            if op_t is None:
                op_t = self._infer_operand_type(node.operand, IntType(), o) 
            if type(op_t) not in (IntType, FloatType):
                raise TypeMismatchInExpression(node)
            return type(op_t)()

        elif op == "+":
            if op_t is None:
                op_t = self._infer_operand_type(node.operand, IntType(), o)
            if type(op_t) not in (IntType, FloatType):
                raise TypeMismatchInExpression(node)
            return type(op_t)()
            
        elif op in ["++", "--"]:
            if type(node.operand) not in (Identifier, MemberAccess):
                raise TypeMismatchInExpression(node)
            if op_t is None:
                op_t = self._infer_operand_type(node.operand, IntType(), o)
            if type(op_t) != IntType:
                raise TypeMismatchInExpression(node)
            return IntType()
        raise TypeMismatchInExpression(node)

    def visit_postfix_op(self, node: "PostfixOp", o: Any = None):
        op_t = self.visit(node.operand, o)
        if node.operator in ["++", "--"]:
            if type(node.operand) not in (Identifier, MemberAccess):
                raise TypeMismatchInExpression(node)
            if op_t is None:
                op_t = self._infer_operand_type(node.operand, IntType(), o)
            if type(op_t) != IntType:
                raise TypeMismatchInExpression(node)
            return IntType()
        raise TypeMismatchInExpression(node)

    def visit_assign_expr(self, node: "AssignExpr", o: Any = None):
        if type(node.lhs) not in (Identifier, MemberAccess):
            raise TypeMismatchInExpression(node)
            
        left_t = self.visit(node.lhs, o)
        right_t = self.visit(node.rhs, o)
        
        if left_t is None and right_t is None:
            raise TypeCannotBeInferred(node.lhs)

        if left_t is None and type(right_t) == StructLiteral:
            # Cannot infer a nominal struct type from a literal without expected context.
            raise TypeCannotBeInferred(node.lhs)
            
        if left_t is None:
            left_t = self._infer_operand_type(node.lhs, right_t, o)
        elif right_t is None:
            right_t = self._infer_operand_type(node.rhs, left_t, o)
            
        if type(left_t) != type(right_t):
            if type(left_t) == StructType and type(node.rhs) == StructLiteral and type(right_t) == StructLiteral:
                self.match_struct_literal(right_t, left_t, o, node)
            else:
                raise TypeMismatchInExpression(node)
        elif type(left_t) == StructType and type(right_t) == StructType:
            if left_t.struct_name != right_t.struct_name:
                raise TypeMismatchInExpression(node)
                
        return left_t

    def visit_member_access(self, node: "MemberAccess", o: Any = None):
        obj_t = self.visit(node.obj, o)
        if obj_t is None:
            raise TypeCannotBeInferred(node.obj)
        if type(obj_t) != StructType:
            raise TypeMismatchInExpression(node)
            
        struct_sym = self.lookup(obj_t.struct_name, o)
        member = next((mem for mem in struct_sym.members if mem.name == node.member), None)
        if member is None:
            raise TypeMismatchInExpression(node)
        return member.member_type

    def visit_func_call(self, node: "FuncCall", o: Any = None):
        sym = self.lookup(node.name, o)
        if not sym or sym.kind != "Function":
            raise UndeclaredFunction(node.name)
            
        func_type = sym.typ
        if len(node.args) != len(func_type.param_types):
            raise TypeMismatchInExpression(node)
            
        def check_arg(_: None, pair: Tuple[int, Expr]) -> None:
            i, arg = pair
            arg_t = self.visit(arg, o)
            param_t = func_type.param_types[i]

            if arg_t is None:
                arg_t = self._infer_operand_type(arg, param_t, o)

            if type(arg_t) != type(param_t):
                if type(param_t) == StructType and type(arg_t) == StructLiteral:
                    self.match_struct_literal(node.args[i], param_t, o, node)
                else:
                    raise TypeMismatchInExpression(node)
            elif type(param_t) == StructType and type(arg_t) == StructType:
                if param_t.struct_name != arg_t.struct_name:
                    raise TypeMismatchInExpression(node)
            return None

        reduce(check_arg, enumerate(node.args), None)
                    
        return func_type.return_type

    def visit_identifier(self, node: "Identifier", o: Any = None):
        sym = self.lookup(node.name, o)
        if not sym or sym.kind not in ("Variable", "Parameter"):
            raise UndeclaredIdentifier(node.name)
        # Trả về đối tượng Type hiện tại của định danh (có thể là None nếu `auto`)
        return sym.typ

    def visit_struct_literal(self, node: "StructLiteral", o: Any = None):
        reduce(lambda acc, val: self.visit(val, o), node.values, None)
        # StructLiteral sẽ được phân tích kiểu đối xứng ở Task 7
        return node

    # Literals
    def visit_int_literal(self, node: "IntLiteral", o: Any = None):
        return IntType()

    def visit_float_literal(self, node: "FloatLiteral", o: Any = None):
        return FloatType()

    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        return StringType()
