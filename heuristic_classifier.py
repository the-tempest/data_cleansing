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

	def classify(self, token, classification):
		'''takes in a token and returns
		a list of predictions'''
		certainties = {}
		for f in heuristics[classification]:
			tipe, value = f(token, self)
			certainties[tipe] = value
		top_score = dict_max(certainties)
		return top_score

	def build_heuristic_classifiers(self):
		'''builds the self.column_classifiers data member by creating classifier objects created
		by classifier(name of the type, possible ascii values in the type string, list of the known condensed forms)'''
		# TODO complete classifiers
		self.heuristic_classifiers = []

		# names
		names = ['full name', 'first name', 'last name', 'datestring',
				'full address', 'street address', 'city state', 'email',
				'location', 'description', 'url', 'city', 'state']

		# possible values
		datestring_pv = [32, 44, 46] + ASCII_NUMS + ASCII_UPPER + ASCII_LOWER
		email_pv = [43, 45, 46, 64, 95] + ASCII_NUMS + ASCII_UPPER + ASCII_LOWER
		description_pv = ASCII_PRINTABLE
		url_punc = [33, 58, 59, 61, 63, 91, 93, 95, 126] + [x for x in range(35, 48)]
		url_pv = ASCII_LOWER + ASCII_UPPER + ASCII_NUMS + url_punc
		possible_values = [ASCII_NAME, ASCII_NAME, ASCII_NAME, datestring_pv,
					 ASCII_ADDRESS, ASCII_ADDRESS, ASCII_NAME, email_pv,
					 ASCII_NAME, description_pv, url_pv, ASCII_NAME, ASCII_NAME]
		# TODO better city and state pv

		# regular expressions
		#fn_regex = r'''^[-.a-zA-Z']*?,?\s(?:[-a-zA-Z']*\.?\s)*?[-a-zA-Z']*\.?$'''
		na_regex = [r'''^[A-Z][a-z'-]+$''']
		#ds_regex = r'''^(?:[A-Z][a-zA-Z]*\.?,?\s)?(?:[0-3][0-9]\s)?[A-Z][a-zA-Z]*\.?,?\s(?:[0-3][0-9]\.?,?\s)?[0-9]*$'''
		#fa_regex = r'''^(?:[Oo][Nn][Ee]|[0-9-]*[a-zA-Z]?)\s+(?:[NSEW]\.?[NSEW]?\.?\s+|(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+)?(?:\d*(?:[SNRTsnrt][TDHtdh])?(?:\s+[a-zA-Z'-]*)?|(?:[a-zA-Z'-]*\s+)*?(?:[a-zA-Z'-]*))\.?(?:\s+\d*)?,?(?:\s+[NSEW]\.?[NESW]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])?)?(?:\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|\s+(?:[a-zA-Z][a-z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?(?:\s+(?:[#]\s*)?\w*(?:[-/: ]\w*)?))?,?\s(?:[a-zA-Z'-]*\s)*?[a-zA-Z'-]*,?\s[a-zA-Z]*,?\s(?:\d{5}|\d{5}(?:\s|[.-])?\d{4})(?:,?\s[A-Za-z'-]*)*$'''
		#sa_regex = r'''^(?:[Oo][Nn][Ee]|[0-9-]*[a-zA-Z]?)\s+(?:[NSEW]\.?[NSEW]?\.?\s+|(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+)?(?:\d*(?:[SNRTsnrt][TDHtdh])?(?:\s+[a-zA-Z'-]*)?|(?:[a-zA-Z'-]*\s+)*?(?:[a-zA-Z'-]*))\.?(?:\s+\d*)?,?(?:\s+[NSEW]\.?[NESW]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])?)?(?:\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|\s+(?:[a-zA-Z][a-z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?(?:\s+(?:[#]\s*)?\w*(?:[-/: ]\w*)?))?$'''
		#cs_regex = r'''^(?:[a-zA-Z'-]*\s)*?[a-zA-Z'-]*,?\s[a-zA-Z]*$'''
		#em_regex = r'''^\S*?@\S*?(?:\.\S*?)+$'''
		#lo_regex = r'''^(?:[A-Z][a-z'-]*\s)*?(?:[A-Z][a-z'-]*)$'''
		#de_regex = r'''^(?:["'<-]?[A-Za-z0-9'-]+[>"',;:-]?(?:\s|[.?!]\s+))+$'''
		#ur_regex = r'''^\S*?.\S*'''
		regex = [FULL_NAME_REGEXS, FIRST_NAME_REGEXS, LAST_NAME_REGEXS, DATESTRING_REGEXS,
				FULL_ADDRESS_REGEXS, STREET_ADDRESS_REGEXS, CITYSTATE_REGEXS, EMAIL_REGEXS,
				LOCATION_REGEXS, DESCRIPTION_REGEXS, URL_REGEXS, na_regex, na_regex]
		# TODO better regex for city and state


		# known examples
		full_name_ex      = COMMON_PREFIXES + COMMON_SUFFIXES + COMMON_FIRST_NAMES + COMMON_LAST_NAMES
		first_name_ex     = COMMON_PREFIXES + COMMON_FIRST_NAMES
		last_name_ex      = COMMON_SUFFIXES + COMMON_LAST_NAMES
		datestring_ex     = COMMON_DATE_NAMES + COMMON_DATE_ABBREV
		full_address_ex   = COMMON_ADDRESS_NAMES + COMMON_ADDRESS_FEATURES + COMMON_STATEPROV_ABBREV + COMMON_CITIES
		street_address_ex = COMMON_ADDRESS_NAMES + COMMON_ADDRESS_FEATURES
		city_state_ex     = COMMON_STATEPROV_ABBREV + COMMON_CITIES
		email_ex          = COMMON_URL_EXTENSIONS + COMMON_EMAIL_DOMAINS
		location_ex       = COMMON_CITIES + COMMON_LOCATION_FEATURES
		description_ex    = COMMON_ADJECTIVES
		url_ex            = COMMON_URL_EXTENSIONS + COMMON_URL
		city_ex           = COMMON_CITIES
		state_ex          = COMMON_STATES
		known_examples = [full_name_ex, first_name_ex, last_name_ex, datestring_ex,
						  full_address_ex, street_address_ex, city_state_ex, email_ex,
						  location_ex, description_ex, url_ex, city_ex, state_ex]

		for i in range(len(names)):
			curr = classifier(names[i],
							  possible_values[i],
							  regex[i],
							  known_examples[i])
			self.heuristic_classifiers.append(curr)