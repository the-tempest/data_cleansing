from secrets import password, port, database, user, host, path

execfile(path + "error_detection_number.py")
execfile(path + "error_form_detection.py")

numeric_classes = ['date', 'longitude', 'latitude', 'number', 'zip', 'phone_number', 'ip', 'year', 'isbn']


class error_detection:

	def __init__(self, table):
		self.t = table


	def find_table_errors(self,errors_to_check_list):

		form_detective = error_form_detector(self.t)
		number_detective = error_detector_number(self.t)
		error_dictionary = {}

		for column in self.t.columns:
			for item in errors_to_check_list:

				if column.colName in numeric_classes:
					list_of_errors = self.numeric_error_switcher(number_detective, item, column)
					error_dictionary[column.colName][item] = list_of_errors

				else: # if we get a third catagory not numbers or stirngs we need to change this
					list_of_errors = self.string_error_switcher(item, column)
					error_dictionary[column.colName][item] = list_of_errors



		return error_dictionary

	def numeric_error_switcher(self, detective, error_string, curr_column):
		switcher = {"range check": detective.range_check(curr_column.rows),
					"misclassified number": detective.misclassified_number(curr_column),
					"number format check": detective.number_format_check(curr_column)  }


		return switcher.get(error_string, )

	def string_error_switcher(self, detective, error_string, curr_column):
		switcher = {"format checks": detective.format_checks(curr_column.rows),
					"email check": detective.email_check(curr_column),
					"column duplications": detective.cluster_rows(curr_column.rows)}

		return switcher.get(error_string, ) # second argument blank so that if trying to call a numeric error checker on a non numeric column	