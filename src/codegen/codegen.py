"""
Code generator for TyC.
"""

from typing import Any

from ..utils.nodes import *
from ..utils.visitor import BaseVisitor
from .emitter import *
from .frame import *
from .io import IO_SYMBOL_LIST
from .utils import *


class StringArrayType:
    """Marker type for JVM main(String[] args)."""
    pass


class AutoType:
    """Placeholder for 'auto' variables without initialization."""
    pass


class CodeGenerator(BaseVisitor):
    """Minimal AST -> Jasmin code generator."""

    def __init__(self):
        self.emit = None
        self.functions = {}
        self.current_return_type = VoidType()
        self.class_name = "TyC"
        self.structs: dict[str, list[tuple[str, Type]]] = {}

    def _enter_switch(self, frame: Frame) -> int:
        if hasattr(frame, "enter_switch"):
            return frame.enter_switch()
        break_label = frame.get_new_label()
        frame.brk_label.append(break_label)
        if frame.con_label:
            frame.con_label.append(frame.con_label[-1])
        else:
            frame.con_label.append(break_label)
        return break_label

    def _exit_switch(self, frame: Frame) -> None:
        if hasattr(frame, "exit_switch"):
            frame.exit_switch()
            return
        if not frame.con_label or not frame.brk_label:
            raise RuntimeError("Error when exit switch")
        frame.con_label.pop()
        frame.brk_label.pop()

    def _lookup_symbol(self, name: str, sym_list: list[Symbol]) -> Symbol:
        for sym in reversed(sym_list):
            if sym.name == name:
                return sym
        raise RuntimeError(f"Undeclared symbol: {name}")

    def _infer_type(self, node: Expr, o: Access):
        if isinstance(node, IntLiteral):
            return IntType()
        if isinstance(node, FloatLiteral):
            return FloatType()
        if isinstance(node, StringLiteral):
            return StringType()
        if isinstance(node, Identifier):
            return self._lookup_symbol(node.name, o.sym).type
        if isinstance(node, AssignExpr):
            return self._infer_type(node.rhs, o)
        if isinstance(node, FuncCall):
            return self.functions[node.name].type.return_type
        if isinstance(node, MemberAccess):
            obj_type = self._infer_type(node.obj, o)
            return self._get_struct_member_type(obj_type, node.member)
        if isinstance(node, StructLiteral):
            if o is not None and getattr(o, "expected_type", None) is not None:
                return o.expected_type
            raise RuntimeError("StructLiteral requires expected struct type")
        if isinstance(node, PrefixOp):
            if node.operator in ["++", "--", "!"]:
                return IntType()
            if node.operator in ["+", "-"]:
                return self._infer_type(node.operand, o)
        if isinstance(node, PostfixOp):
            return IntType()
        if isinstance(node, BinaryOp):
            if node.operator in ["+", "-", "*", "/", "%"]:
                left_type = self._infer_type(node.left, o)
                right_type = self._infer_type(node.right, o)
                if is_float_type(left_type) or is_float_type(right_type):
                    return FloatType()
                return IntType()
            if node.operator in ["<", "<=", ">", ">=", "==", "!=", "&&", "||"]:
                return IntType()
        return IntType()

    def _get_struct_members(self, struct_type) -> list[tuple[str, Type]]:
        if not is_struct_type(struct_type):
            raise RuntimeError(f"Expected struct type, got {type(struct_type)}")
        struct_name = struct_type.struct_name
        if struct_name not in self.structs:
            raise RuntimeError(f"Unknown struct type: {struct_name}")
        return self.structs[struct_name]

    def _get_struct_member_type(self, struct_type, member_name: str) -> Type:
        for name, member_type in self._get_struct_members(struct_type):
            if name == member_name:
                return member_type
        raise RuntimeError(f"Unknown member {member_name} in struct {struct_type.struct_name}")

    def _emit_struct_class(self, decl: StructDecl) -> None:
        struct_emitter = Emitter(f"{decl.name}.j")
        struct_emitter.print_out(struct_emitter.emit_prolog(decl.name))
        for member in decl.members:
            member_name, member_type = self._get_struct_member_decl_info(member)
            struct_emitter.print_out(struct_emitter.emit_field(member_name, member_type))
        struct_emitter.print_out(self._emit_struct_default_constructor(decl, struct_emitter))
        struct_emitter.emit_epilog()

    def _emit_struct_default_constructor(self, decl: StructDecl, emitter: Emitter) -> str:
        code = ""
        code += ".method public <init>()V\n"
        code += ".limit stack 4\n"
        code += ".limit locals 1\n"
        code += "\taload_0\n"
        code += "\tinvokespecial java/lang/Object/<init>()V\n"

        for member in decl.members:
            member_name, member_type = self._get_struct_member_decl_info(member)
            if is_string_type(member_type):
                code += "\taload_0\n"
                code += "\tldc \"\"\n"
                code += f"\tputfield {decl.name}/{member_name} {emitter.get_jvm_type(member_type)}\n"
            elif is_struct_type(member_type):
                code += "\taload_0\n"
                code += f"\tnew {member_type.struct_name}\n"
                code += "\tdup\n"
                code += f"\tinvokespecial {member_type.struct_name}/<init>()V\n"
                code += f"\tputfield {decl.name}/{member_name} {emitter.get_jvm_type(member_type)}\n"

        code += "\treturn\n"
        code += ".end method\n"
        return code

    def _emit_struct_copy(self, value_code: str, struct_type, frame) -> str:
        struct_name = struct_type.struct_name
        members = self._get_struct_members(struct_type)
        src_idx = frame.get_new_index()
        dst_idx = frame.get_new_index()

        code = value_code
        code += self.emit.emit_write_var("$src", struct_type, src_idx, frame)
        code += self.emit.emit_new_instance(struct_name, frame)
        code += self.emit.emit_write_var("$dst", struct_type, dst_idx, frame)

        for member_name, member_type in members:
            code += self.emit.emit_read_var("$dst", struct_type, dst_idx, frame)
            code += self.emit.emit_read_var("$src", struct_type, src_idx, frame)
            code += self.emit.emit_get_field(f"{struct_name}/{member_name}", member_type, frame)
            if is_struct_type(member_type):
                code = self._emit_struct_copy(code, member_type, frame)
            code += self.emit.emit_put_field(f"{struct_name}/{member_name}", member_type, frame)

        code += self.emit.emit_read_var("$dst", struct_type, dst_idx, frame)
        return code

    def _emit_read_with_default(self, fn_name: str, default_value, default_type, frame) -> tuple[str, Type]:
        lbl_try_start = frame.get_new_label()
        lbl_try_end = frame.get_new_label()
        lbl_handler = frame.get_new_label()
        lbl_done = frame.get_new_label()

        code = (
            f".catch java/util/NoSuchElementException from Label{lbl_try_start} "
            f"to Label{lbl_try_end} using Label{lbl_handler}\n"
        )
        code += self.emit.emit_label(lbl_try_start, frame)
        code += self.emit.emit_invoke_static(
            f"io/{fn_name}", FunctionType([], default_type), frame
        )
        code += self.emit.emit_label(lbl_try_end, frame)
        code += self.emit.emit_goto(lbl_done, frame)

        code += self.emit.emit_label(lbl_handler, frame)
        code += self.emit.emit_pop(frame)

        if is_int_type(default_type):
            code += self.emit.emit_push_iconst(int(default_value), frame)
        elif is_float_type(default_type):
            code += self.emit.emit_push_fconst(str(default_value), frame)
        elif is_string_type(default_type):
            code += self.emit.emit_push_const(str(default_value), StringType(), frame)

        code += self.emit.emit_label(lbl_done, frame)
        return code, default_type

    def _get_struct_member_decl_info(self, member) -> tuple[str, Type]:
        if isinstance(member, MemberDecl):
            return member.name, member.member_type
        if isinstance(member, VarDecl):
            return member.name, member.var_type
        raise RuntimeError(f"Unsupported struct member declaration: {type(member)}")

    def _emit_auto_init(self, sym: Symbol, frame, target_type: Type) -> str:
        sym.type = target_type
        if is_int_type(target_type):
            code = self.emit.emit_push_iconst(0, frame)
        elif is_float_type(target_type):
            code = self.emit.emit_push_fconst("0.0", frame)
        elif is_string_type(target_type):
            code = self.emit.emit_push_const("", StringType(), frame)
        elif is_struct_type(target_type):
            code = self.emit.emit_new_instance(target_type.struct_name, frame)
        else:
            raise RuntimeError("Unsupported auto initialization type")
        code += self.emit.emit_write_var(sym.name, target_type, sym.value.value, frame)
        return code

    def _scan_return_type(self, stmt: Stmt, sym: list[Symbol]) -> Type | None:
        infer_frame = Frame("__infer__", VoidType())
        if stmt is None:
            return None
        if isinstance(stmt, ReturnStmt):
            if stmt.expr is None:
                return VoidType()
            return self._infer_type(stmt.expr, Access(infer_frame, sym))
        if isinstance(stmt, BlockStmt):
            local_sym = list(sym)
            for inner in stmt.statements:
                if isinstance(inner, VarDecl):
                    if inner.var_type is None and inner.init_value is None:
                        continue
                    var_type = inner.var_type if inner.var_type else self._infer_type(inner.init_value, Access(infer_frame, local_sym))
                    local_sym.append(Symbol(inner.name, var_type, Index(0)))
                ret_type = self._scan_return_type(inner, local_sym)
                if ret_type is not None:
                    return ret_type
            return None
        if isinstance(stmt, IfStmt):
            ret_type = self._scan_return_type(stmt.then_stmt, list(sym))
            if ret_type is not None:
                return ret_type
            return self._scan_return_type(stmt.else_stmt, list(sym)) if stmt.else_stmt else None
        if isinstance(stmt, WhileStmt):
            return self._scan_return_type(stmt.body, list(sym))
        if isinstance(stmt, ForStmt):
            local_sym = list(sym)
            if isinstance(stmt.init, VarDecl):
                if stmt.init.var_type is not None or stmt.init.init_value is not None:
                    init_type = stmt.init.var_type if stmt.init.var_type else self._infer_type(stmt.init.init_value, Access(infer_frame, local_sym))
                    local_sym.append(Symbol(stmt.init.name, init_type, Index(0)))
            return self._scan_return_type(stmt.body, local_sym)
        if isinstance(stmt, SwitchStmt):
            for case_stmt in stmt.cases:
                for case_inner in case_stmt.statements:
                    ret_type = self._scan_return_type(case_inner, list(sym))
                    if ret_type is not None:
                        return ret_type
            if stmt.default_case:
                for default_inner in stmt.default_case.statements:
                    ret_type = self._scan_return_type(default_inner, list(sym))
                    if ret_type is not None:
                        return ret_type
        return None

    def _infer_function_return_type(self, decl: FuncDecl) -> Type:
        param_syms = [Symbol(p.name, p.param_type, Index(0)) for p in decl.params]
        ret_type = self._scan_return_type(decl.body, param_syms)
        return ret_type if ret_type is not None else VoidType()

    def _stmt_always_returns(self, stmt: Stmt) -> bool:
        if isinstance(stmt, ReturnStmt):
            return True
        if isinstance(stmt, BlockStmt):
            for inner in stmt.statements:
                if self._stmt_always_returns(inner):
                    return True
            return False
        if isinstance(stmt, IfStmt) and stmt.else_stmt is not None:
            return self._stmt_always_returns(stmt.then_stmt) and self._stmt_always_returns(stmt.else_stmt)
        return False

    def visit_program(self, node: Program, o: Any = None):
        self.emit = Emitter(f"{self.class_name}.j")
        self.emit.print_out(self.emit.emit_prolog(self.class_name))

        for decl in node.decls:
            if isinstance(decl, StructDecl):
                self.structs[decl.name] = [self._get_struct_member_decl_info(m) for m in decl.members]
                self._emit_struct_class(decl)

        for io_sym in IO_SYMBOL_LIST:
            self.functions[io_sym.name] = io_sym

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                return_type = decl.return_type if decl.return_type else self._infer_function_return_type(decl)
                param_types = [p.param_type for p in decl.params]
                self.functions[decl.name] = Symbol(
                    decl.name, FunctionType(param_types, return_type), CName(self.class_name)
                )

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                self.visit(decl, None)

        self.emit.emit_epilog()

    def visit_func_decl(self, node: FuncDecl, o: Any = None):
        if node.return_type is None:
            self.current_return_type = self.functions[node.name].type.return_type
        else:
            self.current_return_type = node.return_type
        frame = Frame(node.name, self.current_return_type)
        frame.enter_scope(True)

        if node.name == "main":
            mtype = FunctionType([StringArrayType()], VoidType())
        else:
            mtype = FunctionType([p.param_type for p in node.params], self.current_return_type)

        self.emit.print_out(self.emit.emit_method(node.name, mtype, True))

        start_label = frame.get_start_label()
        end_label = frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))

        if node.name == "main":
            self.emit.print_out(
                self.emit.emit_get_static("java/util/Locale/US", "Ljava/util/Locale;", frame)
            )
            self.emit.print_out(
                self.emit.emit_invoke_static_raw(
                    "java/util/Locale/setDefault",
                    "(Ljava/util/Locale;)V",
                    frame,
                    1,
                    False,
                )
            )

        local_syms: list[Symbol] = []
        if node.name == "main":
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", StringArrayType(), start_label, end_label
                )
            )

        for param in node.params:
            idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(idx, param.name, param.param_type, start_label, end_label)
            )
            local_syms.append(Symbol(param.name, param.param_type, Index(idx)))

        sub_body = SubBody(frame, local_syms)
        self.visit(node.body, sub_body)

        if is_void_type(self.current_return_type):
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))

        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_scope()
        self.emit.print_out(self.emit.emit_end_method(frame))

    def visit_block_stmt(self, node: BlockStmt, o: SubBody = None):
        frame = o.frame
        frame.enter_scope(False)
        start_label = frame.get_start_label()
        end_label = frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))

        local_syms = list(o.sym)
        sub_body = SubBody(frame, local_syms)
        for stmt in node.statements:
            sub_body = self.visit(stmt, sub_body)

        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_scope()
        return o

    def visit_var_decl(self, node: VarDecl, o: SubBody = None):
        frame = o.frame
        idx = frame.get_new_index()

        if node.var_type is None and node.init_value is None:
            o.sym.append(Symbol(node.name, AutoType(), Index(idx)))
            return o

        var_type = node.var_type if node.var_type else self._infer_type(node.init_value, Access(frame, o.sym))
        self.emit.print_out(
            self.emit.emit_var(
                idx, node.name, var_type, frame.get_start_label(), frame.get_end_label()
            )
        )
        if node.init_value is None:
            if is_int_type(var_type):
                self.emit.print_out(self.emit.emit_push_iconst(0, frame))
            elif is_float_type(var_type):
                self.emit.print_out(self.emit.emit_push_fconst("0.0", frame))
            elif is_string_type(var_type):
                self.emit.print_out(self.emit.emit_push_const("", StringType(), frame))
            elif is_struct_type(var_type):
                self.emit.print_out(self.emit.emit_new_instance(var_type.struct_name, frame))
            self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
        else:
            access = Access(frame, o.sym)
            if isinstance(node.init_value, StructLiteral) and is_struct_type(var_type):
                access.expected_type = var_type
            rhs_code, rhs_type = self.visit(node.init_value, access)
            if is_struct_type(var_type) and is_struct_type(rhs_type):
                rhs_code = self._emit_struct_copy(rhs_code, var_type, frame)
            if is_float_type(var_type) and is_int_type(rhs_type):
                rhs_code += self.emit.emit_i2f(frame)
            self.emit.print_out(rhs_code)
            self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
        o.sym.append(Symbol(node.name, var_type, Index(idx)))
        return o

    def visit_expr_stmt(self, node: ExprStmt, o: SubBody = None):
        code, expr_type = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        if not is_void_type(expr_type):
            self.emit.print_out(self.emit.emit_pop(o.frame))
        return o

    def visit_if_stmt(self, node: IfStmt, o: SubBody = None):
        frame = o.frame
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        else_label = frame.get_new_label()
        end_label = frame.get_new_label()
        then_returns = self._stmt_always_returns(node.then_stmt)
        else_returns = self._stmt_always_returns(node.else_stmt) if node.else_stmt else False
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(else_label, frame))
        self.visit(node.then_stmt, o)
        if node.else_stmt and not then_returns:
            self.emit.print_out(self.emit.emit_goto(end_label, frame))
        self.emit.print_out(self.emit.emit_label(else_label, frame))
        if node.else_stmt:
            self.visit(node.else_stmt, o)
        if node.else_stmt and not (then_returns and else_returns):
            self.emit.print_out(self.emit.emit_label(end_label, frame))
        elif not node.else_stmt:
            self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_while_stmt(self, node: WhileStmt, o: SubBody = None):
        frame = o.frame
        frame.enter_loop()
        start_label = frame.get_continue_label()
        end_label = frame.get_break_label()

        self.emit.print_out(self.emit.emit_label(start_label, frame))
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(end_label, frame))
        self.visit(node.body, o)
        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_loop()
        return o

    def visit_return_stmt(self, node: ReturnStmt, o: SubBody = None):
        if node.expr is None:
            self.emit.print_out(self.emit.emit_return(VoidType(), o.frame))
            return o
        access = Access(o.frame, o.sym)
        if isinstance(node.expr, StructLiteral) and is_struct_type(self.current_return_type):
            access.expected_type = self.current_return_type
        code, ret_type = self.visit(node.expr, access)
        if is_float_type(self.current_return_type) and is_int_type(ret_type):
            code += self.emit.emit_i2f(o.frame)
            ret_type = FloatType()
        self.emit.print_out(code)
        self.emit.print_out(self.emit.emit_return(self.current_return_type, o.frame))
        return o

    def visit_binary_op(self, node: BinaryOp, o: Access = None):
        left_code, left_type = self.visit(node.left, o)
        right_code, right_type = self.visit(node.right, o)
        frame = o.frame

        if node.operator in ["+", "-"]:
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            code = left_code
            if is_float_type(result_type) and is_int_type(left_type):
                code += self.emit.emit_i2f(frame)
            code += right_code
            if is_float_type(result_type) and is_int_type(right_type):
                code += self.emit.emit_i2f(frame)
            return code + self.emit.emit_add_op(node.operator, result_type, frame), result_type
        if node.operator in ["*", "/"]:
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            code = left_code
            if is_float_type(result_type) and is_int_type(left_type):
                code += self.emit.emit_i2f(frame)
            code += right_code
            if is_float_type(result_type) and is_int_type(right_type):
                code += self.emit.emit_i2f(frame)
            return code + self.emit.emit_mul_op(node.operator, result_type, frame), result_type
        if node.operator == "%":
            return left_code + right_code + self.emit.emit_mod(frame), IntType()
        if node.operator in ["<", "<=", ">", ">=", "==", "!="]:
            op_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            code = left_code
            if is_float_type(op_type) and is_int_type(left_type):
                code += self.emit.emit_i2f(frame)
            code += right_code
            if is_float_type(op_type) and is_int_type(right_type):
                code += self.emit.emit_i2f(frame)
            return code + self.emit.emit_re_op(node.operator, op_type, frame), IntType()
        if node.operator == "&&":
            label_false = frame.get_new_label()
            label_end = frame.get_new_label()
            code = left_code
            code += self.emit.emit_if_false(label_false, frame)
            code += right_code
            code += self.emit.emit_if_false(label_false, frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_goto(label_end, frame)
            code += self.emit.emit_label(label_false, frame)
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_label(label_end, frame)
            return code, IntType()
        if node.operator == "||":
            label_true = frame.get_new_label()
            label_end = frame.get_new_label()
            code = left_code
            code += self.emit.emit_if_true(label_true, frame)
            code += right_code
            code += self.emit.emit_if_true(label_true, frame)
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_goto(label_end, frame)
            code += self.emit.emit_label(label_true, frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_label(label_end, frame)
            return code, IntType()
        raise RuntimeError(f"Unsupported operator: {node.operator}")

    def visit_assign_expr(self, node: AssignExpr, o: Access = None):
        if isinstance(node.lhs, Identifier):
            lhs_sym = self._lookup_symbol(node.lhs.name, o.sym)
            idx = lhs_sym.value.value
            access = o
            if isinstance(node.rhs, StructLiteral) and is_struct_type(lhs_sym.type):
                access = Access(o.frame, o.sym)
                access.expected_type = lhs_sym.type
            rhs_code, rhs_type = self.visit(node.rhs, access)
            if isinstance(lhs_sym.type, AutoType):
                lhs_sym.type = rhs_type
            if is_struct_type(lhs_sym.type) and is_struct_type(rhs_type):
                rhs_code = self._emit_struct_copy(rhs_code, lhs_sym.type, o.frame)
            if is_float_type(lhs_sym.type) and is_int_type(rhs_type):
                rhs_code += self.emit.emit_i2f(o.frame)
            code = rhs_code + self.emit.emit_dup(o.frame) + self.emit.emit_write_var(
                node.lhs.name, lhs_sym.type, idx, o.frame
            )
            return code, lhs_sym.type
        if isinstance(node.lhs, MemberAccess):
            obj_code, obj_type = self.visit(node.lhs.obj, o)
            member_type = self._get_struct_member_type(obj_type, node.lhs.member)
            access = o
            if isinstance(node.rhs, StructLiteral) and is_struct_type(member_type):
                access = Access(o.frame, o.sym)
                access.expected_type = member_type
            rhs_code, rhs_type = self.visit(node.rhs, access)
            if is_struct_type(member_type) and is_struct_type(rhs_type):
                rhs_code = self._emit_struct_copy(rhs_code, member_type, o.frame)
            if is_float_type(member_type) and is_int_type(rhs_type):
                rhs_code += self.emit.emit_i2f(o.frame)
            code = obj_code + rhs_code
            code += self.emit.emit_dup_x1(o.frame)
            code += self.emit.emit_put_field(f"{obj_type.struct_name}/{node.lhs.member}", member_type, o.frame)
            return code, member_type
        raise RuntimeError("Unsupported assignment target")

    def visit_func_call(self, node: FuncCall, o: Access = None):
        frame = o.frame
        if node.name in ["readInt", "readFloat", "readString"]:
            if node.name == "readInt":
                return self._emit_read_with_default("readInt", 2, IntType(), frame)
            if node.name == "readFloat":
                return self._emit_read_with_default("readFloat", 2.2, FloatType(), frame)
            if node.name == "readString":
                return self._emit_read_with_default("readString", "votien", StringType(), frame)

        fn_sym = self.functions[node.name]
        fn_type = fn_sym.type
        code = ""
        for arg, param_type in zip(node.args, fn_type.param_types):
            access = o
            if isinstance(arg, Identifier):
                sym = self._lookup_symbol(arg.name, o.sym)
                if isinstance(sym.type, AutoType):
                    code += self._emit_auto_init(sym, frame, param_type)
                arg_code = self.emit.emit_read_var(sym.name, sym.type, sym.value.value, frame)
                arg_type = sym.type
            else:
                if isinstance(arg, StructLiteral) and is_struct_type(param_type):
                    access = Access(o.frame, o.sym)
                    access.expected_type = param_type
                arg_code, arg_type = self.visit(arg, access)
            if is_struct_type(param_type):
                arg_code = self._emit_struct_copy(arg_code, param_type, frame)
            if is_float_type(param_type) and is_int_type(arg_type):
                arg_code += self.emit.emit_i2f(frame)
            code += arg_code
        code += self.emit.emit_invoke_static(f"{fn_sym.value.value}/{node.name}", fn_type, frame)
        return code, fn_type.return_type

    def visit_identifier(self, node: Identifier, o: Access = None):
        sym = self._lookup_symbol(node.name, o.sym)
        if isinstance(sym.type, AutoType):
            code = self._emit_auto_init(sym, o.frame, IntType())
            code += self.emit.emit_read_var(node.name, sym.type, sym.value.value, o.frame)
            return code, sym.type
        return self.emit.emit_read_var(node.name, sym.type, sym.value.value, o.frame), sym.type

    def visit_int_literal(self, node: IntLiteral, o: Access = None):
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: FloatLiteral, o: Access = None):
        return self.emit.emit_push_fconst(str(node.value), o.frame), FloatType()

    def visit_string_literal(self, node: StringLiteral, o: Access = None):
        return self.emit.emit_push_const(node.value, StringType(), o.frame), StringType()

    def visit_struct_decl(self, node: StructDecl, o: Any = None):
        return None

    def visit_member_decl(self, node: MemberDecl, o: Any = None):
        return None

    def visit_param(self, node: Param, o: Any = None):
        return None

    def visit_int_type(self, node: IntType, o: Any = None):
        return node

    def visit_float_type(self, node: FloatType, o: Any = None):
        return node

    def visit_string_type(self, node: StringType, o: Any = None):
        return node

    def visit_void_type(self, node: VoidType, o: Any = None):
        return node

    def visit_struct_type(self, node: StructType, o: Any = None):
        return node

    def visit_for_stmt(self, node: ForStmt, o: Any = None):
        frame = o.frame
        init_handled = False
        if isinstance(node.init, VarDecl):
            # Keep for-loop declared variables visible after the loop.
            o = self.visit(node.init, o)
            init_handled = True

        frame.enter_scope(False)
        start_scope = frame.get_start_label()
        end_scope = frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(start_scope, frame))

        local_syms = list(o.sym)
        sub_body = SubBody(frame, local_syms)

        if node.init is not None and not init_handled:
            if isinstance(node.init, ExprStmt):
                sub_body = self.visit(node.init, sub_body)
            else:
                init_code, init_type = self.visit(node.init, Access(frame, sub_body.sym))
                self.emit.print_out(init_code)
                if not is_void_type(init_type):
                    self.emit.print_out(self.emit.emit_pop(frame))

        frame.enter_loop()
        cond_label = frame.get_new_label()
        continue_label = frame.get_continue_label()
        break_label = frame.get_break_label()

        self.emit.print_out(self.emit.emit_label(cond_label, frame))
        if node.condition is not None:
            cond_code, _ = self.visit(node.condition, Access(frame, sub_body.sym))
            self.emit.print_out(cond_code)
            self.emit.print_out(self.emit.emit_if_false(break_label, frame))

        self.visit(node.body, sub_body)

        self.emit.print_out(self.emit.emit_label(continue_label, frame))
        if node.update is not None:
            update_code, update_type = self.visit(node.update, Access(frame, sub_body.sym))
            self.emit.print_out(update_code)
            if not is_void_type(update_type):
                self.emit.print_out(self.emit.emit_pop(frame))
        self.emit.print_out(self.emit.emit_goto(cond_label, frame))
        self.emit.print_out(self.emit.emit_label(break_label, frame))

        frame.exit_loop()
        self.emit.print_out(self.emit.emit_label(end_scope, frame))
        frame.exit_scope()
        return o

    def visit_switch_stmt(self, node: SwitchStmt, o: Any = None):
        frame = o.frame
        frame.enter_scope(False)
        start_label = frame.get_start_label()
        end_label = frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))

        switch_body = SubBody(frame, list(o.sym))

        switch_type = self._infer_type(node.expr, Access(frame, switch_body.sym))
        switch_code, _ = self.visit(node.expr, Access(frame, switch_body.sym))

        temp_idx = frame.get_new_index()
        self.emit.print_out(switch_code)
        self.emit.print_out(self.emit.emit_write_var("$switch", switch_type, temp_idx, frame))

        break_label = self._enter_switch(frame)

        case_labels = [frame.get_new_label() for _ in node.cases]
        default_label = frame.get_new_label() if node.default_case else break_label

        for case_stmt, case_label in zip(node.cases, case_labels):
            self.emit.print_out(self.emit.emit_read_var("$switch", switch_type, temp_idx, frame))
            case_code, _ = self.visit(case_stmt.expr, Access(frame, switch_body.sym))
            self.emit.print_out(case_code)
            self.emit.print_out(self.emit.emit_re_op("==", switch_type, frame))
            self.emit.print_out(self.emit.emit_if_true(case_label, frame))

        self.emit.print_out(self.emit.emit_goto(default_label, frame))

        for case_stmt, case_label in zip(node.cases, case_labels):
            self.emit.print_out(self.emit.emit_label(case_label, frame))
            for stmt in case_stmt.statements:
                self.visit(stmt, switch_body)

        if node.default_case:
            self.emit.print_out(self.emit.emit_label(default_label, frame))
            for stmt in node.default_case.statements:
                self.visit(stmt, switch_body)

        self.emit.print_out(self.emit.emit_label(break_label, frame))
        self._exit_switch(frame)
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_scope()
        return o

    def visit_case_stmt(self, node: CaseStmt, o: Any = None):
        return None

    def visit_default_stmt(self, node: DefaultStmt, o: Any = None):
        return None

    def visit_break_stmt(self, node: BreakStmt, o: Any = None):
        self.emit.print_out(self.emit.emit_goto(o.frame.get_break_label(), o.frame))
        return o

    def visit_continue_stmt(self, node: ContinueStmt, o: Any = None):
        self.emit.print_out(self.emit.emit_goto(o.frame.get_continue_label(), o.frame))
        return o

    def visit_prefix_op(self, node: PrefixOp, o: Any = None):
        frame = o.frame
        if node.operator in ["+", "-"]:
            operand_code, operand_type = self.visit(node.operand, o)
            if node.operator == "+":
                return operand_code, operand_type
            return operand_code + self.emit.emit_neg_op(operand_type, frame), operand_type
        if node.operator == "!":
            operand_code, _ = self.visit(node.operand, o)
            label_true = frame.get_new_label()
            label_end = frame.get_new_label()
            code = operand_code
            code += self.emit.emit_if_false(label_true, frame)
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_goto(label_end, frame)
            code += self.emit.emit_label(label_true, frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_label(label_end, frame)
            return code, IntType()
        if node.operator in ["++", "--"]:
            if isinstance(node.operand, Identifier):
                sym = self._lookup_symbol(node.operand.name, o.sym)
                code = self.emit.emit_read_var(sym.name, sym.type, sym.value.value, frame)
                code += self.emit.emit_push_iconst(1, frame)
                if node.operator == "++":
                    code += self.emit.emit_add_op("+", sym.type, frame)
                else:
                    code += self.emit.emit_add_op("-", sym.type, frame)
                code += self.emit.emit_dup(frame)
                code += self.emit.emit_write_var(sym.name, sym.type, sym.value.value, frame)
                return code, sym.type
            if isinstance(node.operand, MemberAccess):
                obj_code, obj_type = self.visit(node.operand.obj, o)
                member_type = self._get_struct_member_type(obj_type, node.operand.member)
                code = obj_code
                code += self.emit.emit_dup(frame)
                code += self.emit.emit_get_field(f"{obj_type.struct_name}/{node.operand.member}", member_type, frame)
                code += self.emit.emit_push_iconst(1, frame)
                if node.operator == "++":
                    code += self.emit.emit_add_op("+", member_type, frame)
                else:
                    code += self.emit.emit_add_op("-", member_type, frame)
                code += self.emit.emit_dup_x1(frame)
                code += self.emit.emit_put_field(f"{obj_type.struct_name}/{node.operand.member}", member_type, frame)
                return code, member_type
        raise RuntimeError("Unsupported prefix operator")

    def visit_postfix_op(self, node: PostfixOp, o: Any = None):
        frame = o.frame
        if node.operator in ["++", "--"]:
            if isinstance(node.operand, Identifier):
                sym = self._lookup_symbol(node.operand.name, o.sym)
                code = self.emit.emit_read_var(sym.name, sym.type, sym.value.value, frame)
                code += self.emit.emit_dup(frame)
                code += self.emit.emit_push_iconst(1, frame)
                if node.operator == "++":
                    code += self.emit.emit_add_op("+", sym.type, frame)
                else:
                    code += self.emit.emit_add_op("-", sym.type, frame)
                code += self.emit.emit_write_var(sym.name, sym.type, sym.value.value, frame)
                return code, sym.type
            if isinstance(node.operand, MemberAccess):
                obj_code, obj_type = self.visit(node.operand.obj, o)
                member_type = self._get_struct_member_type(obj_type, node.operand.member)
                code = obj_code
                code += self.emit.emit_dup(frame)
                code += self.emit.emit_get_field(f"{obj_type.struct_name}/{node.operand.member}", member_type, frame)
                code += self.emit.emit_dup_x1(frame)
                code += self.emit.emit_push_iconst(1, frame)
                if node.operator == "++":
                    code += self.emit.emit_add_op("+", member_type, frame)
                else:
                    code += self.emit.emit_add_op("-", member_type, frame)
                code += self.emit.emit_put_field(f"{obj_type.struct_name}/{node.operand.member}", member_type, frame)
                return code, member_type
        raise RuntimeError("Unsupported postfix operator")

    def visit_member_access(self, node: MemberAccess, o: Any = None):
        obj_code, obj_type = self.visit(node.obj, o)
        member_type = self._get_struct_member_type(obj_type, node.member)
        code = obj_code + self.emit.emit_get_field(f"{obj_type.struct_name}/{node.member}", member_type, o.frame)
        return code, member_type

    def visit_struct_literal(self, node: StructLiteral, o: Any = None):
        struct_type = getattr(o, "expected_type", None)
        if struct_type is None or not is_struct_type(struct_type):
            raise RuntimeError("StructLiteral requires expected struct type")

        frame = o.frame
        members = self._get_struct_members(struct_type)
        struct_name = struct_type.struct_name

        code = self.emit.emit_new_instance(struct_name, frame)
        tmp_idx = frame.get_new_index()
        code += self.emit.emit_write_var("$tmp", struct_type, tmp_idx, frame)

        for (member_name, member_type), value in zip(members, node.values):
            code += self.emit.emit_read_var("$tmp", struct_type, tmp_idx, frame)
            access = Access(frame, o.sym)
            if isinstance(value, StructLiteral) and is_struct_type(member_type):
                access.expected_type = member_type
            value_code, value_type = self.visit(value, access)
            if is_float_type(member_type) and is_int_type(value_type):
                value_code += self.emit.emit_i2f(frame)
            code += value_code
            code += self.emit.emit_put_field(f"{struct_name}/{member_name}", member_type, frame)

        code += self.emit.emit_read_var("$tmp", struct_type, tmp_idx, frame)
        return code, struct_type

