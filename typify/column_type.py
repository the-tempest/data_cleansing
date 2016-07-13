# column_type.py
# this defines a column_typer class which
# takes in a table object and attempts to
# classify each column in it, returning
# a report in the form of a string

import mysql.connector, os, re
execfile("heuristics.py")
execfile("helper.py")
execfile("features/features.py")
execfile("classifier.py")

#The form strings are in the process of being totally replaced with regular expressions
#TODO: unicode support

ASCII_NUMS = [n for n in range(48, 58)]
ASCII_UPPER = [n for n in range(65, 91)]
ASCII_LOWER = [n for n in range(97, 123)]
ASCII_ADDRESS = [32, 39, 44, 45, 46] + ASCII_NUMS + [58, 59] + ASCII_UPPER + ASCII_LOWER
ASCII_NAME = [32, 44, 45, 46] + ASCII_UPPER + ASCII_LOWER
NAME_REGEX = r'''^[A-Z][a-z'-]*$'''

class column_typer:
	def __init__(self, table):
		self.build_classifiers()

	def build_report(self, table):
		ret = ''
		results = table_typify(table)
		for item in results:
			actual = item[0]
			prediction = item[1]
			fraction = str(item[2])
			line = "The column named "
			line += actual
			line += " appears to be of the type "
			line += prediction
			line += " with a certainty of "
			line += fraction
			line += "%.\n\n"
			line += ret
		return ret 

	def table_typify(self, table):
		'''takes in a table and returns a list
		of tuples of the form (a, p, f) where
		a is the actual column name
		p is the predicted column name
		f is the certainty of the guess'''
		actual = []
		predictions = []
		fractions = []
		# generate data for the tuples
		for elem in table.getColumns():
			column = elem.rows
			guesses = column_typify(column)
			prediction, fraction = column_predict(guesses)
			actual.append(elem.colName)
			predictions.append(prediction)
			fractions.append(fraction)
		results = []
		# construct tuples
		for i in range(len(table.getColumns())):
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
			fraction = "{0:.2f}".format(fraction) 
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
		predictions = []
		for item in column:
			guess = token_typify(item)
			predictions.append(guess)
		return predictions

	def token_typify(self, token):
		'''takes in a token and returns a
		prediction for its type'''
		certainties = {}
		for f in heuristics:
			tipe, value = f(token)
			certainties[tipe] = value
		prediction = dict_max(certainties)
		return prediction

	def build_classifiers(self):
		'''builds the self.column_classifiers data member by creating classifier objects created 
		by classifier(name of the type, possible ascii values in the type string, list of the known condensed forms)'''
		# TODO complete classifiers
		self.column_classifiers = []

		# names
		names = ['full name', 'first name', 'last name', 'datestring',
				'full address', 'street address', 'city state', 'email',
				'location', 'description']

		# possible values
		datestring_pv = [32, 44, 46] + ASCII_NUMS + ASCII_UPPER + ASCII_LOWER
		email_pv = [43, 45, 46, 64, 95] + ASCII_NUMS + ASCII_UPPER + ASCII_LOWER
		description_pv = []
		possible_values = [ASCII_NAME, ASCII_NAME, ASCII_NAME, datestring_pv,
					 ASCII_ADDRESS, ASCII_ADDRESS, ASCII_NAME, email_pv,
					 ASCII_NAME, description_pv]

		# regular expressions
		fn_regex = r'''^[-.a-zA-Z']*?,?\s(?:[-a-zA-Z']*\.?\s)*?[-a-zA-Z']*\.?$'''
		ds_regex = r'''^(?:[A-Z][a-zA-Z]*\.?,?\s)?(?:[0-3][0-9]\s)?[A-Z][a-zA-Z]*\.?,?\s(?:[0-3][0-9]\.?,?\s)?[0-9]*$'''
		fa_regex = r'''^\d*\s(?:[NSEW]\.\s?|[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?\s)?[a-zA-Z'-]*\s[a-zA-Z][a-z]*?\.?\s(?:(?:[a-zA-Z][a-z]*\.?|[Pp][Oo]\.?\s?[Bb][Oo][Xx])(?:\s\d*[a-zA-Z]?))?,?\s(?:[a-zA-Z'-]*\s)*?[a-zA-Z'-]*,?\s[a-zA-Z]*,?\s(?:\d{5}|\d{5}(?:\s|[.-])?\d{4})(?:,?\s[A-Za-z'-]*)*$'''
		sa_regex = r'''^\d*\s(?:[NSEW]\.\s?|[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?\s)?[a-zA-Z'-]*\s[a-zA-Z][a-z]*?\.?\s(?:(?:[a-zA-Z][a-z]*\.?|[Pp][Oo]\.?\s?[Bb][Oo][Xx])(?:\s\d*[a-zA-Z]?))?$'''
		cs_regex = r'''^(?:[a-zA-Z'-]*\s)*?[a-zA-Z'-]*,?\s[a-zA-Z]*$'''
		em_regex = r'''^\S*?@\S*?(?:\.\S*?)+$'''
		lo_regex = r'''^(?:[A-Z][a-z'-]*\s)*?(?:[A-Z][a-z'-]*)$'''
		de_regex = r'''^(?:["'<-]?[A-Za-z'-]+[>"',;:-]?(?:\s|[.?!]\s*))+$'''
		regex = [fn_regex, NAME_REGEX, NAME_REGEX, ds_regex,
				fa_regex, sa_regex, cs_regex, em_regex,
				lo_regex, de_regex]

		# known examples
		full_name_ex = COMMON_FIRST_NAMES + COMMON_LAST_NAMES
		city_state_ex = []
		email_ex = []
		location_ex = []
		description_ex = []
		known_examples = [full_name_ex, COMMON_FIRST_NAMES, COMMON_LAST_NAMES, COMMON_DATE_NAMES,
						  COMMON_ADDRESS_NAMES, COMMON_ADDRESS_NAMES, city_state_ex, email_ex,
						  location_ex, description_ex]

		# common features
		full_name_cf = COMMON_PREFIXES + COMMON_SUFFIXES
		city_state_cf = []
		email_cf = []
		location_cf = []
		description_cf = []
		common_features = [full_name_cf, COMMON_PREFIXES, COMMON_SUFFIXES, COMMON_DATE_ABBREV,
						   COMMON_ADDRESS_FEATURES, COMMON_ADDRESS_FEATURES, city_state_cf, email_cf,
						   location_cf, description_cf]

		for i in len(names):
			curr = classifier(names[i],
							  possible_values[i],
							  regex[i],
							  known_examples[i],
							  common_features[i])
			self.classifiers.append(curr)