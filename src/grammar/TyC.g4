grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

// ------------ PARSER START----------------------------
program: decl_list EOF;

//1. --- DECLARATION ---
decl_list: declaration decl_list | ;
declaration: variable_decl | func_decl | struct_decl ;
variable_decl: AUTO IDENTIFIER opt_init SEMI | type IDENTIFIER opt_init SEMI ;

//2. --- STRUCT ---

struct_decl
    : STRUCT IDENTIFIER LBRACE struct_member_list RBRACE SEMI ;
struct_member_list
    : struct_member struct_member_list | ;
struct_member
    : type IDENTIFIER SEMI ;

//3. --- FUNCTION ---
func_decl: opt_return_type IDENTIFIER LPAREN opt_param_list RPAREN block ;
opt_return_type: return_type | ;
return_type: type | VOID ;

//4. --- PARAMETER ---
opt_param_list: param_list | ;
param_list: param | param COMMA param_list;
param: type IDENTIFIER;

//5. --- TYPE ---
type: INT | FLOAT | STRING | IDENTIFIER;
//6. --- BLOCK & STAMENT ---
block: LBRACE stmt_list RBRACE; 
stmt_list: stmt stmt_list | ; 
stmt: var_decl_stmt
    | assign_stmt
    | if_stmt
    | while_stmt
    | for_stmt
    | switch_stmt
    | break_stmt
    | continue_stmt
    | return_stmt
    | expr_stmt
    | block
    ;

//7. --- VARIABLE DECLARATION ---
var_decl_stmt: AUTO IDENTIFIER opt_init SEMI | type IDENTIFIER opt_init SEMI ;
opt_init: ASSIGNMENT expr | ;

//8. --- ASSIGNMENT ---
assign_stmt: lhs ASSIGNMENT expr SEMI ;
lhs: IDENTIFIER | members_access; 
//9. --- IF ---
if_stmt: IF LPAREN expr RPAREN stmt opt_else ;
opt_else: ELSE stmt | ;

//10. --- WHILE / FOR ---
while_stmt: WHILE LPAREN expr RPAREN stmt ;
for_stmt: FOR LPAREN opt_for_init SEMI opt_expr SEMI opt_for_update RPAREN stmt ;
opt_for_init: for_init | ;
for_init:     AUTO IDENTIFIER opt_init
            | type IDENTIFIER opt_init
            | lhs ASSIGNMENT expr ;
opt_for_update: for_update | ;
for_update: lhs ASSIGNMENT expr | expr ;
//11. --- SWITCH ---
switch_stmt: SWITCH LPAREN expr RPAREN LBRACE case_list opt_default RBRACE  ;
case_list: case_stmt case_list| ;
case_stmt: CASE INTLIT COLON stmt_list;
opt_default: default_stmt| ;
default_stmt: DEFAULT COLON stmt_list;

//12. --- JUMP STATEMENTS ---
break_stmt: BREAK SEMI;
continue_stmt: CONTINUE SEMI;
return_stmt: RETURN opt_expr SEMI;
//13. --- EXPRESSION (BNF + PRECEDENCE) ---
expr_stmt: expr SEMI ;
expr: logical_or_expr ;
logical_or_expr: logical_or_expr OR logical_and_expr | logical_and_expr ;
logical_and_expr: logical_and_expr AND equality_expr | equality_expr ;
equality_expr
    : equality_expr (EQUAL | NOT_EQUAL) relational_expr
    | relational_expr
    ;

relational_expr
    : relational_expr (LT | LE | GT | GE) additive_expr
    | additive_expr
    ;

additive_expr
    : additive_expr (ADD | SUB) multiplicative_expr
    | multiplicative_expr
    ;

multiplicative_expr
    : multiplicative_expr (MUL | DIV | MOD) unary_expr
    | unary_expr
    ;

unary_expr
    : (NOT | SUB | INCREMENT | DECREMENT) unary_expr
    | postfix_expr
    ;

postfix_expr
    : postfix_expr INCREMENT
    | postfix_expr DECREMENT
    | primary_expr
    ;

primary_expr
    : literal
    | IDENTIFIER
    | members_access
    | func_call
    | LPAREN expr RPAREN
    ;

opt_expr
    : expr
    | /* empty */
    ;

//14. --- PRIMARY / CALL / ACCESS ---
func_call: IDENTIFIER LPAREN opt_arg_list RPAREN;
opt_arg_list: arg_list| ;
arg_list: expr | expr COMMA arg_list ;
members_access: IDENTIFIER DOT IDENTIFIER | members_access DOT IDENTIFIER ;
//15. --- LITERAL ---
literal
    : INTLIT
    | FLOATLIT
    | STRINGLIT
    ;




// ------------ PARSER END----------------------------

// ------------ LEXER START----------------------------
// 1. --- KEYWORDS ---
AUTO     : 'auto';
BREAK    : 'break';
CASE     : 'case';
CONTINUE : 'continue';
DEFAULT  : 'default';
ELSE     : 'else';
FLOAT    : 'float';
FOR      : 'for';
IF       : 'if';
INT      : 'int';
RETURN   : 'return';
STRING   : 'string';
STRUCT   : 'struct';
SWITCH   : 'switch';
VOID     : 'void';
WHILE    : 'while';

//2. --- OPERATORS ---
ADD        : '+';
SUB       : '-';
MUL         : '*';
DIV         : '/';
MOD         : '%';

NOT         : '!';
AND         : '&&';
OR          : '||';

EQUAL       : '==';
NOT_EQUAL   : '!=';
LT          : '<';
GT          : '>';
LE          : '<=';
GE          : '>=';

ASSIGNMENT      : '=';

// Increment/Decrement
INCREMENT         : '++';
DECREMENT         : '--';

// Member Access (Struct)
DOT         : '.';

// --- SEPARATORS ---
LPAREN      : '(';
RPAREN      : ')';
LBRACE      : '{';
RBRACE      : '}';
LBRACK      : '[';
RBRACK      : ']';
SEMI        : ';';
COMMA       : ',';
COLON       : ':';

// 4. Identifiers & Literals 
IDENTIFIER: [a-zA-Z_'][a-zA-Z0-9_']*;
fragment DIGIT: [0-9];
fragment FRAC: '.'DIGIT*;
fragment EXPONENT: [Ee]'-'?DIGIT+;
FLOATLIT: DIGIT* (FRAC|FRAC? EXPONENT);
INTLIT: '0' | [1-9] DIGIT*;
STRINGLIT: ["] (ESCAPE_SEQUENCE | ~('\\' | '"' | '\r' | '\n'))* ["] { self.text = self.text[1:-1] };
fragment ESCAPE_SEQUENCE: '\\' [btnfr"'\\];

// 5. Whitespace & Comments

// Comments: Block trước, Line sau
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
// ------------ LEXER END----------------------------

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs

ERROR_CHAR: .;
ILLEGAL_ESCAPE
    : '"' (ESCAPE_SEQUENCE | ~('\\' | '"' | '\n' | '\r'))*
      '\\' ~[btnfr"'\\]
      {
          raise IllegalEscape(self.text[1:])
      }
    ;
UNCLOSE_STRING
    : '"' (ESCAPE_SEQUENCE | ~('\\' | '"' | '\n' | '\r'))*
      ( '\n' | '\r' | EOF )
      {
          raise UncloseString(self.text[1:-1])
      }
    ;
