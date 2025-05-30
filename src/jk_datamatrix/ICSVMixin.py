

import typing

from .DataMatrixCSVWriter import DataMatrixCSVWriter





class ICSVMixin:

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def saveAsCSVFile(self, filePath:str):
		DataMatrixCSVWriter.saveAsCSVFile(self, filePath)
	#

	def toCSVStr(self) -> str:
		return DataMatrixCSVWriter.toCSVStr(self)
	#

	def toCSVStrList(self) -> typing.List[str]:
		return DataMatrixCSVWriter.toCSVStrList(self)
	#

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

#





