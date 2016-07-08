import os, math, operator, csv, sys
from os import listdir
from os.path import isfile, join
import subprocess

execfile('table.py')

class numeric_classifier:
	def __init__(self):

		self.numeric_types = [] #list of all numeric_type classes (strings)


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
			
		return switcher.get(feature, "feature not yet implemented") #base case for a feature not yet implemented 
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
		self.types_feature_dictionary = {} # a dictionary of feature dictionaries
		self.name = name
		self.features = []


	def train(self, training_dir):
		''' Will train given some training data, can edit this later. must give path to directory'''

		training_files_list = [f for f in listdir(training_dir) if isfile(join(training_dir, f))] # gets list of files in teh training _dir
		for file in training_files_list:
			file_path = training_dir + file # build up the whole path
			

			table_name = subprocess.check_output([sys.executable, "extraction.py", file]) #
			t = getTable(table_name) #  returns table object
			column_names = []
			for column in t.columns:
				column_names.append(column.colName)
			for type in types:
				if type in column_names:
					index = t.column_index[type]
					col = t.column_names[index] # we have the column object now 
					self.train_type(col)

	def train_type(self, col):
		row_list = col.row
		for item in row_list:
			if col.colName in self.type_switch_feature_dictionary: #if the type is in the dict
				



trained_date = numeric_type("date")a