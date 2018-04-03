import sys
from operator import itemgetter

from ast import ASTNode

def printdict(dict, isVar):
	if isVar == 1:
		for i in dict:
			if(i[1] != '_'):
				print(i, ":", dict[i])
			else:
				print((i[0], "global"), ":", dict[i])
	else:
		for i in dict:
			print(i, ":", dict[i])

def comparePrimitiveWithDef(funcName, funcRet, funcDerive, paramList, dictOutput):
	(funcRet1, funcDerive1, paramList1) = dictOutput
	if(funcDerive != funcDerive1):
		print("Derivation of return type not matching on primitive and declaration for function "+str(funcName))
		sys.exit()
	else:
		if(funcRet != funcRet1):
			print("Return type not matching on primitive and declaration for function "+str(funcName))
			sys.exit()
		else:
			if(not compareFuncParamLists(paramList, paramList1)):
				print("Parameters for function declaration not same as primitive for function "+str(funcName))
				sys.exit()

def compareFuncParamLists(paramList, paramList1):
	if(len(paramList) != len(paramList1)):
		return False
	else:
		for i in range(len(paramList)):
			if((paramList[i][0] != paramList1[i][0]) or (paramList[i][1] != paramList1[i][1])):
				return False
		return True

def arithmeticTypeCheck(nodeL, nodeR):
	if(nodeL.dtype != nodeR.dtype):
		print("type mismatch in arithmetic operation")
		return False
	else:
		if(nodeL.pointerdepth != nodeR.pointerdepth):
			print("pointer mismatch in arithmetic operation")
			return False
		if(nodeL.pointerdepth != 0):
			print("pointer arithmetic not allowed")
			return False
		if(nodeL.data == 'VAR' or nodeR.data == 'VAR'):
			print("Direct base type access in arithmetic operation")
			return False
	return True

def assignmentTypeCheck(nodeL, nodeR, typeCheck):
	if(nodeL.dtype != nodeR.dtype):
		print("type mismatch in "+typeCheck+" operation")
		return False
	else:
		if(nodeL.pointerdepth != nodeR.pointerdepth):
			print("pointer mismatch in "+typeCheck+" operation")
			return False
		if(nodeL.pointerdepth == 0):
			if(nodeL.data == 'VAR' or nodeR.data == 'VAR'):
				print("Direct base type access in "+typeCheck+" operation")
				return False
	return True

def giveVarSymOutput(name, currentScope, varSymDict):
	if (name, currentScope) in varSymDict:
		return varSymDict[(name, currentScope)]
	else:
		if(name, "_") in varSymDict:
			return varSymDict[(name, "_")]
		else:
			print("Variable "+str(name)+" does not exist in functionscope "+str(currentScope))
			sys.exit()

def checkTypeParams(functionCallParamList, funcSymDictParamList, functionName):
	if(len(functionCallParamList) != len(funcSymDictParamList)):
		print("Number of parameters mismatch while calling "+str(functionName))
		sys.exit()
	else:
		for i in range(len(funcSymDictParamList)):
			if((functionCallParamList[i].dtype != funcSymDictParamList[i][0]) or (functionCallParamList[i].pointerdepth != funcSymDictParamList[i][1])):
				print("Parameter number : "+str(i+1)+" - type or pointer mismatch while calling function "+str(functionName))
				sys.exit()

def printFunctionNodesAST(li, fileName):
	ASTfileName = fileName+".ast"
	ASTFile = open(ASTfileName, "w")
	for function in li:
		ASTFile.write('FUNCTION '+ function.name + '\n')
		ASTFile.write('PARAMS ('+giveParamsForOutput(function.paramList)+')' + '\n')
		ASTFile.write('RETURNS '+ givePointerAsStars(function.retDerive)+ function.retType + '\n')
		giveASTfromList(function.ASTList, ASTFile, 1)
		returnSTMT = function.returnSTMT
		if(returnSTMT is not None):
			if returnSTMT == []:
				ASTFile.write('RETURN'+ '\n')
				ASTFile.write('('+ '\n')
				ASTFile.write(')' + '\n\n')
			else:
				giveASTfromList(returnSTMT, ASTFile, 0)
				ASTFile.write('\n')
		else:
			ASTFile.write('\n')
	ASTFile.close()

def givePointerAsStars(num):
	ret = ""
	while(num > 0):
		ret += "*"
		num -= 1
	return ret

def giveParamsForOutput(paramList):
	ret = ""
	for index, i in enumerate(paramList):
		ret += (i[0] + " " + givePointerAsStars(i[1])+i[2])
		if(index != len(paramList)-1):
			ret += ", "
	return ret

def giveASTfromList(ASTList, ASTFile, level):
	for i in ASTList:
		i.giveOutputFile(level, ASTFile)

def giveTableSYM(varSymDict, funcSymDict, fileName):
	SYMfileName = fileName+".sym"
	SYMFile = open(SYMfileName, "w")
	SYMFile.write("Procedure table :-\n")
	SYMFile.write("-----------------------------------------------------------------\n")
	SYMFile.write("Name\t\t|\tReturn Type  |  Parameter List\n")
	funcSymDictKeys = funcSymDict.keys()
	funcSymDictKeys = sorted(funcSymDictKeys)
	for i in funcSymDictKeys:
		SYMFile.write(giveProcTableFuncString(i, funcSymDict[i])+"\n")
	SYMFile.write("-----------------------------------------------------------------\n")
	SYMFile.write("Variable table :- \n")
	SYMFile.write("-----------------------------------------------------------------\n")
	SYMFile.write("Name\t|\tScope\t\t|\tBase Type  |  Derived Type\n")
	SYMFile.write("-----------------------------------------------------------------\n")
	varSymDictKeys = varSymDict.keys()
	varSymDictKeys = sorted(varSymDictKeys, key = lambda x:(x[1], x[0]))
	for i in varSymDictKeys:
		ret = i[0]+"\t\t|\t"
		if(i[1] == "main"):
			ret += "main\t\t|\t"
		elif(i[1] == "_"):
			ret += "procedure global\t|\t"
		else:
			ret += "procedure "+i[1]+"\t|\t"
		ret += varSymDict[i][0]+"\t   |\t"
		ret += givePointerAsStars(varSymDict[i][1])+"\n"
		SYMFile.write(ret)
	SYMFile.write("-----------------------------------------------------------------\n")
	SYMFile.write("-----------------------------------------------------------------\n")
	SYMFile.close()

def giveProcTableFuncString(i, funcSymDictI):
	ret = ""
	ret += (i + "\t\t|\t" + funcSymDictI[0] + givePointerAsStars(funcSymDictI[1]) + "\t\t|\t" + giveParamsForOutput(funcSymDictI[2]))
	return ret
