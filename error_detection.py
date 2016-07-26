import difflib
from secrets import password, port, database, user, host
import extraction, re, math

em_regexp = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
execfile("table.py")
execfile("typify/helper.py")
d = difflib.Differ()
class error_detector:
	def __init__(self,file_path):
		self.name = "hi"
		table_name = extraction.extract(file_path);
		self.t = getTable(table_name, user, password, host, database)
		

	def check_on_table(self):
		table = self.t


		table.build_column_index()
		column_errors = []
		for column in table.columns:
			if column.tentClass == "email": # someone needs to implement this now its not that hard...
				indices = self.email_check(column.rows)
			else:
				indices = self.format_checks(column.rows)
			column_errors.append(indices)




	def email_check(self,column):
		''' Uses a regular expresion to see if emails are valid''' 
		prog = re.compile(em_regexp)
		possible_error_indices = []
		for x in range(len(column)):
			result = prog.findall(column[x])
			if len(result) == 0:
				possible_error_indices.append(x)

		return possible_error_indices


	def format_checks(self, column_rows):
		'''Looks for formating errors in a column'''
		column = column_rows
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

		med,index = self.medianList(list_of_diffs)
		
		# print med

		# list_of_diffs
		IQR, Q1, Q3, I1, I3 = self.compute_IQR(list_of_diffs)

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


	def compute_IQR(self,L):
		L = sorted(L)
		length = len(L)
		#compute median
		m, i = self.medianList(L)
		if m in L: # means odd sized list
			lower = L[0:length/2]
			upper = L[(length/2)+1:]

		else:
			lower = L[0:length/2]
			upper = L[length/2:]
		#print upper
		#print lower
		Q1, index1 = self.medianList(lower)
		Q3, index2 = self.medianList(upper)
		IQR = Q3-Q1

		return IQR, Q1, Q3, index1, index2+i

	def medianList(self,L):
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