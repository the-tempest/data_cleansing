execfile("typify/column_type.py")
execfile("extraction.py")
from secrets import password, port, database, user, host
NUMBER_OF_CLASSES = 7
list_of_classes = ['Date', 'Longitude', 'Latitude', 'Number', 'Zip', 'Phone_Number', 'IP']

class column_type_tester:
	def __init__(self,filepath):
		table_name = extraction.extract(filepath)
		t = getTable(table_name, user, password, host, database)
		self.column_typer = column_typer(t)
		self.name = '123'

	def initialize_confusion_matrix(self):
		confusion_matrix = []
		matrix_indices = {}
		for x in range(NUMBER_OF_CLASSES):
			for y in range(NUMBER_OF_CLASSES):
				if len(confusion_matrix) == y:
					confusion_matrix.append([])
					confusion_matrix[x].append(0)
				else:
					confusion_matrix[x].append(0)
			
			matrix_indices[list_of_classes[x]] = x

		return confusion_matrix, matrix_indices

	def test_on_file(self, filepath):
		
		typify_results = self.column_typer.table_typify(self.column_typer.my_table) # list of tuples
		confusion_matrix, matrix_indices = self.initialize_confusion_matrix()
			
		print typify_results
		print confusion_matrix

		for item in typify_results:
			if item[0] == item[1]: # if labeled correctly
				confusion_matrix[matrix_indices[item[0]]][matrix_indices[item[0]]] += 1
			else:
				confusion_matrix[matrix_indices[item[0]]][matrix_indices[item[1]]] += 1

		return confusion_matrix




