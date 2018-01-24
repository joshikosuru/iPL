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
	'AMPERSAND'
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

def p_statement_INIT(p):
	'statement : VOID MAIN LPAREN RPAREN LFBRACK lines RFBRACK'
	p[0] = p[6]

def p_lines_line(p):
	'''
	lines : line SEMICOLON lines
		  | line SEMICOLON
	'''
	p[0] = p[1]


def p_line_decl(p):
	'''
	line : INT decllist
		 | assignment
	'''
	if p[1] == 'int':
		p[0] = p[2]
	else:
		p[0] = p[1]

def p_decllist_id(p):
	'''
	decllist : POINTER NAME x
			 | NAME x
	'''
	if p[1] == '*':
		noOfPointerDecl += 1
		p[0] = p[3]
	else:
		noOfScalarDecl += 1
		p[0] = p[2]

def p_x_listhandle(p):
	'''
	x : COMMA POINTER NAME x
	  | COMMA NAME x
	  |
	'''

	if p[1] == '':
		pass
	elif p[2] == '*':
		p[0] = p[4]
		noOfPointerDecl += 1
	else:
		p[0] = p[3]
		noOfScalarDecl += 1

def p_error(p):
	if p:
		print("syntax error at {0}".format(p.value))
	else:
		print("syntax error at EOF")


def process(data):
	lex.lex()
	yacc.yacc()
	yacc.parse(data)

if __name__ == "__main__":
	with open (sys.argv[1], "r") as myfile:
		data = myfile.read()
	process(data)