#!/usr/bin/python3

import sys
import ply.lex as lex
import ply.yacc as yacc

tokens = (


	'INT',
	'VOID',
	'MAIN',

	'NAME', 
	'NUMBER',
	'POINTER', 
	'ASSIGN', 
	'COMMA', 
	'LFBRACK', 
	'RFBRACK', 
	'LPAREN', 
	'RPAREN', 
	'SEMICOLON', 
	'AMPERSAND',

)

reserved_words = {
	'int' : 'INT',
	'void' : 'VOID',
	'main' : 'MAIN'
}

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

t_ignore = " \t\n"

noOfScalarDecl = 0
noOfPointerDecl = 0
noOfAssignDecl = 0


# precedence = (
# 			('right', 'POINTER'),
# 	)


def p_statement_INIT(p):
	'statement : VOID MAIN LPAREN RPAREN LFBRACK lines RFBRACK'
	p[0] = p[6]

def p_pointerdef_ch(p):

	"""pointerdef : POINTER NAME
					| POINTER pointerdef
	"""
	p[0] = p[1]+p[2]
	# print( p[2]+"---" + p[0])

# def p_pointeraddr_amp(p):
# 	"""
# 	pointeraddr : AMPERSAND NAME 
# 				| AMPERSAND pointerdef
# 	"""

def p_lines_eps(p):
	'lines : '


def p_lines_line(p):
	'''
	lines : line SEMICOLON lines
	'''
	p[0] = p[1]


def p_line_decl(p):
	'''
	line : INT decllist
		 | assignmentlist
	'''
	if p[1] == 'int':
		p[0] = p[2]
	else:
		p[0] = p[1]

def p_declist_ts(p):
	'decllist : pointerdef x'
	global noOfPointerDecl
	noOfPointerDecl += 1 


def p_assignmentlist_id(p):
	'assignmentlist : assignment COMMA assignmentlist'


def p_assignmentlist_single(p):
	'assignmentlist : assignment'

def p_decllist_id(p):
	'''
	decllist : NAME x
	'''
	global noOfScalarDecl
	noOfScalarDecl += 1
	p[0] = p[2]

def p_x_eps(p):
	' x : '

def p_x_ts(p):
	' x : COMMA pointerdef x'
	global noOfPointerDecl
	p[0] = p[3]
	noOfPointerDecl += 1

def p_x_listhandle(p):
	'''
	x : COMMA  NAME x
	  
	'''
	global noOfScalarDecl
	p[0] = p[3]
	noOfScalarDecl += 1

# def p_assignment_eps(p):
# 	'assignment : '


def p_assignment_new(p):
	"""
	assignment : startwithstar ASSIGN NUMBER
				| startwithstar ASSIGN startwithany
				| NAME ASSIGN startwithany
	"""
	global noOfAssignDecl
	noOfAssignDecl +=1

def p_startwithstar_define(p):
	'startwithstar : POINTER startwithany'

def p_startwithany_define(p):
	"""
	startwithany : POINTER startwithany
				| AMPERSAND startwithany
				| NAME
	"""


# def p_assignment_handle(p):
# 	"""
# 	assignment : 	pointerdef ASSIGN NUMBER
# 				|	NAME ASSIGN pointerdef
# 				|  	NAME ASSIGN pointeraddr
# 				| pointerdef ASSIGN pointeraddr
# 				| pointerdef ASSIGN pointerdef
# 	"""
# 	global noOfAssignDecl
# 	noOfAssignDecl += 1





# def p_assignment_twohandle(p):
# 	"""
# 	assignment : startwithany ASSIGN assignment
# 	""" 
# 	global noOfAssignDecl
# 	noOfAssignDecl += 1

def p_error(p):
	if p:
		print("syntax error at {0}".format(p.value))
	else:
		print("syntax error at EOF")
	sys.exit()


def process(data):
	lex.lex()
	yacc.yacc()
	yacc.parse(data)
	print(noOfScalarDecl)
	print(noOfPointerDecl)
	print(noOfAssignDecl)

if __name__ == "__main__":
	with open (sys.argv[1], "r") as myfile:
		data = myfile.read()
	process(data)