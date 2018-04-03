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
			# lis += (self.children[0] + "("+tempVarList+")\n")
			templis = (self.children[0] + "("+tempVarList+")\n")
			return templis, counter, lis
		elif(self.data == 'RETURN'):
			var, counter, lis = self.children[0].expand(counter, lis)
			lis += ("return "+var+"\n")
			return "", counter, lis
