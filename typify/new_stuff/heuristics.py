# heuristics.py

# this file contains all the string heuristics
# that we use to predict what type a string token
# belongs to. They take in a token and a classifier,
# which is a helper class defined in classifier.py

# the process for each heuristic:
# 1. check legality of characters in the token, return 0 if the token doesn't work at all
# 2. create any required temporary variables
# 3. assign points based on category:
#    - 20 points for column name
#    - 30 points for regular expression
#    - 40 points for being a known example
#    - 10 points for a miscellaneous classification
# 4. return name of type being tested and point value (out of 100)

# TODO massively simplify these
# I think possible values should be taken totally out
# example lists in features.py should also be much shorter
# time complexity has been getting pretty bad lately

NAME_LENGTH = 7
NUM_NAME_SPACES = 1.5
LOCATION_LENGTH = 9
NUM_LOCATION_SPACES = 1

FULL_NAME_POS      = 0
FIRST_NAME_POS     = 1
LAST_NAME_POS      = 2
DATESTRING_POS     = 3
FULL_ADDRESS_POS   = 4
STREET_ADDRESS_POS = 5
CITY_STATE_POS     = 6
EMAIL_POS          = 7
LOCATION_POS       = 8
DESCRIPTION_POS    = 9
URL_POS            = 10
CITY_POS           = 11
STATE_POS          = 12

def full_name_heuristic(token, typer):
	'''returns a  name heuristic value or negative infinity
	if it definitely isn't a name'''
	split_token = token.split()
	possibles = ['name', 'person']
	value = generic_heuristic(token, typer, possibles, FULL_NAME_POS, split_token)
	if value == 0:
		return 'full name', 0
	# misc part
	misc_value = 0
	lengths = [len(x) for x in split_token]
	avg_len = float(sum(lengths)) / float(len(lengths))
	spaces = len(split_token) - 1
	# account for name length
	misc_value += NAME_LENGTH - abs(avg_len - NAME_LENGTH)
	# account for number of spaces
	misc_value += 2 * (NUM_NAME_SPACES - abs(spaces - NUM_NAME_SPACES))
	misc_value /= 2
	if misc_value > 10:
		misc_value = 10

	return 'full name', value + misc_value

def first_name_heuristic(token, typer):
	'''returns a  first name heuristic value or negative infinity
	if it definitely isn't first a name'''
	split_token = token.split()
	possibles = ['first', 'name']
	value = generic_heuristic(token, typer, possibles, FIRST_NAME_POS, split_token)
	if value == 0:
		return 'first name', 0
	# misc part #############################
	misc_value = 0
	lengths = [len(x) for x in split_token]
	if len(lengths) == 1:
		misc_value = 10

	return 'first name', value + misc_value

def last_name_heuristic(token, typer):
	'''returns a last name heuristic value or negative infinity
	if it definitely isn't a name'''
	split_token = token.split()
	possibles = ['last', 'sur', 'name']
	value = generic_heuristic(token, typer, possibles, LAST_NAME_POS, split_token)
	if value == 0:
		return 'last name', 0
	# misc part
	misc_value = 0
	lengths = [len(x) for x in split_token]
	if len(lengths) == 1:
		misc_value = 10

	return 'last name', value + misc_value

def datestring_heuristic(token, typer):
	'''returns a certainty value for token being a date string
	or zero if it definitely isn't a date string'''
	split_token = token.split()
	possibles = ['date', 'day']
	value = generic_heuristic(token, typer, possibles, DATESTRING_POS, split_token)
	if value == 0:
		return 'datestring', 0
	# misc part
	misc_value = 0
	if len(split_token) == 3:
		misc_value = 10

	return 'datestring', value + misc_value

def full_address_heuristic(token, typer):
	'''returns a certainty value for token being an address
	or zero if it definitely isn't an address'''
	split_token = token.split()
	possibles = ['possibles']
	value = generic_heuristic(token, typer, possibles, FULL_ADDRESS_POS, split_token)
	if value == 0:
		return 'full address', 0
	# misc part
	misc_value = 0
	if len(split_token) in range(9, 12):
		misc_value += 10

	return 'full address', value + misc_value

def street_address_heuristic(token, typer):
	'''returns a certainty value for token being a
	street address or zero if it definitely
	isn't an address'''
	split_token = token.split()
	possibles = ['street', 'address']
	value = generic_heuristic(token, typer, possibles, STREET_ADDRESS_POS, split_token)
	if value == 0:
		return 'street address', 0
	# misc part
	misc_value = 0
	if len(split_token) == 2:
		misc_value = 10

	return 'street address', value + misc_value

def city_state_heuristic(token, typer):
	'''returns a certainty value for token being a
	street address or zero if it definitely
	isn't an address'''
	split_token = token.split()
	possibles = ['city', 'state']
	value = generic_heuristic(token, typer, possibles, CITY_STATE_POS, split_token)
	if value == 0:
		return 'city state', 0
	# misc part
	misc_value = 0
	if len(split_token) == 2:
		misc_value += 5
		if len(split_token[1]) == 2:
			misc_value += 5
	
	return 'city state', value + misc_value

def email_heuristic(token, typer):
	'''returns a certainty value for token being an email
	or zero if it definitely isn't an email'''
	split_token = token.split()
	possibles = ['address', 'email']
	value = generic_heuristic(token, typer, possibles, EMAIL_POS, split_token)
	if value == 0:
		return 'email', 0
	# misc part
	misc_value = 0
	if '@' in token:
		misc_value = 10

	return 'email', value + misc_value

