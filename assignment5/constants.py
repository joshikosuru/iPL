binaryOperators = [
    "LE", "GE", "LT", "GT", "NE", "EQ", "OR", "AND", "PLUS", "MINUS", "MUL", "DIV", "ASGN"
]

unaryOperators = [
    "VAR", "ADDR", "UMINUS", "CONST", "DEREF", "NOT"
]

binaryOpMap = {
	"LE" : "<=",
	"GE" : ">=",
	"LT" : "<",
	"GT" : ">",
	"NE" : "!=",
	"EQ" : "==",
	"OR" : "||",
	"AND" : "&&",
	"PLUS" : "+",
	"MINUS" : "-",
	"MUL" : "*",
	"DIV" : "/",
	"ASGN" : "="
}

OpMap_asm = {
	"LE" : "sle",
	"GE" : "sle",
	"LT" : "slt",
	"GT" : "slt",
	"NE" : "sne",
	"EQ" : "seq",
	"OR" : "or",
	"AND" : "and",
	"PLUS" : "add",
	"MINUS" : "sub",
	"MUL" : "mul",
	"DIV" : "div",
	"ASGN" : "=",
	"NOT" : "not",
	"UMINUS" : "negu"
}

unaryOpMap = {
    "VAR" : "",
    "ADDR" : "&",
    "UMINUS" : "-",
    "CONST" : "",
    "DEREF" : "*",
    "NOT" : "!"
}
