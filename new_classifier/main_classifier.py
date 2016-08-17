# main_classifier.py
# this defines a main_classifier class which
# takes in a table object and attempts to
# classify each column in it, returning
# a report in the form of a string

import mysql.connector, os, re, random
from secrets import path
execfile(path+"typify/heuristics.py")
execfile(path+"typify/helper.py")
execfile(path+"typify/features/features.py") # TODO give it a spot
execfile(path+"typify/classifier.py")
execfile(path+'new_classifier/naivebayes_classifier.py')
execfile(path+'new_classifier/heuristic_classifier.py')
execfile(path+'table.py')

class main_classifier:
	def __init__(self):
		self.naivebayes_class = naivebayes_classifier()
		self.heuristic_class = heuristic_classifier()

		# the data that is used by the classifier
		self.my_table     = None
		self.results      = None
		self.result_table = None
		self.report       = ''

	def new_table(self, table):
		'''takes in a new table and generates the data for it'''
		self.my_table     = table
		self.results      = self.classify_table()
		self.result_table = self.apply_predictions()
		self.report       = self.build_report()

	def build_report(self):
		ret = ''
		results = self.results
		i = 0
		for item in results:
			line = self.build_column_report(item)
			ret += line
			#adding in the misclassified token list
			ret +=self.build_column_error_report(self.my_table.columns[i])
			i += 1
		return ret

	def build_column_report(self,column_tuple):
		# TODO perhaps make this more abstracted
		'''Classifies the columns in my_table and
		returns a summary report as a string'''
		actual = column_tuple[0]
		prediction = column_tuple[1]
		fraction = str(column_tuple[2])
		line = "The column named "
		line += actual
		line += " appears to be of the type "
		line += str(prediction)
		line += " with a certainty of "
		line += fraction
		line += ".\n"
		return line

	def build_column_error_report(self, column):
		list = self.misclassified(column)
		line = ""
		for i in list:
			line += "the token "
			line+= column.rows[i]
			line +=" was incorrectly classified as "
			line+= column.guesses[i]
		line += ".\n"
		return line

	def misclassified(self, column):
		'''returns a list of the tokens that may
		have been misclassfied as their classification is 
		not the plurality type'''
		think = column.tentClass
		dyct = column.guesses
		error_list = []
		for i in range(len(dyct)):
			if dyct[i]!=think:
				error_list.append(i)
		return error_list
			
	def apply_predictions(self):
		''' takes in a table and returns a table
		with the tentative classifications filled in'''
		for i, col in enumerate(self.my_table.getColumns()):
			prediction = self.results[i][1]
			col.tentativeClassification(prediction)
		return self.my_table

	def reset_table(self):
		'''sets the tentative classifications
		in the table to None'''
		for col in self.my_table.getColumns():
			col.tentativeClassification(None)

	def classify_table(self):
		'''takes in a table and returns a list
		of tuples of the form (a, p, f) where
		a is the actual column name
		p is the predicted column name
		f is the certainty of the guess'''
		actual = []
		predictions = []
		fractions = []
		cols = self.my_table.getColumns()
		size = len(cols)

		# generate data for the tuples
		for col in cols:
			column = col.rows
			self.heuristic_class.curr_col_name = col.colName
			guesses = self.get_column_predictions(column)
			prediction, fraction = self.classify_column(guesses)
			# TODO add dictionaries to column
			actual.append(col.colName)
			predictions.append(prediction)
			fractions.append(fraction)
		results = []

		# construct tuples
		for i in range(size):
			a = actual[i]
			p = predictions[i]
			f = fractions[i]
			t = (a, p, f)
			results.append(t)
		return results

	def classify_column(self, guesses):
		'''takes in a list of predictions for
		a column and returns a tuple of the form
		(prediction, certainty)'''
		results = {}
		# populate the dictionary
		for l in guesses:
			for guess in l:
				if guess not in results:
					results[guess] = 0
				results[guess] += 1
		size = len(guesses)
		for key in results.keys():
			fraction = float(results[key]) / float(size)
			fraction = float("{0:.3f}".format(fraction))
			results[key] = fraction
		best_guess = dict_max(results)
		guess_fraction = results[best_guess]
		# ensure there actually is a good guess
		if best_guess <= .5:
			return 'misc', None
		return best_guess, guess_fraction

	def get_column_predictions(self, column):
		'''takes in a column and
		returns a list of predictions
		for each token'''
		predictions = []
		i = 0
		self.prev = {}
		for token in column:
			guesses = self.get_token_predictions(token)
			if token not in self.prev:
				self.prev[token] = guesses
			for guess in guesses:
				predictions.append(guess)
		self.prev = {}
		return predictions

	def get_token_predictions(self, token):
		'''takes in a token and returns a
		list of predictions for its type'''

		# looks at previous guesses to save time
		if token in self.prev:
			return self.prev[token]

		# Naive Bayes part
		nb_guess = self.naivebayes_class.classify(token)
		guesses  = [nb_guess]

		# Heuristic part
		h_guess = self.heuristic_class.classify(token)
		guesses += h_guess

		return guesses