





class DataMatrixRow(object):

	def __init__(self, columnNamesToIndexMap:dict, rowData:list):
		self.__columnNamesToIndexMap = columnNamesToIndexMap
		self.__rowData = rowData
	#

	def __getitem__(self, ii):
		if isinstance(ii, int):
			return self.__rowData[ii]
		elif isinstance(ii, str):
			n = self.__columnNamesToIndexMap[ii]
			return self.__rowData[n]
		else:
			raise Exception()
	#

	def __setitem__(self, ii, value):
		if isinstance(ii, int):
			self.__rowData[ii] = value
		elif isinstance(ii, str):
			n = self.__columnNamesToIndexMap[ii]
			self.__rowData[n] = value
		else:
			raise Exception()
	#

	def __len__(self):
		return len(self.__rowData)
	#

	def clone(self):
		return DataMatrixRow(self.__columnNamesToIndexMap, list(self.__rowData))
	#

#