def location_heuristic(token, typer):
	'''returns a certainty value for token being a location
	or zero if it definitely isn't a location'''
	split_token = token.split()
	possibles = ['location', 'place', 'country', 'county', 'territory', 'district', 'region', 'zone', 'area', 'division', 'neighborhood', 'locality', 'sector']
	value = generic_heuristic(token, typer, possibles, LOCATION_POS, split_token)
	if value == 0:
		return 'location', 0
	# misc part
	misc_value = 0
	lengths = [len(x) for x in split_token]
	avg_len = float(sum(lengths)) / float(len(lengths))
	spaces = len(split_token) - 1
	# account for number of spaces
	misc_value += NUM_LOCATION_SPACES - abs(spaces - NUM_LOCATION_SPACES)
	# account for location length
	misc_value += LOCATION_LENGTH - abs(avg_len - LOCATION_LENGTH)
	if misc_value < 0:
		misc_value = 0

	return 'location', value + misc_value

def description_heuristic(token, typer):
	'''returns a certainty value for token being a description
	or zero if it definitely isn't a description'''
	split_token = token.split()
	possibles = ['des', 'note', 'rep', 'sum', 'exp']
	value = generic_heuristic(token, typer, possibles, DESCRIPTION_POS, split_token)
	if value == 0:
		return 'description', 0
	# misc part
	misc_value = 0
	len_split_token = len(split_token)
	if len_split_token > 10:
		misc_value += 10
	else:
		misc_value += len_split_token

	return 'description', value + misc_value

def url_heuristic(token, typer):
	'''returns a certainty value for token being a url
	or zero if it definitely isn't a url'''
	split_token = token.split()
	possibles = ['url', 'web', 'address']
	value = generic_heuristic(token, typer, possibles, URL_POS, split_token)
	if value == 0:
		return 'url', 0
	# misc part
	misc_value = 0
	if 'www' in token:
		misc_value = 10

	return 'url', value + misc_value

def city_heuristic(token, typer):
	'''returns a certainty value for token being a
	city or zero if it definitely
	isn't an city'''
	split_token = token.split()
	possibles = ['city', 'town', 'village', 'municipality']
	value = generic_heuristic(token, typer, possibles, CITY_POS, split_token)
	if value == 0:
		return 'city', 0
	# misc part
	misc_value = 0
	if len(token.split()) == 1:
		misc_value += 10

	return 'city', value + misc_value

def state_heuristic(token, typer):
	'''returns a certainty value for token being a
	state or zero if it definitely
	isn't an state'''
	split_token = token.split()
	possibles = ['state', 'province', 'prefecture', 'territory']
	# main part
	value = generic_heuristic(token, typer, possibles, STATE_POS, split_token)
	if value == 0:
		return 'state', 0
	# misc part
	misc_value = 0
	if len(split_token) in [1, 2]:
		misc_value += 10

	return 'state', value + misc_value

def generic_heuristic(token, typer, possibles, pos, split_token):
	'''returns a certainty value for token being a
	certain type'''
	my_typer = typer.heuristic_classifiers[pos]
	
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))

	#check if it can't be the type
	if not my_typer.can_be(char_val_list):
		return 0

	value = 0

	# check column name
	for x in possibles:
		if x in typer.curr_col_name.lower():
			value += 20
			break

	#account for the form of the token
	if my_typer.has_form(token):
		value += 30

	# check examples
	for word in split_token:
		if my_typer.is_a(word):
			value += 40
			break

	return value


def repetition_heuristic(column, tipe):
	'''returns a heuristic value based on the amount of repetition in the column
	if the column doesn't already have a strong classification'''
	# TODO figure out what to do with this
	# it's a bit redundant
	value = 0
	length = len(column)

	if tipe in ['full name', 'full address', 'street address', 'city state', 'email']:
		return value

	token_dict = {}
	for elem in column:
		if not token_dict.has_key(elem):
			token_dict[elem] = 0
		token_dict[elem] += 1

	distinct_vals = len(token_dict.keys())
	if float(length)/distinct_vals >= 10:
		value += 100

	return value


def propname_city(token, typer):
	'''this is not really a heuristic of the same form as the others; it functions
	as a tie breaker'''
	# get the right classifier
	# TODO implement
	my_typer = typer.heuristic_classifiers[FULL_NAME_POS]

	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	split_token = token.split()
	len_split_token = len(split_token)

	#check if it can't be a description
	if not my_typer.can_be(char_val_list):
		return 'description', 0

	# main part #####################
	value = 0

	# check column name
	if 'description' in typer.curr_col_name.lower():
		value += 10
	elif 'note' in typer.curr_col_name.lower():
		value += 10

	#account for the form of the token
	if my_typer.has_form(token):
		value += 20

	# looking at format of individual words
	for word in split_token:
		if my_typer.is_a(word.lower()):
			value += 50
			break

	# misc part #############################
	misc_value = 0
	# account for description length
	# using number of spaces
	if len_split_token > 10:
		misc_value += 10
	else:
		misc_value += len_split_token

	return 'description', value + misc_value

name_heuristics = [full_name_heuristic, first_name_heuristic, last_name_heuristic,
				   city_state_heuristic, city_heuristic, state_heuristic]

string_heuristics = [datestring_heuristic, full_address_heuristic, street_address_heuristic,
					 email_heuristic, location_heuristic, description_heuristic, url_heuristic]

heuristics = {'name': name_heuristics, 'string': string_heuristics}