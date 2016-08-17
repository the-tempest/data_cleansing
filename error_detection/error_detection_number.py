import difflib
from secrets import password, port, database, user, host, path
import extraction, re
import math

em_regexp = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
execfile(path+"table.py")
execfile(path+"typify/helper.py")
execfile(path+'typify/numeric_classifier.py')


d = difflib.Differ()
class error_detector_number:
	#assumes that the columns it looks at are numeric and for sales, or age or something like that
	def __init__(self,tt):
		self.name = "hi"
		self.t = tt
		
		#print "above"		
	
	
	def execute1(self, filename):
		filename = filename.replace("\n", "")
		filename = filename.replace(" ", "_")
		table_name = extraction.extract(filename)
		#self.t = getTable(table_name);
	# call Keith and Pawel's script
		c = column_typer(self.t);
		cl = c.build_report();
		print self.t.columns[0].tentClass
		print "below"
		dirToSave = path+"output";
		fn = table_name + ".txt"
		pathToSave = os.path.join(dirToSave, fn);
		
		with open(pathToSave, "w") as text_file:
			text_file.write(cl);
		
	
	def check_on_table(self):
		table = self.t
		column_errors = []
		for column in table.columns:

			indices = self.number_format_check(column)
			indices2 = self.misclassified(column)
		#	column_errors.append(indices)

			column_errors.append(indices2)
		print "here"
		print column.tentClass
		print column.colName
		return column_errors

	def range_check(self, rows):
		'''Looks for formating errors in a column'''
		flagged = []
		format_dictionary = {}
		mean = 0
		total = 0

		split_rows = []
		max_length = 0
		for row in rows:
			split = row.split()
			split_rows.append(split)
			length = len(split)
			if length > max_length:
				max_length = length

		for curr_num in range(max_length):
			for x in split_rows:
				if no_letters(x[curr_num]):
					sub_regex = re.compile(r'''[^0-9]''')
					x[curr_num] = sub_regex.sub('', x[curr_num])
					total += int(x[curr_num])
			mean = float(total)/float(len(rows))
		#	print total
		#	print len(column)
		#	print mean
			variance = 0.0
			for x in range(len(split_rows)):
				if no_letters(split_rows[x][curr_num]):
					add = int(split_rows[x][curr_num]) - mean
					add = add * add
					variance += add
				else:
					if x not in flagged:
						flagged.append(x)
			#print flagged
			variance = variance/len(split_rows)
			std = math.sqrt(variance)
			#print mean
			#print std
			for x in range(len(split_rows)):
				if  no_letters(split_rows[x][curr_num]):
					if abs(int(split_rows[x][curr_num])-mean)> 2*std:
						if x not in flagged:
							flagged.append(x)
			
		return flagged
	
	def misclassified(self, column):
		think = column.tentClass
		dyct = column.guesses
		error_list = []
		for i in range(len(dyct)):
			if dyct[i]!=think:
				error_list.append(i)
		return error_list
	



	def number_format_check(self, column):
		print "getting here"
		error = []
		column_rows = column.rows
		format_dictionary = {}
		for x in range(len(column_rows)):
			string = make_form(column_rows[x])
			string = condense(string)
			column_rows[x] = string
			if string in format_dictionary:
				format_dictionary[string] += 1
			else: 
				format_dictionary[string] = 1

		general_form = max(format_dictionary, key = format_dictionary.get) # the most common format_dictionary
		#print general_form		
		for x in range(len(column_rows)):
			if column_rows[x]!=general_form:
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