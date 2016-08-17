import re
execfile(path+"typify/features/features.py")

class new_classifier:
	'''this class is a class used only in the column_classifiers data member in order to structure the types better.
	The class contains:
		1. A name of the type (Ex: 'names')
		3. A list of regular expressions representing forms of the type
		4. A list of a set of known examples for the particular type (Ex: John)'''
	def __init__(self, n, regs, ke):
		self.name = n
		self.raw_regs = REGEXS[self.name]
		self.regs = []
		for regex in self.raw_regs:	
			self.regExs.append(re.compile(regex))

		self.knownExamples = {}
		for elem in ke:
			self.knownExamples[elem] = 1

	def check_regex(self, token):
		'''Tests whether the given token is in the form of the regular expression for the type'''
		for regex in self.regExs:
			if regex.match(token) != None:
				return True
		return False

	def check_examples(self, token):
		'''Tests whether the given string is stored in the list of known string examples of the particular types'''
		for elem in token.split():
			if elem in self.knownExamples:
				return True
		return False
