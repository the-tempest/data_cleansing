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
		
		confusion_matrix, matrix_indices = self.initialize_confusion_matrix()

		self.confusion_matrix = confusion_matrix
		self.matric_indices = matric_indices

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

	def test_on_file(self):
		
		typify_results = self.column_typer.table_typify(self.column_typer.my_table) # list of tuples
			
		print typify_results
		print confusion_matrix

		for item in typify_results:
			if item[0] == item[1]: # if labeled correctly
				self.confusion_matrix[self.matrix_indices[item[0]]][self.matrix_indices[item[0]]] += 1
			else:
				self.confusion_matrix[self.matrix_indices[item[0]]][self.matrix_indices[item[1]]] += 1

		precision = self.compute_precision()
		recall = self.compute_recall()
		fscore = self.fscore(precision, recall)

		print precision
		print compute_recall

		return fscore

	def compute_precision():
		curr_numerator = 0
		curr_denominator = 0
		for x in range(NUMBER_OF_CLASSES):
			curr_numerator += self.confusion_matrix[x][x]	
			false_positives = 0	
			for y in range(NUMBER_OF_CLASSES): # maybe iterate this in opposite direction
				if x != y:
					false_positives += self.confusion_matrix[y][x]
			curr_denominator += false_positives + self.confusion_matrix[x][x]		
				

		return curr_numerator / curr_denominator

	def compute_recall():
		curr_numerator = 0
		curr_denominator = 0

		for x in range(NUMBER_OF_CLASSES):
			curr_numerator += self.confusion_matrix[x][x]
			false_negatives = 0
			for y in range(NUMBER_OF_CLASSES): 
				if x != y:
					false_negatives += self.confusion_matrix[x][y]
			curr_denominator += false_negatives + self.confusion_matrix[x][x]

		return curr_numerator / curr_denominator

	def fscore(precision, recall):
		numerator = precision * recall
		denominator = precision + recall

		return numerator / denominator

