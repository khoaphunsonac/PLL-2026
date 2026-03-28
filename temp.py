from functools import reduce
class Type: pass
class IntType(Type): pass
class BoolType(Type): pass 
class FloatType(Type): pass
class UType(Type): pass
class Symbol(): 
    def __init__(self, name, typ):
        self.name = name
        self.typ = typ
def infer(name, typ, env):
    for sym in env:
        if sym.name == name:
            sym.typ = typ 
            return typ
    return typ
    
class StaticCheck(Visitor):

    def visitProgram(self,ctx:Program,o):
        env = reduce(lambda a, c: self.visit(c, a), ctx.decl, [])
        for stmt in ctx.stmts:
            self.visit(stmt, env)

    def visitVarDecl(self,ctx:VarDecl,o): 
        return o + [Symbol(ctx.name, UType())]

    def visitAssign(self,ctx:Assign,o): 
        rt = self.visit(ctx.rhs,o)
        lt = self.visit(ctx.lhs,o)
        
        if type(lt) is UType and type(rt) is UType :
            raise TypeCannotBeInferred(ctx)
        elif type(lt) is UType:
            lt = infer(ctx.lhs.name, rt, o)
        elif type(rt) is UType:
            rt = infer(ctx.rhs.name, lt, o)
        elif type(lt) is type(rt) :
            return type(lt)
        if type(lt) is not type(rt):
            raise TypeMismatchInStatement(ctx)
        return o
    def visitBinOp(self,ctx:BinOp,o): 
        e1 = self.visit(ctx.e1,o)
        e2 = self.visit(ctx.e2,o)
        if ctx.op in ["+", "-", "*", "/"]:
            if type(e1) is UType:
                e1 = infer(ctx.e1.name, IntType(), o)
            if type(e2) is UType:
                e2 = infer(ctx.e2.name, IntType(), o)
                
            if type(e1) is IntType and type(e2) is IntType:
                return IntType()
            raise TypeMismatchInExpression(ctx)
            
        elif ctx.op in ["+.", "-.", "*.", "/."]:
            if type(e1) is UType:
                e1 = infer(ctx.e1.name, FloatType(), o)
            if type(e2) is UType:
                e2 = infer(ctx.e2.name, FloatType(), o)
                
            if type(e1) is FloatType and type(e2) is FloatType:
                return FloatType()
            raise TypeMismatchInExpression(ctx)
            
        elif ctx.op in [">", "="]:
            if type(e1) is UType:
                e1 = infer(ctx.e1.name, IntType(), o)
            if type(e2) is UType:
                e2 = infer(ctx.e2.name, IntType(), o)
                
            if type(e1) is IntType and type(e2) is IntType:
                return BoolType()
            raise TypeMismatchInExpression(ctx)
            
        elif ctx.op in [">.", "=."]:
            if type(e1) is UType:
                e1 = infer(ctx.e1.name, FloatType(), o)
            if type(e2) is UType:
                e2 = infer(ctx.e2.name, FloatType(), o)
                
            if type(e1) is FloatType and type(e2) is FloatType:
                return BoolType()
            raise TypeMismatchInExpression(ctx)
            
        elif ctx.op in ["&&", "||", ">b", "=b"]:
            if type(e1) is UType:
                e1 = infer(ctx.e1.name, BoolType(), o)
            if type(e2) is UType:
                e2 = infer(ctx.e2.name, BoolType(), o)
                
            if type(e1) is BoolType and type(e2) is BoolType:
                return BoolType()
            raise TypeMismatchInExpression(ctx)
        
    def visitUnOp(self, ctx: UnOp, o):
        et = self.visit(ctx.e, o)
        
        if ctx.op == "-":
            if type(et) is UType:
                et = infer(ctx.e.name, IntType(), o)
            if type(et) is IntType:
                return IntType()
            raise TypeMismatchInExpression(ctx)
            
        elif ctx.op == "-.":
            if type(et) is UType:
                et = infer(ctx.e.name, FloatType(), o)
            if type(et) is FloatType:
                return FloatType()
            raise TypeMismatchInExpression(ctx)
            
        elif ctx.op == "!":
            if type(et) is UType:
                et = infer(ctx.e.name, BoolType(), o)
            if type(et) is BoolType:
                return BoolType()
            raise TypeMismatchInExpression(ctx)
            
        elif ctx.op == "i2f":
            if type(et) is UType:
                et = infer(ctx.e.name, IntType(), o)
            if type(et) is IntType:
                return FloatType()
            raise TypeMismatchInExpression(ctx)
            
        elif ctx.op == "floor":
            if type(et) is UType:
                et = infer(ctx.e.name, FloatType(), o)
            if type(et) is FloatType:
                return IntType()
            raise TypeMismatchInExpression(ctx)

    def visitIntLit(self,ctx:IntLit,o): 
        return IntType()

    def visitFloatLit(self,ctx,o): 
        return FloatType()

    def visitBoolLit(self,ctx,o): 
        return BoolType()

    def visitId(self,ctx,o): 
        sym = next(filter(lambda x: x.name == ctx.name,o),False)
        if not sym: raise UndeclaredIdentifier(ctx.name)
        return sym.typ