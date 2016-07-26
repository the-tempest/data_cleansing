import difflib
from secrets import password, port, database, user, host
import extraction, re
import math

em_regexp = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
execfile("table.py")
execfile("typify/helper.py")
d = difflib.Differ()
class error_detector_number:
	#assumes that the columns it looks at are numeric and for sales, or age or something like that
	def __init__(self,file_path):
		self.name = "hi"
		table_name = extraction.extract(file_path);
		self.t = getTable(table_name, user, password, host, database)
		
	
	def check_on_table(self):
		table = self.t
		table.build_column_index
		column_errors = []
		for column in table.columns:
			indices = self.range_check(column.rows)
			indices 2 = self.misclassified(column)
			column_errors.append(indices)
		print column_errors
		print "Here"


	def range_check(self, column):
		'''Looks for formating errors in a column'''
		flagged = []
		format_dictionary = {}
		mean = 0
		sum = 0
		for x in range(len(column)):
			sum = x+sum
		mean = float(sum)/float(len(column))
		variance = 0
		for x in range(len(column)):
			add = int (column[x])- mean
			add = add * add
			variance = variance + add
		variance = variance/len(column)
		std = math.sqrt(variance)
		print mean
		print std
		for x in column:
			if abs(int(x)-mean)> 2*std:
				flagged.append(int(x))
		return flagged
	
	def misclassified(self, column):
		think = column.tentClass
		error_list = []
		for i in column.Guesses:
			if i!=think:
				error_list.append(i)
		return error_list
				

def make_form(inString):
	'''Turns the input string into a string that represents the general form of the string'''
	ret = ''
	for char in inString:
		ord_char = ord(char)
		if ord_char <= 57 and ord_char >= 48:
			ret += '0' # it's a digit
		elif ord_char <= 90 and ord_char >= 65:
			ret += 'X' # it's uppercase
		elif ord_char >= 97 and ord_char <= 122:
			ret += 'x' # it's lowercase
		else:
			ret += char # it's punctuation
	return ret

def condense(inString):
	'''Turns the input form string into a standardized form string with word and number lengths removed'''
	condString = ''
	index = 0
	length = len(inString)
	while index < length:
		condString += inString[index]
		if inString[index] == 'x':
			while (index < length and inString[index] == 'x'):
				index += 1
			continue
		if inString[index] == '0':
			while (index < length and inString[index] == '0'):
				index += 1
			continue
		index += 1
	return condString