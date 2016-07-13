# heuristics.py

# this file contains all the string heuristics
# that we use to predict what type a string token
# belongs to. They take in a token and a classifier,
# which is a helper class defined in classifier.py
# TODO these need to be merged with the numeric 
# heuristics somehow

#TODO - IMPLEMENT FURTHER FEATURES
#Adjacent Column Names
#TODO - THINK OF MORE FEATURES TO IMPLEMENT

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

def full_name_heuristic(token, typer):
	'''returns a  name heuristic value or negative infinity
	if it definitely isn't a name'''
	# get the right classifier
	my_class = typer.column_classifiers[FULL_NAME_POS]

	# build a list of characteristics that will be used throughout the rest of the heuristic
	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()
	lengths = [len(x) for x in temp]
	avg_len = float(sum(lengths)) / float(len(lengths))
	spaces = len(temp) - 1

	#check if it can't be a name
	if not my_class.can_be(char_val_list):
		return value

	# check column name
	if 'name' in typer.column_name.lower():
		value += 10

	# counting common features of names
	#if my_class.contains_a(token.lower()):
	#	value += 1

	# account for name length
	value += NAME_LENGTH - abs(avg_len - NAME_LENGTH)

	#account for the form of the token
	if my_typer.has_form(token):
		value += 20

	# looking at format of individual words
	for word in temp:
		#check for common names
		#TODO: Need to change because it will flag all single names as full names
		if (my_typer.is_a(word.lower()) and spaces > 0):
			value += 50
		
	# account for number of spaces
	value += NUM_SPACES - abs(spaces - NUM_NAME_SPACES)
	
	return 'full name', value

def first_name_heuristic(token, typer):
	'''returns a  first name heuristic value or negative infinity
	if it definitely isn't a name'''
	# get the right classifier
	my_typer = typer.column_classifiers[FIRST_NAME_POS]

	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()
	lengths = [len(x) for x in temp]

	# check if it can't be a name
	if not my_typer.can_be(char_val_list):
		return value

	# check column name
	if 'first' in typer.column_name.lower():
		value += 10
	if 'name' in typer.column_name.lower():
		value += 10

	# counting common features of names
	#if my_typer.contains_a(token.lower()):
	#	value += 1

	# account for name length
	if len(lengths) == 0:
		return 0
	if len(lengths) == 1:
		value += 10

	#account for the form of the token
	if my_typer.has_form(token):
		value += 20	

	# check for common names
	if my_typer.is_a(token.lower()):
		value += 50

	return 'first name', value

def last_name_heuristic(token, typer):
	'''returns a last name heuristic value or negative infinity
	if it definitely isn't a name'''
	# get the right classifier
	my_typer = typer.column_classifiers[LAST_NAME_POS]

	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()
	lengths = [len(x) for x in temp]

	# check if it can't be a name
	if not my_typer.can_be(char_val_list):
		return value

	# check column name
	if 'last' in typer.column_name.lower():
		value += 10
	if 'sur' in typer.column_name.lower():
		value += 10
	if 'name' in typer.column_name.lower():
		value += 10

	# counting common features of names
	#if my_typer.contains_a(token.lower()):
	#	value += 1

	# account for name length
	if len(lengths) == 0:
		return 0
	if len(lengths) == 1:
		value += 10

	#account for the form of the token
	if my_typer.has_form(token):
		value += 20	

	# check for common names
	if my_typer.is_a(token.lower()):
		value += 50

	return 'last name', value

def datestring_heuristic(token, typer):
	'''returns a certainty value for token being a date string
	or zero if it definitely isn't a date string'''
	# get the right classifier
	my_typer = typer.column_classifiers[DATESTRING_POS]

	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()

	#check if it can't be a datestring
	if not my_typer.can_be(char_val_list):
		return value

	# check column name
	if 'date' in typer.column_name.lower():
		value += 10

	# counting common features of date strings
	#if my_typer.contains_a(token.lower()):
	#	value += 1

	# account for datestring length
	if len(temp) == 3:
		value += 10
	
	#account for the form of the token
	if my_typer.has_form(token):
		value += 20	

	for word in temp:
		if my_typer.is_a(word):
			value += 50

	return 'datestring', value

def full_address_heuristic(token, typer):
	'''returns a certainty value for token being an address
	or zero if it definitely isn't an address'''
	# get the right classifier
	my_typer = typer.column_classifiers[FULL_ADDRESS_POS]


	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()

	#check if it can't be a full address
	if not my_typer.can_be(char_val_list):
		return value

	# check column name
	if 'add' in typer.column_name.lower():
		value += 5
		if 'address' in typer.column_name.lower():
			value += 5

	# counting common features of address strings
	#if my_typer.contains_a(token.lower()):
	#	value += 1
	
	#account for the form of the token
	if my_typer.has_form(token):
		value += 20	

	for word in temp:
		if my_typer.is_a(word):
			value += 20

	return 'full address', value

