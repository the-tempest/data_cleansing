import difflib
execfile("typify/helper.py")
d = difflib.Differ()
class error_detector:
	def __init__(self):
		self.name = "hi"

	def format_checks(self, column):
		'''Looks for formating errors in a column'''
		format_dictionary = {}
		for cell in column:
			string = make_form(cell)
			string = condense(string)
			if string in format_dictionary:
				format_dictionary[string] += 1
			else: 
				format_dictionary[string] = 1

		general_form = max(format_dictionary, key = format_dictionary.get) # the most common format_dictionary
		general_form = general_form.splitlines()
		list_of_diffs = []
		for cell in column:
			cell = cell.splitlines()
			result = list(d.compare(general_form, cell))

			# compare returns 4 things. I think for now only looking at dif to the general form
			result = result[1]
			result = result.replace('?', '')
			result = result.replace('\n', '')

			diff = len(result) - result.count(' ')
			list_of_diffs.append(diff)
		#list_of_diffs maps to the list of rows in column
		mean = sum(list_of_diffs) / float(len(list_of_diffs)) # to avoid int division

		median,index = median(list_of_diffs)
		IQR, Q1, Q3, I1, I3 = compute_IQR(list_of_diffs)

		outlier_max_range = 1.5*IQR + Q3
		outlier_min_range = 1.5*IQR - Q1

		possible_error_indices = []
		for x in range(len(list_of_diffs)):
			if list_of_diffs[x] < outlier_min_range or list_of_diffs[x] > outlier_max_range:
				possible_error_indices.append(x) 
				#appending indices in column that will have 
		for item in possible_error_indices:
			print column[item]





														


def compute_IQR(L):
	L = sorted(L)
	length = len(L)
	#compute median
	m, i = median(L)
	if m in L: # means odd sized list
		lower = L[0:length/2]
		upper = L[(length/2)+1:]

	else:
		lower = L[0:length/2]
		upper = L[length/2:]
	print upper
	print lower
	Q1, index1 = median(lower)
	Q3, index2 = median(upper)
	IQR = Q3-Q1

	return IQR, Q1, Q3, index1, index2+i

def median(L):
	length = len(L)

	if (length % 2) == 1: 
		return L[length/2], length/2
	else:
		x1 = L[length/2]
		x2 = L[(length/2) - 1]
		return float(x1 + x2)/2, length/2
