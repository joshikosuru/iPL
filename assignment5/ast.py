import sys
from constants import binaryOperators, unaryOperators, binaryOpMap ,OpMap_asm, unaryOpMap

class ASTNode(object):
	def __init__(self):
		self.data = None
		self.dtype = None
		self.pointerdepth = None
		self.children = []

	def __init__(self, data, dtype, pointerdepth, li):
		self.data = data
		self.dtype = dtype
		self.pointerdepth = pointerdepth
		self.children = li[:]

	def isCondition(self):
		if self.data == 'IF' or self.data == 'WHILE' or self.data == 'IFELSE':
			return True
		else:
			return False

	def appendchild(self, child):
		self.children.append(child)

	def giveOutputFile(self, level, file):

		if (self.data == 'CALL'):
			file.write('\t'*level+self.data+' '+self.children[0]+'(\n')
			temp = self.children[1]
			for index in range(len(temp)):
				item = temp[index]
				item.giveOutputFile(level+1,file)
				if index != len(temp)-1:
					file.write('\t'*(level+1)+',\n')
			file.write('\t'*level+')\n')
		elif (self.data == 'VAR' or self.data == 'CONST'):
			file.write('\t'*level+self.data+'('+str(self.children[0])+')\n')
		else:
			check = False
			if self.data == 'IFELSE':
				self.data = 'IF'
				check = True
			file.write('\t'*level+self.data+'\n')
			file.write('\t'*level+'(\n')
			if check:
				self.data = 'IFELSE'
			for index,item in enumerate(self.children):
				if isinstance(item,ASTNode):
					item.giveOutputFile(level+1,file)
				else:
					for listitem in item:
						listitem.giveOutputFile(level+1,file)

				if index != len(self.children)-1:
					file.write('\t'*(level+1)+',\n')
			file.write('\t'*level+')\n')

	def giveBlocks(self):
		if (self.data ==  'IF'):

			block1 = [self.children[0],2,3,'IF'] # GRAMMAR HAS TO BE WRITTEN
			returnblock = []
			returnblock.append(block1)

			block2 = []
			block2num = 2
			for item in self.children[1]:
				blocklist = item.giveBlocks()
				if blocklist[0]:
					block2.append(blocklist[1])
				else:
					if len(block2)==0:
						block2=[]
					else:
						block2.append(block2num+1)
						block2.append('GOTO')
						returnblock.append(block2)
						block2 = []
						block2num += 1

					for some_item in blocklist[1]:
						a= len(some_item)
						if(some_item[a-1] == 'IF'):
							some_item[a-2] += block2num-1
							some_item[a-3] += block2num-1
						elif some_item[a-1] == 'GOTO':
							some_item[a-2] += block2num-1
						else:
							continue
						returnblock.append(some_item)
					block2num = len(returnblock) + 1
					# block2.append(item)
			if len(block2)!= 0:
				block2.append(block2num+1)
				block2.append('GOTO')
				returnblock.append(block2)

			block3 = ['END']
			returnblock.append(block3)
			b = len(block1)
			returnblock[0][b-2] = len(returnblock)
			return [False,returnblock]

		elif (self.data == 'WHILE'):
			block1 = [self.children[0],2,3,'IF'] # GRAMMAR HAS TO BE WRITTEN
			returnblock = []
			returnblock.append(block1)

			block2 = []
			block2num = 2
			for item in self.children[1]:
				blocklist = item.giveBlocks()
				if blocklist[0]:
					block2.append(blocklist[1])
				else:
					if len(block2)==0:
						block2=[]
					else:
						block2.append(block2num+1)
						block2.append('GOTO')
						returnblock.append(block2)
						block2 = []
						block2num += 1

					for some_item in blocklist[1]:
						a= len(some_item)
						if(some_item[a-1] == 'IF'):
							some_item[a-2] += block2num-1
							some_item[a-3] += block2num-1
						elif some_item[a-1] == 'GOTO':
							some_item[a-2] += block2num-1
						else:
							continue
						returnblock.append(some_item)
					block2num = len(returnblock) + 1
					# block2.append(item)
			if len(block2)!= 0:
				block2.append(1)
				block2.append('GOTO')
				returnblock.append(block2)

			block3 = ['END']
			returnblock.append(block3)
			b = len(block1)
			end_block_id = len(returnblock)
			returnblock[0][b-2] = end_block_id

			for i in range(1,len(returnblock)-1):
				c = returnblock[i]
				if c[len(c)-1] == 'IF':

					if c[len(c)-2] == end_block_id:
						returnblock[i][len(c)-2] = 1
					if c[len(c)-3] == end_block_id:
						returnblock[i][len(c)-1] = 1

				else:
					if c[len(c)-2] == end_block_id:
						returnblock[i][len(c)-2] = 1

			return [False,returnblock]



		elif (self.data == 'IFELSE'):
			block1 = [self.children[0],2,3,'IF'] # GRAMMAR HAS TO BE WRITTEN
			returnblock = []
			returnblock.append(block1)

			block2 = []
			block2num = 2
			for item in self.children[1]:
				blocklist = item.giveBlocks()
				if blocklist[0]:
					block2.append(blocklist[1])
				else:
					if len(block2)==0:
						block2=[]
					else:
						block2.append(block2num+1)
						block2.append('GOTO')
						returnblock.append(block2)
						block2 = []
						block2num += 1

					for some_item in blocklist[1]:
						a= len(some_item)
						if(some_item[a-1] == 'IF'):
							some_item[a-2] += block2num-1
							some_item[a-3] += block2num-1
						elif some_item[a-1] == 'GOTO':
							some_item[a-2] += block2num-1
						else:
							continue
						returnblock.append(some_item)
					block2num = len(returnblock) + 1
					# block2.append(item)
			if len(block2)!= 0:
				block2.append(block2num+1)
				block2.append('GOTO')
				returnblock.append(block2)

			b = len(block1)
			returnblock[0][b-2] = len(returnblock) + 1

			id_we_put = len(returnblock) + 1

			if_end_id = len(returnblock)

			block2num = id_we_put
			block2 = []

			for item in self.children[2]:
				blocklist = item.giveBlocks()
				if blocklist[0]:
					block2.append(blocklist[1])
				else:
					if(len(block2)==0):
						block2=[]
					else:
						block2.append(block2num+1)
						block2.append('GOTO')
						returnblock.append(block2)
						block2 = []
						block2num += 1

					for some_item in blocklist[1]:
						a= len(some_item)
						if(some_item[a-1]== 'IF'):
							some_item[a-2] += block2num - 1
							some_item[a-3] += block2num - 1
						elif some_item[a-1] == 'GOTO':
							some_item[a-2] += block2num - 1
						else:
							continue
						returnblock.append(some_item)
					block2num = len(returnblock) + 1
			if len(block2)!= 0:
				block2.append(block2num+1)
				block2.append('GOTO')
				returnblock.append(block2)

			block3 = ['END']
			returnblock.append(block3)

			for i in range(1,if_end_id):
				c= returnblock[i]
				if c[len(c)-1] == 'IF':

					if c[len(c) - 2] == id_we_put:
						returnblock[i][len(c)-2] = len(returnblock)
					if c[len(c)-3] == id_we_put:
						returnblock[i][len(c)-3] = len(returnblock)

				else:
					if c[len(c)-2] == id_we_put:
						returnblock[i][len(c)-2] = len(returnblock)

			return [False,returnblock]
		else:
			return [True,self] # null list is of temp variables / statements

	def expand(self, counter, lis):
		if(self.data == "ASGN"):
			right, counter, lis = (self.children[1]).expand(counter, lis)
			left, counter, lis = (self.children[0]).expand(counter, lis)
			lis += (left+" = "+right+"\n")
			return "", counter, lis
		elif(self.data in binaryOperators):
			left, counter, lis = (self.children[0]).expand(counter, lis)
			right, counter, lis = (self.children[1]).expand(counter, lis)
			var = "t"+str(counter)
			lis += (var+" = "+left+" "+binaryOpMap[self.data]+" "+right+"\n")
			counter += 1
			return var, counter, lis
		elif(self.data == "NOT" or self.data == "UMINUS"):
			left, counter, lis = (self.children[0]).expand(counter, lis)
			var = "t"+str(counter)
			lis += (var+" = "+unaryOpMap[self.data]+left+"\n")
			counter += 1
			return var, counter, lis
		elif(self.data == "ADDR" or self.data == "DEREF"):
			left, counter, lis = (self.children[0]).expand(counter, lis)
			var = unaryOpMap[self.data]+left
			return var, counter, lis
		elif(self.data == "CONST" or self.data == "VAR"):
			return str(self.children[0]), counter, lis
		elif(self.data == 'CALL'):
			paramTemp = []
			for i in self.children[1]:
				templis = ""
				tempVar, counter, templis = i.expand(counter, templis)
				lis += templis
				paramTemp.append(tempVar)
			tempVarList = ""
			for index, t in enumerate(paramTemp):
				tempVarList += t
				if(index != len(paramTemp) - 1):
					tempVarList += ","
			# lis += (self.children[0] + "("+tempVarList+")\n")
			templis = (self.children[0] + "("+tempVarList+")")
			return templis, counter, lis
		elif(self.data == 'RETURN'):
			var, counter, lis = self.children[0].expand(counter, lis)
			lis += ("return "+var+"\n")
			return "", counter, lis


	def expand_assembly(self, free_reglist,lis,varAccessDict,for_addr):
		if(self.data == "ASGN"):
			right, free_reglist, lis = (self.children[1]).expand_assembly(free_reglist,lis,varAccessDict,False)
			left, free_reglist, lis = (self.children[0]).expand_assembly(free_reglist,lis,varAccessDict,True)
			if self.children[0].data=="VAR":
				lis += ("\tsw "+num_to_reg(right)+", "+str(left)+"($sp)\n")
			else:
				lis += ("\tsw "+num_to_reg(right)+", 0("+num_to_reg(left)+")\n")
				free_reglist.append(left)
			free_reglist.append(right)			
			return -1, free_reglist, lis
		elif(self.data in binaryOperators):
			leftreg, free_reglist, lis = (self.children[0]).expand_assembly(free_reglist,lis,varAccessDict,for_addr)
			rightreg, free_reglist, lis = (self.children[1]).expand_assembly(free_reglist,lis,varAccessDict,for_addr)
			newreg,newnum=giveminRegister(free_reglist)
			free_reglist.remove(newnum)
			if ((self.data == "GE") or (self.data=="GT")):
				lis += ("\t"+OpMap_asm[self.data]+" "+newreg+", "+num_to_reg(rightreg)+", "+num_to_reg(leftreg)+"\n")
			else:
				lis += ("\t"+OpMap_asm[self.data]+" "+newreg+", "+num_to_reg(leftreg)+", "+num_to_reg(rightreg)+"\n")
			free_reglist.append(leftreg)
			free_reglist.append(rightreg)

			movereg,movenum = giveminRegister(free_reglist)
			lis += ("\tmove "+movereg+", "+newreg+"\n")
			free_reglist.remove(movenum)
			free_reglist.append(newnum)
			return movenum, free_reglist, lis
		elif(self.data == "NOT" or self.data == "UMINUS"):
			regnum,free_reglist,lis = (self.children[0].expand_assembly(free_reglist,lis,varAccessDict,for_addr))
			newreg,newnum = giveminRegister(free_reglist)
			free_reglist.remove(newnum)
			lis += ("\t"+OpMap_asm[self.data]+" "+newreg+", "+num_to_reg(regnum)+"\n")
			free_reglist.append(regnum)
			movereg,movenum = giveminRegister(free_reglist)
			lis += ("\tmove "+movereg+", "+newreg+"\n")
			free_reglist.remove(movenum)
			free_reglist.append(newnum)
			return movenum,free_reglist,lis			
		elif(self.data == "ADDR"):
			if self.children[0].data=="DEREF":
				return self.children[0].children[0].expand_assembly(free_reglist,lis,varAccessDict,for_addr)
			varcount,free_reglist,lis = (self.children[0].expand_assembly(free_reglist,lis,varAccessDict,True))
			register,regnum = giveminRegister(free_reglist)
			free_reglist.remove(regnum)
			if varcount == (-1):
				lis += ("\tla "+register+", global_"+self.children[0].children[0]+"\n")
				# here by calling children twice im assuming the second child is name only.
			else:
				lis += ("\taddi "+register+", $sp, "+str(varcount) +"\n")
			return regnum, free_reglist, lis
		elif(self.data == "DEREF"):
			regnum,free_reglist,lis = (self.children[0].expand_assembly(free_reglist,lis,varAccessDict,for_addr))
			newreg,newnum = giveminRegister(free_reglist)
			free_reglist.remove(newnum)
			if self.children[0].data == "VAR" and for_addr:
				if regnum == (-1):
					# means it is global var
					lis +=("\tlw "+newreg+", global_"+self.children[0].children[0]+"\n")
				else:
					lis +=("\tlw "+newreg+", "+str(regnum)+"($sp)\n")
			else:
				lis +=("\tlw "+newreg+", 0("+num_to_reg(regnum)+")\n")
				free_reglist.append(regnum)
			return newnum,free_reglist,lis
		elif(self.data == "CONST"):
			register,regnum = giveminRegister(free_reglist)
			free_reglist.remove(regnum)
			lis += ("\tli "+register+", "+str(self.children[0])+"\n")
			return regnum, free_reglist, lis
		elif(self.data == "VAR"):
			regnum = 0
			if for_addr:
				if self.children[0] in varAccessDict:
					return varAccessDict[self.children[0]], free_reglist, lis
				else:
					return -1,free_reglist,lis
			register,regnum = giveminRegister(free_reglist)
			free_reglist.remove(regnum)
			if self.children[0] in varAccessDict:
				lis += ("\tlw "+register+", "+str(varAccessDict[self.children[0]])+"($sp)\n")
			else:
				lis += ("\tlw "+register+", global_"+self.children[0]+"\n")
			return regnum,free_reglist,lis		

		elif(self.data == 'CALL'):
			paramTemp = []
			for i in self.children[1]:
				templis = ""
				tempVar, counter, templis = i.expand(counter, templis)
				lis += templis
				paramTemp.append(tempVar)
			tempVarList = ""
			for index, t in enumerate(paramTemp):
				tempVarList += t
				if(index != len(paramTemp) - 1):
					tempVarList += ","
			# lis += (self.children[0] + "("+tempVarList+")\n")
			templis = (self.children[0] + "("+tempVarList+")")
			return templis, counter, lis
		elif(self.data == 'RETURN'):
			regnum, free_reglist, lis = self.children[0].expand_assembly(free_reglist,lis,varAccessDict,for_addr)
			lis += ("\tmove $v1, "+num_to_reg(regnum)+" # move return value to $v1\n")
			return regnum, free_reglist, lis

def num_to_reg(a):
	if a<8:
		return "$s"+str(a)
	elif a<18:
		return "$t"+str(a-8)
	else:
		print("Insuffient number of registers")
		sys.exit()

def giveminRegister(num_list):
	num_list.sort()
	a = num_list[0]
	if a<8:
		return "$s"+str(a),a
	elif a<18:
		return "$t"+str(a-8),a
	else:
		print("Insuffient number of registers")
		sys.exit()