def street_address_heuristic(token, typer):
	'''returns a certainty value for token being a
	street address or zero if it definitely
	isn't an address'''
	# get the right classifier
	my_typer = typer.column_classifiers[STREET_ADDRESS_POS]

	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()

	#check if it can't be a street address
	if not my_typer.can_be(char_val_list):
		return value

	# check column name
	if 'street' in typer.column_name.lower():
		value += 10
	if 'add' in typer.column_name.lower():
		value += 5
		if 'address' in typer.column_name.lower():
			value += 5

	# counting common features of address strings
	#if my_typer.contains_a(token.lower()):
	#	value += 1
	
	#account for the form of the token
	if my_typer.has_form(token):
		value += 20	

	# check examples
	for word in temp:
		if my_typer.is_a(word):
			value += 20

	return 'street address', value

def city_state_heuristic(token, typer):
	'''returns a certainty value for token being a
	street address or zero if it definitely
	isn't an address'''
	# get the right classifier
	my_typer = typer.column_classifiers[CITY_STATE_POS]

	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()

	#check if it can't be a city state
	if not my_typer.can_be(char_val_list):
		return value

	# check column name
	if 'city' in typer.column_name.lower():
		value += 10
	if 'state' in typer.column_name.lower():
		value += 5
		
	# counting common features of address strings
	#if my_typer.contains_a(token.lower()):
	#	value += 1

	#account for the form of the token
	if my_typer.has_form(token):
		value += 20	

	# check examples
	for word in temp:
		if my_typer.is_a(word):
			value += 10

	return 'city state', value

def email_heuristic(token, typer):
	'''returns a certainty value for token being an email
	or zero if it definitely isn't an email'''
	# get the right classifier
	my_typer = typer.column_classifiers[EMAIL_POS]

	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()

	#check if it can't be an email
	if not my_typer.can_be(char_val_list):
		return value
	if '@' not in token:
		return value
	else:
		value += 20

	# check column name
	if 'address' in typer.column_name.lower():
		value += 5
	if 'email' in typer.column_name.lower():
		value += 10

	# counting common features of emails
	#if my_typer.contains_a(token.lower()):
	#	value += 1

	#account for the form of the token
	if my_typer.has_form(token):
		value += 20	

	# check examples
	for word in temp:
		if my_typer.is_a(word):
			value += 10
	
	return 'email', value

def location_heuristic(token, typer):
	'''returns a certainty value for token being a location
	or zero if it definitely isn't a location'''
	# get the right classifier
	my_typer = typer.column_classifiers[LOCATION_POS]

	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()
	lengths = [len(x) for x in temp]
	if len(lengths) == 0:
		return 0
	avg_len = float(sum(lengths)) / float(len(lengths))
	spaces = len(temp) - 1

	#check if it can't be a location
	if not my_typer.can_be(char_val_list):
		return value

	# check column name
	if 'location' in typer.column_name.lower():
		value += 10
	elif 'place' in typer.column_name.lower():
		value += 10
	elif 'country' in typer.column_name.lower():
		value += 10

	# counting common features of locations
	#if my_typer.contains_a(token.lower()):
	#	value += 1

	# account for location length
	value += LOCATION_LENGTH - abs(avg_len - LOCATION_LENGTH)

	#account for the form of the token
	if my_typer.has_form(token):
		value += 20	

	# looking at format of individual words
	for word in temp:
		if my_typer.is_a(word.lower()):
			value += 50
	
	# account for number of spaces
	value += NUM_LOCATION_SPACES - abs(spaces - NUM_LOCATION_SPACES)
	
	return 'location', value

def description_heuristic(token, typer):
	'''returns a certainty value for token being a description
	or zero if it definitely isn't a description'''
	# get the right classifier
	my_typer = typer.column_classifiers[DESCRIPTION_POS]

	value = 0
	char_val_list = []
	for char in token: 
		char_val_list.append(ord(char))
	split_token = token.split()
	len_split_token = len(split_token)

	#check if it can't be a description
	if not my_typer.can_be(char_val_list):
		return value

	# check column name
	if 'description' in typer.column_name.lower():
		value += 10
	if 'note' in typer.column_name.lower():
		value += 10

	# counting common features of descriptions
	#if my_typer.contains_a(token.lower()):
	#	value += 1

	# account for description length
	# using number of spaces
	# maxes out at 100
	# since that's where it normalizes
	if len_split_token == 0:
		value = 0
	if len_split_token >= 100:
		value = 100
	else:
		value += len_split_token

	#account for the form of the token
	if my_typer.has_form(token):
		value += 20	

	return 'description', value


heuristics = [full_name_heuristic, first_name_heuristic, last_name_heuristic,
				datestring_heuristic, full_address_heuristic, street_address_heuristic,
				city_state_heuristic, email_heuristic, location_heuristic,
				description_heuristic]