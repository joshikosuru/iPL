class Tree(object):
	def __init__(self):
		self.left = None
		self.right = None
		self.data = None

	def __init__(self, left, right, data):
		self.left = left
		self.right = right
		self.data = data		

	def giveOutputFile(self, level, file):
		if(self.data == 'VAR' or self.data == 'CONST'):
			file.write('\t'*level+self.data+'('+str(self.left)+')\n')
		else:	
			file.write('\t'*level+self.data+'\n')
			file.write('\t'*level+'(\n')
			(self.left).giveOutputFile(level+1, file)
			if(self.right is not None):
				file.write('\t'*(level+1)+',\n')
				(self.right).giveOutputFile(level+1, file)
			file.write('\t'*level+')\n')
		if(level == 0):
			file.write('\n')