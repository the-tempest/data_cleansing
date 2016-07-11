import mysql.connector, os, re
execfile("heuristics.py")
execfile("helper.py")
execfile("features/features.py")
execfile("classifier.py")

#The code that is commented out is the old heurisitc way that I evaluated things
#There is new code before it that examines form types rather than using heuristics
#the heuristics might be a better way to go but they were pretty bad

#The form strings I used replace all letters with X or x depending on case and all numbers with 0

#The condensed form strings take out word lengths by reducing any sequence of x's to x and
#take out number lengths by reducing any sequence of 0's to 0

#TODO: unicode support

ASCII_NUMS = [n for n in range(48, 58)]
ASCII_UPPER = [n for n in range(65, 91)]
ASCII_LOWER = [n for n in range(97, 123)]

class column_typer:
	#TODO make it loop over a table instead of just one column at a time
	def __init__(self, col):
		self.reset(col)
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
		'''takes in a table and returns a
		tuple'''
		actual = []
		predictions = []
		fractions = []
		for elem in table.getColumns():
			column = elem.rows
			guesses = column_typify(column)
			prediction, fraction = column_predict(guesses)
			actual.append(col.colName)
			predictions.append(prediction)
			fractions.append(fraction)
		results = []
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
		for item in guesses:
			if item not in results:
				results[item] = 0
			results[item] += 1
		size = len(guesses)
		for key in results:
			fraction = float(results[key]) / float(size)
			fraction = "{0:.2f}".format(fraction) 
			results[key] = fraction
		best_guess = dict_max(results)
		guess_fraction = results[best_guess]
		if best_guess < .5:
			return 'misc', None
		return best_guess, guess_fraction

	def column_typify(self, column):
		'''takes in a column and
		returns a list of classifications'''
		predictions = []
		for item in column:
			guess = token_typify(item)
			predictions.append(guess)
		return predictions

	def token_typify(self, token):
		'''takes in a token and returns a
		predictive classification'''
		certainties = {}
		for f in heuristics:
			tipe, value = f(token)
			certainties[tipe] = value
		prediction = dict_max(certainties)
		return prediction

	def build_classifiers(self):
		'''builds the self.column_classifiers data member by creating classifier objects created 
		by classifier(name of the type, possible ascii values in the type string, list of the known condensed forms)'''
		# TODO put in regular expressions to phase out forms
		# TODO add rest of classifiers
		self.column_classifiers = []

		# full names ------------------------------------------------
		legal_symbols = [32, 44, 45, 46]
		legal_ascii = legal_symbols + ASCII_UPPER + ASCII_LOWER
		possible_forms = ['Xx', 'Xx Xx', 'Xx X Xx', 'Xx X. Xx', 'Xx x Xx', 'Xx x. Xx', 'Xx, Xx', 'Xx, Xx X', 'Xx, Xx X.', 'Xx, Xx x.', 'Xx, Xx x', 'X Xx', 'X. Xx', 'Xx, X', 'Xx, X.']
		known_examples = COMMON_FIRST_NAMES + COMMON_LAST_NAMES
		common_features = COMMON_PREFIXES + COMMON_SUFFIXES
		self.column_classifiers.append(classifier('full names', legal_ascii, possible_forms, known_examples, common_features))

		# first names ------------------------------------------
		legal_symbols = [32, 44, 45, 46]
		legal_ascii = legal_symbols + ASCII_UPPER + ASCII_LOWER
		possible_forms = ['Xx', 'X Xx', 'X. Xx']
		known_examples = COMMON_FIRST_NAMES
		self.column_classifiers.append(classifier('first names', legal_ascii, possible_forms, known_examples, COMMON_PREFIXES))

		# last names ------------------------------------------
		legal_symbols = [32, 44, 45, 46]
		legal_ascii = legal_symbols + ASCII_UPPER + ASCII_LOWER
		possible_forms = ['Xx', 'X Xx', 'X. Xx']
		known_examples = COMMON_LAST_NAMES
		self.column_classifiers.append(classifier('last names', legal_ascii, possible_forms, known_examples, COMMON_SUFFIXES))

		# datestrings ------------------------------------------------
		types_without_dow = ['Xx 0, 0', '0 Xx 0', 'Xx. 0, 0', '0 Xx. 0', 'x 0, 0', '0 x 0', 'x. 0, 0', '0 x. 0']
		types_with_dow = []
		for elem in types_without_dow:
			types_with_dow.append('x ' + elem)
			types_with_dow.append('Xx ' + elem)
			types_with_dow.append('Xx. ' + elem)
			types_with_dow.append('x. ' + elem)
			types_with_dow.append('Xx, ' + elem)
			types_with_dow.append('x, ' + elem)
			types_with_dow.append('Xx., ' + elem)
			types_with_dow.append('x., ' + elem)

		legal_symbols = [32, 44, 46]
		legal_ascii = legal_symbols + ASCII_NUMS + ASCII_UPPER + ASCII_LOWER
		possible_forms = ['x 0', 'Xx 0', '0 x', '0 Xx', 'x. 0', 'Xx. 0', '0 x.', '0 Xx.'] + types_without_dow + types_with_dow
		self.column_classifiers.append(classifier('datestrings', legal_ascii, possible_forms, COMMON_DATE_NAMES, COMMON_DATE_ABBREV))

		# full addresses ---------------------------------
		address_types = ['0 Xx Xx.', '0 Xx x.', '0 Xx x', '0 Xx Xx', '0 X Xx Xx.', '0 X Xx x.', '0 X Xx x', '0 X Xx Xx', '0 X. Xx Xx.', '0 X. Xx x.', '0 X. Xx x', '0 X. Xx Xx']
		for x in range(len(address_types)):
			address_types.append(address_types[x] + ', Xx. 0')
			address_types.append(address_types[x] + ', Xx 0')
			address_types.append(address_types[x] + ', x. 0')
			address_types.append(address_types[x] + ', x 0')
			address_types.append(address_types[x] + ' Xx. 0')
			address_types.append(address_types[x] + ' Xx 0')
			address_types.append(address_types[x] + ' x. 0')
			address_types.append(address_types[x] + ' x 0')

		for x in range(len(address_types)):
			address_types.append(address_types[x] + ', Xx, XX 0')
			address_types.append(address_types[x] + ', Xx Xx, XX 0')
			address_types.append(address_types[x] + ' Xx, XX 0')
			address_types.append(address_types[x] + ' Xx Xx, XX 0')

		legal_symbols = [32, 39, 44, 45, 46] + ASCII_NUMS + [58, 59] + ASCII_UPPER + ASCII_LOWER
		self.column_classifiers.append(classifier('addresses', legal_symbols, address_types, COMMON_ADDRESS_NAMES, COMMON_ADDRESS_FEATURES))


		# street addresses

		# city state

		# email --------------------------------------

		# location

		# descriptions

	def reset(self, col):
		'''resets the dictionaries and other data members so that a different set of data can be run'''
		self.column_list = col.rows
		self.column_name = col.colName
		self.prev_column_list = col.prev
		self.next_column_list = col.next
		self.column_type_dict = {'full names': 0,'first names': 0,'last names':0, 'datestrings':0, 'dates': 0,'times': 0,'datetimes': 0, 'addresses': 0, 'numbers': 0, 'zipnumbers': 0, 'misc': 0}
		self.column_length = len(self.column_list)
		self.line_form_dict = {}
		self.cond_column_form = ''