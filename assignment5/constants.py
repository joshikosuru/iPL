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

unaryOpMap = {
    "VAR" : "",
    "ADDR" : "&",
    "UMINUS" : "-",
    "CONST" : "",
    "DEREF" : "*",
    "NOT" : "!"
}
