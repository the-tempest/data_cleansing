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
# example lists in features.py should also be much shorter
# time complexity has been getting pretty bad lately


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
	'''returns a certainty value for token being a description'''
	possibles = ['des', 'web', 'rep', 'sum']
	my_classifier = typer.heuristic_classifiers['state']
	value = generic_heuristic(token, typer, my_classifier, possibles)
	return 'city', value

def url_heuristic(token, typer):
	'''returns a certainty value for token being a url'''
	possibles = ['url', 'web', 'address', 'site']
	my_classifier = typer.heuristic_classifiers['state']
	value = generic_heuristic(token, typer, my_classifier, possibles)
	return 'city', value

def city_heuristic(token, typer):
	'''returns a certainty value for token being a city'''
	possibles = ['city', 'town', 'village', 'municipality']
	my_classifier = typer.heuristic_classifiers['state']
	value = generic_heuristic(token, typer, my_classifier, possibles)
	return 'city', value

def state_heuristic(token, typer):
	'''returns a certainty value for token being a state'''
	possibles = ['state', 'province', 'territory']
	my_classifier = typer.heuristic_classifiers['state']
	value = generic_heuristic(token, typer, my_classifier, possibles)
	return 'state', value

def date_heuristic(token, typer):
	'''returns a certainty value for token being a date'''
	possibles = ['date', 'day']
	my_classifier = typer.heuristic_classifiers['date']
	value = generic_heuristic(token, typer, my_classifier, possibles)
	return 'date', value

def longitude_heuristic(token, typer):
	'''returns a certainty value for token being a longitude'''
	possibles = ['longitude']
	my_classifier = typer.heuristic_classifiers['longitude']
	value = generic_heuristic(token, typer, my_classifier, possibles)
	return 'longitude', value

def latitude_heuristic(token, typer):
	'''returns a certainty value for token being a latitude'''
	possibles = ['latitude']
	my_classifier = typer.heuristic_classifiers['latitude']
	value = generic_heuristic(token, typer, my_classifier, possibles)
	return 'latitude', value

def number_heuristic(token, typer):
	'''returns a certainty value for token being a number'''
	possibles = ['number', 'count', 'quantity', 'amount']
	my_classifier = typer.heuristic_classifiers['number']
	value = generic_heuristic(token, typer, my_classifier, possibles)
	return 'number', value

def zip_heuristic(token, typer):
	'''returns a certainty value for token being an ip'''
	possibles = ['zip', 'code']
	my_classifier = typer.heuristic_classifiers['zip']
	value = generic_heuristic(token, typer, my_classifier, possibles)
	return 'zip', value

def phone_heuristic(token, typer):
	'''returns a certainty value for token being an phone'''
	possibles = ['phone', 'number']
	my_classifier = typer.heuristic_classifiers['phone_number']
	value = generic_heuristic(token, typer, my_classifier, possibles)
	return 'phone_number', value

def ip_heuristic(token, typer):
	'''returns a certainty value for token being an ip'''
	possibles = ['ip', 'address']
	my_classifier = typer.heuristic_classifiers['ip']
	value = generic_heuristic(token, typer, my_classifier, possibles)
	return 'ip', value

def year_heuristic(token, typer):
	'''returns a certainty value for token being a year'''
	possibles = ['year']
	my_classifier = typer.heuristic_classifiers['year']
	value = generic_heuristic(token, typer, my_classifier, possibles)
	return 'year', value

def isbn_heuristic(token, typer):
	'''returns a certainty value for token being an isbn'''
	possibles = ['isbn', 'code']
	my_classifier = typer.heuristic_classifiers['isbn']
	value = generic_heuristic(token, typer, my_classifier, possibles)
	return 'isbn', value

def generic_heuristic(token, typer, my_classifier, possibles):
	'''returns a certainty value for token being a
	certain type'''
	
	#check if it can't be the type
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not my_classifier.can_be(char_val_list):
		return 0

	value = 0
	# check column name
	for x in possibles:
		if x in my_classifier.curr_col_name.lower():
			value += 4
			break

	#account for the form of the token
	if my_classifier.has_form(token):
		value += 3

	# check examples
	for word in token.split():
		if my_typer.is_a(word):
			value += 3
			break

	return value
	
heuristics = [full_name_heuristic, first_name_heuristic, last_name_heuristic,
			 datestring_heuristic, full_address_heuristic, street_address_heuristic,
			 city_state_heuristic, email_heuristic,
			 description_heuristic, url_heuristic, city_heuristic,
			 state_heuristic]
