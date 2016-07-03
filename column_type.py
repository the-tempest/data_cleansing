import mysql.connector, os
class column_typer: 	
	def __init__(self, column_list):
		self.column_list = column_list
		self.column_type_dict = {'names': 0,'datestrings':0, 'dates': 0,'times': 0,'datetimes': 0, 'addresses': 0, 'locations': 0, 'numbers': 0, 'zipnumbers': 0, 'misc': 0}
		self.line_form_dict = {}
		self.column_type = ''
		self.column_length = len(column_list)
		self.cond_column_form = ''

	def column_typify(self):
		for elem in self.column_list:
			form = make_form(elem)
			if self.line_form_dict.has_key(form):
				self.line_form_dict[form] += 1
			else:
				self.line_form_dict[form] = 1

			word_type_dictionary = {'names': 0, 'dates': 0, 'times': 0, 'locations': 0, 'zipnumbers': 0, 'numbers': 0, 'misc': 0}
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

					temp_val = self.location_heuristic(character_type_dictionary, length, item)
					if temp_val != False:
						if temp_val > max_val:
							word_type = 'locations'
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
					if word_type_dictionary.keys() == ['names','locations']:
						self.column_type_dict['locations'] += 1
					elif word_type_dictionary.keys() == ['dates','times']:
						self.column_type_dict['datetimes'] += 1
					elif (word_type_dictionary.keys() == ['names','numbers'] or word_type_dictionary.keys() == ['locations','numbers']):
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
						if 'locations' in word_type_dictionary.keys():
							words += word_type_dictionary['locations']

						numbers = 0
						if 'zipnumbers' in word_type_dictionary.keys():
							words += word_type_dictionary['zipnumbers']
						if 'numbers' in word_type_dictionary.keys():
							words += word_type_dictionary['numbers']

						if word_type_dictionary.keys() == ['names','locations']:
							self.column_type_dict['locations'] += 1
						elif word_type_dictionary.keys() == ['zipnumbers','numbers']:
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
						if 'locations' in word_type_dictionary.keys():
							words += word_type_dictionary['locations']

						numbers = 0
						if 'zipnumbers' in word_type_dictionary.keys():
							words += word_type_dictionary['zipnumbers']
						if 'numbers' in word_type_dictionary.keys():
							words += word_type_dictionary['numbers']

						if (words > 0 and numbers > 0):
							self.column_type_dict['addresses'] += 1
						else:
							self.column_type_dict['misc'] += 1

		ret = ''

		if self.column_type_dict['zipnumbers'] == self.column_length:
			ret += 'zipnumbers'
		else:
			ret += dict_max(self.column_type_dict)

		ret += ' with the main form of: '

		condensed_forms = {}
		for key in self.line_form_dict.keys():
			cond_key = condense(key)
			if condensed_forms.has_key(cond_key):
				condensed_forms[cond_key] += 1
			else:
				condensed_forms[cond_key] = 1

		print self.line_form_dict
		print condensed_forms

		self.cond_column_form = dict_max(condensed_forms)
		print self.cond_column_form
		for key in self.line_form_dict.keys():
			if condense(key) != self.cond_column_form:
				del self.line_form_dict[key]

		ret += dict_max(self.line_form_dict)

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
		if (char_dict['colons'] + char_dict['numbers'] + char_dict['slashes'] + char_dict['delimiters']) > 0:
			return False
		value +=  7- abs(length - 7)
		return value

	def date_heuristic(self, char_dict, length, token):
		value = 0
		if (char_dict['colons'] + char_dict['letters']) > 0:
			return False
		value += 10 * (2 - abs(char_dict['slashes'] - 2))
		value += 4 * (5 - abs(char_dict['numbers'] - 5))
		return value

	def time_heuristic(self, char_dict, length, token):
		value = 0
		if (char_dict['letters'] + char_dict['delimiters'] + char_dict['slashes']) > 0:
			return False
		value += 10 * (2 - abs(char_dict['colons'] - 2))
		value += 4 * (5 - abs(char_dict['numbers'] - 5))
		return value

	def location_heuristic(self, char_dict, length, token):
		value = 0
		if (char_dict['colons'] + char_dict['numbers']) > 0:
			return False
		value += 9 - abs(length - 9)
		return value

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
	return num

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




