execfile("typify/column_type.py")
execfile("extraction")
from secrets import password, port, database, user, host



class column_type_tester:
	def __init__(self):
		self.name = name
		self.column_typer = column_typer()

	def test_on_file(self, filepath):
		table_name = extraction.extract(filepath)
		t = getTable(table_name, user, password, host, database)
		typify_results = self.column_typer.table_typify(t) # list of tuples

		column_names = []
		for col in t.columns: #build list of actual column names 
			column_names.append(col.colName)

		

