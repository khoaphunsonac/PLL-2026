from build.TyCVisitor import TyCVisitor
from src.utils.nodes import *

class ASTGeneration(TyCVisitor):

    # ============================================================================
    # 1. Program and Top-level Declarations
    # ============================================================================
    def visitProgram(self, ctx):
        decls = self.visit(ctx.decl_list())
        return Program(decls)

    def visitDecl_list(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        current_decl = self.visit(ctx.declaration())
        next_decls = self.visit(ctx.decl_list())
        return [current_decl] + next_decls

    def visitDeclaration(self, ctx):
        return self.visit(ctx.getChild(0))

    def visitVar_decl_stmt(self, ctx):
        name = ctx.IDENTIFIER().getText()
        init_value = self.visit(ctx.opt_init())

        if ctx.AUTO():
            var_type = None
        else:
            var_type = self.visit(ctx.type_())

        return VarDecl(var_type, name, init_value)

    def visitOpt_init(self, ctx):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.expr())

    # ============================================================================
    # 2. Struct Declarations
    # ============================================================================
    def visitStruct_decl(self, ctx):
        name = ctx.IDENTIFIER().getText()
        members = self.visit(ctx.struct_member_list())
        return StructDecl(name, members)

    def visitStruct_member_list(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        member = self.visit(ctx.struct_member())
        next_members = self.visit(ctx.struct_member_list())
        return [member] + next_members

    def visitStruct_member(self, ctx):
        member_type = self.visit(ctx.type_())
        name = ctx.IDENTIFIER().getText()
        return MemberDecl(member_type, name)

    # ============================================================================
    # 3. Function Declarations & Types
    # ============================================================================
    def visitFunc_decl(self, ctx):
        return_type = self.visit(ctx.opt_return_type())
        name = ctx.IDENTIFIER().getText()
        params = self.visit(ctx.opt_param_list())
        body = self.visit(ctx.block())
        return FuncDecl(return_type, name, params, body)

    def visitOpt_return_type(self, ctx):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.return_type())

    def visitReturn_type(self, ctx):
        if ctx.VOID():
            return VoidType()
        return self.visit(ctx.type_())

    def visitOpt_param_list(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return self.visit(ctx.param_list())

    def visitParam_list(self, ctx):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.param())]
        current_param = self.visit(ctx.param())
        next_params = self.visit(ctx.param_list())
        return [current_param] + next_params

    def visitParam(self, ctx):
        param_type = self.visit(ctx.type_())
        name = ctx.IDENTIFIER().getText()
        return Param(param_type, name)

    def visitType(self, ctx):
        if ctx.INT(): return IntType()
        elif ctx.FLOAT(): return FloatType()
        elif ctx.STRING(): return StringType()
        else: return StructType(ctx.IDENTIFIER().getText())

    # ============================================================================
    # 4. Statements
    # ============================================================================
    def visitBlock(self, ctx):
        stmts = self.visit(ctx.stmt_list())
        return BlockStmt(stmts)

    def visitStmt_list(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        current_stmt = self.visit(ctx.stmt())
        next_stmts = self.visit(ctx.stmt_list())
        return [current_stmt] + next_stmts

    def visitStmt(self, ctx):
        return self.visit(ctx.getChild(0))

    def visitIf_stmt(self, ctx):
        condition = self.visit(ctx.expr())
        then_stmt = self.visit(ctx.stmt())
        else_stmt = self.visit(ctx.opt_else())
        return IfStmt(condition, then_stmt, else_stmt)

    def visitOpt_else(self, ctx):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.stmt())

    def visitWhile_stmt(self, ctx):
        condition = self.visit(ctx.expr())
        body = self.visit(ctx.stmt())
        return WhileStmt(condition, body)

    def visitFor_stmt(self, ctx):
        init = self.visit(ctx.opt_for_init())
        condition = self.visit(ctx.opt_expr())
        update = self.visit(ctx.opt_for_update())
        body = self.visit(ctx.stmt())
        return ForStmt(init, condition, update, body)

    def visitOpt_for_init(self, ctx):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.for_init())

    def visitFor_init(self, ctx):
        if ctx.AUTO() or ctx.type_():
            var_type = None if ctx.AUTO() else self.visit(ctx.type_())
            name = ctx.IDENTIFIER().getText()
            init_value = self.visit(ctx.opt_init())
            return VarDecl(var_type, name, init_value)
        else:
            lhs = self.visit(ctx.lhs())
            rhs = self.visit(ctx.expr())
            return ExprStmt(AssignExpr(lhs, rhs))

    def visitOpt_for_update(self, ctx):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.for_update())

    def visitFor_update(self, ctx):
        if ctx.ASSIGNMENT():
            lhs = self.visit(ctx.lhs())
            rhs = self.visit(ctx.expr())
            return AssignExpr(lhs, rhs)
        elif ctx.postfix_expr():
            ops = self.visit(ctx.inc_dec_list())
            expr = self.visit(ctx.postfix_expr())
            for op in reversed(ops):
                expr = PrefixOp(op, expr)
            return expr
        else:
            expr = self.visit(ctx.primary_expr())
            ops = self.visit(ctx.inc_dec_list())
            for op in ops:
                expr = PostfixOp(op, expr)
            return expr

    def visitInc_dec_list(self, ctx):
        op = self.visit(ctx.inc_dec_op())
        if ctx.getChildCount() == 1:
            return [op]
        return [op] + self.visit(ctx.inc_dec_list())

    def visitInc_dec_op(self, ctx):
        return ctx.getText()

    def visitSwitch_stmt(self, ctx):
        expr = self.visit(ctx.expr())
        cases, default_case = self.visit(ctx.switch_clause_list())
        return SwitchStmt(expr, cases, default_case)

    def visitSwitch_clause_list(self, ctx):
        if ctx.default_clause():
            cases_before = self.visit(ctx.case_list(0))
            default_case = self.visit(ctx.default_clause())
            cases_after = self.visit(ctx.case_list(1))
            return cases_before + cases_after, default_case
        else:
            cases = self.visit(ctx.case_list(0))
            return cases, None

    def visitCase_list(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.case_clause())] + self.visit(ctx.case_list())

    def visitCase_clause(self, ctx):
        expr = self.visit(ctx.expr())
        stmts = self.visit(ctx.stmt_list())
        return CaseStmt(expr, stmts)

    def visitDefault_clause(self, ctx):
        stmts = self.visit(ctx.stmt_list())
        return DefaultStmt(stmts)

    def visitBreak_stmt(self, ctx):
        return BreakStmt()

    def visitContinue_stmt(self, ctx):
        return ContinueStmt()

    def visitReturn_stmt(self, ctx):
        expr = self.visit(ctx.opt_expr())
        return ReturnStmt(expr)

    def visitExpr_stmt(self, ctx):
        expr = self.visit(ctx.expr())
        return ExprStmt(expr)

    def visitOpt_expr(self, ctx):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.expr())

    # ============================================================================
    # 5. Expressions
    # ============================================================================
    def visitExpr(self, ctx):
        if ctx.ASSIGNMENT():
            lhs = self.visit(ctx.lhs())
            rhs = self.visit(ctx.expr())
            return AssignExpr(lhs, rhs)
        return self.visit(ctx.logical_or_expr())

    def visitLhs(self, ctx):
        if ctx.getChildCount() == 1:
            return Identifier(ctx.IDENTIFIER().getText())
        obj = self.visit(ctx.primary_expr())
        member = ctx.IDENTIFIER().getText()
        return MemberAccess(obj, member)

    def visitLogical_or_expr(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.logical_and_expr())
        left = self.visit(ctx.logical_or_expr())
        op = ctx.OR().getText()
        right = self.visit(ctx.logical_and_expr())
        return BinaryOp(left, op, right)

    def visitLogical_and_expr(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.equality_expr())
        left = self.visit(ctx.logical_and_expr())
        op = ctx.AND().getText()
        right = self.visit(ctx.equality_expr())
        return BinaryOp(left, op, right)

    def visitEquality_expr(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.relational_expr())
        left = self.visit(ctx.equality_expr())
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.relational_expr())
        return BinaryOp(left, op, right)

    def visitRelational_expr(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.additive_expr())
        left = self.visit(ctx.relational_expr())
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.additive_expr())
        return BinaryOp(left, op, right)

    def visitAdditive_expr(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.multiplicative_expr())
        left = self.visit(ctx.additive_expr())
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.multiplicative_expr())
        return BinaryOp(left, op, right)

    def visitMultiplicative_expr(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.unary_expr())
        left = self.visit(ctx.multiplicative_expr())
        op = ctx.getChild(1).getText()
        right = self.visit(ctx.unary_expr())
        return BinaryOp(left, op, right)

    def visitUnary_expr(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.prefix_expr())
        op = ctx.getChild(0).getText()
        operand = self.visit(ctx.unary_expr())
        return PrefixOp(op, operand)

    def visitPrefix_expr(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.postfix_expr())
        op = self.visit(ctx.inc_dec_op())
        operand = self.visit(ctx.prefix_expr())
        return PrefixOp(op, operand)

    def visitPostfix_expr(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.primary_expr())
        operand = self.visit(ctx.postfix_expr())
        op = self.visit(ctx.inc_dec_op())
        return PostfixOp(op, operand)

    def visitPrimary_expr(self, ctx):
        if ctx.literal(): return self.visit(ctx.literal())
        elif ctx.func_call(): return self.visit(ctx.func_call())
        elif ctx.struct_literal(): return self.visit(ctx.struct_literal())
        elif ctx.LPAREN(): return self.visit(ctx.expr())
        elif ctx.DOT():
            obj = self.visit(ctx.primary_expr())
            member = ctx.IDENTIFIER().getText()
            return MemberAccess(obj, member)
        else: return Identifier(ctx.IDENTIFIER().getText())

    # ============================================================================
    # 6. Literals, Struct Initialization & Function Calls
    # ============================================================================
    def visitFunc_call(self, ctx):
        name = ctx.IDENTIFIER().getText()
        args = self.visit(ctx.opt_arg_list())
        return FuncCall(name, args)

    def visitOpt_arg_list(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return self.visit(ctx.arg_list())

    def visitArg_list(self, ctx):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.expr())]
        current_expr = self.visit(ctx.expr())
        next_exprs = self.visit(ctx.arg_list())
        return [current_expr] + next_exprs

    def visitStruct_literal(self, ctx):
        # Tránh lỗi nếu grammar của bạn dùng opt_ hay dùng trực tiếp
        if hasattr(ctx, 'opt_struct_literal_elements') and ctx.opt_struct_literal_elements():
            values = self.visit(ctx.opt_struct_literal_elements())
            return StructLiteral(values)
        elif hasattr(ctx, 'struct_literal_elements') and ctx.struct_literal_elements():
            values = self.visit(ctx.struct_literal_elements())
            return StructLiteral(values)
        return StructLiteral([])

    def visitOpt_struct_literal_elements(self, ctx):
        if ctx.getChildCount() == 0:
            return []
        return self.visit(ctx.struct_literal_elements())

    def visitStruct_literal_elements(self, ctx):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.expr())]
        current_expr = self.visit(ctx.expr())
        next_exprs = self.visit(ctx.struct_literal_elements())
        return [current_expr] + next_exprs

    def visitLiteral(self, ctx):
        if ctx.INTLIT(): return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.FLOATLIT(): return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif ctx.STRINGLIT(): return StringLiteral(ctx.STRINGLIT().getText())