#!/usr/bin/python3

import sys
import ply.lex as lex
import ply.yacc as yacc

import utils
from func import Func
from ast import ASTNode

tokens = (

	# TOKENS FOR RESERVED KEYWORDS HERE
	'INT',
	'FLOAT',
	'VOID',
	'MAIN',
	'IF',
	'WHILE',
	'ELSE',
	'RETURN',

	# REMAINING TOKENS HERE
	'NAME',
	'NUMBER',
	'FLOATNUM',
	'POINTER',
	'ASSIGN',
	'COMMA',
	'LFBRACK',
	'RFBRACK',
	'LPAREN',
	'RPAREN',
	'SEMICOLON',
	'AMPERSAND',
	'PLUS',
	'MINUS',
	'DIVIDE',
	'LTE',
	'GTE',
	'LT',
	'GT',
	'COMPAREEQUAL',
	'NEGATION',
	'COMPARENOTEQUAL',
	'OR',
	'AND'
)

reserved_words = {
	'int': 'INT',
	'void': 'VOID',
	'float': 'FLOAT',
	'main': 'MAIN',
	'if': 	'IF',
	'while': 'WHILE',
	'else': 'ELSE',
	'return': 'RETURN'
}


def t_FLOATNUM(t):
	r'\d+\.\d+'
	try:
		t.value = float(t.value)
	except ValueError:
		print("Float value too large %f", t.value)
		t.value = 0.0
	return t


def t_NUMBER(t):
	r'\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Integer value too large %d", t.value)
		t.value = 0
	return t


