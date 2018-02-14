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
	'PLUS',
	'MINUS',
	# 'UMINUS',
	'DIVIDE',

)

reserved_words = {
	'int' : 'INT',
	'void' : 'VOID',
	'main' : 'MAIN'
}

class Tree(object):
	def __init__(self):
		self.left = None
		self.right = None
		self.data = None


def giveOutputFile(tree, level):
	if isinstance(tree, Tree):	
		if(tree.data == 'VAR' or tree.data == 'CONST'):
			file.write('\t'*level+tree.data+'('+str(tree.left)+')\n')
		else:	
			file.write('\t'*level+tree.data+'\n')
			file.write('\t'*level+'(\n')
			giveOutputFile(tree.left, level+1)
			if(tree.right is not None):
				file.write('\t'*(level+1)+',\n')
				giveOutputFile(tree.right, level+1)
			file.write('\t'*level+')\n')
	else:
		file.write('\t'*level+str(tree)+'\n')
	if(level == 0):
		file.write('\n')


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
t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/'

t_ignore = " \t\n"

# Parsing rules
precedence = (
	('left', 'PLUS', 'MINUS'),
	('left', 'POINTER', 'DIVIDE'),
	('right', 'UMINUS'),
)

noOfScalarDecl = 0
noOfPointerDecl = 0
noOfAssignDecl = 0


def p_statement_INIT(p):
	'statement : VOID MAIN LPAREN RPAREN LFBRACK lines RFBRACK'
	p[0] = p[6]

def p_pointerdef_ch(p):

	"""pointerdef : POINTER NAME
					| POINTER pointerdef
	"""
	p[0] = p[1]+p[2]


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


# def p_assignmentlist_id(p):
# 	'assignmentlist : assignment COMMA assignmentlist'


def p_assignmentlist_single(p):
	'assignmentlist : assignment'
	parseTree = p[1]

	giveOutputFile(parseTree, 0)
	

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



def p_assignment_new_name(p):
	"""
	assignment : NAME ASSIGN arithmeticexpr
	"""
	global noOfAssignDecl
	noOfAssignDecl +=1
	root = Tree()
	root.data = 'ASGN'
	x = Tree() 
	x.data = 'VAR'
	x.left = p[1] 
	root.left = x
	root.right = p[3][0]
	if(not p[3][1]):
		print("syntax error at =")
		sys.exit()
	p[0] = root



def p_assignment_new_startwithstar(p):
	"""
	assignment : startwithstar ASSIGN arithmeticexpr
	"""
	global noOfAssignDecl
	noOfAssignDecl +=1
	root = Tree()
	root.data = 'ASGN'
	root.left = p[1]
	root.right = p[3][0]
	p[0] = root

def p_arithmeticexpr_binop(p):
	"""
	arithmeticexpr : arithmeticexpr PLUS arithmeticexpr
				   | arithmeticexpr MINUS arithmeticexpr
				   | arithmeticexpr POINTER arithmeticexpr
				   | arithmeticexpr DIVIDE arithmeticexpr
	"""
	# print [repr(p[i]) for i in range(0,4)]
	x = Tree()
	x.left = p[1][0]
	x.right = p[3][0]
	if p[2] == '+':
		x.data = 'PLUS'
	elif p[2] == '-':
		x.data = 'MINUS'
	elif p[2] == '*':
		x.data = 'MUL'
	elif p[2] == '/':
		x.data = 'DIV'
	p[0] = [x, p[1][1] or p[3][1]]

def p_arithmeticexpr_uminus(p):
	"""
	arithmeticexpr : MINUS arithmeticexpr %prec UMINUS
	"""
	x = Tree()
	x.data = 'UMINUS'
	x.left = p[2][0]
	p[0] = [x, p[2][1]]

def p_arithmeticexpr_paren(p):
	'arithmeticexpr : LPAREN arithmeticexpr RPAREN'
	p[0] = p[2]

def p_arithmeticexpr_terminal_NUMBER(p):
	"""
	arithmeticexpr : NUMBER
	"""
	x = Tree()
	x.data = 'CONST'
	x.left = p[1]
	p[0] = [x, False]

def p_arithmeticexpr_terminal_startwithany(p):
	"""
	arithmeticexpr : startwithany
	"""
	p[0] = [ p[1], True]

def p_startwithstar_define(p):
	'startwithstar : POINTER startwithany'
	x = Tree()
	x.data = 'DEREF'
	x.left = p[2]
	p[0] = x

def p_startwithany_define(p):
	"""
	startwithany : POINTER startwithany
				| AMPERSAND startwithany
				| NAME
	"""
	x = Tree()
	if p[1] == '*':
		x.data = 'DEREF'
		x.left = p[2]		
	elif p[1] == '&':
		x.data = 'ADDR'
		x.left = p[2]
	else:
		x.data = 'VAR'
		x.left = p[1]
	p[0] = x


def p_error(p):
	if p:
		print("syntax error at {0}".format(p.value))
	else:
		print("syntax error at EOF")
	sys.exit()


def process(data):
	global file
	lex.lex()
	yacc.yacc()
	yacc.parse(data)
	file.close()
	# print(noOfScalarDecl)
	# print(noOfPointerDecl)
	# print(noOfAssignDecl)

if __name__ == "__main__":
	with open (sys.argv[1], "r") as myfile:
		data = myfile.read()
		file = open("Parser_ast_"+sys.argv[1]+".txt", "w")
	process(data)