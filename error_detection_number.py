import difflib
from secrets import password, port, database, user, host, path
import extraction, re
import math

em_regexp = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
execfile(path+"table.py")
execfile(path+"typify/helper.py")
execfile(path+"main.py")
execfile(path+'numeric_classifier.py')


d = difflib.Differ()
class error_detector_number:
	#assumes that the columns it looks at are numeric and for sales, or age or something like that
	def __init__(self,file_path):
		self.name = "hi"
		table_name = extraction.extract(file_path);		
		execute(file_path)
		self.t = getTable(table_name)
#		print self.t.columns[0].guesses
		
		#print "above"		
	
	
	def execute(self, filename):
		filename = filename.replace("\n", "")
		filename = filename.replace(" ", "_")
		table_name = extraction.extract(filename)
		#self.t = getTable(table_name);
	# call Keith and Pawel's script
		c = column_typer(self.t);
		cl = c.build_report();
		dirToSave = path+"output";
		fn = table_name + ".txt"
		pathToSave = os.path.join(dirToSave, fn);
	#	print pathToSave
	#	print 'this'
		with open(pathToSave, "w") as text_file:
			text_file.write(cl);
	
	def check_on_table(self):
		table = self.t
		table.build_column_index
		column_errors = []
		for column in table.columns:
			indices = self.format_check(column)
			indices2 = self.misclassified(column)
		#	column_errors.append(indices)
			column_errors.append(indices2)
		#	print column.guesses
		print column_errors
		print "here"
		print column.tentClass
		print column.colName
		#print "Here"


	def range_check(self, column):
		'''Looks for formating errors in a column'''
		flagged = []
		format_dictionary = {}
		mean = 0
		sum = 0
		for x in column:
			if no_letters(x):
				sum = int(x)+sum
			print sum
		mean = float(sum)/float(len(column))
	#	print sum
	#	print len(column)
	#	print mean
		variance = 0
		for x in range(len(column)):
			print column
			if no_letters(column[x]):
				print "not"
				add = int (column[x])- mean
				add = add * add
				variance = variance + add
			else:
				flagged.append(x)
				print x
				print "here"
		#print flagged
		variance = variance/len(column)
		std = math.sqrt(variance)
		#print mean
		#print std
		for x in range(len(column)):
			if  no_letters(column[x]):
				if abs(int(column[x])-mean)> 2*std:
					flagged.append(x)
		
		return flagged
	
	def misclassified(self, column):
		think = column.tentClass
		dict = column.guesses
		error_list = []
		for i in range(len(dict)):
			if dict[i]!=think:
				error_list.append(dict[i])
		return error_list
	



	def format_check(self, column):
		print "getting here"
		error = []
		a = column
		column_rows = column.rows
		column = []
		for item in column_rows:
			column.append(item)
		format_dictionary = {}
		for x in range(len(column)):
			string = make_form(column[x])
			string = condense(string)
			column[x] = string
			if string in format_dictionary:
				format_dictionary[string] += 1
			else: 
				format_dictionary[string] = 1

		general_form = max(format_dictionary, key = format_dictionary.get) # the most common format_dictionary
		#print general_form		
		for x in range(len(column)):
			if column[x]!=general_form:
				error.append(x)
		return error	
	
	#def leading_zero(self, column):
		# if most of the tokens don't have leading zeros, then probably none of them should
		
	
	
	

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