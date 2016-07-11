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

		for t in self.numeric_types: # going to check that it can be of any type
			type_probabilities[t.name] = 1
			for feature, feature_occurance in t.feature_dictionary: #for a specific type compute P(feature | type)
				
				curr_dictionary = feature_occurance
				total_number = sum(curr_dictionary.itervalues())

				posterier_type_prob = self.type_switch(feature, nText, curr_dictionary)
				
				type_probabilities[t.name] *= posterier_type_prob

		#find the max of all types to guess what the type of the column is
		max(type_probabilities.iteritems(), key=operator.itemgetter(1))[0] 
		
	

	def type_switch(self, feature, arg, curr_dict): # need to build this up
		''' feature is the thing we are using to compute a prob. arg is the given text from a cell dict is the type we are in. This function is looped from in classify'''
		switcher = {"length" : self.compute_feature_prob(len(arg), curr_dict ),
					"slashes" : self.compute_feature_prob(count_a_char(arg, "/"), curr_dict),
					"dashes" : self.compute_feature_prob(count_a_char(arg, "-"), curr_dict),
					"decimal points": self.compute_feature_prob(count_a_char(arg, "."), curr_dict)
					}
			
		return switcher.get(feature, "feature not yet implemented") #base case for a feature not yet implemented 
	def count_a_char(nText, char):
		'''A helpful feature for dates probably '''
		total = 0
		for elem in nText:
			if elem is char:
				total += 1

		return total

	def compute_feature_prob(self, feature, feature_dict):
		if feature in feature_dict:
			return (feature_dict[feature]) / (sum(feature_dict.itervalues())) # float this or log this?
		else:
			return 0 # or mabye 1

# want to build a bunch of these and save them should train these. 
class numeric_type:
	def __init__(self, name, types = [], features =[]):
		self.name = name
		self.features = features
		self.types = types
		self.types_feature_dictionary = {} # a dictionary of feature dictionaries


	def train(self, training_dir):
		''' Will train given some training data, can edit this later. must give path to directory
			need to put r in front of training_dir for windows at least'''

		training_files_list = [f for f in listdir(training_dir) if isfile(join(training_dir, f))] # gets list of files in teh training _dir
		for training_file in training_files_list:
			file_path = training_dir + "\\" + training_file # build up the whole path
			print file_path + "\n"
			print training_file + "\n"
			table_name = subprocess.check_output([sys.executable, "extraction.py", file_path]) #
			t = getTable(table_name, "root", "spence23", "localhost", "world") #  returns table object
			column_names = []
			for column in t.columns:
				if column in self.types:
					column_names.append(column.colName)
			
			#for type in types:
				#if type in column_names:
			for col in column_names:	
				index = t.column_index[col]
				column_obj = t.column_names[index] # we have the column object now 
				self.train_type(column_obj)

	def train_type(self, col):
		row_list = col.rows

		for item in row_list: # each element
		
			if col.colName in self.types_feature_dictionary: #if the type is in the dict

				curr_type_dict = self.types_feature_dictionary[col.colName] # dictionary 
			
				for feature in self.features: # string of features 
			
					if feature in curr_type_dict: # if feature dict exits
						curr_feature_dict = curr_type_dict[feature]
						build_feature_freq(curr_feature_dict, item, feature)
					else:
						curr_type_dict[feature] = {}
						build_feature_freq(curr_type_dict[feature], item , feature)
			else:
				print " invalid type/column name! FIX HEADER OR CODE"
						
	def build_feature_freq(self, curr_dict, nText, feature):
		feature_result = feature_switch(feature, nText)
		if feature_result in curr_dict:
			curr_dict[feature_result] += 1
		else:
			curr_dict[feature_result] = 1

	def feature_switch(self, feature, arg): # need to build this up
		''' feature is the thing we are using to compute a prob.
		arg is the given text from a cell
		dict is the type we are in. This function is looped from in classify'''
		switcher = {"length" :  len(arg),
					"slashes" : self.count_a_char(arg, "/"),
					"dashes" : self.count_a_char(arg, "-")

					}
			
		return switcher.get(feature, "feature not yet implemented") #base case for a feature not yet implemented 

	def count_a_char(nText, char):
		'''A helpful feature for dates probably '''
		total = 0
		for elem in nText:
			if elem == char:
				total += 1

		return total