def t_NAME(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if t.value in reserved_words:
		t.type = reserved_words[t.value]
	return t


def t_error(t):
	print("Lexical Error at "+str(t.value))
	t.lexer.skip(1)
	sys.exit()


t_POINTER = r'\*'
t_ASSIGN = r'='
t_COMMA = r','
t_LFBRACK = r'{'
t_RFBRACK = r'}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_AMPERSAND = r'&'
t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/'

t_LTE = r'<='
t_GTE = r'>='
t_LT = r'<'
t_GT = r'>'
t_COMPAREEQUAL = r'=='
t_NEGATION = r'!'
t_COMPARENOTEQUAL = r'!='
t_OR = r'\|\|'
t_AND = r'&&'

t_ignore = " \t\n"


# Parsing rules
precedence = (
	('left', 'PLUS', 'MINUS'),
	('left', 'POINTER', 'DIVIDE'),
	('right', 'UMINUS'),
	('left', 'OR', 'AND'),
	('right', 'NEGATION'),
)


def p_statement_init(p):
	"""
	statement : globaldeclarations functionblocks
	"""


def p_globaldeclarations_init(p):
	"""
	globaldeclarations  : globaldeclarations globalvardecl SEMICOLON
						| globaldeclarations functiondecl SEMICOLON
						|
	"""


def p_globalvardecl(p):
	"""
	globalvardecl : type declarationlist
	"""
	for i in varSymDict:
		if varSymDict[i][0] == "default":
			varSymDict[i] = (p[1], varSymDict[i][1])


def p_declarationlist(p):
	"""
	declarationlist : pointerdef xdeclarationlist
	"""
	global currentScope
	global varSymDict
	(name, pointercount) = p[1]
	if (name, currentScope) not in varSymDict:
		varSymDict[(name, currentScope)] = ("default", pointercount)
	else:
		print("Variable "+str(name)+" defined twice in scope of "+str(currentScope))
		sys.exit()


def p_xdeclarationlist(p):
	"""
	xdeclarationlist : COMMA declarationlist
					|
	"""


def p_functiondecl(p):
	"""
	functiondecl    : type pointerdef LPAREN paramlist RPAREN
					| VOID pointerdef LPAREN paramlist RPAREN
	"""
	global paramList, funcSymDict
	funcName, funcRet, funcDerive = p[2][0], p[1], p[2][1]
	if(funcName not in funcSymDict):
		funcSymDict[funcName] = (funcRet, funcDerive, paramList)
		paramList = []
	else:
		print("Function "+str(funcName)+" primitive defined twice")
		sys.exit()


# def p_funcnamedecl(p):
# 	"""
# 	funcnamedecl : pointerdef
# 	"""


def p_paramlist(p):
	"""
	paramlist   : nonemptyparamlist
				|
	"""


def p_nonemptyparamlist(p):
	"""
	nonemptyparamlist : type pointerdef xparamlist
	"""
	global paramList
	paramList.insert(0, (p[1], p[2][1], p[2][0]))


def p_xparamlist(p):
	"""
	xparamlist  : COMMA nonemptyparamlist
				|
	"""


def p_pointerdef(p):
	"""
	pointerdef      : NAME
					| POINTER pointerdef
	"""
	if p[1] == "*":
		p[0] = (p[2][0], p[2][1] + 1)
	else:
		p[0] = (p[1], 0)


def p_type(p):
	"""
	type    : INT
			| FLOAT
	"""
	p[0] = p[1]


def p_functionblocks(p):
	"""
	functionblocks  : functionblock functionblocks
					|
	"""


def p_functionblock(p):
	"""
	functionblock   : functionblockname LFBRACK functionlines returnstmtforfunc SEMICOLON RFBRACK
					| functionblockname1 LFBRACK functionlines RETURN SEMICOLON RFBRACK
					| functionblockname1 LFBRACK functionlines RFBRACK
	"""
	# type, name, pointerdepth, paramList
	global FunctionNodes
	if p[4] == '}':
		temp = Func(p[1][1],p[1][0],p[1][2],p[1][3],p[3],[])
	elif p[4] == 'return':
		temp = Func(p[1][1],p[1][0],p[1][2],p[1][3],p[3],[])
	else:
		temp = Func(p[1][1],p[1][0],p[1][2],p[1][3],p[3],[p[4]])
	FunctionNodes.append(temp)

def p_functionblock_main(p):
	"""
	functionblock : mainblock
	"""

def p_returnstmtforfunc(p):
	"""
	returnstmtforfunc : returnstmt
	"""
	(funcRet, funcDerive, _) = funcSymDict[currentScope]
	temp = ASTNode('RETURN',funcRet ,funcDerive, [])
	if not utils.assignmentTypeCheck(temp, p[1], "return"):
		sys.exit()
	p[0] = ASTNode('RETURN', p[1].dtype, p[1].pointerdepth, [p[1]])


def p_returnstmt(p):
	"""
	returnstmt  : RETURN arithmeticexpr
	"""
	p[0] = p[2]


def p_functionblockname(p):
	"""
	functionblockname : type pointerdef LPAREN paramlist RPAREN
	"""
	global currentScope
	currentScope, _ = p[2]
	global paramList, funcSymDict, varSymDict
	funcName, funcRet, funcDerive = p[2][0], p[1], p[2][1]
	if(funcName not in funcSymDict):
		print("Function primitive not defined for "+str(funcName))
		sys.exit()
	else:
		utils.comparePrimitiveWithDef(funcName, funcRet, funcDerive, paramList, funcSymDict[funcName])
		for i in paramList:
			varSymDict[(i[2], currentScope)] = (i[0], i[1])
		temp = paramList[:]
		paramList = []
	p[0] = (p[1], p[2][0], p[2][1], temp)


def p_functionblockname1(p):
	"""
	functionblockname1 : VOID pointerdef LPAREN paramlist RPAREN
	"""
	global currentScope
	currentScope, _ = p[2]
	global paramList, funcSymDict, varSymDict
	funcName, funcRet, funcDerive = p[2][0], p[1], p[2][1]
	if(funcName not in funcSymDict):
		print("Function primitive not defined for "+str(funcName))
		sys.exit()
	else:
		utils.comparePrimitiveWithDef(funcName, funcRet, funcDerive, paramList, funcSymDict[funcName])
		for i in paramList:
			varSymDict[(i[2], currentScope)] = (i[0], i[1])
		temp = paramList[:]
		paramList = []
	p[0] = (p[1], p[2][0], p[2][1], temp)



def p_mainblock(p):
	"""
	mainblock   : VOID mainfunctionname LFBRACK functionlines RFBRACK
	"""
	global FunctionNodes
	temp = Func('Main','void',0,[],p[4],None)
	FunctionNodes.append(temp)
	p[0] = temp


def p_mainfunctionname(p):
	"""
	mainfunctionname : MAIN LPAREN RPAREN
	"""
	global currentScope
	currentScope = "main"


def p_functionlines(p):
	"""
	functionlines : functionvardeclarations functionwork
	"""
	p[0] = p[2]

def p_functiondeclarations(p):
	"""
	functionvardeclarations : functionvardeclarations functionvardeclaration SEMICOLON
							|
	"""


def p_functionvardeclaration(p):
	"""
	functionvardeclaration : type declarationlist
	"""
	global varSymDict
	for i in varSymDict:
		if varSymDict[i][0] == "default":
			varSymDict[i] = (p[1], varSymDict[i][1])


def p_functionwork_block(p):
	"""
	functionwork    : ifblock functionwork
					| whileblock functionwork
	"""
	temp = p[2][:]
	temp.insert(0,p[1])
	p[0] = temp


def p_functionwork_eps(p):
	"""
	functionwork : 
	"""
	p[0] = []


def p_functionwork_line(p):
	"""
	functionwork : functionworkline SEMICOLON functionwork
	"""
	temp = p[3][:]
	temp.insert(0,p[1])
	p[0] = temp



# def p_block(p):
# 	"""
# 	block   : ifblock
# 			| whileblock
# 	"""


def p_whileblock(p):
	"""
	whileblock : WHILE LPAREN condition RPAREN conditionalbody
	"""
	p[0] = ASTNode('WHILE', None, None, [p[3], p[5]])


def p_ifblock_if(p):
	"""
	ifblock : IF LPAREN condition RPAREN conditionalbody
	"""
	p[0] = ASTNode('IF', None, None, [p[3], p[5]])


def p_ifblock_else(p):
	"""
	ifblock : IF LPAREN condition RPAREN conditionalbody ELSE elseconditionalbody
	"""
	p[0] = ASTNode('IFELSE', None, None, [p[3], p[5], p[7]])


def p_elseconditionalbody_else(p):
	"""
	elseconditionalbody : conditionalbody
	"""
	p[0] = p[1]


def p_elseconditionalbody_elseif(p):
	"""
	elseconditionalbody : ifblock
	"""
	p[0] = p[1]


def p_conditionalbody(p):
	"""
	conditionalbody : LFBRACK functionwork RFBRACK
					| functionworkline SEMICOLON
	"""
	if(p[1] == '{'):
		p[0] = p[2]
	else:
		p[0] = [p[1]]


def p_condition(p):
	"""
	condition : booleanexpr
	"""
	p[0] = p[1]


def p_booleanexpr_term(p):
	"""
	booleanexpr : booleanexpr OR booleanexpr
				| booleanexpr AND booleanexpr
				| LPAREN booleanexpr RPAREN
				| NEGATION booleanexpr
	"""
	if(p[2] == '||'):
		p[0] = ASTNode('OR', None, None, [p[1], p[3]])
	elif(p[2] == '&&'):
		p[0] = ASTNode('AND', None, None, [p[1], p[3]])
	elif(p[1] == '!'):
		p[0] = ASTNode('NOT', None, None, [p[2]])
	else:
		p[0] = p[2]


def p_booleanexpr_boolfromarith(p):
	"""
	booleanexpr : boolfromarith
	"""
	p[0] = p[1]


def p_boolfromarith_def(p):
	"""
	boolfromarith   : arithmeticexpr LTE arithmeticexpr
					| arithmeticexpr GTE arithmeticexpr
					| arithmeticexpr LT arithmeticexpr
					| arithmeticexpr GT arithmeticexpr
					| arithmeticexpr COMPARENOTEQUAL arithmeticexpr
					| arithmeticexpr COMPAREEQUAL arithmeticexpr
	"""
	if not utils.assignmentTypeCheck(p[1], p[3], "comparison"):
		sys.exit()
	if(p[2] == '<='):
		p[0] = ASTNode('LE', None, None, [p[1], p[3]])
	elif(p[2] == '>='):
		p[0] = ASTNode('GE', None, None, [p[1], p[3]])
	elif(p[2] == '<'):
		p[0] = ASTNode('LT', None, None, [p[1], p[3]])
	elif(p[2] == '>'):
		p[0] = ASTNode('GT', None, None, [p[1], p[3]])
	elif(p[2] == '!='):
		p[0] = ASTNode('NE', None, None, [p[1], p[3]])
	else:
		p[0] = ASTNode('EQ', None, None, [p[1], p[3]])


def p_functionworkline(p):
	"""
	functionworkline    : assignment
						| functioncall
	"""
	p[0] = p[1]


# def p_functioncallstmt_leftpointer(p):
# 	"""
# 	functioncallstmt : startwithstar ASSIGN functioncall
# 	"""


# def p_functioncallstmt_leftvar(p):
# 	"""
# 	functioncallstmt : NAME ASSIGN functioncall
# 	"""


# def p_functioncallhandler(p):
# 	"""
# 	functioncallhandler : NAME LPAREN functionparam RPAREN
# 	"""
#
#
# def p_functionparam(p):
# 	"""
# 	functionparam   : nonemptyfunctionparam
# 					|
# 	"""
#
#
# def p_nonemptyfunctionparam(p):
# 	"""
# 	nonemptyfunctionparam : startwithany xnonemptyfunctionparam
# 	"""
#
#
# def p_xnonemptyfunctionparam(p):
# 	"""
# 	xnonemptyfunctionparam  : COMMA nonemptyfunctionparam
# 							|
# 	"""


def p_assignment_leftvar(p):
	"""
	assignment : NAME ASSIGN arithmeticexpr
	"""
	global currentScope, varSymDict
	(dtype, pointerdepth) = utils.giveVarSymOutput(p[1], currentScope, varSymDict)
	nodeL = ASTNode('VAR', dtype, pointerdepth, [p[1]])
	if(not utils.assignmentTypeCheck(nodeL, p[3], "assignment")):
		print("Type mismatch at assignment")
		sys.exit()
	p[0] = ASTNode('ASGN', nodeL.dtype, nodeL.pointerdepth, [nodeL, p[3]])


def p_assignment_leftpointer(p):
	"""
	assignment : startwithstar ASSIGN arithmeticexpr
	"""
	if(not utils.assignmentTypeCheck(p[1], p[3], "assignment")):
		print("Type mismatch at assignment")
		sys.exit()
	p[0] = ASTNode('ASGN', p[1].dtype, p[1].pointerdepth, [p[1], p[3]])


def p_startwithstar_define(p):
	"""
	startwithstar : POINTER startwithany
	"""
	if(p[2].pointerdepth - 1 < 0):
		print("Pointer depth less than zero")
		sys.exit()
	p[0] = ASTNode('DEREF', p[2].dtype, p[2].pointerdepth - 1, [p[2]])


def p_startwithany_define(p):
	"""
	startwithany    : POINTER startwithany
					| AMPERSAND NAME
					| NAME
	"""
	global varSymDict, currentScope
	if(p[1] == "*"):
		if(p[2].pointerdepth - 1 < 0):
			print("Pointer depth less than zero")
			sys.exit()
		p[0] = ASTNode('DEREF', p[2].dtype, p[2].pointerdepth - 1, [p[2]])
	elif(p[1] == "&"):
		(dtype, pointerdepth) = utils.giveVarSymOutput(p[2], currentScope, varSymDict)
		p[0] = ASTNode('ADDR', dtype, pointerdepth + 1, [ASTNode('VAR', dtype, pointerdepth, [p[2]])])
	else:
		(dtype, pointerdepth) = utils.giveVarSymOutput(p[1], currentScope, varSymDict)
		p[0] = ASTNode('VAR', dtype, pointerdepth, [p[1]])


def p_arithmeticexpr_binop(p):
	"""
	arithmeticexpr  : arithmeticexpr PLUS arithmeticexpr
					| arithmeticexpr MINUS arithmeticexpr
					| arithmeticexpr POINTER arithmeticexpr
					| arithmeticexpr DIVIDE arithmeticexpr
	"""
	if(p[2] == "+"):
		if(not utils.arithmeticTypeCheck(p[1], p[3])):
			print("Type mismatch at +")
			sys.exit()
		p[0] = ASTNode('PLUS', p[1].dtype, p[1].pointerdepth, [p[1], p[3]])
	elif(p[2] == "-"):
		if(not utils.arithmeticTypeCheck(p[1], p[3])):
			print("Type mismatch at -")
			sys.exit()
		p[0] = ASTNode('MINUS', p[1].dtype, p[1].pointerdepth, [p[1], p[3]])
	elif(p[2] == "*"):
		if(not utils.arithmeticTypeCheck(p[1], p[3])):
			print("Type mismatch at *")
			sys.exit()
		p[0] = ASTNode('MUL', p[1].dtype, p[1].pointerdepth, [p[1], p[3]])
	else:
		if(not utils.arithmeticTypeCheck(p[1], p[3])):
			print("Type mismatch at /")
			sys.exit()
		p[0] = ASTNode('DIV', p[1].dtype, p[1].pointerdepth, [p[1], p[3]])


def p_arithmeticexpr_uminus(p):
	"""
	arithmeticexpr : MINUS arithmeticexpr %prec UMINUS
	"""
	if(p[2].pointerdepth == 0):
		if(p[2].data == 'VAR'):
			print("Direct base type access in UMINUS operation")
			sys.exit()
	p[0] = ASTNode('UMINUS', p[2].dtype, p[2].pointerdepth, [p[2]])


def p_arithmeticexpr_paren(p):
	"""
	arithmeticexpr : LPAREN arithmeticexpr RPAREN
	"""


def p_arithmeticexpr_terminal_number(p):
	"""
	arithmeticexpr  : NUMBER
	"""
	p[0] = ASTNode('CONST', 'int', 0, [p[1]])


def p_arithmeticexpr_terminal_floatnumber(p):
	"""
	arithmeticexpr : FLOATNUM
	"""
	p[0] = ASTNode('CONST', 'float', 0, [p[1]])


def p_arithmeticexpr_terminal_startwithany(p):
	"""
	arithmeticexpr : startwithany
	"""
	p[0] = p[1]


def p_arithmeticexpr_terminal_functioncall(p):
	"""
	arithmeticexpr : functioncall
	"""
	p[0] = p[1]


def p_functioncall(p):
	"""
	functioncall : functioncallname LPAREN functioncalllist RPAREN
	"""
	global functionCallParamList, funcSymDict
	p[0] = ASTNode('CALL', funcSymDict[p[1]][0], funcSymDict[p[1]][1], [p[1], functionCallParamList])
	utils.checkTypeParams(functionCallParamList, funcSymDict[p[1]][2], p[1])
	functionCallParamList = []


def p_functioncallname(p):
	"""
	functioncallname : NAME
	"""
	p[0] = p[1]


def p_functioncalllist(p):
	"""
	functioncalllist    : functioncalllistnotempty
						|
	"""


def p_functioncalllistnotempty(p):
	"""
	functioncalllistnotempty : arithmeticexpr xfunctioncalllistnotempty
	"""
	global functionCallParamList
	functionCallParamList.insert(0, p[1])


def p_xfunctioncalllistnotempty(p):
	"""
	xfunctioncalllistnotempty   : COMMA functioncalllistnotempty
								|
	"""


def p_error(p):
	if p:
		print("syntax error at {0}".format(p.value))
	else:
		print("syntax error at EOF")
	sys.exit()


def process(lines):
	global FunctionNodes , fileName
	lex.lex()
	yacc.yacc()
	yacc.parse(lines)
	utils.printdict(varSymDict, 1)
	utils.printdict(funcSymDict, 0)
	utils.printFunctionNodesAST(FunctionNodes,fileName)
	print("Successfully Parsed")


if __name__ == "__main__":
	paramList = []
	functionCallParamList = []
	currentScope = "_"
	varSymDict = {} # (name, currScope) -> (type, pointercount)
	funcSymDict = {} # funcSymDict[funcName] = (funcRet, funcDerive, paramList) #paramlist->(type, pointercount, name)
	pointerCount = 0
	FunctionNodes = []
	fileName = sys.argv[1]
	with open(fileName, "r") as myFile:
		data = myFile.read()
	process(data)
