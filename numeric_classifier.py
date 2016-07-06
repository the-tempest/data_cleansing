import os, math

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
				self.type_switch


	def type_switch(self, type, arg, dict): # need to build this up
		switcher = {"length" : self.compute_length_prob(len(arg), dict )}
			
		return switcher.get(arg, "feature not yet implemented")

	def compute_length_prob(self, test_length, length_dict):
		if test_length in length_dict:
			return (length_dict[test_length]) / (sum(length_dict.itervalues()))
		else:
			return 0 # or mabye 1

# want to build a bunch of these and save them should train these. 
class numeric_type:
	def __init__(self, name):
		self.feature_dictionary = {} # a dictionary of feature dictionaries
		self.name = name


trained_date = numeric_type("date")