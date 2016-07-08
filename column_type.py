import mysql.connector, os
execfile("features/features.py")

#The code that is commented out is the old heurisitc way that I evaluated things
#There is new code before it that examines form types rather than using heuristics
#the heuristics might be a better way to go but they were pretty bad

#The form strings I used replace all letters with X or x depending on case and all numbers with 0

#The condensed form strings take out word lengths by reducing any sequence of x's to x and
#take out number lengths by reducing any sequence of 0's to 0

#Unicode characters are still a problem that I am working on fixing...

NAME_LENGTH = 7
NUM_SPACES = 1.5
ASCII_NUMS = [n for n in range(48, 58)]
ASCII_UPPER = [n for n in range(65, 91)]
ASCII_LOWER = [n for n in range(97, 123)]
NAME_FEATURES = COMMON_PREFIXES + COMMON_SUFFIXES


class column_typer:
	def __init__(self, col):
		self.reset(col)
		self.build_classifiers()

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

		return (tipe, prob, lst of examples)
		return ret

	def full_name_heuristic(self, token):
		'''returns a  name heuristic value or negative infinity
		if it definitely isn't a name'''
		# check if it can't be a name
		value = 0
		char_val_list = []
		for char in token:
			char_val_list.append(ord(char))
		if not self.column_classifiers[0].can_be(char_val_list):
			return value

		# check column name
		if 'name' in self.column_name.lower():
			value += 10

		# counting common features of names
		if self.column_classifiers[0].contains_a(token.lower()):
			value += 1

		# account for name length
		temp = token.split()
		lengths = [len(x) for x in temp]
		if len(lengths) == 0:
			return 0
		avg_len = float(sum(lengths)) / float(len(lengths))
		value += NAME_LENGTH - abs(avg_len - NAME_LENGTH)

		# looking at format of individual words
		for word in temp:
			# check for common names
			#TODO: Need to change because it will flag all single names as full names
			if self.column_classifiers[0].is_a(word.lower()):
				return value += 100
			word_form = condense(make_form(word))
			if word_form == 'Xx':
				value += 2
			if word_form.strip('.') == 'X':
				value += 1
		
		# account for number of spaces
		spaces = len(temp) - 1
		value += NUM_SPACES - abs(spaces - NUM_SPACES)
		
		return value

	def first_name_heuristic(self, token):
		'''returns a  first name heuristic value or negative infinity
		if it definitely isn't a name'''
		#TODO edit to be more relevant to first names

		# check if it can't be a name
		value = 0
		char_val_list = []
		for char in token:
			char_val_list.append(ord(char))
		if not self.column_classifiers[1].can_be(char_val_list):
			return value

		# check column name
		if 'first' in self.column_name.lower():
			value += 10
		if 'name' in self.column_name.lower():
			value += 10

		# counting common features of names
		if self.column_classifiers[1].contains_a(token.lower()):
			value += 1

		# account for name length
		temp = token.split()
		lengths = [len(x) for x in temp]
		if len(lengths) == 0:
			return 0
		if len(lengths) == 1:
			value += 10

		# check for common names
		#TODO: Need to change because it will flag all single names as full names
		if self.column_classifiers[1].is_a(token.lower()):
			return 100
		word_form = condense(make_form(token))
		if word_form == 'Xx':
			value += 2
		if word_form.strip('.') == 'X':
			value += 1
	
		return value

	def last_name_heuristic(self, token):
		'''returns a last name heuristic value or negative infinity
		if it definitely isn't a name'''
		#TODO edit to be more relevant to last names

		# check if it can't be a name
		value = 0
		char_val_list = []
		for char in token:
			char_val_list.append(ord(char))
		if not self.column_classifiers[2].can_be(char_val_list):
			return value

		# check column name
		if 'last' in self.column_name.lower():
			value += 10
		if 'sur' in self.column_name.lower():
			value += 10
		if 'name' in self.column_name.lower():
			value += 10

		# counting common features of names
		for self.column_classifiers[2].contains_a(token.lower()):
			value += 1

		# account for name length
		temp = token.split()
		lengths = [len(x) for x in temp]
		if len(lengths) == 0:
			return 0
		if len(lengths) == 1:
			value += 10

		# check for common names
		#TODO: Need to change because it will flag all single names as full names
		if self.column_classifiers[2].is_a(token.lower()):
			return 100
		word_form = condense(make_form(token))
		if word_form == 'Xx':
			value += 2
		if word_form.strip('.') == 'X':
			value += 1
	
		return value

	def datestring_heuristic(self, token):
		'''returns a certainty value for token being a date string
		or zero if it definitely isn't a date string'''
		value = 0
		char_val_list = []
		for char in token:
			char_val_list.append(ord(char))
		if not self.column_classifiers[3].can_be(char_val_list):
			return value

		# check column name
		if 'date' in self.column_name.lower():
			value += 10

		# counting common features of date strings
		for self.column_classifiers[3].contains_a(token.lower()):
			value += 1

		# account for name length
		temp = token.split()
		if len(temp) == 3:
			value += 10
		
		numStrings = 0
		numNums = 0
		for word in temp:
			word_form = condense(make_form(word))
			if '0' in word_form:
				numNums += 1
			elif 'X' in word_form or 'x' in word_form:
				numStrings += 1
		numPair = (numStrings, numNums)
		if numPair == (2,1) or numPair == (2,2) or numPair (1,1):
			value += 5

		form = condense(make_form(token))
		if self.column_classifiers[3].has_form(form):
			value += 10

		for word in temp:
			if self.column_classifiers[3].is_a(word):
				value += 20


		return value

	def address_heuristic(self, token):
		'''returns a certainty value for token being an address
		or zero if it definitely isn't an address'''

	def email_heuristic(self, token):
		'''returns a certainty value for token being an email
		or zero if it definitely isn't an email'''

	def date_heuristic(self, char_dict, length, token):
		'''returns a really crappy date heuristic value that probably doesn't work or False
		if it definitely isn't a date'''
		
		# this calls Will's thing
		# need to figure out how to merge/use both files

		return 0

	def time_heuristic(self, char_dict, length, token):
		'''returns a really crappy time heuristic value that probably doesn't work or False
		if it definitely isn't a time'''
		
		# same as date

		return 0

	def build_classifiers(self):
		'''builds the self.column_classifiers data member by creating classifier objects created 
		by classifier(name of the type, possible ascii values in the type string, list of the known condensed forms)'''
		self.column_classifiers = []

		# names ------------------------------------------------
		legal_symbols = [32, 44, 45, 46]
		legal_ascii = legal_symbols + ASCII_UPPER + ASCII_LOWER
		possible forms = ['Xx', 'Xx Xx', 'Xx X Xx', 'Xx X. Xx', 'Xx x Xx', 'Xx x. Xx', 'Xx, Xx', 'Xx, Xx X', 'Xx, Xx X.', 'Xx, Xx x.', 'Xx, Xx x', 'X Xx', 'X. Xx', 'Xx, X', 'Xx, X.']
		known_examples = COMMON_FIRST_NAMES + COMMON_LAST_NAMES
		common_features = COMMON_PREFIXES + COMMON_SUFFIXES
		self.column_classifiers.append(classifier('full names', legal_ascii, possible_forms, known_examples, common_features))

		# first names ------------------------------------------
		legal_symbols = [32, 44, 45, 46]
		legal_ascii = legal_symbols + ASCII_UPPER + ASCII_LOWER
		possible forms = ['Xx', 'X Xx', 'X. Xx']
		known_examples = COMMON_FIRST_NAMES
		self.column_classifiers.append(classifier('first names', legal_ascii, possible_forms, known_examples, COMMON_PREFIXES))

		# last names ------------------------------------------
		legal_symbols = [32, 44, 45, 46]
		legal_ascii = legal_symbols + ASCII_UPPER + ASCII_LOWER
		possible forms = ['Xx', 'X Xx', 'X. Xx']
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
		possible forms = ['x 0', 'Xx 0', '0 x', '0 Xx', 'x. 0', 'Xx. 0', '0 x.', '0 Xx.'] + types_without_dow + types_with_dow
		known_examples = COMMON_DATE_NAMES
		self.column_classifiers.append(classifier('datestrings', legal_ascii, possible_forms, known_examples, COMMON_DATE_ABBREV))

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

		self.column_classifiers.append(classifier('addresses', [32, 39, 44, 45, 46] + ASCII_NUMS + [58, 59] + ASCII_UPPER + ASCII_LOWER, address_types, []))

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

