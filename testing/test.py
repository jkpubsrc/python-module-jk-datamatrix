#!/usr/bin/python3





from jk_datamatrix import DataMatrix






m = DataMatrix([ "word", "number", "status" ])
m.addRow("Apple", 123, True)
m.addRow("Carrot", 234, False)
m.addRow("Pear", 345, True)
m.addRow("Banana", 456, False)
m.addRow("Cherry", 567, True)
m.addRow("Blackberry", 678, False)
m.addRow("Avocado", 789, True)
m.dump()

m.orderByColumn("word")
m.dump()

m.orderByColumn("number")
m.dump()

m.orderByColumn("status")
m.dump()

m.removeRowsByValues(number=345)
m.dump()

m.addColumn("foobar", [ 1, 2, 3 ])
m.dump()

m.moveColumn("foobar", after="status")
m.dump()


print()
print()
for line in m.toCSVStrList():
	print(repr(line))



