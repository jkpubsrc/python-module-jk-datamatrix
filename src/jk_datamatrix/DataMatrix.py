


from operator import itemgetter

from jk_console import SimpleTable, SimpleTableCell, SimpleTableColumn, SimpleTableConstants, SimpleTableRow

from .DataMatrixRow import DataMatrixRow






class DataMatrix(object):

	def __init__(self, columnNames:list):
		self.__columnNames = columnNames
		self.__nCols = len(self.__columnNames)
		self.__rows = []
	#

	def clear(self):
		self.__rows.clear()
	#

	def __bool__(self):
		return len(self.__rows) > 0
	#

	def __len__(self):
		return len(self.__rows)
	#

	def __createColumnNamesToIndexMap(self) -> dict:
		ret = {}
		for i, c in enumerate(self.__columnNames):
			ret[c] = i
		return ret
	#

	@property
	def columnNames(self) -> list:
		return list(self.__columnNames)
	#

	@property
	def rows(self):
		cmim = self.__createColumnNamesToIndexMap()
		for row in self.__rows:
			yield DataMatrixRow(cmim, row)
	#

	@property
	def lastRow(self) -> DataMatrixRow:
		cmim = self.__createColumnNamesToIndexMap()
		if self.__rows:
			return DataMatrixRow(cmim, self.__rows[-1])
		return None
	#

	@property
	def firstRow(self) -> DataMatrixRow:
		cmim = self.__createColumnNamesToIndexMap()
		if self.__rows:
			return DataMatrixRow(cmim, self.__rows[0])
		return None
	#

	def getRow(self, rowNo:int) -> DataMatrixRow:
		cmim = self.__createColumnNamesToIndexMap()
		return DataMatrixRow(cmim, self.__rows[rowNo])
	#

	def addColumn(self, columnName:str):
		n = self.getColumnIndex(columnName)
		if n >= 0:
			raise Exception("Column already exists: " + repr(columnName))

		self.__columnNames.append(columnName)
		for i in range(0, len(self.__rows)):
			self.__rows[i].append(None)
		self.__nCols += 1
	#

	def removeColumn(self, columnName:str):
		n = self.getColumnIndexE(columnName)

		self.__columnNames.pop(n)
		for i in range(0, len(self.__rows)):
			self.__rows[i].pop(n)
		self.__nCols -= 1
	#

	def getAllColumnValuesAsSet(self, columnName:str) -> set:
		n = self.getColumnIndexE(columnName)

		ret = set()
		for row in self.__rows:
			ret.add(row[n])

		return ret
	#

	def get(self, rowNo:int, columNo:int):
		return self.__rows[rowNo][columNo]
	#

	def findByValue(self, columnName:str, value) -> DataMatrixRow:
		n = self.getColumnIndexE(columnName)

		for irow, rowData in enumerate(self.__rows):
			if rowData[n] == value:
				cmim = self.__createColumnNamesToIndexMap()
				return DataMatrixRow(cmim, rowData)

		return None
	#

	def extractFilterByValues(self, columnNamesToData:dict):
		cmim = self.__createColumnNamesToIndexMap()

		columnIndicesToData = {}
		for columnName, expectedValue in columnNamesToData.items():
			assert isinstance(columnName, str)
			assert columnName in cmim
			columnIndicesToData[cmim[columnName]] = expectedValue

		ret = DataMatrix(self.__columnNames)

		for row in self.__rows:
			bOk = True
			for columnIndex, expectedValue in columnIndicesToData.items():
				v = row[columnIndex]
				if v != expectedValue:
					bOk = False
					break
			if bOk:
				ret.addRow(*row)

		return ret
	#

	def findByValues(self, **columnNamesToData):
		assert columnNamesToData
		cmim = self.__createColumnNamesToIndexMap()

		columnIndicesToData = {}
		for columnName, expectedValue in columnNamesToData.items():
			assert isinstance(columnName, str)
			assert columnName in cmim
			columnIndicesToData[cmim[columnName]] = expectedValue

		for row in self.__rows:
			bOk = True
			for columnIndex, expectedValue in columnIndicesToData.items():
				v = row[columnIndex]
				if v != expectedValue:
					bOk = False
					break
			if bOk:
				return DataMatrixRow(cmim, row)

		return None
	#

	def extractFilterByLatestEncountered(self, columnName:str):
		# TODO
		n = self.getColumnIndexE(columnName)

		ret = DataMatrix(self.__columnNames)

		allreadySeen = set()
		for i in reversed(range(0, len(self.__rows))):
			row = self.__rows[i]
			if row[n] in allreadySeen:
				continue
			else:
				ret.addRow(*row)
				allreadySeen.add(row[n])

		ret.reverse()

		return ret
	#

	def getRowByMaxValue(self, columnName:str):
		n = self.getColumnIndexE(columnName)

		vStored = None
		bIsFirst = True
		rowSelected = None
		for irow, rowData in enumerate(self.__rows):
			v = rowData[n]
			if v is not None:
				if bIsFirst:
					vStored = v
					rowSelected = rowData
					bIsFirst = False
				else:
					if v > vStored:			
						vStored = v
						rowSelected = rowData

		if vStored is not None:
			cmim = self.__createColumnNamesToIndexMap()
			return DataMatrixRow(cmim, rowSelected)
		else:
			return None
	#

	def groupBy(self, keyColumnName:str, valueColumnName:str):
		nKey = self.getColumnIndexE(keyColumnName)
		nVal = self.getColumnIndexE(valueColumnName)

		ret = DataMatrix(self.__columnNames)

		mapping = {}		# maps keys to a set
		for row in self.__rows:
			itemKey = row[nKey]
			m = mapping.get(itemKey)
			if m is None:
				m = set()
				mapping[itemKey] = m
			m.add(row[nVal])

		ret = DataMatrix(self.__columnNames)

		allreadySeen = set()
		for row in self.__rows:
			itemKey = row[nKey]
			if itemKey in allreadySeen:
				continue
			else:
				newRow = list(row)
				newRow[nVal] = mapping[itemKey]
				ret.addRow(*newRow)
				allreadySeen.add(itemKey)

		return ret
	#

	def reverse(self):
		self.__rows.reverse()
	#

	def orderByColumn(self, columnName:str):
		n = self.getColumnIndexE(columnName)
		self.__rows.sort(key = itemgetter(n))
	#

	def getColumnIndexE(self, columnName:str) -> int:
		for i, t in enumerate(self.__columnNames):
			if t == columnName:
				return i
		raise Exception("No such column: " + repr(columnName))
	#

	def getColumnIndex(self, columnName:str) -> int:
		for i, t in enumerate(self.__columnNames):
			if t == columnName:
				return i
		return -1
	#

	def addRow(self, *args):
		data = list(args)
		while len(data) < self.__nCols:
			data.append(None)
		self.__rows.append(data)
	#

	def dump(self):
		table = SimpleTable()
		table.addRow(*self.__columnNames).hlineAfterRow = True
		for row in self.__rows:
			table.addRow(*[ str(x) for x in row ])

		print()
		table.print()
		print()
	#
#