def dict_max(Adict):
	'''returns the key with the largest value in a dictionary'''
	max_val = float("-inf")
	max_key = ''
	for key in Adict.keys():
		if Adict[key] > max_val:
			max_val = Adict[key]
			max_key = key

	return max_key

def key_sum(Adict):
	'''returns the sum of the values of the keys in a dictionary'''
	total = 0
	vals = Adict.values()
	for num in vals:
		total += num
	return total

def make_form(inString):
	'''Turns the input string into a string that represents the general form of the string'''
	returnString = ''
	for char in inString:
		if (ord(char) <= 57 and ord(char) >= 48):
			returnString += '0'
		elif (ord(char) <= 90 and ord(char) >= 65):
			returnString += 'X'
		elif (ord(char) >= 97 and ord(char) <= 122):
			returnString += 'x'
		else:
			returnString += char
	return returnString

def condense(inString):
	'''Turns the input form string into a standardized form string with word and number lengths removed'''
	condString = ''
	index = 0
	while index < len(inString):
		condString += inString[index]
		if inString[index] == 'x':
			while (index < len(inString) and inString[index] == 'x'):
				index += 1
			continue
		if inString[index] == '0':
			while (index < len(inString) and inString[index] == '0'):
				index += 1
			continue
		index += 1

	return condString

def normalize(val, maxVal):
	'''Normalizes the input value over a 0-1 scale'''
	return float(val)/float(maxVal)
	#TODO: Make it quadratic or logarithmic or something to make it work better

class classifier:
	'''this class is a class used only in the column_classifiers data member in order to structure the types better.
	The class contains:
		1. A name of the type (Ex: 'names')
		2. A list of possible ascii values that can be contained in the type (Ex: names can contain lower_case_letters
			97-122 but cannot contain '=' 61)
		3. A list of the known forms that this particular types comes in. (Ex: names can be written as 'Xx Xx' or 'Xx' or 'Xx X. Xx' etc) 
			I wrote in many known forms but there are plenty that I missed'''
	def __init__(self, n, pv, kf, ke, cf):
		#TODO make all the lists into dictionaries (for time complexity purposes)
		self.name = n
		self.possVals = pv
		self.knownForms = kf
		self.knownExamples = {}
		for elem in ke:
			self.knownExamples[elem] = 1
		self.commonFeatures = cf

	def can_be(self, vals):
		'''Tests whether the sequence of ascii values inputted has any that are not allowed in this particular type'''
		for elem in vals:
			if elem not in self.possVals:
				return False
		return True

	def has_form(self, form):
		'''Tests whether the given condensed form is in the known forms of this particular type'''
		return form in self.knownForms

	def is_a(self, inString):
		'''Tests whether the given string is stored in the list of known string examples of the particular types'''
		return inString in self.knownExamples

	def contains_a(self, inString):
		'''Tests whether the given string contains a common feature of the particular type'''
		for f in self.commonFeatures:
			if f in inString:
				return True
		return False

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