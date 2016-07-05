import mysql.connector, os

#The code that is commented out is the old heurisitc way that I evaluated things
#There is new code before it that examines form types rather than using heuristics
#the heuristics might be a better way to go but they were pretty bad

#The form strings I used replace all letters with X or x depending on case and all numbers with 0

#The condensed form strings take out word lengths by reducing any sequence of x's to x and
#take out number lengths by reducing any sequence of 0's to 0

#Unicode characters are still a problem that I am working on fixing...

class column_typer:
	def __init__(self, column_list):
		self.reset(column_list)

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
				if x.is_a(cond_form):
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


			
			"""word_type_dictionary = {'names': 0, 'dates': 0, 'times': 0, 'zipnumbers': 0, 'numbers': 0, 'misc': 0}
			for item in elem.split():


				character_type_dictionary = {'colons': 0, 'letters': 0, 'numbers': 0, 'slashes':0, 'delimiters':0, 'misc':0}
				length = len(item)
				tempString = item
				for character in item:
					if (ord(character) <= 57 and ord(character) >= 48): # is an ascii number
						character_type_dictionary['numbers'] += 1
					elif (ord(character) == 46 or ord(character) == 44): # is a , or a .
						character_type_dictionary['delimiters'] += 1
					elif ((ord(character) <= 90 and ord(character) >= 65) or ((ord(character) >= 97) and ord(character) <= 122)): #is a letter
						character_type_dictionary['letters'] += 1
					elif (ord(character) == 58 or ord(character) == 59):
						character_type_dictionary['colons'] += 1
					elif (ord(character) == 47 or ord(character) == 92 or ord(character) == 45):
						character_type_dictionary['slashes'] += 1
					else:
						character_type_dictionary['misc'] += 1

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

			for key in word_type_dictionary.keys():
				if word_type_dictionary[key] == 0:
					del word_type_dictionary[key]

			if len(word_type_dictionary.keys()) == 1:
				self.column_type_dict[word_type_dictionary.keys()[0]] += 1
			else:
				wordNum = key_sum(word_type_dictionary)
				if (wordNum == 2):
					elif word_type_dictionary.keys() == ['dates','times']:
						self.column_type_dict['datetimes'] += 1
					elif word_type_dictionary.keys() == ['names','numbers']:
						self.column_type_dict['datestrings'] += 1
					else:
						self.column_type_dict['misc'] += 1
				elif (wordNum == 3):
					if ('dates' in word_type_dictionary.keys() or 'times' in word_type_dictionary.keys() or 'misc' in word_type_dictionary.keys()):
						self.column_type_dict['misc'] += 1
					else:
						words = 0
						if 'names' in word_type_dictionary.keys():
							words += word_type_dictionary['names']

						numbers = 0
						if 'zipnumbers' in word_type_dictionary.keys():
							words += word_type_dictionary['zipnumbers']
						if 'numbers' in word_type_dictionary.keys():
							words += word_type_dictionary['numbers']

						if word_type_dictionary.keys() == ['zipnumbers','numbers']:
							self.column_type_dict['numbers'] += 1
						elif (words == 1 and numbers == 2):
							self.column_type_dict['datestrings'] += 1
						elif (words == 2 and numbers == 1):
							self.column_type_dict['addresses'] += 1
						else:
							self.column_type_dict['misc'] += 1
				else:
					if ('dates' in word_type_dictionary.keys() or 'times' in word_type_dictionary.keys() or 'misc' in word_type_dictionary.keys()):
						self.column_type_dict['misc'] += 1
					else:
						words = 0
						if 'names' in word_type_dictionary.keys():
							words += word_type_dictionary['names']

						numbers = 0
						if 'zipnumbers' in word_type_dictionary.keys():
							words += word_type_dictionary['zipnumbers']
						if 'numbers' in word_type_dictionary.keys():
							words += word_type_dictionary['numbers']

						if (words > 0 and numbers > 0):
							self.column_type_dict['addresses'] += 1
						else:
							self.column_type_dict['misc'] += 1"""

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

		return ret

	def name_heuristic(self, char_dict, length, token):
		'''returns a really crappy name heuristic value that probably doesn't work or False
		if it definitely isn't a name'''
		value = 0
		if (char_dict['colons'] + char_dict['numbers']) > 0:
			return False
		value +=  7- abs(length - 7)
		return value

	def date_heuristic(self, char_dict, length, token):
		'''returns a really crappy date heuristic value that probably doesn't work or False
		if it definitely isn't a date'''
		value = 0
		if (char_dict['colons'] + char_dict['letters']) > 0:
			return False
		value += 10 * (2 - abs(char_dict['slashes'] - 2))
		value += 4 * (5 - abs(char_dict['numbers'] - 5))
		return value

	def time_heuristic(self, char_dict, length, token):
		'''returns a really crappy time heuristic value that probably doesn't work or False
		if it definitely isn't a time'''
		value = 0
		if (char_dict['letters'] + char_dict['delimiters'] + char_dict['slashes']) > 0:
			return False
		value += 10 * (2 - abs(char_dict['colons'] - 2))
		value += 4 * (5 - abs(char_dict['numbers'] - 5))
		return value

	def build_classifiers(self):
		'''builds the self.column_classifiers data member by creating classifier objects created 
		by classifier(name of the type, possible ascii values in the type string, list of the known condensed forms)'''
		self.column_classifiers = []
		numbers = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
		upper_case_letters = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90]
		lower_case_letters = [97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]

		self.column_classifiers.append(classifier('names', [32, 44, 45, 46] + upper_case_letters + lower_case_letters, 
			['Xx', 'Xx Xx', 'Xx X Xx', 'Xx X. Xx', 'Xx x Xx', 'Xx x. Xx', 'Xx, Xx', 'Xx, Xx X', 'Xx, Xx X.', 'Xx, Xx x.', 'Xx, Xx x', 'X Xx', 'X. Xx', 'Xx, X', 'Xx, X.']))

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

		self.column_classifiers.append(classifier('datestrings', [32, 44, 46] + numbers + upper_case_letters + lower_case_letters, 
			['x 0', 'Xx 0', '0 x', '0 Xx', 'x. 0', 'Xx. 0', '0 x.', '0 Xx.'] + types_without_dow + types_with_dow))

		date_types = ['0/0', '0/0/0', '0-0', '0-0-0', '0.0', '0.0.0']
		self.column_classifiers.append(classifier('dates', [45, 46, 47] + numbers, date_types))

		time_types = ['0:0', '0:0:0']
		self.column_classifiers.append(classifier('times', numbers + [58], time_types))

		datetime_types = []
		for x in date_types:
			for y in time_types:
				datetime_types.append(x + ' ' + y)
				datetime_types.append(y + ' ' + x)
		self.column_classifiers.append(classifier('datetimes', [32, 45, 46, 47] + numbers + [58], datetime_types))

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

		self.column_classifiers.append(classifier('addresses', [32, 39, 44, 45, 46] + numbers + [58, 59] + upper_case_letters + lower_case_letters, address_types))

		self.column_classifiers.append(classifier('numbers', [44, 46] + numbers, ['0', '0.0', '0,0', '0,0,0', '0,0,0,0', '0,0,0,0,0', '0,0.0', '0,0,0.0', '0,0,0,0.0', '0,0,0,0,0.0']))

	def reset(self, column_list):
		'''resets the dictionaries and other data members so that a different set of data can be run'''
		self.column_list = column_list
		self.column_type_dict = {'names': 0,'datestrings':0, 'dates': 0,'times': 0,'datetimes': 0, 'addresses': 0, 'numbers': 0, 'zipnumbers': 0, 'misc': 0}
		self.column_length = len(column_list)

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


class classifier:
	'''this class is a class used only in the column_classifiers data member in order to structure the types better.
	The class contains:
		1. A name of the type (Ex: 'names')
		2. A list of possible ascii values that can be contained in the type (Ex: names can contain lower_case_letters
			97-122 but cannot contain '=' 61)
		3. A list of the known forms that this particular types comes in. (Ex: names can be written as 'Xx Xx' or 'Xx' or 'Xx X. Xx' etc) 
			I wrote in many known forms but there are plenty that I missed'''
	def __init__(self, n, pv, kf):
		self.name = n
		self.possVals = pv
		self.knownForms = kf

	def can_be(self, vals):
		'''Tests whether the sequence of ascii values inputted has any that are not allowed in this particular type'''
		for elem in vals:
			if elem not in self.possVals:
				return False
		return True

	def is_a(self, form):
		'''Tests whether the given condensed form is in the known forms of this particular type'''
		if form in self.knownForms:
			return True
		return False

