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
		if(function.name == 'main'):
			ASTFile.write('Function Main' + '\n')
		else:
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

def giveCFGFile(fnode,fileName):
	CFGfileName = fileName+".cfg"
	CFGFile = open(CFGfileName, "w")

	blockCount = -1
	temp = 0
	for fitem in fnode:
		z = helperForCFG(fitem.name,fitem.paramList)
		CFGFile.write(z)
		x = ASTNode('IF',None,None,[True,fitem.ASTList])
		blocks1 = x.giveBlocks()
		blocks = blocks1[1]
		for i in range(1,len(blocks)):
			CFGFile.write("\n<bb "+str(i+blockCount)+">\n")
			a = blocks[i]
			if a[-1] == 'IF':
				var,temp,lis = a[0].expand(temp,"")
				CFGFile.write(lis)
				CFGFile.write("if("+var+") goto <bb "+str(blockCount+a[1]-1)+">\n")
				CFGFile.write("else goto <bb "+str(blockCount+a[2]-1)+">\n")
			elif a[-1] == 'GOTO':
				for j in range(0,len(a)-2):
					var,temp,lis = a[j].expand(temp,"")
					CFGFile.write(lis)
				CFGFile.write("goto <bb "+str(blockCount+a[len(a)-2]-1)+">\n")
			else:
				if(fitem.returnSTMT is not None):
					if(len(fitem.returnSTMT) > 0):
						var,temp,lis = fitem.returnSTMT[0].expand(temp,"")
						CFGFile.write(lis)
					else:
						CFGFile.write("return\n\n")
				else:
					CFGFile.write("return\n\n")
		blockCount += len(blocks)-1

def helperForCFG(funcName, paramList):
	ret = ""
	ret = "function "+funcName+"("+giveParamsForOutput(paramList)+")"
	return ret

def writeGlobalVaribles(varSymDict):
	li = []
	stri = ""
	for i in varSymDict.keys():
		if(i[1] == '_'):
			li.append(i[0])
	li.sort()
	for i in li:
		val = varSymDict[(i, '_')]
		if(val[0] == 'float' and val[1] == 0):
			stri += ("global_"+i+":\t.space\t8\n")
		else:
			stri += ("global_"+i+":\t.word\t0\n")

	return stri

def writeFS(f, varSymDict,blockCount):
	li = []
	for i in varSymDict.keys():
		if i[1] == f.name and varSymDict[i][2] == 0:
			li.append(i[0])
	li.sort()
	spaceForF = 0
	varAccessDict = {}
	for i in li:
		if(varSymDict[(i, f.name)][0] == 'int' or varSymDict[(i, f.name)][1] > 0):
			spaceForF += 4
		else:
			spaceForF += 8
		varAccessDict[i] = spaceForF
	free_reglist = list(range(18))
	stri = ""
	stri += ('\t.text\t# The .text assembler directive indicates\n')
	stri += ('\t.globl '+str(f.name)+'\t# The following is the code\n')
	stri += (str(f.name)+":\n")
	stri += ("# Prologue begins\n\tsw $ra, 0($sp)\t# Save the return address\n\tsw $fp, -4($sp)\t# Save the frame pointer\n\tsub $fp, $sp, 8\t# Update the frame pointer\n\tsub $sp, $sp, "+str(8+spaceForF)+"\t# Make space for the locals\n# Prologue ends\n")

	spaceForFcpy = spaceForF + 8
	fparams = f.paramList
	for i in fparams:
		if (i[0] == 'int' or i[1]>0):
			spaceForFcpy += 4
		else:
			spaceForFcpy += 8
		varAccessDict[i[2]] = spaceForFcpy
	newblockCount = blockCount
	x = ASTNode('IF',None,None,[True,f.ASTList])
	blocks1 = x.giveBlocks()
	blocks = blocks1[1]
	for i in range(1,len(blocks)):
		free_reglist = list(range(18))
# 		this initialisation of free_reglist idk if its true
		stri += ("label"+str(i+blockCount)+":\n")
		a = blocks[i]
		if a[-1] == 'IF':
			var,free_reglist,lis = a[0].expand_assembly(free_reglist,"",varAccessDict,False)
			stri += lis
			stri += ("\tbne $s0, $0, label"+str(blockCount+a[1]-1)+"\n\tj label"+str(blockCount+a[2]-1)+"\n")
		elif a[-1] == 'GOTO':
			for j in range(0,len(a)-2):
				var,free_reglist,lis = a[j].expand_assembly(free_reglist,"",varAccessDict,False)
				stri += lis

			stri += ("\tj label"+str(blockCount+a[len(a)-2]-1)+"\n")
		else:
			if(f.returnSTMT is not None):
				if(len(f.returnSTMT) > 0):
					var,free_reglist,lis = f.returnSTMT[0].expand_assembly(free_reglist,"",varAccessDict,False)
					stri += lis

			stri += ("\tj epilogue_"+(str(f.name))+"\n")
	newblockCount += len(blocks)-1

	stri += ("\n# Epilogue begins\nepilogue_"+str(f.name)+":\n"+"\tadd $sp, $sp, "+str(8+spaceForF)+"\n\tlw $fp, -4($sp)\n\tlw $ra, 0($sp)\n\tjr $ra\t# Jump back to the called procedure\n# Epilogue ends\n")
	return stri ,  newblockCount

def generateAssemblyCode(fnode, fileName, varSymDict):
	SFileName = fileName+".s"
	SFile = open(SFileName, "w")

	SFile.write('\n\t.data\n')
	SFile.write(writeGlobalVaribles(varSymDict))
	SFile.write('\n')
	blockCount = -1
	for f in fnode:
		stri,blockCount = writeFS(f, varSymDict,blockCount)
		SFile.write(stri)
	SFile.close()


	# SFile.write('\t.text\t# The .text assembler directive indicates')
	# SFile.write('\t.globl main	# The following is the code')
def giveParamNamesInOrder(paramList):
	q = []
	for i in paramList:
		q.append(i[2])
	return q