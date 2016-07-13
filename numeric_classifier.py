import os, math, operator, csv, sys
from os import listdir
from os.path import isfile, join
import subprocess
import pickle
import time

execfile('table.py')
training_directory = r"uploaded\numeric_training_data"

features = ['length', 'slashes', 'dashes', 'spaces', 'decimal points']
types = ['Date', 'Longitude', 'Latitude', 'Number', 'Zip', 'Phone_Number', 'IP']


class numeric_classifier:
	def __init__(self, numeric_types = types, features = features):
		self.features = features
		self.numeric_types = numeric_types #list of all numeric_type classes (strings)
		
		if os.path.isfile("types_feature_dictionary.dat"):		
			self.feature_dictionary = self.load("types_feature_dictionary.dat")
		else:
			trainer = numeric_trainer(self.numeric_types, self.features)
			trainer.train(training_directory)
			self.feature_dictionary = trainer.types_feature_dictionary
			

	def classify(self, nText):
		type_probabilities = {}

		for t in self.numeric_types: # going to check that it can be of any type
			type_probabilities[t] = 1
			for feature in self.feature_dictionary[t]: #for a specific type compute P(feature | type)
				#print feature
				curr_dictionary = self.feature_dictionary[t][feature]
				total_number = sum(curr_dictionary.itervalues())

				posterier_type_prob = self.type_switch(feature, nText, curr_dictionary)
				
				type_probabilities[t] += posterier_type_prob

		#find the max of all types to guess what the type of the column is
		result = max(type_probabilities.iteritems(), key=operator.itemgetter(1))[0] 
		#print type_probabilities
		#print result
		return result
	

	def type_switch(self, feature, arg, curr_dict): # need to build this up
		''' feature is the thing we are using to compute a prob. arg is the given text from a cell dict is the type we are in. This function is looped from in classify'''
		switcher = {"length" : self.compute_feature_prob(len(arg), curr_dict ),
					"slashes" : self.compute_feature_prob(self.count_a_char(arg, "/"), curr_dict),
					"dashes" : self.compute_feature_prob(self.count_a_char(arg, "-"), curr_dict),
					"decimal points": self.compute_feature_prob(self.count_a_char(arg, "."), curr_dict),
					"spaces": self.compute_feature_prob(self.count_a_char(arg, " "), curr_dict)
					}
			
		return switcher.get(feature, "feature not yet implemented") #base case for a feature not yet implemented 
	def count_a_char(self, nText, char):
		'''A helpful feature for dates probably '''
		total = 0
		for elem in nText:
			if elem is char:
				total += 1

		return total

	def compute_feature_prob(self, feature, feature_dict):
		if feature in feature_dict:
			return float((feature_dict[feature])) / float((sum(feature_dict.itervalues()))) # float this or log this?
		else:
			return 0 # or mabye 1

	
	def load(self, sFilename):
		f = open(sFilename, "r")
		u = pickle.Unpickler(f)
		dObj = u.load()
		f.close()
		return dObj
		#"""Given a file name, load and return the object stored in the file."""
        # f = open(sFilename,"r")
        # u = picl.e.Unpickler(f)
        # dObj = u.load()
        # f.close()
        # return dObj

class numeric_trainer:
	def __init__(self, types = [], features =[]):
		self.features = features
		self.types = types
		self.types_feature_dictionary = {} # a dictionary of feature dictionaries


	def train(self, training_dir):
		''' Will train given some training data, can edit this later. must give path to directory
				need to put r in front of training_dir for windows at least'''

		#first need to initialize types_feature_dictionary

		training_files_list = [f for f in listdir(training_dir) if isfile(join(training_dir, f))] # gets list of files in teh training _dir
		for training_file in training_files_list:
			file_path = training_dir  + "\\" + training_file # build up the whole path
			
			print file_path + "\n"
		
			table_name = subprocess.check_output([sys.executable, "extraction.py", file_path]) #
			##print 101
			print table_name
			t = getTable(table_name, "root", "spence23", "localhost", "world") #  returns table object
			t.build_column_index()
			column_names = []
			for column in t.columns:
				if column.colName in self.types:
					column_names.append(column.colName)
			#print column_names
			#for type in types:
				#if type in column_names:
			for col in column_names:	
				index = t.column_index[col]
				column_obj = t.columns[index] # we have the column object now 
				#print column_obj.colName
				self.train_type(column_obj)

		self.save(self.types_feature_dictionary, "types_feature_dictionary.dat")

	def train_type(self, col):
		row_list = col.rows
	
		for item in row_list: # each element
			if item == "NULL":
				continue
			#print item
			if col.colName in self.types_feature_dictionary: #if the type is in the dict

				curr_type_dict = self.types_feature_dictionary[col.colName] # dictionary 
			
				for feature in self.features: # string of features 
					
					if feature in curr_type_dict: # if feature dict exits
						curr_feature_dict = curr_type_dict[feature]
						self.build_feature_freq(curr_feature_dict, item, feature)
					else:
						curr_type_dict[feature] = {}
						self.build_feature_freq(curr_type_dict[feature], item , feature)
			else:
				self.types_feature_dictionary[col.colName] = {}
				curr_type_dict = self.types_feature_dictionary[col.colName]

				for feature in self.features:
				
					if feature in curr_type_dict: # if feature dict exits
						curr_feature_dict = curr_type_dict[feature]
						self.build_feature_freq(curr_feature_dict, item, feature)
					else:
						curr_type_dict[feature] = {}
						self.build_feature_freq(curr_type_dict[feature], item , feature)

				#print " invalid type/column name! FIX HEADER OR CODE"
						
	def build_feature_freq(self, curr_dict, nText, feature):
		feature_result = self.feature_switch(feature, nText)
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
					"dashes" : self.count_a_char(arg, "-"),
					"decimal points" : self.count_a_char(arg, "."),
					"spaces": self.count_a_char(arg, " ")
					}
			
		return switcher.get(feature, "feature not yet implemented") #base case for a feature not yet implemented 

	def count_a_char(self, nText, char):
		'''A helpful feature for dates probably '''
		total = 0
		for elem in nText:
			if elem == char:
				total += 1

		return total


	def save(self, dObj, sFilename):
		f = open(sFilename, "w")
		p = pickle.Pickler(f)
		p.dump(dObj)
		f.close()
		# """Given an object and a file name, write the object to the file using pickle."""

  #       f = open(sFilename, "w")
  #       p = pickle.Pickler(f)
  #       p.dump(dObj)
  #       f.close()
