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

	def table_typify(self, table):
		for col in table.getColumns():
			# TODO add functionality
			print "implement me!"

	def column_typify(self):
		for elem in self.column_list:
			#skips null values - may want to change what this does
			if elem == None:
				continue

			#The part before the long docstring that I removed deals with adding things to the column_type_dict
			#and the part after deals with finding the max of that dict and finding the forms of the data

			length = len(elem)
			form = make_form(elem)

			#filling in the form dictionary
			if self.line_form_dict.has_key(form):
				self.line_form_dict[form] += 1
			else:
				self.line_form_dict[form] = 1

			#turns the string into a list of the ascii values that make up the string
			char_val_list = []
			for char in elem:
				char_val_list.append(ord(char))

			#deals with numbers that are 5 long - sets them to be zipnumbers
			if length == 5:
				zipnum = True
				for char in elem:
					if not (ord(char) <= 57 and ord(char) >= 48):
						zipnum = False
				if zipnum:
					self.column_type_dict['zipnumbers'] += 1
					continue


			#looks for a condensed form match in all of the classifier types and if it finds it sets found to True and moves on to the next
			#value in the column
			found = False
			cond_form = condense(form)
			for x in self.column_classifiers:
				if x.has_form(cond_form):
					self.column_type_dict[x.name] += 1
					found = True
					break

			#if it isnt found in the types stored in the classifier types then find which types it can be
			#if it can only be one of the types then lets make it that type. otherwise lets make it misc because we don't know
			if not found:
				possibles = []
				for x in self.column_classifiers:
					if x.can_be(char_val_list):
						possibles.append(x.name)
				if len(possibles) == 0:
					self.column_type_dict['misc'] += 1
				if len(possibles) == 1:
					self.column_type_dict[possibles[0]] += 1
				else:
					self.column_type_dict['misc'] += 1

		ret = ''

		if self.column_type_dict['zipnumbers'] == self.column_length:
			ret += 'zipnumbers'
		else:
			ret += dict_max(self.column_type_dict)

		ret += ' with the main form of: '

		#condensed_forms is used to tally up forms with ignoring word lengths
		#This ensures that a dict with 1 'Xxxx' and 1 'Xxxxxx' and 1 'Xxx' and 2 'XXXXX'
		#still finds the main form to be 'Xx'
		condensed_forms = {}
		for key in self.line_form_dict.keys():
			cond_key = condense(key)
			if condensed_forms.has_key(cond_key):
				condensed_forms[cond_key] += 1
			else:
				condensed_forms[cond_key] = 1
		self.cond_column_form = dict_max(condensed_forms)

		#take out all the keys from the line_form_dict that don't have the same condensed form as
		#the max form (the 'right' form)
		#TODO: this code can be changed to tag different condensed forms as a way of flagging particular values as ones that need to be changed
		#for key in self.line_form_dict.keys():
		#	if condense(key) != self.cond_column_form:
		#		del self.line_form_dict[key]
		#This code doesn't do what I want so I commented it out for now

		ret += dict_max(self.line_form_dict)

		#organizing the print statement to print out all remaining forms
		ret += "\nAll forms:"
		for key in self.line_form_dict.keys():
			ret += "\n\""
			ret += key
			ret += "\""

		#return (tipe, prob, lst of examples)
		return ret

	def token_typify(self, token):
		#TODO implement this fully
		# this takes in a token (from a column) and 
		# returns a classification
		print "implement me!"

	def build_classifiers(self):
		'''builds the self.column_classifiers data member by creating classifier objects created 
		by classifier(name of the type, possible ascii values in the type string, list of the known condensed forms)'''
		# TODO put in regular expressions to phase out forms
		self.column_classifiers = []

		# names ------------------------------------------------
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

		# addresses ---------------------------------
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

		# email --------------------------------------

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

#NAMES
regex = re.compile(r'[a-zA-Z'-]*,? (?:[a-zA-Z'-]*)* [a-zA-Z'-]*')

#FIRST NAMES
regex = re.compile(r'[A-Z][a-z'-]*')

#LAST NAMES
regex = re.compile(r'[A-Z][a-zA-Z'-]*')

#DATESTRINGS
regex = re.compile(r'^(?:[A-Z][a-zA-Z]*\.?,?\s)?(?:[0-3][0-9]\s)?[A-Z][a-zA-Z]*\.?,?\s(?:[0-3][0-9]\.?,?\s)?[0-9]*$')

#FULL_ADDRESSES
regex = re.compile(r'^\d*\s(?:[NSEW]\.?|[a-zA-Z][a-z]{3,4})?\s[a-zA-Z'-]*\s[a-zA-Z][a-z]*?\.?,?\s[a-zA-Z]*?,?\s(?:\d{5}|\d{5}[\s.-]?\d{4})$')


"""
for item in elem.split():

	if (character_type_dictionary['colons'] + character_type_dictionary['letters'] + character_type_dictionary['slashes'] + character_type_dictionary['misc']) == 0:
		if (length == 5 and character_type_dictionary['delimiters'] == 0):
			word_type_dictionary['zipnumbers'] += 1
		else:
			word_type_dictionary['numbers'] += 1
	else:
		word_type = ''
		max_val = float("-inf")
		temp_val = self.name_heuristic(character_type_dictionary, length, item)
		if temp_val != False:
			if temp_val > max_val:
				word_type = 'names'
				max_val = temp_val

		temp_val = self.date_heuristic(character_type_dictionary, length, item)
		if temp_val != False:
			if temp_val > max_val:
				word_type = 'dates'
				max_val = temp_val

		temp_val = self.time_heuristic(character_type_dictionary, length, item)
		if temp_val != False:
			if temp_val > max_val:
				word_type = 'times'
				max_val = temp_val

		if word_type == '':
			word_type_dictionary['misc'] += 1
		else:
			word_type_dictionary[word_type] += 1
"""