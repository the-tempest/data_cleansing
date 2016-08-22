import difflib
from secrets import password, port, database, user, host, path
import extraction, re, math
from const import string_types, number_types

execfile(path + "table.py")
execfile(path + "typify/helper.py")
execfile(path + "error_detection/fingerprint.py")
d = difflib.Differ()



class error_detector:
	def __init__(self,table):
		self.name = "hi"
		self.t = table
		self.STRING_TYPES = string_types
		self.NUMBER_TYPES = number_types


	def cluster_rows(self,column):
		#TODO: implement a use for this outside of print statements
		''' Takes in a list of elements in a column and prints out clusters'''
		rows = column.rows
		clustered_dictionary, finger_dict = fingerprint_column(rows)

		for item in clustered_dictionary.keys():
			#print "Found Cluster: " + str(item)
			#print "Elements in cluster " + item + " are: " 
			for x in range(len(finger_dict[item])):
			#	print x, ": ",  rows[finger_dict[item][x]]
				x = 1
			#print "\n"
		return []


	def format_check(self, column):
		#use a different method if there is a problem with the column classification or regex form classification
		if (column.tentClass == None or column.tentClass == 'misc' or column.forms == []):
			return self.format_check_misc(column.rows)

		#use regexs - might want to make this into another helper function
		possible_error_indices = []

		compiled_forms = []
		for regex in column.forms:
			compiled_forms.append(re.compile(regex))

		column_rows = column.rows
		for index in range(len(column_rows)):
			matched = False
			for regexObj in compiled_forms:
				if regexObj.match(column_rows[index]) != None:
					matched = True
					break
			if not matched:
				possible_error_indices.append(index)

		return possible_error_indices



	def format_check_misc(self, rows):
		'''Looks for formating errors in a column and takes in a list of rows in a column'''
		column = []
		for item in rows: # i needed to do this for some reason because rows was getting edited outside of this scope 
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
		general_form = general_form.splitlines()
		# print general_form
		# print column
		list_of_diffs = []
		for cell in column:

			cell = cell.splitlines()
			result = list(d.compare(general_form, cell))

			# compare returns 4 things. I think for now only looking at dif to the general form
			
			if len(result) == 1: # the strings are the same
				list_of_diffs.append(0)
				continue

			
			result = result[-1]
			result = result.replace('?', '')
			result = result.replace('\n', '')

			diff = len(result) - result.count(' ')
			list_of_diffs.append(diff)
		#list_of_diffs maps to the list of rows in column
		if len(list_of_diffs) == 0:
			return 0
		else:
			mean = sum(list_of_diffs) / float(len(list_of_diffs)) # to avoid int division

		med = 0
		# print sorted(list_of_diffs)

		med,index = medianList(list_of_diffs)
		
		# print med

		# list_of_diffs
		IQR, Q1, Q3, I1, I3 = compute_IQR(list_of_diffs)

		# print IQR, Q1, Q3

		outlier_max_range = math.floor(1.5*IQR + Q3)
		outlier_min_range = math.ceil(Q1 - 1.5*IQR)
		
		# print outlier_max_range
		# print outlier_min_range

		possible_error_indices = []
		for x in range(len(list_of_diffs)):
			if list_of_diffs[x] <= outlier_min_range or list_of_diffs[x] >= outlier_max_range:
				possible_error_indices.append(x) 
				#appending indices in column that will have 
		#for item in possible_error_indices:
			#print column[item]

		return possible_error_indices

	'''def execute1(self, filename):
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
			text_file.write(cl);'''
		
	
	'''def check_on_table(self):
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
		return column_errors'''

	def range_check(self, column):
		'''Looks for formating errors in a column'''
		if column.tentClass in self.STRING_TYPES + ['date', 'phone_number', 'ip', 'isbn']:
			return []
		flagged = []
		format_dictionary = {}
		mean = 0
		total = 0
		rows = column.rows

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
				if (curr_num < len(x) and no_letters(x[curr_num])):
					sub_regex = re.compile(r'''[^0-9]''')
					x[curr_num] = sub_regex.sub('', x[curr_num])
					total += int(x[curr_num])
			mean = float(total)/float(len(rows))
		#	print total
		#	print len(column)
		#	print mean
			variance = 0.0
			for x in range(len(split_rows)):
				if (curr_num < len(split_rows[x]) and no_letters(split_rows[x][curr_num])):
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
				if (curr_num < len(split_rows[x]) and no_letters(split_rows[x][curr_num])):
					if abs(int(split_rows[x][curr_num])-mean)> 2*std:
						if x not in flagged:
							flagged.append(x)
			
		return flagged

	def date_range_check(self, column):
		'''TODO: implement this'''
	
	def misclassified(self, column):
		if column.tentClass in [None, 'misc']:
			return []
		think = column.tentClass
		dyct = column.guesses
		error_list = []
		for i in range(len(dyct)):
			if dyct[i]!=think:
				error_list.append(i)
		return error_list
	

	
def compute_IQR(L):
		L = sorted(L)
		length = len(L)
		#compute median
		m, i = medianList(L)
		if m in L: # means odd sized list
			lower = L[0:length/2]
			upper = L[(length/2)+1:]

		else:
			lower = L[0:length/2]
			upper = L[length/2:]
		#print upper
		#print lower
		Q1, index1 = medianList(lower)
		Q3, index2 = medianList(upper)
		IQR = Q3-Q1

		return IQR, Q1, Q3, index1, index2+i

def medianList(L):
	L = sorted(L)
	length = len(L)

	if (length % 2) == 1: 
		return L[length/2], length/2
	else:
		x1 = L[length/2]
		x2 = L[(length/2) - 1]
		return float(x1 + x2)/2, length/2


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