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