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
			for index in range(1,len(self.children)):
				item = self.children[index]
				item.giveOutputFile(level+1,file):
				if index != len(self.children)-1:
					file.write('\t'*(level+1)+',\n')
			file.write('\t'*level+')\n')
		elif (self.data == 'VAR' or self.data == 'CONST'):
			file.write('\t'*level+self.data+'('+str(self.left)+')\n')
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