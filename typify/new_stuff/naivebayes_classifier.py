import os, math, operator, csv, sys
from os import listdir
from os.path import isfile, join
import subprocess
import pickle
import extraction
import re

from secrets import password, port, database, user, host, path
execfile(path+'table.py')
training_directory = (path+"training_data")

# TODO put location back into types once data is found
MY_FEATURES = ['length', 'slashes', 'dashes', 'spaces', 'dots', 'commas',
			'upper', 'lower', 'numbers'] # default features and types
MY_TYPES = ['date', 'longitude', 'latitude', 'number', 'zip', 'phone_number', 'ip', 'year', 'isbn', # numerics are built in
		    'name', # this is made more specific by heuristics
		    'string'] # this is made more specific by heuristics
LEN_TYPES = len(MY_TYPES)


''' Form of the feature_dictionary that gets built in train and is used to classify
{'Phone_Number': {'slashes': {0: 1000},
				'length': {16: 635, 17: 277, 15: 88},
				'spaces': {0: 1000},
				'decimal points': {0: 1000},
				'dashes': {2: 1000}},
'Zip': {
	'slashes': {0: 998},
	'length': {4: 36, 5: 461, 6: 1, 8: 7, 9: 40, 10: 453},
	'spaces': {0: 998},
	'decimal points': {0: 998},
	'dashes': {0: 545, 1: 453}}}
'''

class naivebayes_classifier:
	def __init__(self):
		self.features = MY_FEATURES
		self.types = MY_TYPES #list of all numeric_type classes (strings)

		if os.path.isfile(path+"new_trained_dictionary.dat"):
			self.trained_dictionary = self.load(path+"new_trained_dictionary.dat")
		else:
			print 'have to train'
			t = trainer()
			t.train(training_directory)
			self.trained_dictionary = t.trained_dictionary

	def classify(self, nText):
		'''Takes in a string and classifies it to one of the classifiers types '''
		type_probabilities = {}
		for t in self.types:
			type_probabilities[t] = 1 #initialize
			for feature in self.trained_dictionary[t]: #for a specific type compute P(feature | type)
				curr_dictionary = self.trained_dictionary[t][feature]
				prev_type_prob = self.type_switch(feature, nText, curr_dictionary)
				type_probabilities[t] += prev_type_prob		
		max_key = max(type_probabilities, key=type_probabilities.get)
		return max_key

	def type_switch(self, feature, arg, curr_dict): # need to build this up
		''' feature is the thing we are using to compute a prob. arg is the given text from a cell dict is the type we are in. This function is looped from in classify'''
		switcher = {"length" : self.compute_feature_prob(len(arg), curr_dict ),
					"slashes" : self.compute_feature_prob(arg.count("/"), curr_dict),
					"dashes" : self.compute_feature_prob(arg.count("-"), curr_dict),
					"dots": self.compute_feature_prob(arg.count("."), curr_dict),
					"spaces": self.compute_feature_prob(arg.count(" "), curr_dict),
					"commas": self.compute_feature_prob(arg.count(","), curr_dict),
					"lower": self.compute_feature_prob(len(re.findall('[a-z]', arg)), curr_dict),
					"upper": self.compute_feature_prob(len(re.findall('[A-z]', arg)), curr_dict),
					"numbers": self.compute_feature_prob(len(re.findall('[\d]', arg)), curr_dict)
					}
		return switcher.get(feature, "feature not yet implemented") #base case

	def compute_feature_prob(self, feature, feature_dict):
		if feature in feature_dict:
			return float((feature_dict[feature])) / float((sum(feature_dict.itervalues()))) # float this or log this?
		return 0

	def load(self, sFilename):
		f = open(sFilename, "r")
		u = pickle.Unpickler(f)
		dObj = u.load()
		f.close()
		return dObj


class trainer: # class fo holding training functions
	def __init__(self):
		self.features = MY_FEATURES
		self.types = MY_TYPES
		self.trained_dictionary = {} # a dictionary of feature dictionaries

	def train(self, training_dir=r"/training_data"):
		''' Will train given some training data, can edit this later. must give path to directory
				need to put r in front of training_dir for windows at least'''

		training_files_list = [f for f in listdir(training_dir) if isfile(join(training_dir, f))] # gets list of files in the training _dir
		for training_file in training_files_list:
			
			file_path = os.path.join(training_dir, training_file) # build up the whole path
			print file_path + "\n"
			table_name = extraction.extract(file_path);
			t = getTable(table_name, user, password, host, database) #  returns table object
			column_names = []

			for column in t.columns:
				# remove characters 0-9 in column name
				firstNum = "0"
				for x in range(10):
					column.colName = column.colName.replace(chr(ord(firstNum) + x), "")
				print column.colName
				if column.colName in self.types: #building the columns we are going to train as long as they are types we want
					column_names.append(column.colName)
			t.build_column_index()
			for col in column_names:
				index = t.column_index[col]
				column_obj = t.columns[index] # we have the column object now
				self.train_on_column(column_obj)

		self.save(self.trained_dictionary, path+"new_trained_dictionary.dat")

	def train_on_column(self, col):
		row_list = col.rows
		for item in row_list: # each cell in a column's row list
			if item == "NULL": # workaround for now for empty cells
				continue
			if col.colName in self.trained_dictionary: #if the type is in the dict
				curr_type_dict = self.trained_dictionary[col.colName] # get dictionary of feature dictionaries
				for feature in self.features: # string of features
					if feature in curr_type_dict: # if feature dict exits
						curr_feature_dict = curr_type_dict[feature]
						self.build_feature_freq(curr_feature_dict, item, feature)
					else:
						curr_type_dict[feature] = {}
						self.build_feature_freq(curr_type_dict[feature], item , feature)
			else:
				self.trained_dictionary[col.colName] = {}
				curr_type_dict = self.trained_dictionary[col.colName]
				for feature in self.features:
					if feature in curr_type_dict: # if feature dict exits
						curr_feature_dict = curr_type_dict[feature]
						self.build_feature_freq(curr_feature_dict, item, feature)
					else:
						curr_type_dict[feature] = {}
						self.build_feature_freq(curr_type_dict[feature], item , feature)

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
					"slashes" : arg.count("/"),
					"dashes" : arg.count("-"),
					"dots" : arg.count("."),
					"spaces": arg.count(" "),
					"commas": arg.count(","),
					"upper": len(re.findall("[A-z]", arg)),
					"lower": len(re.findall("[a-z]", arg)),
					"numbers": len(re.findall("[\d]", arg))
					}

		return switcher.get(feature, "feature not yet implemented") #base case for a feature not yet implemented

	def save(self, dObj, sFilename): # save dictionary with pickle
		f = open(sFilename, "w")
		p = pickle.Pickler(f)
		p.dump(dObj)
		f.close()


#########################33 put this back in classify if we want statistics, right under max_key
##### everything down here is statistical stuff we aren't using currently
#min_key = min(type_probabilities, key=type_probabilities.get)
#max_value = type_probabilities[max_key]
#min_value = type_probabilities[min_key]
#
#denominator = max_value - min_value	
##### normalizing probabilities to be from 0 to 1
#for item in type_probabilities:
#	type_probabilities[item] = (type_probabilities[item] - min_value) / denominator
#
#mean = sum(type_probabilities.itervalues())/LEN_TYPES
#
##### computing the standard deviation of the data
#variance = 0 
#for item in type_probabilities:
#	deviation = type_probabilities[item] - mean
#	deviation = deviation * deviation
#	variance += deviation
#
#variance = variance / len(type_probabilities)
#std_dev = math.sqrt(variance)
#return max_key, type_probabilities, mean , std_dev