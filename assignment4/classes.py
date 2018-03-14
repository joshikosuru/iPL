from constants import *

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

		if(self.data == 'IF' or self.data == 'WHILE'):
			file.write('\t'*level+self.data+'\n')
			file.write('\t'*level+'(\n')
			(self.left).giveOutputFile(level+1,file)
			file.write('\t'*(level+1)+',\n')
			for item in (self.right):
				item.giveOutputFile(level+1,file)
			file.write('\n')
			file.write('\t'*level+')\n')
		elif(self.data == 'IFELSE'):
			file.write('\t'*level+'IF'+'\n')
			file.write('\t'*level+'(\n')
			(self.left).giveOutputFile(level+1,file)
			
			for item in self.right:
				file.write('\t'*(level+1)+',\n')
				for asgn in item:
					asgn.giveOutputFile(level+1,file)
			# self.right has two items list of if body asgns, else body asgns
			file.write('\n')
			file.write('\t'*level+')\n')
		elif(self.data == 'VAR' or self.data == 'CONST'):
			file.write('\t'*level+self.data+'('+str(self.left)+')\n')
		else:	
			file.write('\t'*level+self.data+'\n')
			file.write('\t'*level+'(\n')
			(self.left).giveOutputFile(level+1, file)
			if(self.right is not None):
				file.write('\t'*(level+1)+',\n')
				(self.right).giveOutputFile(level+1, file)
			file.write('\t'*level+')\n')
		# if(level == 0):
		# 	file.write('\n')

	def giveBlocks(self):

		if (self.data ==  'IF'):

			block1 = [self.left,2,3,'IF'] # GRAMMAR HAS TO BE WRITTEN
			returnblock = []
			returnblock.append(block1)

			block2 = []
			block2num = 2
			for item in self.right:
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
			block1 = [self.left,2,3,'IF'] # GRAMMAR HAS TO BE WRITTEN
			returnblock = []
			returnblock.append(block1)

			block2 = []
			block2num = 2
			for item in self.right:
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
			block1 = [self.left,2,3,'IF'] # GRAMMAR HAS TO BE WRITTEN
			returnblock = []
			returnblock.append(block1)

			block2 = []
			block2num = 2
			for item in self.right[0]:
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

			for item in self.right[1]:
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
			right, counter, lis = (self.right).expand(counter, lis)
			left, counter, lis = (self.left).expand(counter, lis)
			lis += (left+" = "+right+"\n")
			return "", counter, lis
		elif(self.data in binaryOperators):
			left, counter, lis = (self.left).expand(counter, lis)
			right, counter, lis = (self.right).expand(counter, lis)
			var = "t"+str(counter)
			lis += (var+" = "+left+" "+binaryOpMap[self.data]+" "+right+"\n")
			counter += 1
			return var, counter, lis
		elif(self.data == "NOT" or self.data == "UMINUS"):
			left, counter, lis = (self.left).expand(counter, lis)
			var = "t"+str(counter)
			lis += (var+" = "+unaryOpMap[self.data]+left+"\n")
			counter += 1
			return var, counter, lis
		elif(self.data == "ADDR" or self.data == "DEREF"):
			left, counter, lis = (self.left).expand(counter, lis)
			var = unaryOpMap[self.data]+left
			return var, counter, lis
		elif(self.data == "CONST" or self.data == "VAR"):
			return str(self.left), counter, lis


def giveCfgFile(rootlist,file):
	x = Tree(True,rootlist,'IF')
	blocks = x.giveBlocks()
	blocks = blocks[1]
	temp = 0
	for i in range(1,len(blocks)):
		file.write("\n<bb "+str(i)+">\n")

		a = blocks[i]
		if a[len(a)-1] == 'IF':
			var,temp,lis = a[0].expand(temp,"")
			file.write(lis)
			file.write("if("+var+") goto <bb "+str(a[1]-1)+">\n")
			file.write("else goto <bb "+str(a[2]-1)+">\n")

		elif a[len(a)-1] == 'GOTO':

			for j in range(0,len(a)-2):
				var,temp,lis = a[j].expand(temp,"")
				file.write(lis)
			file.write("goto <bb "+str(a[len(a)-2]-1)+">\n")
		else:
			file.write("End\n")

		