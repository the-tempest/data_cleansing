execfile("typify/column_type.py")
execfile("extraction.py")
from secrets import password, port, database, user, host
list_of_classes = ['Date', 'Longitude', 'Latitude', 'Number', 'Zip', 'Phone_Number', 'IP', 'full name', 'first name', 'last name', 'datestring',
		'full address', 'street address', 'city state', 'email', 'location', 'description', 'url', 'city', 'state']
NUMBER_OF_CLASSES = len(list_of_classes)

class column_type_tester:
	def __init__(self,filepath):
		table_name = extraction.extract(filepath)
		self.t = getTable(table_name, user, password, host, database)
		self.column_typer = column_typer(self.t)

		confusion_matrix, matrix_indices = self.initialize_confusion_matrix()

		self.confusion_matrix = confusion_matrix
		self.matrix_indices = matrix_indices
		print "What class is each column? Here is the list of choices:"
		print list_of_classes
		print "\n"
		for col in self.t.getColumns():
			print "Column name in the spreadsheet: " + col.colName + "\n"
			print list_of_classes
			print "Here are some of the entries: \n"
			for i in range(5):
				print col.rows[i]
			actualClass = self.getResp("\nSo what's the column class? ")
			col.actualClass = actualClass




	def getResp(self, prompt):
		response = raw_input(prompt)
		if not response in list_of_classes:
			return self.getResp("That's not a valid classname, try again: ")
		else:
			return response

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

	def clear_matrix(self):
		for x in range(NUMBER_OF_CLASSES):
			for y in range(NUMBER_OF_CLASSES):
				self.confusion_matrix[x][y] = 0

	def column_test(self):
		self.clear_matrix()
		typify_results = self.column_typer.table_typify(self.column_typer.my_table) # list of tuples

		print typify_results
		#print self.confusion_matrix
		for i in range(len(typify_results)):
			actual = self.t.getColumns()[i].actualClass
			classified = typify_results[i][1]
			if (actual == classified):
				print "MATCH"
			self.confusion_matrix[self.matrix_indices[actual]][self.matrix_indices[classified]] += 1

		return self.calcF()

	def entry_test(self):
		self.clear_matrix()
		for col in self.t.getColumns():
			self.column_typer.curr_col_name = col.colName
			actual = col.actualClass
			for entry in col.rows:
				classified = self.column_typer.token_typify(entry)
				self.confusion_matrix[self.matrix_indices[actual]][self.matrix_indices[classified]] += 1
		return self.calcF();

	def calcF(self):
		precision = self.compute_precision_avg()
		recall = self.compute_recall_avg()
		fscore = self.f1score(precision, recall)

		print precision
		print recall
		print fscore
		return fscore

	def compute_precision_avg(self):
		precisions = []
		for i in range(NUMBER_OF_CLASSES):
			num, den = self.compute_precision(i)
			if den != 0:
				precisions.append(float(num)/float(den))
		return sum(precisions)/float(len(precisions))

	def compute_recall_avg(self):
		recalls = []
		for i in range(NUMBER_OF_CLASSES):
			num, den = self.compute_recall(i)
			if den != 0:
				recalls.append(float(num)/float(den))
		return sum(recalls)/float(len(recalls))

	def compute_precision(self, x):
		numerator = self.confusion_matrix[x][x]
		false_positives = 0
		for y in range(NUMBER_OF_CLASSES): # maybe iterate this in opposite direction
			if x != y:
				false_positives += self.confusion_matrix[y][x]
		denominator = false_positives + self.confusion_matrix[x][x]

		return (numerator, denominator)

	def compute_recall(self, x):
		numerator = self.confusion_matrix[x][x]
		denominator = sum(self.confusion_matrix[x])
		return (numerator, denominator)

	def f1score(self, precision, recall):
		numerator = 2 * precision * recall
		denominator = precision + recall

		return numerator / denominator
