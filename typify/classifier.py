import re

class classifier:
	'''this class is a class used only in the column_classifiers data member in order to structure the types better.
	The class contains:
		1. A name of the type (Ex: 'names')
		2. A list of possible ascii values that can be contained in the type (Ex: names can contain lower_case_letters
			97-122 but cannot contain '=' 61)
		3. A regular expression representing the form of the type
		4. A list of a set of known examples for the particular type (Ex: John)
		5. A list of the known features or common strings that are found in examples of this type (Ex: Dr. or Mr. or II)'''
	def __init__(self, n, pv, reg, ke, cf):
		self.name = n
		
		self.possVals = {}
		for elem in pv:
			self.possVals[elem] = 1
		
		self.regEx = re.compile(reg)

		self.knownExamples = {}
		for elem in ke:
			self.knownExamples[elem] = 1
		
		self.commonFeatures = {}
		for elem in cf:
			self.commonFeatures[elem] = 1

	def can_be(self, vals):
		'''Tests whether the sequence of ascii values inputted has any that are not allowed in this particular type'''
		for elem in vals:
			if elem not in self.possVals:
				return False
		return True

	def has_form(self, token):
		'''Tests whether the given token is in the form of the regular expression for the type'''
		if len(re.findall(self.regEx, token)) == 1:
			return True
		return False

	def is_a(self, inString):
		'''Tests whether the given string is stored in the list of known string examples of the particular types'''
		return inString in self.knownExamples

	def contains_a(self, inString):
		'''Tests whether the given string contains a common feature of the particular type'''
		for elem in inString:
			if elem in self.commonFeatures:
				return True
		return False