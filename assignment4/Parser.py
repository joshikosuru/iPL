#!/usr/bin/python3

import sys
import ply.lex as lex
import ply.yacc as yacc

from classes import Tree,giveCfgFile

tokens = (

	# TOKENS FOR RESERVED KEYWORDS HERE
	'INT',
	'VOID',
	'MAIN',
	'IF',
	'WHILE',
	'ELSE',

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
	'int' : 'INT',
	'void' : 'VOID',
	'main' : 'MAIN',
	'if' : 	'IF',
	'while' : 'WHILE',
	'else' : 'ELSE'
}

def t_NUMBER(t):
	r'\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Integer value too large %d", t.value)
		t.value = 0
	return t

def t_FLOATNUM(t):
	r'[0-9]+\.[0-9]+'
	try:
		t.value = float(t.value)
	except ValueError:
		print("Float value too large %f", t.value)
		t.value = 0.0
	return t

def t_NAME(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if t.value in reserved_words:
		t.type = reserved_words[t.value]
	return t

def t_error(t):
	print("Syntax Error")
	sys.exit()
	t.lexer.skip(1)

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
	('left','OR','AND'),
	('right','NEGATION'),
)



################ INITIAL READING INTO void main(){ 'code' }  ##############
def p_statement_INIT(p):
	"""
	statement : VOID MAIN LPAREN RPAREN LFBRACK lines RFBRACK
	"""
	global rootList
	for line in p[6]:
		rootList.append(line)
	p[0] = p[6]


# LINES := line; REMAINING LINES
def p_lines_line(p):
	"""
	lines : line SEMICOLON lines
	"""
	if (p[1][1]):
		# is assignment
		returnList = []
		returnList.append(p[1][0])
		for listitem in p[3]:
			returnList.append(listitem)
		p[0] = returnList
	else:
		p[0] = p[3]


# WHEN ALL LINES ARE FINISHED
def p_lines_eps(p):
	"""
	lines : 
	"""
	p[0] = []

def p_lines_defblock(p):
	""" 
	lines : ifblock lines
			| whileblock lines 
	"""

	returnList = []
	returnList.append(p[1])

	for listitem in p[2]:
		returnList.append(listitem)
	p[0] = returnList

############### IF - WHILE CONDITIONAL HANDLING ##############

def p_ifblock_if(p):
	"""
	ifblock : IF LPAREN CONDITION  RPAREN conditionalbody
	"""
	x = Tree(p[3],p[5],'IF')
	p[0] = x

def p_whileblock_def(p):
	"""
	whileblock : WHILE LPAREN CONDITION RPAREN conditionalbody
	"""
	x = Tree(p[3],p[5],'WHILE')
	p[0] = x

def p_ifblock_ifelse(p):
	"""
	ifblock : IF LPAREN CONDITION RPAREN  conditionalbody ELSE ifelsehandler
	"""

	x = Tree(p[3],[p[5],p[7]],'IFELSE')

	p[0] = x

def p_ifelsehandler_terminate(p):
	"""
	ifelsehandler : conditionalbody
	"""
	p[0]=p[1]

def p_ifelsehandler_nem(p):
	"""
	ifelsehandler : ifblock
	"""
	p[0]=[p[1]]

def p_conditionalbody_def(p):
	"""
	conditionalbody : line SEMICOLON 
					| LFBRACK lines RFBRACK 
	"""	
	if p[1] == '{':
		p[0] = p[2]
	else :
		if p[1][1]:
			p[0] = [p[1][0]]
		else :
			sys.exit()
			p[0] = Tree(None,None,'None')

def p_CONDITION_exist(p):
	"""
	CONDITION : booleanexpr
	"""
	p[0]=p[1]

def p_booleanexpr_term(p):
	"""
	booleanexpr : booleanexpr OR booleanexpr
	            | booleanexpr AND booleanexpr
	            | LPAREN booleanexpr RPAREN
	            | NEGATION booleanexpr
	"""
	if p[2] == '||':
		x = Tree(p[1],p[3],'OR')
	elif p[2] == '&&':
		x = Tree(p[1],p[3],'AND')
	elif p[1] == '(':
		x = p[2]
	else:
		x = Tree(p[2],None,'NOT')

	p[0] = x


