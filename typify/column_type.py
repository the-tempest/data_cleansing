# column_type.py
# this defines a column_typer class which
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
execfile(path+"error_detection.py")


#TODO: figure out what to do with unicode

ASCII_NUMS = [n for n in range(48, 58)]
ASCII_UPPER = [n for n in range(65, 91)]
ASCII_LOWER = [n for n in range(97, 123)]
ASCII_PRINTABLE = [n for n in range(32, 128)]
ASCII_ADDRESS = [32, 39, 44, 45, 46] + ASCII_NUMS + [58, 59] + ASCII_UPPER + ASCII_LOWER
ASCII_NAME = [32, 44, 45, 46] + ASCII_UPPER + ASCII_LOWER
NAME_REGEX = r'''^[A-Z][a-z'-]*$'''

class column_typer:
	def __init__(self, table):
		self.build_classifiers()
		self.my_table = table
		self.numClass = numeric_classifier()

	def build_report(self):
		ret = ''
		results = self.table_typify(self.my_table)
		possible_errors = self.find_table_errors(self.my_table)
		i = 0
		#if self.my_table.columns[0].tentClass==None:
		#	print "ERROR"
		print self.my_table.columns[0].tentClass + "1"
		for item in results:
			line = self.build_column_report(item)
			ret += line
			#adding in the misclassified token list
	#		ret +=self.build_column_misclassificationtest_report(self.my_table.columns[i])
			i = i +1
		return ret

	def build_column_report(self,column_tuple):
		# TODO perhaps make this more abstracted
		'''Classifies the columns in my_table and
		returns a summary report as a string'''

		#print results
		
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


	def build_column_misclassification_report(self, column):
		list = self.misclassified(column)
		line = ""
		for i in l:
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
			
	def apply_predictions(self, table):
		''' takes in a table and returns a table
		with the tentative classifications filled in'''
		tuples = table_typify(table)
		for i, col in enumerate(table.getColumns()):
			prediction = tuples[i][1]
			col.tentativeClassification(prediction)
		return table


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
			self.curr_col_name = elem.colName
			guesses = self.column_typify(column)
			dict = guesses[1]
			guesses = guesses[0]
			#print "real guesses"
			#print guesses
			elem.addDict(self.generate_dict(guesses)) #this calls a function of column and adds a dictionary to one of its elements
			#print "guesses after dict function call"
			#print guesses
			prediction, fraction = self.column_predict(guesses, column)
			elem.addGuesses(dict)
			# values to go into the tuple
			actual.append(elem.colName)
			predictions.append(prediction)
			fractions.append(fraction)
		results = []
		# construct tuples
		for i in range(len(table.getColumns())):
			a = actual[i]
			p = predictions[i]
			f = fractions[i]
			if p == 'misc':
				print "got here"
				predictions[i] = self.differentiate(i,predictions)
				p = predictions[i]
			table.getColumns()[i].tentativeClassification(p)
			t = (a, p, f)
			print t
			results.append(t)
		return results


	def column_predict(self, guesses, column):
		'''takes in a list of predictions for
		a column and returns a tuple of the form
		(prediction, certainty)'''
		results = {}
		# populate the dictionary

		for item in guesses:
			#print "this is item    "
			#print item
			#if (not isinstance(item,tuple)): # same problem as in generate dict below
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
		if repetition_heuristic(column, best_guess) == 100:
			return best_guess, 1.00
		# ensure there actually is a good guess
		print guess_fraction
		if float (guess_fraction) < float(.9):
			print	"here"
			return 'misc', guess_fraction # this function is broken
			# because for some guesses, all of the elements are tuples and best_guess
			# is thus empty, need a way to deal with tuples!
		return best_guess, guess_fraction #best_guess, guess_fraction

	def generate_dict(self, guesses):
		'''takes in a list of predictions for
		a column and returns a list of all the predictions and the
		fractions corresponding for that specific column'''
		results = {}
		# populate the dictionary
		# problem here is that Will's numeric classifier returns dictionaries
		# guesses
		for item in guesses:
			if (not isinstance(item, tuple)): # need to get rid of this eventually
				if item in results:
					results[item] += 1
				else:
					results[item] = 1
		size = len(guesses)
		for key in results.keys():
			fraction = float(results[key]) / float(size)
			fraction = "{0:.2f}".format(fraction)
			results[key] = fraction
		# ensure there actually is a good guess
		return results

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
		if no_letters(token):
			tipe, probability_dictionary, mean, std_dev = self.numClass.classify(token)
			#print tipe
			return tipe
		certainties = {}
		for f in heuristics:
			tipe, value = f(token, self)
			certainties[tipe] = value
		prediction = dict_max(certainties)
		#print "prediction"
		#print prediction
		
		#print "getting here"
		return prediction

	def differentiate(self, i, predictions):
		'''this will address the cases where the fractions are below .7'''
		#i indicates the index of the column in the table we are using
		#get best two predictions

		table = self.my_table
		elem = table.columns[i]
		dict = elem.dictionary
		best_guess = dict_max(dict)
		guess_fraction = dict[best_guess]
		del dict[best_guess]
		best_guess2 = dict_max(dict)
		guess_fraction = dict[best_guess2]
		column = elem.rows
		self.curr_col_name = elem.colName
		guesses = self.column_typify(column)
		guesses = guesses[0]
		tie_breaker1 = tie_breaker(i,guesses, best_guess, best_guess2, predictions,self)
		prediction = tie_breaker1.differ()		
		return prediction
		
		#ALSO: we can use the information from previous columns to learn about the current one
		# EX: if we already have name column, perhaps given more weight to the alternative type of a given
		#column



		# remember, you need to return a tuple of the form t = (a, p, f)

	def build_classifiers(self):
		'''builds the self.column_classifiers data member by creating classifier objects created
		by classifier(name of the type, possible ascii values in the type string, list of the known condensed forms)'''
		# TODO complete classifiers
		self.column_classifiers = []

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
		ds_regex = r'''^(?:[A-Z][a-zA-Z]*\.?,?\s)?(?:[0-3][0-9]\s)?[A-Z][a-zA-Z]*\.?,?\s(?:[0-3][0-9]\.?,?\s)?[0-9]*$'''
		fa_regex = r'''^(?:[Oo][Nn][Ee]|[0-9-]*[a-zA-Z]?)\s+(?:[NSEW]\.?[NSEW]?\.?\s+|(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+)?(?:\d*(?:[SNRTsnrt][TDHtdh])?(?:\s+[a-zA-Z'-]*)?|(?:[a-zA-Z'-]*\s+)*?(?:[a-zA-Z'-]*))\.?(?:\s+\d*)?,?(?:\s+[NSEW]\.?[NESW]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])?)?(?:\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|\s+(?:[a-zA-Z][a-z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?(?:\s+(?:[#]\s*)?\w*(?:[-/: ]\w*)?))?,?\s(?:[a-zA-Z'-]*\s)*?[a-zA-Z'-]*,?\s[a-zA-Z]*,?\s(?:\d{5}|\d{5}(?:\s|[.-])?\d{4})(?:,?\s[A-Za-z'-]*)*$'''
		sa_regex = r'''^(?:[Oo][Nn][Ee]|[0-9-]*[a-zA-Z]?)\s+(?:[NSEW]\.?[NSEW]?\.?\s+|(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+)?(?:\d*(?:[SNRTsnrt][TDHtdh])?(?:\s+[a-zA-Z'-]*)?|(?:[a-zA-Z'-]*\s+)*?(?:[a-zA-Z'-]*))\.?(?:\s+\d*)?,?(?:\s+[NSEW]\.?[NESW]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])?)?(?:\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|\s+(?:[a-zA-Z][a-z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?(?:\s+(?:[#]\s*)?\w*(?:[-/: ]\w*)?))?$'''
		cs_regex = r'''^(?:[a-zA-Z'-]*\s)*?[a-zA-Z'-]*,?\s[a-zA-Z]*$'''
		em_regex = r'''^\S*?@\S*?(?:\.\S*?)+$'''
		lo_regex = r'''^(?:[A-Z][a-z'-]*\s)*?(?:[A-Z][a-z'-]*)$'''
		de_regex = r'''^(?:["'<-]?[A-Za-z0-9'-]+[>"',;:-]?(?:\s|[.?!]\s+))+$'''
		ur_regex = r'''^\S*?.\S*'''
		regex = [fn_regex, NAME_REGEX, NAME_REGEX, ds_regex,
				fa_regex, sa_regex, cs_regex, em_regex,
				lo_regex, de_regex, ur_regex, NAME_REGEX, NAME_REGEX]
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
			self.column_classifiers.append(curr)
