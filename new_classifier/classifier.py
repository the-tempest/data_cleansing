import re

class classifier:
	'''this class is a class used only in the column_classifiers data member in order to structure the types better.
	The class contains:
		1. A name of the type (Ex: 'names')
		2. A list of possible ascii values that can be contained in the type (Ex: names can contain lower_case_letters
			97-122 but cannot contain '=' 61)
		3. A list of regular expressions representing forms of the type
		4. A list of a set of known examples for the particular type (Ex: John)'''
	def __init__(self, name, possible_values=[], regexs=[], examples=[], column_names=[]):
		self.my_name = name

		self.my_possibles = {}
		for val in possible_values:
			self.my_possibles[val] = 1

		self.my_regexs = []
		for regex in regexs:	
			self.my_regexs.append(re.compile(regex))

		self.my_examples = {}
		for ex in examples:
			self.my_examples[ex] = 1

		self.my_columns = []
		for col in column_names:
			self.my_columns.append(col)

	def check_possibles(self, token):
		'''Tests whether the sequence of ascii values inputted has any that are not allowed in this particular type'''
		for char in token:
			if char not in self.my_possibles:
				return False
		return True

	def check_regexs(self, token):
		'''Tests whether the given token is in the form of the regular expression for the type'''
		for regex in self.my_regexs:
			if regex.match(token) != None:
				return True
		return False

	def check_examples(self, token):
		'''Tests whether the given string is stored in the list of known string examples of the particular types'''
		for elem in token.split():
			if elem in self.my_examples:
				return True
		return False

	def check_column_name(self, col_name):
		'''Tests whether the name of the tokens column matches a possible column name for the type'''
		for elem in self.my_columns:
			if elem in col_name:
				return True
		return False