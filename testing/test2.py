#!/usr/bin/python3





from jk_datamatrix import DataMatrix, DataMatrixJSONLoader






m = DataMatrix([ "word", "number", "status" ])
m.addRow("Apple", 123, True)
m.addRow("Carrot", 234, False)
m.addRow("Pear", 345, True)
m.addRow("Banana", 456, False)
m.addRow("Cherry", 567, True)
m.addRow("Blackberry", 678, False)
m.addRow("Avocado", 789, True)
m.orderByColumn("word")
m.orderByColumn("number")
m.orderByColumn("status")
m.removeRowsByValues(number=345)
m.dump()


print()
print()
for line in m.toCSVStrList():
	print(repr(line))


print()
print()
sJSON = m.toJSONStr()
print(sJSON)


print()
print()


m2 = DataMatrixJSONLoader.loadFromJSONStr(sJSON)
m2.dump()


