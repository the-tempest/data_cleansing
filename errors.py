from secrets import password, port, database, user, host, path

execfile(path + "error_detection_number.py")
execfile(path + "error_form_detection.py")
execfile(path + "didYouMean.py")
numeric_classes = ['date', 'longitude', 'latitude', 'number', 'zip', 'phone_number', 'ip', 'year', 'isbn']
names = ['full name', 'first name', 'last name', 'datestring',
				'full address', 'street address', 'city state', 'email',
				'location', 'description', 'url', 'city', 'state']

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
		dict = {}
		dict_errors  = self.make_other_format()
		for c in dict_errors:
			column = c
			l = []
			for index in column:
				s= ""
				if column[index]!=[]:
					for error in column[index]:
						s = s + " " + str(error)
				#can make more calls to other functions here
				l.append(s)
			dict[c] = l
		return dict
	
	# essentially we are using inference rules, not really machine learning, but hardcoding ideas into the code
	def error_information_generator(self, type, errors):
		''' We want to categorize the reasons for error as they are grouped by 
		error types. For dates if we have range, then values too large, number format, then format off'''
		#errors is a string of errors corresponding to the token
		
		l = errors.split()
		switcher = self.returns_switcher(type)
		#---the below section is the same for pretty much all of the error description functions
		s = "" #this is the string that will eventually get returned
		i = 0
		for i in l:
			if i ==0:
				s = s + switcher.get(i)
				i+=1
			else:
				s = s + " and " + switcher.get(i)		
	
	
	
	
	def returns_switcher(self, type):
		numeric_classes = ['date', 'longitude', 'latitude', 'number', 'zip', 'phone_number', 'ip', 'year', 'isbn']
		decider{'date':"", 'longitude':"", 'latitude':"", 'number':"",'zip':"",'phone_number':"", 'ip':"", 'year':"", 'isbn':""}
		decider['date'] = {"range check" : "probably not applicable", #so far the only values that can be out of range are amounts like age and weigh
					"misclassified number": "misclassified number",
					"number format check": "the format of this date may be off a bit"
					}
		
		decider['longitude'] = {"range check" : "The location of this longitude latitude value is outside of the general range of the group", #so far the only values that can be out of range are amounts like age and weigh
								"misclassified number": "misc",
								"number format check": "There is probably a typo amongst any other mistakes"
					}
		decider['latitude']= {"range check" : "The location of this longitude latitude value is outside of the general range of the group", #so far the only values that can be out of range are amounts like age and weigh
							"misclassified number": "misc",
							"number format check": "There is probably a typo amongst any other mistakes"
					}
		decider['number']= {"range check" : "Out of range", #so far the only values that can be out of range are amounts like age and weigh
							"misclassified number": "misc",
							"number format check": "the format of the number falls out of the usual for entries in the column"
							}
		decider['zip'] = decider['number']
		decider['phone_number'] = {"range check" : "the phone number seems to be outside of the usual geographical area of the majority", #so far the only values that can be out of range are amounts like age and weigh
							"misclassified number": "misc",
							"number format check": "possibly the phone_number is incorrectly formatted"
							}
		decider['ip'] = decider['number']
		decider['year'] = decider['number']
		decider['isbn'] = {"range check" : "", #so far the only values that can be out of range are amounts like age and weigh
							"misclassified number": "misc",
							"number format check": "there is probably a typo"
							}
		

	def string_correction(self, token, errors):
		decider = {}
		names = ['full name', 'first name', 'last name', 'datestring',
				'full address', 'street address', 'city state', 'email',
				'location', 'description', 'url', 'city', 'state']
		
		decider = {'':}
		
		
	def format_into_binary(errors):
		'''this function takes in a list of errors and returns a string of numbers that represent that error type.
		This ability to represent all the errors as a binary sequence is useful in deriving additional meaning from 
		the combination of errors. It could be that the combination of errors means more than this distinct parts'''
		
		
											
		
					
		
						
					
					
				
					
					
	
		
	
		
		