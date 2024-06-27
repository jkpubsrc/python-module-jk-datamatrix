


import typing

import jk_typing
import jk_console

from ._IDataMatrix import _IDataMatrix
from .DataMatrixRow import DataMatrixRow
from .ICSVMixin import ICSVMixin




class _MyItemGetter(object):

	def __init__(self, columnNo:int):
		self.__columnNo = columnNo
	#

	def __call__(self, row):
		item = row[self.__columnNo]
		if item is None:
			return ""
		return item
	#

#





DataMatrix = typing.NewType("DataMatrix", object)

class DataMatrix(_IDataMatrix,ICSVMixin):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, columnNames:typing.List[str]):
		self.__columnNames = columnNames
		self.__nCols = len(self.__columnNames)
		self.__rows:typing.List[typing.List[typing.Any]] = []
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def columnNames(self) -> typing.List[str]:
		return list(self.__columnNames)
	#

	@property
	def rows(self) -> typing.Iterable[DataMatrixRow]:
		cmim = self.__createColumnNamesToIndexMap()
		for _rowDat in self.__rows:
			yield DataMatrixRow(cmim, _rowDat)
	#

	@property
	def rowdicts(self) -> typing.Iterable[typing.Dict[str,typing.Any]]:
		for _rowData in self.__rows:
			_rowDict:typing.Dict[str,typing.Any] = {}
			for i in range(0, self.__nCols):
				colName = self.__columnNames[i]
				_rowDict[colName] = _rowData[i]
			yield _rowDict
	#

	@property
	def nRows(self) -> int:
		return len(self.__rows)
	#

	@property
	def nColumns(self) -> int:
		return self.__nCols
	#

	@property
	def lastRow(self) -> typing.Union[DataMatrixRow,None]:
		cmim = self.__createColumnNamesToIndexMap()
		if self.__rows:
			return DataMatrixRow(cmim, self.__rows[-1])
		return None
	#

	@property
	def firstRow(self) -> typing.Union[DataMatrixRow,None]:
		cmim = self.__createColumnNamesToIndexMap()
		if self.__rows:
			return DataMatrixRow(cmim, self.__rows[0])
		return None
	#

	################################################################################################################################
	## Helper Method
	################################################################################################################################

	def __createColumnNamesToIndexMap(self) -> typing.Dict[str,int]:
		ret = {}
		for i, c in enumerate(self.__columnNames):
			ret[c] = i
		return ret
	#

	################################################################################################################################
	## Public Method
	################################################################################################################################

	def clone(self) -> DataMatrix:
		dm = DataMatrix(list(self.__columnNames))
		for row in self.__rows:
			dm.__rows.append(list(row))
		return dm
	#

	#
	# Create a new empty matrix of equal structure than this matrix.
	#
	def cloneEmpty(self) -> DataMatrix:
		dm = DataMatrix(list(self.__columnNames))
		return dm
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

	def getRow(self, rowNo:int) -> DataMatrixRow:
		assert isinstance(rowNo, int)

		cmim = self.__createColumnNamesToIndexMap()
		return DataMatrixRow(cmim, self.__rows[rowNo])
	#

	#
	# Add a column.
	#
	# @param	str columnName		(required) A unique column name.
	# @param	any[] values		(optional) Values to put into the column.
	#
	def addColumn(self, columnName:str, values:typing.Union[tuple,list] = None):
		assert isinstance(columnName, str)

		n = self.getColumnIndex(columnName)
		if n >= 0:
			raise Exception("Column already exists: " + repr(columnName))

		self.__columnNames.append(columnName)

		if values is None:
			iMax = 0
		else:
			assert isinstance(values, (list,tuple))
			iMax = min(len(values), len(self.__rows))

		for i in range(0, iMax):
			self.__rows[i].append(values[i])
		for i in range(iMax, len(self.__rows)):
			self.__rows[i].append(None)

		self.__nCols += 1
	#

	#
	# Insert a column at the specified position.
	#
	# @param	int position		(required) The position where to insert the column.
	# @param	str columnName		(required) A unique column name.
	# @param	any[] values		(optional) Values to put into the column.
	#
	def insertColumn(self, position:int, columnName:str, values:typing.Union[tuple,list] = None):
		assert isinstance(position, int)
		assert isinstance(columnName, str)

		n = self.getColumnIndex(columnName)
		if n >= 0:
			raise Exception("Column already exists: " + repr(columnName))

		self.__columnNames.insert(position, columnName)

		if values is None:
			iMax = 0
		else:
			assert isinstance(values, (list,tuple))
			iMax = min(len(values), len(self.__rows))

		for i in range(0, iMax):
			self.__rows[i].insert(position, values[i])
		for i in range(iMax, len(self.__rows)):
			self.__rows[i].insert(position, None)

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

	def getAllColumnValues(self, columnName:str) -> typing.List[typing.Any]:
		n = self.getColumnIndexE(columnName)

		ret = []
		for row in self.__rows:
			ret.append(row[n])

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

	def extractFilterByValues(self, **columnNamesToData):
		assert columnNamesToData
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

	def removeRowsByValues(self, **columnNamesToData) -> int:
		assert columnNamesToData
		cmim = self.__createColumnNamesToIndexMap()

		columnIndicesToData = {}
		for columnName, expectedValue in columnNamesToData.items():
			assert isinstance(columnName, str)
			assert columnName in cmim
			columnIndicesToData[cmim[columnName]] = expectedValue

		listOfRowsToRemove = []
		for i, row in enumerate(self.__rows):
			bOk = True
			for columnIndex, expectedValue in columnIndicesToData.items():
				v = row[columnIndex]
				if v != expectedValue:
					bOk = False
					break
			if bOk:
				listOfRowsToRemove.append(i)

		for i in reversed(listOfRowsToRemove):
			del self.__rows[i]

		return len(listOfRowsToRemove)
	#

	def removeRowByValues(self, **columnNamesToData) -> bool:
		assert columnNamesToData
		cmim = self.__createColumnNamesToIndexMap()

		columnIndicesToData = {}
		for columnName, expectedValue in columnNamesToData.items():
			assert isinstance(columnName, str)
			assert columnName in cmim
			columnIndicesToData[cmim[columnName]] = expectedValue

		for i, row in enumerate(self.__rows):
			bOk = True
			for columnIndex, expectedValue in columnIndicesToData.items():
				v = row[columnIndex]
				if v != expectedValue:
					bOk = False
					break
			if bOk:
				del self.__rows[i]
				return True

		return False
	#

	def removeRow(self, rowNo:int) -> bool:
		assert isinstance(rowNo, int)
		assert 0 <= rowNo < len(self.__rows)

		del self.__rows[rowNo]
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
		assert isinstance(columnName, str)

		n = self.getColumnIndexE(columnName)
		self.__rows.sort(key = _MyItemGetter(n))
	#

	def getColumnIndexE(self, columnName:str) -> int:
		assert isinstance(columnName, str)

		for i, t in enumerate(self.__columnNames):
			if t == columnName:
				return i
		raise Exception("No such column: " + repr(columnName))
	#

	def getColumnIndex(self, columnName:str) -> int:
		assert isinstance(columnName, str)

		for i, t in enumerate(self.__columnNames):
			if t == columnName:
				return i
		return -1
	#

	def addRow(self, *args, **kwargs):
		data:typing.List[typing.Any] = list(args)

		while len(data) < self.__nCols:
			data.append(None)

		for columnName, v in kwargs.items():
			n = self.getColumnIndexE(columnName)
			data[n] = v

		self.__rows.append(data)
	#

	def toSimpleTable(self) -> jk_console.SimpleTable:
		table = jk_console.SimpleTable()
		table.addRow(*self.__columnNames).hlineAfterRow = True
		for row in self.__rows:
			table.addRow(*[ str(x) for x in row ])
		return table
	#

	def dump(self):
		print()
		print(self.toStr())
		print()
	#

	def toStr(self) -> str:
		table = self.toSimpleTable()
		return "\n".join(table.printToLines())
	#

	def toStrLines(self) -> typing.List[str]:
		table = self.toSimpleTable()
		return table.printToLines()
	#

	def __str__(self):
		return self.toStr()
	#

	def __getitem__(self, rowNo:int) -> DataMatrixRow:
		assert isinstance(rowNo, int)
		assert rowNo >= 0

		cmim = self.__createColumnNamesToIndexMap()
		return DataMatrixRow(cmim, self.__rows[rowNo])
	#

	def moveColumn(self, columnName:str, *, before:str = None, after:str = None) -> bool:
		# ensure that the target column exists
		if before is not None:
			if columnName == before:
				return False
			self.getColumnIndexE(before)
		elif after is not None:
			if columnName == after:
				return False
			self.getColumnIndexE(after)
		else:
			raise Exception("Eithe specify before or after!")

		nSourceCol = self.getColumnIndexE(columnName)
		colData = self.getAllColumnValues(columnName)
		self.removeColumn(columnName)

		if before:
			nTargetCol = self.getColumnIndexE(before)
		elif after:
			nTargetCol = self.getColumnIndexE(after) + 1
		else:
			raise Exception()
		self.insertColumn(nTargetCol, columnName, colData)

		return True
	#

#








