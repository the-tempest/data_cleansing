import mysql.connector, os
class column_typer: 	
	def __init__(self, column_list):
		self.column_list = column_list
		self.column_type_dict = {'names': 0, 'dates': 0, 'addresses': 0, 'numbers': 0}


	def column_parser(self):

		for item in self.column_list:
			character_type_dictionary = {'colons':0, 'letters': 0, 'numbers': 0, 'slashes':0, 'delimiters':0, 'misc':0 }
			
			for character in item:
				if ord(character) <= 57 and ord(character) >= 48: # is an ascii number
					character_type_dictionary[numbers] += 1

				if ord(character) == 46 or ord(character) == 44: # is a , or a .
					character_type_dictionary[delimiters] += 1

				if ord(character) <= 90 and ord(character) >= 65

					




