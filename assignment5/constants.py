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
	"NOT" : "xori",
	"UMINUS" : "negu"
}

FloatSBinaryOpMap = {
    "LE" : "c.le.s",
	"GE" : "c.le.s",
	"LT" : "c.lt.s",
	"GT" : "c.lt.s",
	"NE" : "c.eq.s",
	"EQ" : "c.eq.s"
}

unaryOpMap = {
    "VAR" : "",
    "ADDR" : "&",
    "UMINUS" : "-",
    "CONST" : "",
    "DEREF" : "*",
    "NOT" : "!"
}