def p_boolfromarith_def(p):
	"""
	boolfromarith : arithmeticexpr LTE arithmeticexpr
		        	 | arithmeticexpr GTE arithmeticexpr
		        	 | arithmeticexpr LT arithmeticexpr
		        	 | arithmeticexpr GT arithmeticexpr
		        	 | arithmeticexpr COMPARENOTEQUAL arithmeticexpr
		        	 | arithmeticexpr COMPAREEQUAL arithmeticexpr
	"""
	if p[2] == '<=':
		x = Tree(p[1][0], p[3][0], 'LE')
	elif p[2] == '>=':
		x = Tree(p[1][0], p[3][0], 'GE')
	elif p[2] == '<':
		x = Tree(p[1][0], p[3][0], 'LT')
	elif p[2] == '>':
		x = Tree(p[1][0], p[3][0], 'GT')
	elif p[2] == '!=':
		x = Tree(p[1][0], p[3][0], 'NE')
	elif p[2] == '==':
		x = Tree(p[1][0], p[3][0], 'EQ')

	p[0] = x



	

def p_booleanexpr_boolfromarith(p):
	"""
	booleanexpr : boolfromarith
	"""
	p[0] = p[1]

################ IF - WHILE CONDITIONAL HANDLING END #########



# DIVIDING LINE AS DECLARATION OR ASSIGNMENT
def p_line_decl(p):
	"""
	line : INT decllist
		 | assignmentlist
	"""
	if p[1] == 'int':
		p[0] = [p[2],False]
	else:
		p[0] = [p[1],True]


############################# HANDLING DECLARATION #####################################

# HANDLING DECLARATION LIST FOR POINTER DECLARATION
def p_declist_ts(p):
	"""
	decllist : pointerdef x
	"""
	global noOfPointerDecl
	noOfPointerDecl += 1


# TERMINAL RULES FOR POINTER DECLARATION
def p_pointerdef_ch(p):

	"""
	pointerdef : POINTER NAME
					| POINTER pointerdef
	"""
	p[0] = p[1]+p[2]


# POINTER DECLARATION AFTER COMMA
def p_x_ts(p):
	"""
	x : COMMA pointerdef x
	"""
	global noOfPointerDecl
	p[0] = p[3]
	noOfPointerDecl += 1


# HANDLING DECLARATION LIST FOR VARIABLE DECLARATION
def p_decllist_id(p):
	"""
	decllist : NAME x
	"""
	global noOfScalarDecl
	noOfScalarDecl += 1
	p[0] = p[2]


# VARIABLE DECLARATION AFTER COMMA
def p_x_listhandle(p):
	"""
	x : COMMA  NAME x
	"""
	global noOfScalarDecl
	p[0] = p[3]
	noOfScalarDecl += 1


# TERINATING CONDITION FOR x
def p_x_eps(p):
	"""
	x : 
	"""

########### RULES FOR HANDLING DECLARATIONS END #############


########### RULES FOR HANDLING ASSIGNMENTS AND CONSTRUCTION OF AST ##############

# ONLY SINGLE ASSIGNMENT IN A LINE ALLOWED
def p_assignmentlist_single(p):
	"""
	assignmentlist : assignment
	"""
	parseTree = p[1]
	p[0] =p[1]
	# global rootList
	# rootList.append(parseTree)


# ASSIGNMENT WITH LHS AS NAME (SHOULD NOT HAVE ALL CONSTANTS ON RIGHT SIDE)
def p_assignment_new_name(p):
	"""
	assignment : NAME ASSIGN arithmeticexpr
	"""
	global noOfAssignDecl
	noOfAssignDecl +=1
	p[0] = Tree( Tree(p[1], None, 'VAR'), p[3][0], 'ASGN')
	if(not p[3][1]):
		print("syntax error at =")
		sys.exit()


