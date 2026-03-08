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

options {
    language=Python3;
}

// ------------ PARSER START----------------------------
program: decl_list EOF;

decl_list: declaration decl_list | ;
declaration: func_decl | struct_decl ;
variable_decl: AUTO IDENTIFIER opt_init SEMI | type IDENTIFIER opt_init SEMI ;
opt_init: ASSIGNMENT expr | ;

struct_decl: STRUCT IDENTIFIER LBRACE struct_member_list RBRACE SEMI? ;
struct_member_list: struct_member struct_member_list | ;
struct_member: type IDENTIFIER SEMI ;
struct_literal: LBRACE struct_literal_elements RBRACE | LBRACE RBRACE ;
struct_literal_elements: expr | expr COMMA struct_literal_elements ;

func_decl: opt_return_type IDENTIFIER LPAREN opt_param_list RPAREN block ;
opt_return_type: return_type | ;
return_type: type | VOID ;

opt_param_list: param_list | ;
param_list: param | param COMMA param_list ;
param: type IDENTIFIER;

type: INT | FLOAT | STRING | IDENTIFIER;

block: LBRACE stmt_list RBRACE; 
stmt_list: stmt stmt_list | ; 
stmt: var_decl_stmt
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

var_decl_stmt: AUTO IDENTIFIER opt_init SEMI | type IDENTIFIER opt_init SEMI ;

if_stmt: IF LPAREN expr RPAREN stmt opt_else ;
opt_else: ELSE stmt | ;

while_stmt: WHILE LPAREN expr RPAREN stmt ;

for_stmt: FOR LPAREN opt_for_init SEMI opt_expr SEMI opt_for_update RPAREN stmt ;

opt_for_init: for_init | ;
for_init: AUTO IDENTIFIER opt_init 
        | type IDENTIFIER opt_init 
        | lhs ASSIGNMENT expr ;

opt_for_update: for_update | ;
for_update
    : lhs ASSIGNMENT expr
    | inc_dec_list postfix_expr
    | primary_expr inc_dec_list
    ;

inc_dec_list : inc_dec_op | inc_dec_op inc_dec_list;
inc_dec_op : INCREMENT | DECREMENT ;

switch_stmt: SWITCH LPAREN expr RPAREN LBRACE switch_clause_list RBRACE ;
switch_clause_list: case_list default_clause case_list | case_list;
case_list: case_clause case_list | ;

case_clause: CASE expr COLON stmt_list ;
default_clause: DEFAULT COLON stmt_list ;

break_stmt: BREAK SEMI;
continue_stmt: CONTINUE SEMI;
return_stmt: RETURN opt_expr SEMI;

expr_stmt: expr SEMI ;

expr: lhs ASSIGNMENT expr | logical_or_expr ;

lhs: IDENTIFIER | primary_expr DOT IDENTIFIER ;

logical_or_expr: logical_or_expr OR logical_and_expr | logical_and_expr ;
logical_and_expr: logical_and_expr AND equality_expr | equality_expr ;

equality_expr: equality_expr (EQUAL | NOT_EQUAL) relational_expr | relational_expr ;
relational_expr: relational_expr (LT | LE | GT | GE) additive_expr | additive_expr ;
additive_expr: additive_expr (ADD | SUB) multiplicative_expr | multiplicative_expr ;
multiplicative_expr: multiplicative_expr (MUL | DIV | MOD) unary_expr | unary_expr ;

unary_expr
    : NOT unary_expr
    | SUB unary_expr
    | ADD unary_expr
    | prefix_expr
    ;

prefix_expr
    : inc_dec_op prefix_expr
    | postfix_expr
    ;

postfix_expr
    : postfix_expr inc_dec_op
    | primary_expr
    ;

primary_expr
    : literal
    | IDENTIFIER
    | func_call
    | struct_literal
    | LPAREN expr RPAREN
    | primary_expr DOT IDENTIFIER
    ;

opt_expr: expr | ;

// 14. --- PRIMARY / CALL / ACCESS ---
func_call: IDENTIFIER LPAREN opt_arg_list RPAREN;
opt_arg_list: arg_list | ;
arg_list: expr | expr COMMA arg_list ;

literal: INTLIT | FLOATLIT | STRINGLIT ;

// ------------ PARSER END----------------------------

// ------------ LEXER START----------------------------

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

ADD        : '+';
SUB        : '-';
MUL        : '*';
DIV        : '/';
MOD        : '%';
NOT        : '!';
AND        : '&&';
OR         : '||';
EQUAL      : '==';
NOT_EQUAL  : '!=';
LT         : '<';
GT         : '>';
LE         : '<=';
GE         : '>=';
ASSIGNMENT : '=';
INCREMENT  : '++';
DECREMENT  : '--';
DOT        : '.';

LPAREN     : '(';
RPAREN     : ')';
LBRACE     : '{';
RBRACE     : '}';
SEMI       : ';';
COMMA      : ',';
COLON      : ':';

// --- STRING ERROR HANDLING ---
fragment ESCAPE_SEQUENCE : '\\' [bfnrt"\\] ;

ILLEGAL_ESCAPE
    : '"' (ESCAPE_SEQUENCE | ~('\\' | '"' | '\n' | '\r'))* '\\' ~[bfnrt"\\\r\n]
      { self.text = self.text[1:] }
    ;

UNCLOSE_STRING
    : '"' (ESCAPE_SEQUENCE | ~('\\' | '"' | '\n' | '\r'))* '\\'? ( '\n' | '\r' | EOF )
      { self.text = self.text[1:].rstrip('\n\r') }
    ;

STRINGLIT
    : '"' (ESCAPE_SEQUENCE | ~('\\' | '"' | '\n' | '\r'))* '"'
      { self.text = self.text[1:-1] }
    ;

fragment DIGIT    : [0-9] ;
fragment LETTER   : [a-zA-Z_] ;
fragment EXPONENT : [Ee] [+-]? DIGIT+ ;

IDENTIFIER : LETTER (LETTER | DIGIT)* ;

FLOATLIT: DIGIT+ DOT DIGIT* EXPONENT?  
        | DOT DIGIT+ EXPONENT?         
        | DIGIT+ EXPONENT;

INTLIT: DIGIT+ ;

WS : [ \t\r\n\f]+ -> skip ;
BLOCK_COMMENT : '/*' .*? '*/' -> skip;
LINE_COMMENT  : '//' ~[\r\n]* -> skip;

ERROR_CHAR : . ;

// ------------ LEXER END----------------------------