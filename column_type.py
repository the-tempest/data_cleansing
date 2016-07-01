import mysql.connector, os
class column_typer: 	
	def __init__(self, column_list):
		self.column_list = column_list
		self.column_type_dict = {'names': 0, 'dates': 0,'times': 0, 'whole_addresses': 0, 'numbers': 0, 'misc': 0}


	def column_typify(self):
		for word in self.column_list:
			word_type_dictionary = {'name': 0, 'date': 0, 'time': 0, 'location': 0, 'zipnumber': 0, 'number': 0, 'misc': 0}
			for item in tokenize(word):
				character_type_dictionary = {'colons':0, 'letters': 0, 'numbers': 0, 'slashes':0, 'delimiters':0, 'misc':0}
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
						word_type_dictionary['zipnumber'] += 1
					else:
						word_type_dictionary['number'] += 1
				else:
					word_type = ''
					max_val = float("-inf")
					temp_val = self.name_heuristic(character_type_dictionary, length, item)
					if temp_val != False:
						if temp_val > max_val:
							word_type = 'name'
							max_val = temp_val

					temp_val = self.date_heuristic(character_type_dictionary, length, item)
					if temp_val != False:
						if temp_val > max_val:
							word_type = 'date'
							max_val = temp_val

					temp_val = self.time_heuristic(character_type_dictionary, length, item)
					if temp_val != False:
						if temp_val > max_val:
							word_type = 'time'
							max_val = temp_val

					temp_val = self.location_heuristic(character_type_dictionary, length, item)
					if temp_val != False:
						if temp_val > max_val:
							word_type = 'location'
							max_val = temp_val

					if word_type == '':
						word_type_dictionary['misc'] += 1
					else:
						word_type_dictionary[word_type] += 1


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
		value += 10 * (2 - abs(character_type_dictionary['slashes'] - 2))
		value += 4 * (5 - abs(character_type_dictionary['numbers'] - 5))
		return value

	def time_heuristic(self, char_dict, length, token):
		value = 0
		if (char_dict['letters'] + char_dict['delimiters'] + char_dict['slashes']) > 0:
			return False
		value += 10 * (2 - abs(character_type_dictionary['colons'] - 2))
		value += 4 * (5 - abs(character_type_dictionary['numbers'] - 5))
		return value

	def location_heuristic(self, char_dict, length, token):
		value = 0
		if (char_dict['colons'] + char_dict['numbers']) > 0:
			return False
		value += 9 - abs(length - 9)
		return value