# ASSIGNMENT WITH LHS AS POINTER
def p_assignment_new_startwithstar(p):
	"""
	assignment : startwithstar ASSIGN arithmeticexpr
	"""
	global noOfAssignDecl
	noOfAssignDecl +=1
	p[0] = Tree(p[1], p[3][0], 'ASGN')


# HANDLING ARITHMETIC EXPRESSION
def p_arithmeticexpr_binop(p):
	"""
	arithmeticexpr : arithmeticexpr PLUS arithmeticexpr
				   | arithmeticexpr MINUS arithmeticexpr
				   | arithmeticexpr POINTER arithmeticexpr
				   | arithmeticexpr DIVIDE arithmeticexpr
	"""
	if p[2] == '+':
		x = Tree(p[1][0], p[3][0], 'PLUS')
	elif p[2] == '-':
		x = Tree(p[1][0], p[3][0], 'MINUS')
	elif p[2] == '*':
		x = Tree(p[1][0], p[3][0], 'MUL')
	elif p[2] == '/':
		x = Tree(p[1][0], p[3][0], 'DIV')

	p[0] = [x, p[1][1] or p[3][1]]

# HANDLING -(EXPRESSION)
def p_arithmeticexpr_uminus(p):
	"""
	arithmeticexpr : MINUS arithmeticexpr %prec UMINUS
	"""
	p[0] = [Tree(p[2][0], None, 'UMINUS'), p[2][1]]


# HANDLING PARENTHESIS IN ARITHMETIC EXPRESSION
def p_arithmeticexpr_paren(p):
	"""
	arithmeticexpr : LPAREN arithmeticexpr RPAREN
	"""
	p[0] = p[2]


# TERMINAL HANDLING OF ARITHMETIC EXPRESSION INTO CONSTANT
def p_arithmeticexpr_terminal_NUMBER(p):
	"""
	arithmeticexpr : NUMBER
	"""
	p[0] = [Tree(p[1], None, 'CONST'), False]


# TERMINAL HANDLING OF ARITHMETIC EXPRESSION INTO NON CONSTANT
def p_arithmeticexpr_terminal_startwithany(p):
	"""
	arithmeticexpr : startwithany
	"""
	p[0] = [ p[1], True]


# HANDLING EXPRESSION STARTING WITH STAR
def p_startwithstar_define(p):
	"""
	startwithstar : POINTER startwithany
	"""
	p[0] = Tree(p[2], None, 'DEREF')


# 
def p_startwithany_define(p):
	"""
	startwithany : POINTER startwithany
				| AMPERSAND startwithany
				| NAME
	"""
	if p[1] == '*':
		x = Tree(p[2], None, 'DEREF')
	elif p[1] == '&':
		x = Tree(p[2], None, 'ADDR')
	else:
		x = Tree(p[1], None, 'VAR')
	p[0] = x
################# END ASSIGNMENT HANDLING ##########################


# ERROR HANDLER
def p_error(p):
	if p:
		print("syntax error at {0}".format(p.value))
	else:
		print("syntax error at EOF")
	sys.exit()


def process(data):	
	global file, rootList, noOfScalarDecl, noOfPointerDecl, noOfAssignDecl,cfg_file
	lex.lex()
	yacc.yacc()
	yacc.parse(data)
	file = open(file, "w")
	for x in rootList:
		x.giveOutputFile(0, file)
	file.close()
	cfg_file = open(cfg_file,"w")
	giveCfgFile(rootList,cfg_file)
	cfg_file.close()
	print("Successfully Parsed")
	# print(noOfScalarDecl)
	# print(noOfPointerDecl)
	# print(noOfAssignDecl)

if __name__ == "__main__":
	# To count number of assignments and declarations
	noOfScalarDecl = 0
	noOfPointerDecl = 0
	noOfAssignDecl = 0
	rootList = []
	with open (sys.argv[1], "r") as myfile:
		data = myfile.read()
		file = sys.argv[1]+".ast"
		cfg_file = sys.argv[1]+".cfg"
	process(data)