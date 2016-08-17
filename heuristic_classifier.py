# heuristic_classifier.py
# this defines a heuristic_classifier class which
# takes in a token and returns a prediction
# based on regular expressions and such

import mysql.connector, os, re
from secrets import path
execfile(path+"typify/new_stuff/heuristics.py")
execfile(path+"typify/helper.py")
execfile(path+"typify/features/features.py")
execfile(path+"typify/classifier.py")
execfile(path+'table.py')

ASCII_NUMS = [n for n in range(48, 58)]
ASCII_UPPER = [n for n in range(65, 91)]
ASCII_LOWER = [n for n in range(97, 123)]
ASCII_PRINTABLE = [n for n in range(32, 128)]
ASCII_ADDRESS = [32, 39, 44, 45, 46] + ASCII_NUMS + [58, 59] + ASCII_UPPER + ASCII_LOWER
ASCII_NAME = [32, 44, 45, 46] + ASCII_UPPER + ASCII_LOWER


class heuristic_classifier:
	def __init__(self):
		self.build_heuristic_classifiers()
		self.curr_col_name = ''

	def classify(self, token, classification):
		'''takes in a token and returns
		a list of predictions'''
		certainties = {}
		for f in heuristics:
			tipe, value = f(token, self)
			certainties[tipe] = value
		top_score = dict_max(certainties)
		return top_score

	def build_heuristic_classifiers(self):
		'''builds the self.column_classifiers data member by creating classifier objects created
		by classifier(name of the type, possible ascii values in the type string, list of the known condensed forms)'''
		# TODO complete classifiers
		self.heuristic_classifiers = []

		# TODO add all types

		# names
		names = ['full name', 'first name', 'last name', 'datestring',
				'full address', 'street address', 'city state', 'email',
				'description', 'url', 'city', 'state',
				'date', 'longitude', 'latitude', 'number', 'zip', 'phone_number',
				'ip', 'year', 'isbn']

		# TODO possible values for numeric types
		# TODO better city and state pv
		# possible values
		datestring_pv = [32, 44, 46] + ASCII_NUMS + ASCII_UPPER + ASCII_LOWER
		email_pv = [43, 45, 46, 64, 95] + ASCII_NUMS + ASCII_UPPER + ASCII_LOWER
		description_pv = ASCII_PRINTABLE
		url_punc = [33, 58, 59, 61, 63, 91, 93, 95, 126] + [x for x in range(35, 48)]
		url_pv = ASCII_LOWER + ASCII_UPPER + ASCII_NUMS + url_punc
		date_pv = '' # numbers and 
		longitude_pv = '' # numbers and 
		latitude_pv = '' # numbers and 
		number_pv = '' # numbers and 
		zip_pv = '' # numbers and 
		phone_pv = '' # numbers and 
		ip_pv = '' # numbers and 
		year_pv = '' # numbers and apostrophe
		isbn_pv = '' # numbers and
		possible_values = [ASCII_NAME, ASCII_NAME, ASCII_NAME, datestring_pv,
					 ASCII_ADDRESS, ASCII_ADDRESS, ASCII_NAME, email_pv,
					 description_pv, url_pv, ASCII_NAME, ASCII_NAME,
					 date_pv, longitude_pv, latitude_pv, number_pv, zip_pv, phone_number,
					 ip_pv, year_pv, isbn_pv]
		

		# regular expressions
		# TODO regexs for city and state    
		regex = [FULL_NAME_REGEXS, FIRST_NAME_REGEXS, LAST_NAME_REGEXS, DATESTRING_REGEXS,
				FULL_ADDRESS_REGEXS, STREET_ADDRESS_REGEXS, CITYSTATE_REGEXS, EMAIL_REGEXS,
				DESCRIPTION_REGEXS, URL_REGEXS, [], [],
				DATE_REGEXS, LONGITUDE_REGEXS, LATITUDE_REGEXS,
				NUMBER_REGEXS, ZIP_REGEXS, PHONE_REGEXS,
				IP_REGEXS, YEAR_REGEXS, ISBN_REGEXS]

		# known examples
		# TODO examples for numerics
		full_name_ex      = COMMON_PREFIXES + COMMON_SUFFIXES + COMMON_FIRST_NAMES + COMMON_LAST_NAMES
		first_name_ex     = COMMON_PREFIXES + COMMON_FIRST_NAMES
		last_name_ex      = COMMON_SUFFIXES + COMMON_LAST_NAMES
		datestring_ex     = COMMON_DATE_NAMES + COMMON_DATE_ABBREV
		full_address_ex   = COMMON_ADDRESS_NAMES + COMMON_ADDRESS_FEATURES + COMMON_STATEPROV_ABBREV + COMMON_CITIES
		street_address_ex = COMMON_ADDRESS_NAMES + COMMON_ADDRESS_FEATURES
		city_state_ex     = COMMON_STATEPROV_ABBREV + COMMON_CITIES
		email_ex          = COMMON_URL_EXTENSIONS + COMMON_EMAIL_DOMAINS
		description_ex    = COMMON_ADJECTIVES
		url_ex            = COMMON_URL_EXTENSIONS + COMMON_URL
		city_ex           = COMMON_CITIES
		state_ex          = COMMON_STATES
		date_ex           = []
		longitude_ex      = []
		latitude_ex       = []
		number_ex         = []
		zip_ex            = []
		phone_ex          = []
		ip_ex             = []
		year_ex           = []
		isbn_ex           = []
		known_examples = [full_name_ex, first_name_ex, last_name_ex, datestring_ex,
						  full_address_ex, street_address_ex, city_state_ex, email_ex,
						  description_ex, url_ex, city_ex, state_ex
						  date_ex, longitude_ex, latitude_ex,
						  number_ex, zip_ex, phone_ex,
						  ip_ex, year_ex, isbn_ex]

		for i in range(len(names)):
			curr = classifier(names[i],
							  possible_values[i],
							  regex[i],
							  known_examples[i])
			self.heuristic_classifiers.append(curr)