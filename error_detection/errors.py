from secrets import password, port, database, user, host, path
import os
execfile(path + "error_detection/error_detection_number.py")
execfile(path + "error_detection/error_form_detection.py")
execfile(path + "error_detection/didYouMean.py")

execfile(path + "typify/features/regexlib.py")
execfile(path + "typify/features/exampleslib.py")
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
			error_dictionary[column.colName] = {}
			column.forms = self.regex_form_finder(column)
			for error in errors_to_check_list:
				if column.tentClass in numeric_classes:
					list_of_error_indexes = self.numeric_error_switcher(number_detective, error, column)
					error_dictionary[column.colName][error] = list_of_error_indexes #may want to modify so as to go by
					#column.colName, index , List of errors

				else: # if we get a third catagory not numbers or stirngs we need to change this
					list_of_error_indexes = self.string_error_switcher(form_detective, error, column)
					error_dictionary[column.colName][error] = list_of_error_indexes
					#{column_name: {error_type: [list_of_indexes]}}
			i+=1

		self.ed = error_dictionary
		return error_dictionary

	def regex_form_finder(self, column):
		if (column.tentClass == None or column.tentClass == 'misc'):
			return []
		print column.tentClass
		column_rows = column.rows
		column_len = len(column_rows)
		regex_dict = {}
		regex_list = []
		for regex in self.get_regex_list(column.tentClass):
			regex_dict[regex] = 0
			regex_list.append(re.compile(regex))
		for item in column_rows:
			for regexObj in regex_list:
				if regexObj.match(item) != None:
					regex_dict[regexObj.pattern] += 1

		form_list = []
		for key in regex_dict.keys():
			if float(regex_dict[key])/float(column_len) > .05:
				form_list.append(key)

		return form_list

	def get_regex_list(self, classification):
		switcher = {'full name': FULL_NAME_REGEXS, 'first name': FIRST_NAME_REGEXS, 'last name': LAST_NAME_REGEXS, 'datestring': DATESTRING_REGEXS,
					'full address': FULL_ADDRESS_REGEXS, 'street address': STREET_ADDRESS_REGEXS, 'city state': CITYSTATE_REGEXS, 'email': EMAIL_REGEXS, 
					'location': LOCATION_REGEXS, 'description': DESCRIPTION_REGEXS, 'url': URL_REGEXS, 'city': CITY_REGEXS, 'state': STATE_REGEXS,
					'date': DATE_REGEXS, 'longitude': LONGITUDE_REGEXS, 'latitude': LATITUDE_REGEXS, 'number': NUMBER_REGEXS, 'zip': ZIP_REGEXS,
					'ip': IP_REGEXS, 'phone_number': PHONE_REGEXS, 'year': YEAR_REGEXS, 'isbn': ISBN_REGEXS}

		return switcher.get(classification)

	def numeric_error_switcher(self, detective, error_string, curr_column):
		switcher = {"range check": detective.range_check(curr_column.rows),
					"misclassified number": detective.misclassified(curr_column), # as in the heuristic incorrectly classified
					"number format check": detective.number_format_check(curr_column)}

		return switcher.get(error_string)

	def string_error_switcher(self, detective, error_string, curr_column):
		switcher = {"format checks": detective.format_check(curr_column),
					#"email check": detective.email_check(curr_column),
					"column duplications": detective.cluster_rows(curr_column)}

		return switcher.get(error_string) # second argument blank so that if trying to call a numeric error checker on a non numeric column	
	
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
		dyct = {}
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
			dyct[c] = l
		return dyct
	
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
		#numeric_classes = ['date', 'longitude', 'latitude', 'number', 'zip', 'phone_number', 'ip', 'year', 'isbn']
		decider = {'date':"", 'longitude':"", 'latitude':"", 'number':"",'zip':"",'phone_number':"", 'ip':"", 'year':"", 'isbn':""}
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
		
		decider['full name'] = {"format checks": didYouMean(token),
					"email check": detective.email_check(curr_column),
					"column duplications": detective.cluster_rows(curr_column.rows)}
		
		
		
	def format_into_binary(errors):
		'''this function takes in a list of errors and returns a string of numbers that represent that error type.
		This ability to represent all the errors as a binary sequence is useful in deriving additional meaning from 
		the combination of errors. It could be that the combination of errors means more than this distinct parts'''
		
		
											
		
					
		
						
					
					
				
					
					
	
		
	
		
		