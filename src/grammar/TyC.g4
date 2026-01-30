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
decl_list
    : declaration decl_list
    | /* empty */
    ;

//2. --- STRUCT ---

struct_decl
    : STRUCT IDENTIFIER '{' struct_member_list '}' ';'
    ;
struct_member_list
    : struct_member struct_member_list
    | /* empty */
    ;
struct_member
    : type IDENTIFIER ';'
    ;

//3. --- FUNCTION ---
func_decl
    : opt_return_type IDENTIFIER '(' opt_param_list ')' block
    ;
opt_return_type
    : return_type
    | /* empty */
    ;
return_type
    : type
    | VOID
    ;

//4. --- PARAMETER ---
opt_param_list
    : param_list
    | /* empty */
    ;
param_list
    : param
    | param ',' param_list
    ;
param
    : type IDENTIFIER
    ;

//5. --- TYPE ---
//6. --- BLOCK & STAMENT ---
//7. --- VARIABLE DECLARATION ---
//8. --- ASSIGNMENT ---
//9. --- IF ---
//10. --- WHILE / FOR ---
//11. --- SWITCH ---
//12. --- JUMP STATEMENTS ---
//13. --- EXPRESSION (BNF + PRECEDENCE) ---
//14. --- PRIMARY / CALL / ACCESS ---
//15. --- LITERAL ---





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
