execfile("typify/column_type.py")
execfile("extraction.py")
from secrets import password, port, database, user, host
import copy
num_classes = ['Date', 'Longitude', 'Latitude', 'Number', 'Zip', 'Phone_Number', 'IP', 'ISBN', 'Year']
list_of_classes = ['Date', 'Longitude', 'Latitude', 'Number', 'Zip', 'Phone_Number', 'IP', 'ISBN', 'Year', 'full name', 'first name', 'last name', 'datestring',
		'full address', 'street address', 'city state', 'email', 'location', 'description', 'url', 'city', 'state']
NUMBER_OF_CLASSES = len(list_of_classes)

class column_type_tester:
	def __init__(self,filepath):
		table_name = extraction.extract(filepath)
		self.t = getTable(table_name, user, password, host, database)
		self.column_typer = column_typer(self.t)

		self.heur_conf_mat, self.matrix_indices = self.initialize_confusion_matrix()
		self.bayes_conf_mat = copy.deepcopy(self.heur_conf_mat)
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
				self.heur_conf_mat[x][y] = 0
				self.bayes_conf_mat[x][y] = 0

	def column_test(self):
		self.clear_matrix()
		typify_results = self.column_typer.table_typify(self.column_typer.my_table)

		for i in range(len(typify_results)):
			actual = self.t.getColumns()[i].actualClass
			classified = typify_results[i][1]

			if actual in num_classes:
				self.bayes_conf_mat[self.matrix_indices[actual]][self.matrix_indices[classified]] += 1
			else:
				self.heur_conf_mat[self.matrix_indices[actual]][self.matrix_indices[classified]] += 1

		return self.calcF()

	def entry_test(self):
		self.clear_matrix()
		for col in self.t.getColumns():
			self.column_typer.curr_col_name = col.colName
			actual = col.actualClass
			for entry in col.rows:
				classified = self.column_typer.token_typify(entry)
				if actual in num_classes:
					self.bayes_conf_mat[self.matrix_indices[actual]][self.matrix_indices[classified]] += 1
				else:
					self.heur_conf_mat[self.matrix_indices[actual]][self.matrix_indices[classified]] += 1
		return self.calcF();

	def calcF(self):
		b_precision = self.compute_precision_avg(self.bayes_conf_mat)
		b_recall = self.compute_recall_avg(self.bayes_conf_mat)
		b_fscore = self.f1score(b_precision, b_recall)
		print "Bayes precision: " + str(b_precision)
		print "Bayes recall: " + str(b_recall)
		print "Bayes f1 score: " + str(b_fscore)
		h_precision = self.compute_precision_avg(self.heur_conf_mat)
		print "Heur precision: " + str(h_precision)
		h_recall = self.compute_recall_avg(self.heur_conf_mat)
		print "Heur recall: " + str(h_recall)
		h_fscore = self.f1score(h_precision, h_recall)
		print "Heur f1 score: " + str(h_fscore)


		return b_fscore, h_fscore

	def compute_precision_avg(self, mat):
		precisions = []
		for i in range(NUMBER_OF_CLASSES):
			num, den = self.compute_precision(i, mat)
			if den != 0:
				precisions.append(float(num)/float(den))
		if (len(precisions) != 0):
			return sum(precisions)/float(len(precisions))
		else:
			return 0

	def compute_recall_avg(self, mat):
		recalls = []
		for i in range(NUMBER_OF_CLASSES):
			num, den = self.compute_recall(i, mat)
			if den != 0:
				recalls.append(float(num)/float(den))
		if (len(recalls) != 0):
			return sum(recalls)/float(len(recalls))
		else:
			return 0

	def compute_precision(self, x, mat):
		numerator = mat[x][x]
		false_positives = 0
		for y in range(NUMBER_OF_CLASSES): # maybe iterate this in opposite direction
			if x != y:
				false_positives += mat[y][x]
		denominator = false_positives + mat[x][x]

		return (numerator, denominator)

	def compute_recall(self, x, mat):
		numerator = mat[x][x]
		denominator = sum(mat[x])
		return (numerator, denominator)

	def f1score(self, precision, recall):
		numerator = 2 * precision * recall
		denominator = precision + recall
		if denominator != 0:
			return numerator / denominator
		else:
			return 0
