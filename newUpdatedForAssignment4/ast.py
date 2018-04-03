from constants import binaryOperators, unaryOperators, binaryOpMap, unaryOpMap

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
			if self.data == 'IFELSE':
				self.data = 'IF'
			file.write('\t'*level+self.data+'\n')
			self.data = 'IFELSE'
			file.write('\t'*level+'(\n')
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
		if self.isCondition:
			# conditional block
			ret = []
			firstblock = [self.children[0],2,3,'IF']
			ret.append(firstblock)
			blockcur = []
			blockcurid = 2
			for item in self.children[1]:
				blockitemlist = item.giveBlocks()
				if isinstance(blockitemlist,ASTNode):
					blockcur.append(blockitemlist)
				else:
					if len(blockcur) == 0:
						blockcur = []
					else:
						blockcurid += 1
						blockcur.append(blockcurid)
						blockcur.append('GOTO')
						ret.append(blockcur)
						blockcur = []

					for bitem in blockitemlist:
						if bitem[-1] == 'IF':
							bitem[-2] += blockcurid - 1
							bitem[-3] +=  blockcurid - 1
						if bitem[-1] == 'GOTO':
							bitem[-2] += blockcurid - 1
						else:
							continue
						ret.append(bitem)
					blockcurid = len(ret) + 1

			if(len(blockcur)!=0):
				blockcur.append(blockcurid+1)
				blockcur.append('GOTO')
				ret.append(blockcur)

			ret[0][-2] = len(ret) + 1
			end_block_id = len(ret) + 1 

			if self.data == 'WHILE':
				for i in range(1,len(ret)):
					c = ret[i]
					if c[-1] == 'IF':
						if c[-2] == end_block_id:
							ret[i][-2] = 1
						if c[-3] == end_block_id:
							ret[i][-3] = 1
					elif c[-2] == end_block_id:
						ret[i][-2] = 1
			elif self.data == 'IFELSE':
				blockcurid = end_block_id
				blockcur = []
				for item in self.children[2]:
					blockitemlist = item.giveBlocks()
					if isinstance(blockitemlist,ASTNode):
						blockcur.append(blockitemlist)
					else:
						if len(blockcur) == 0:
							blockcur = []
						else:
							blockcurid += 1
							blockcur.append(blockcurid)
							blockcur.append('GOTO')
							ret.append(blockcur)
							blockcur = []

						for bitem in blockitemlist:
							if bitem[-1] == 'IF':
								bitem[-2] += blockcurid - 1
								bitem[-3] +=  blockcurid - 1
							if bitem[-1] == 'GOTO':
								bitem[-2] += blockcurid - 1
							else:
								continue
							ret.append(bitem)
						blockcurid = len(ret) + 1

				if(len(blockcur)!=0):
					blockcur.append(blockcurid+1)
					blockcur.append('GOTO')
					ret.append(blockcur)

				for i in range(1,end_block_id - 1):
					c = ret[i]
					if c[-1] == 'IF':

						if c[-2] == end_block_id:
							ret[i][-2] = len(ret) + 1
						if c[-3] == end_block_id:
							ret[i][-3] = len(ret) + 1
					elif c[-2] == end_block_id:
						ret[i][-2] = len(ret) + 1


			returnstmt = ['return']
			ret.append(returnstmt)
			return ret
 		else:
			return self

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
			return str(self.left), counter, lis
		elif(self.data == 'CALL'):
			paramTemp = []
			for i in self.children[1]:
				templis = ""
				tempVar, counter, templis = i.expand(counter, templis)
				lis += templis
				paramTemp.append(tempVar)
			tempVarList = ""
			for index, t in paramTemp:
				tempVarList += t
				if(index != len(paramTemp) - 1):
					tempVarList += ","
			lis += (i.name + "("+tempVarList+")\n")
			return "", counter, lis
		elif(self.data == 'RETURN'):
			var, counter, lis = self.children[0].expand(counter, lis)
			lis += ("return "+var+"\n")
			return "", counter, lis
