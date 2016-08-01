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

ASCII_NUMS = [n for n in range(48, 58)]
ASCII_UPPER = [n for n in range(65, 91)]
ASCII_LOWER = [n for n in range(97, 123)]
ASCII_PRINTABLE = [n for n in range(32, 128)]
ASCII_ADDRESS = [32, 39, 44, 45, 46] + ASCII_NUMS + [58, 59] + ASCII_UPPER + ASCII_LOWER
ASCII_NAME = [32, 44, 45, 46] + ASCII_UPPER + ASCII_LOWER

class main_classifier:
	def __init__(self, table):
		self.build_classifiers()
		self.num_class = numeric_classifier()
		self.heu_class = heuristic_classifier()

		# the data that is used by the classifier
		self.my_table     = None
		self.results      = None
		self.result_table = None
		self.report       = None

	def new_table(table):
		'''takes in a new table and generates the data for it'''
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
		dict = column.guesses
		error_list = []
		for i in range(len(dict)):
			if dict[i]!=think:
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
			# TODO add tentative classifications
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
		dyct = {}
		predictions = []
		i = 0
		for item in column:
			guess = self.token_typify(item)
			dyct[i]= guess
			i = i+1
			predictions.append(guess)
			#print dyct
		return predictions, dyct

	def token_typify(self, token):
		'''takes in a token and returns a
		prediction for its type'''
		# TODO add naice bayes
		if no_letters(token):
			tipe, probability_dictionary, mean, std_dev = self.numClass.classify(token)
			#print tipe
			return tipe
		certainties = {}
		for f in heuristics:
			tipe, value = f(token, self)
			certainties[tipe] = value
		prediction = dict_max(certainties)
		return prediction

	def build_heuristic_classifiers(self):
		'''builds the self.column_classifiers data member by creating classifier objects created
		by classifier(name of the type, possible ascii values in the type string, list of the known condensed forms)'''
		# TODO complete classifiers
		self.heuristic_classifiers = []

		# names
		names = ['full name', 'first name', 'last name', 'datestring',
				'full address', 'street address', 'city state', 'email',
				'location', 'description', 'url', 'city', 'state']

		# possible values
		datestring_pv = [32, 44, 46] + ASCII_NUMS + ASCII_UPPER + ASCII_LOWER
		email_pv = [43, 45, 46, 64, 95] + ASCII_NUMS + ASCII_UPPER + ASCII_LOWER
		description_pv = ASCII_PRINTABLE
		url_punc = [33, 58, 59, 61, 63, 91, 93, 95, 126] + [x for x in range(35, 48)]
		url_pv = ASCII_LOWER + ASCII_UPPER + ASCII_NUMS + url_punc
		possible_values = [ASCII_NAME, ASCII_NAME, ASCII_NAME, datestring_pv,
					 ASCII_ADDRESS, ASCII_ADDRESS, ASCII_NAME, email_pv,
					 ASCII_NAME, description_pv, url_pv, ASCII_NAME, ASCII_NAME]
		# TODO better city and state pv

		# regular expressions
		fn_regex = r'''^[-.a-zA-Z']*?,?\s(?:[-a-zA-Z']*\.?\s)*?[-a-zA-Z']*\.?$'''
		na_regex = r'''^[A-Z][a-z'-]*$'''
		ds_regex = r'''^(?:[A-Z][a-zA-Z]*\.?,?\s)?(?:[0-3][0-9]\s)?[A-Z][a-zA-Z]*\.?,?\s(?:[0-3][0-9]\.?,?\s)?[0-9]*$'''
		fa_regex = r'''^(?:[Oo][Nn][Ee]|[0-9-]*[a-zA-Z]?)\s+(?:[NSEW]\.?[NSEW]?\.?\s+|(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+)?(?:\d*(?:[SNRTsnrt][TDHtdh])?(?:\s+[a-zA-Z'-]*)?|(?:[a-zA-Z'-]*\s+)*?(?:[a-zA-Z'-]*))\.?(?:\s+\d*)?,?(?:\s+[NSEW]\.?[NESW]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])?)?(?:\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|\s+(?:[a-zA-Z][a-z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?(?:\s+(?:[#]\s*)?\w*(?:[-/: ]\w*)?))?,?\s(?:[a-zA-Z'-]*\s)*?[a-zA-Z'-]*,?\s[a-zA-Z]*,?\s(?:\d{5}|\d{5}(?:\s|[.-])?\d{4})(?:,?\s[A-Za-z'-]*)*$'''
		sa_regex = r'''^(?:[Oo][Nn][Ee]|[0-9-]*[a-zA-Z]?)\s+(?:[NSEW]\.?[NSEW]?\.?\s+|(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+)?(?:\d*(?:[SNRTsnrt][TDHtdh])?(?:\s+[a-zA-Z'-]*)?|(?:[a-zA-Z'-]*\s+)*?(?:[a-zA-Z'-]*))\.?(?:\s+\d*)?,?(?:\s+[NSEW]\.?[NESW]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])?)?(?:\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|\s+(?:[a-zA-Z][a-z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?(?:\s+(?:[#]\s*)?\w*(?:[-/: ]\w*)?))?$'''
		cs_regex = r'''^(?:[a-zA-Z'-]*\s)*?[a-zA-Z'-]*,?\s[a-zA-Z]*$'''
		em_regex = r'''^\S*?@\S*?(?:\.\S*?)+$'''
		lo_regex = r'''^(?:[A-Z][a-z'-]*\s)*?(?:[A-Z][a-z'-]*)$'''
		de_regex = r'''^(?:["'<-]?[A-Za-z0-9'-]+[>"',;:-]?(?:\s|[.?!]\s+))+$'''
		ur_regex = r'''^\S*?.\S*'''
		regex = [fn_regex, na_regex, na_regex, ds_regex,
				fa_regex, sa_regex, cs_regex, em_regex,
				lo_regex, de_regex, ur_regex, na_regex, na_regex]
		# TODO better regex for city and state


		# known examples
		full_name_ex      = COMMON_PREFIXES + COMMON_SUFFIXES + COMMON_FIRST_NAMES + COMMON_LAST_NAMES
		first_name_ex     = COMMON_PREFIXES + COMMON_FIRST_NAMES
		last_name_ex      = COMMON_SUFFIXES + COMMON_LAST_NAMES
		datestring_ex     = COMMON_DATE_NAMES + COMMON_DATE_ABBREV
		full_address_ex   = COMMON_ADDRESS_NAMES + COMMON_ADDRESS_FEATURES + COMMON_STATEPROV_ABBREV + COMMON_CITIES
		street_address_ex = COMMON_ADDRESS_NAMES + COMMON_ADDRESS_FEATURES
		city_state_ex     = COMMON_STATEPROV_ABBREV + COMMON_CITIES
		email_ex          = COMMON_URL_EXTENSIONS + COMMON_EMAIL_DOMAINS
		location_ex       = COMMON_CITIES + COMMON_LOCATION_FEATURES
		description_ex    = COMMON_ADJECTIVES
		url_ex            = COMMON_URL_EXTENSIONS + COMMON_URL
		city_ex           = COMMON_CITIES
		state_ex          = COMMON_STATES
		known_examples = [full_name_ex, first_name_ex, last_name_ex, datestring_ex,
						  full_address_ex, street_address_ex, city_state_ex, email_ex,
						  location_ex, description_ex, url_ex, city_ex, state_ex]

		for i in range(len(names)):
			curr = classifier(names[i],
							  possible_values[i],
							  regex[i],
							  known_examples[i])
			self.heuristic_classifiers.append(curr)
