import sys

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
		if(nodeL.pointerdepth == 0):
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