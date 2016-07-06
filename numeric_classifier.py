import os, math, operator

class numeric_classifier:
	def __init__(self):

		self.numeric_types = [] #list of all numeric_type classes 


	def classify(self, nText):
		type_probabilities = {}

		for type in self.numeric_types: # going to check that it can be of any type
			type_probabilities[type.name] = 1
			for feature, feature_occurance in type.feature_dictionary: #for a specific type compute P(feature | type)
				
				curr_dictionary = feature_occurance
				total_number = sum(curr_dictionary.itervalues())
				posterier_type_prob = self.type_switch(feature, nText, curr_dictionary)
				type_probabilities[type.name] *= posterier_type_prob

		#find the max of all types to guess what the type of the column is
		max(type_probabilities.iteritems(), key=operator.itemgetter(1))[0] 
		
	

	def type_switch(self, feature, arg, dict): # need to build this up
	''' feature is the thing we are using to compute a prob.
		arg is the given text from a cell
		dict is the type we are in. This function is looped from in classify'''
		switcher = {"length" : self.compute_feature_prob(len(arg), dict ),
					"slashes" : self.compute_feature_prob(count_a_char(arg, "/"), dict),
					"dashes" : self.compute_feature_prob(count_a_char(arg, "-"), dict)

					}
			
		return switcher.get(feature, "feature not yet implemented")
	def count_a_char(nText, char):
		'''A helpful feature for dates probably '''
		sum = 0
		for elem in nText:
			if elem == char
				sum += 1

		return sum

	def compute_feature_prob(self, feature, feature_dict):
		if feature in feature_dict:
			return (feature_dict[feature]) / (sum(feature_dict.itervalues())) # float this or log this?
		else:
			return 0 # or mabye 1

# want to build a bunch of these and save them should train these. 
class numeric_type:
	def __init__(self, name):
		self.feature_dictionary = {} # a dictionary of feature dictionaries
		self.name = name


trained_date = numeric_type("date")