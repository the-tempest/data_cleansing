from secrets import password, port, database, user, host, path

execfile(path + "error_detection_number.py")
execfile(path + "error_form_detection.py")

numeric_classes = ['date', 'longitude', 'latitude', 'number', 'zip', 'phone_number', 'ip', 'year', 'isbn']


class error_detection:

	def __init__(self, table):
		self.t = table
		self.ed ={}
		self.ec = []
		


	def find_table_errors(self,errors_to_check_list):
		self.ec = errors_to_check_list
		form_detective = error_form_detector(self.t)
		number_detective = error_detector_number(self.t)
		error_dictionary = {}
		i = 0
		for column in self.t.columns:
			for item in errors_to_check_list[i]:
				if column.colName in numeric_classes:
					list_of_errors = self.numeric_error_switcher(number_detective, item, column)
					error_dictionary[column.colName][item] = list_of_errors #may want to modify so as to go by
					#column.colName, index , List of errors

				else: # if we get a third catagory not numbers or stirngs we need to change this
					list_of_errors = self.string_error_switcher(item, column)
					error_dictionary[column.colName][item] = list_of_errors
			i+=1

		self.ed = error_dictionary
		return error_dictionary

	def numeric_error_switcher(self, detective, error_string, curr_column):
		switcher = {"range check": detective.range_check(curr_column.rows),
					"misclassified number": detective.misclassified_number(curr_column), # as in the heuristic incorrectly classified
					"number format check": detective.number_format_check(curr_column)}
		


		return switcher.get(error_string, )

	def string_error_switcher(self, detective, error_string, curr_column):
		switcher = {"format checks": detective.format_checks(curr_column.rows),
					"email check": detective.email_check(curr_column),
					"column duplications": detective.cluster_rows(curr_column.rows)}

		return switcher.get(error_string, ) # second argument blank so that if trying to call a numeric error checker on a non numeric column	
	
	def make_other_format(self):
		''' Notice that the format of the first dictionary called ed goes by
		column Name, error type and then list of indices; this function converts from that
		format to a dictionary organized by column Name, index, list of errors'''
		# dictionary organized by column.colName, index, list of errors
		dict_other_format= {}
		i = 0
		for c in self.ed:
			dict_col = {}# matching indices and lists of errors associated
			if c.colName in numeric_classes:	
				for item in self.ec[i]:
					for index in self.ed[c.colName][item]:
						if dict_col[index] ==None:
							dict_col[index] = item
						else:
							dict_col[index].append(item)
			dict_other_format.append(dict_col)
			i +=1
					
					
		return dict_other_format	
				
		
	def info_for_user(self):
		
		i = 0
		dict_errors  = self.make_other_format()
		for c in dict_errors:
			column = c
			for index in column:
				if column[index]!=[]:
					for error in column[index]:
						s = ""
						s = 0
#	def date_errors(self):
		
		


#	def 
					
		
					
		
						
					
					
				
					
					
	
		
	
		
		