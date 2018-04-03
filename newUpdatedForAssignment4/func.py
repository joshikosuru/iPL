class Func(object):
	def __init__(self):
		self.name = None
		self.retType = None
		self.retDerive = None
		self.paramList = None
		self.ASTList = None
		self.returnSTMT = None

	def __init__(self, name, retType, retDerive, paramList, ASTList, returnSTMT):
		self.name = name
		self.retType = retType
		self.retDerive = retDerive
		self.paramList = paramList
		self.ASTList = ASTList
		self.returnSTMT = returnSTMT
