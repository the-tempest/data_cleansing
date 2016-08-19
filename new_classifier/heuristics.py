# heuristics.py

# this file contains all the string heuristics
# that we use to predict what type a string token
# belongs to. They take in a token and a classifier,
# which is a helper class defined in classifier.py

# the process for each heuristic:
# 1. check legality of characters in the token, return 0 if the token doesn't work at all
# 2. create any required temporary variables
# 3. assign points based on category:
#    - 4 points for column name
#    - 3 points for regular expression
#    - 3 points for being a known example
# 4. return name of type being tested and point value (out of 10)

def full_name_heuristic(token, typer):
	'''returns a certainty value for token being a last name'''
	value = generic_heuristic(token, typer, 'full_name')
	return 'full_name', value

def first_name_heuristic(token, typer):
	'''returns a certainty value for token being a first name'''
	value = generic_heuristic(token, typer, 'first_name')
	return 'first_name', value

def last_name_heuristic(token, typer):
	'''returns a certainty value for token being a last name'''
	value = generic_heuristic(token, typer, 'last_name')
	return 'last_name', value

def datestring_heuristic(token, typer):
	'''returns a certainty value for token being a datestring'''
	value = generic_heuristic(token, typer, 'datestring')
	return 'datestring', value

def full_address_heuristic(token, typer):
	'''returns a certainty value for token being a full address'''
	value = generic_heuristic(token, typer, 'full_address')
	return 'full_address', value

def street_address_heuristic(token, typer):
	'''returns a certainty value for token being a street address'''
	value = generic_heuristic(token, typer, 'street_address')
	return 'street_address', value

def city_state_heuristic(token, typer):
	'''returns a certainty value for token being a city, state'''
	value = generic_heuristic(token, typer, 'city_state')
	return 'city_state', value

def email_heuristic(token, typer):
	'''returns a certainty value for token being an email'''
	value = generic_heuristic(token, typer, 'email')
	return 'email', value

def description_heuristic(token, typer):
	'''returns a certainty value for token being a description'''
	value = generic_heuristic(token, typer, 'description')
	return 'description', value

def url_heuristic(token, typer):
	'''returns a certainty value for token being a url'''
	value = generic_heuristic(token, typer, 'url')
	return 'url', value

def city_heuristic(token, typer):
	'''returns a certainty value for token being a city'''
	value = generic_heuristic(token, typer, 'city')
	return 'city', value

def state_heuristic(token, typer):
	'''returns a certainty value for token being a state'''
	value = generic_heuristic(token, typer, 'state')
	return 'state', value

def date_heuristic(token, typer):
	'''returns a certainty value for token being a date'''
	value = generic_heuristic(token, typer, 'date')
	return 'date', value

def longitude_heuristic(token, typer):
	'''returns a certainty value for token being a longitude'''
	value = generic_heuristic(token, typer, 'longitude')
	return 'longitude', value

def latitude_heuristic(token, typer):
	'''returns a certainty value for token being a latitude'''
	value = generic_heuristic(token, typer, 'latitude')
	return 'latitude', value

def number_heuristic(token, typer):
	'''returns a certainty value for token being a number'''
	value = generic_heuristic(token, typer, 'number')
	return 'number', value

def zip_heuristic(token, typer):
	'''returns a certainty value for token being a zip'''
	value = generic_heuristic(token, typer, 'zip')
	return 'zip', value

def phone_heuristic(token, typer):
	'''returns a certainty value for token being an phone'''
	value = generic_heuristic(token, typer, 'phone_number')
	return 'phone_number', value

def ip_heuristic(token, typer):
	'''returns a certainty value for token being an ip'''
	value = generic_heuristic(token, typer, 'ip')
	return 'ip', value

def year_heuristic(token, typer):
	'''returns a certainty value for token being a year'''
	value = generic_heuristic(token, typer, 'year')
	return 'year', value

def isbn_heuristic(token, typer):
	'''returns a certainty value for token being an isbn'''
	value = generic_heuristic(token, typer, 'isbn')
	return 'isbn', value

def generic_heuristic(token, typer, name):
	'''returns a certainty value for token being a
	certain type'''
	my_classifier = typer.heuristic_classifiers[name]

	#check if it can't be the type
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not my_classifier.can_be(char_val_list):
		return 0

	value = 0
	# check column name
	if my_classifier.check_column_name(typer.curr_col_name):
		value += 4

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
			 city_state_heuristic, email_heuristic, description_heuristic,
			 url_heuristic, city_heuristic, state_heuristic,
			 date_heuristic, longitude_heuristic, latitude_heuristic,
			 number_heuristic, zip_heuristic, phone_heuristic,
			 ip_heuristic, year_heuristic, isbn_heuristic]
