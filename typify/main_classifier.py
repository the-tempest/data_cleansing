# main_classifier.py
# this defines a main_classifier class which
# takes in a table object and attempts to
# classify each column in it, returning
# a report in the form of a string

import mysql.connector, os, re
from secrets import path
execfile(path+"typify/heuristics.py")
execfile(path+"typify/helper.py")
execfile(path+"typify/features/features.py")
execfile(path+"typify/classifier.py")
execfile(path+'numeric_classifier.py')
execfile(path+'table.py')
execfile(path+"typify/tie_breaker.py")

class main_classifier:
	def __init__(self):
		self.build_classifiers()
		self.naivebayes_class = naivebayes_classifier()
		self.heuristic_class = heuristic_classifier()

		# the data that is used by the classifier
		self.my_table     = None
		self.results      = None
		self.result_table = None
		self.report       = None

	def new_table(table):
		'''takes in a new table and generates the data for it'''
		# TODO once we use this one, add this function call to main
		self.my_table     = table
		self.results      = self.table_typify()
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
		for i, col in enumerate(self.table.getColumns()):
			prediction = self.results[i][1]
			col.tentativeClassification(prediction)
		return self.table

	def reset_table(self):
		'''sets the tentative classifications
		in the table to None'''
		for col in self.table.getColumns():
			col.tentativeClassification(None)

	def table_typify(self):
		'''takes in a table and returns a list
		of tuples of the form (a, p, f) where
		a is the actual column name
		p is the predicted column name
		f is the certainty of the guess'''
		actual = []
		predictions = []
		fractions = []
		cols = self.table.getColumns()
		size = len(cols)

		# generate data for the tuples
		for elem in cols:
			column = elem.rows
			self.curr_col_name = elem.colName
			guesses = self.column_typify(column)
			prediction, fraction = self.column_predict(guesses)
			# TODO add dictionaries to column
			actual.append(elem.colName)
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

	def column_predict(self, guesses):
		'''takes in a list of predictions for
		a column and returns a tuple of the form
		(prediction, certainty)'''
		results = {}
		# populate the dictionary
		for item in guesses:
			if item not in results:
				results[item] = 0
			results[item] += 1
		size = len(guesses)
		for key in results.keys():
			fraction = float(results[key]) / float(size)
			fraction = "{0:.3f}".format(fraction)
			results[key] = fraction
		best_guess = dict_max(results)
		guess_fraction = results[best_guess]
		# ensure there actually is a good guess
		if best_guess < .5:
			return 'misc', None
		return best_guess, guess_fraction

	def column_typify(self, column):
		'''takes in a column and
		returns a list of predictions
		for each token'''
		dyct = {}
		predictions = []
		i = 0
		for item in column:
			guess = self.token_typify(item)
			dyct[i]= guess
			i = i+1
			predictions.append(guess)
		return predictions, dyct

	def token_typify(self, token):
		'''takes in a token and returns a
		prediction for its type'''
		# TODO finish implementing
		
		# Naive Bayes part
		# returns this tuple
		# (guess, probability_dictionary, mean, std_dev)
		prediction1 = self.naivebayes_classifier.classify(token)[0]

		# Heuristic part
		# one or more guesses
		prediction2 = self.heuristic_classifier.classify(token)
		
		# Figure out the final guess through matching
		if prediction1 in prediction2:
			return prediction1
		
		return 'misc'
