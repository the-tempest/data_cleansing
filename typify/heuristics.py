# heuristics.py

# this file contains all the string heuristics
# that we use to predict what type a string token
# belongs to. They take in a token and a classifier,
# which is a helper class defined in classifier.py

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
	my_typer = typer.column_classifiers[FULL_NAME_POS]

	# build a list of characteristics that will be used throughout the rest of the heuristic
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()
	lengths = [len(x) for x in temp]
	if len(lengths) == 0: # it isn't anything if it's an empty string
		return 'full name', 0
	avg_len = float(sum(lengths)) / float(len(lengths))
	spaces = len(temp) - 1

	#check if it can't be a name
	# uses possible values
	if not my_typer.can_be(char_val_list):
		return 'full name', 0

	# main part ###############################################
	value = 0

	# check column name
	if 'name' in typer.curr_col_name.lower():
		value += 10

	#account for the form of the token
	if my_typer.has_form(token):
		value += 30

	# looking at format of individual words
	if spaces > 0:
		for word in temp:
			#check for common names
			if my_typer.is_a(word.lower()):
				value += 25
				break
	if value > 90:
		value = 90

	# misc part #######################################
	# this is different for each heuristic
	misc_value = 0
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
	if it definitely isn't a name'''
	# get the right classifier
	my_typer = typer.column_classifiers[FIRST_NAME_POS]

	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()
	lengths = [len(x) for x in temp]

	# check if it can't be a name
	if not my_typer.can_be(char_val_list):
		return 'first name', 0
	# account for name length
	if len(lengths) == 0:
		return 'first name', 0

	# main part #####################################
	value = 0

	# check column name
	if 'first' in typer.curr_col_name.lower():
		value += 5
	if 'name' in typer.curr_col_name.lower():
		value += 5

	#account for the form of the token
	if my_typer.has_form(token):
		value += 20

	# check for common names
	if my_typer.is_a(token.lower()):
		value += 50

	# misc part #############################
	misc_value = 0
	if len(lengths) == 1:
		misc_value = 10

	return 'first name', value + misc_value

def last_name_heuristic(token, typer):
	'''returns a last name heuristic value or negative infinity
	if it definitely isn't a name'''
	# get the right classifier
	my_typer = typer.column_classifiers[LAST_NAME_POS]

	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()
	lengths = [len(x) for x in temp]

	# check if it can't be a name
	if not my_typer.can_be(char_val_list):
		return 'last name', 0
	if len(lengths) == 0:
		return 'last name', 0

	# main part #####################
	value = 0

	# check column name
	if 'last' in typer.curr_col_name.lower():
		value += 5
	if 'sur' in typer.curr_col_name.lower():
		value += 5
	if 'name' in typer.curr_col_name.lower():
		value += 5
	if value > 10:
		value = 10

	#account for the form of the token
	if my_typer.has_form(token):
		value += 20

	# check for common names
	if my_typer.is_a(token.lower()):
		value += 50

	# misc part ###################
	misc_value = 0
	if len(lengths) == 1:
		misc_value = 10

	return 'last name', value + misc_value

def datestring_heuristic(token, typer):
	'''returns a certainty value for token being a date string
	or zero if it definitely isn't a date string'''
	# get the right classifier
	my_typer = typer.column_classifiers[DATESTRING_POS]

	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()

	#check if it can't be a datestring
	if not my_typer.can_be(char_val_list):
		return 'datestring', 0

	# main part #####################
	value = 0

	# check column name
	if 'date' in typer.curr_col_name.lower():
		value += 10

	# account for datestring length

	#account for the form of the token
	if my_typer.has_form(token):
		value += 20

	for word in temp:
		if my_typer.is_a(word):
			value += 50
			break

	# misc part #####################3
	misc_value = 0
	if len(temp) == 3:
		misc_value = 10

	return 'datestring', value + misc_value

def full_address_heuristic(token, typer):
	'''returns a certainty value for token being an address
	or zero if it definitely isn't an address'''
	# get the right classifier
	my_typer = typer.column_classifiers[FULL_ADDRESS_POS]

	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()

	#check if it can't be a full address
	if not my_typer.can_be(char_val_list):
		return 'full address', 0

	# main part ######################
	value = 0

	# check column name
	if 'add' in typer.curr_col_name.lower():
		value += 5
		if 'address' in typer.curr_col_name.lower():
			value += 5

	#account for the form of the token
	if my_typer.has_form(token):
		value += 20

	# check form
	for word in temp:
		if my_typer.is_a(word):
			value += 50
			break

	# misc part ######################
	misc_value = 0
	# TODO come up with something

	return 'full address', value + misc_value

def street_address_heuristic(token, typer):
	'''returns a certainty value for token being a
	street address or zero if it definitely
	isn't an address'''
	# get the right classifier
	my_typer = typer.column_classifiers[STREET_ADDRESS_POS]

	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()

	#check if it can't be a street address
	if not my_typer.can_be(char_val_list):
		return 'street address', 0

	# main part ######################333
	value = 0

	# check column name
	if 'street' in typer.curr_col_name.lower():
		value += 5
	if 'address' in typer.curr_col_name.lower():
		value += 5

	#account for the form of the token
	if my_typer.has_form(token):
		value += 20

	# check examples
	for word in temp:
		if my_typer.is_a(word):
			value += 50
			break

	# misc part #####################3
	misc_value = 0
	# TODO think of something

	return 'street address', value + misc_value

def city_state_heuristic(token, typer):
	'''returns a certainty value for token being a
	street address or zero if it definitely
	isn't an address'''
	# get the right classifier
	my_typer = typer.column_classifiers[CITY_STATE_POS]

	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()

	#check if it can't be a city state
	if not my_typer.can_be(char_val_list):
		return 'city, state', 0

	# main part ##############################
	value = 0

	# check column name
	if 'city' in typer.curr_col_name.lower():
		value += 5
	if 'state' in typer.curr_col_name.lower():
		value += 5

	#account for the form of the token
	if my_typer.has_form(token):
		value += 20

	# check examples
	for word in temp:
		if my_typer.is_a(word):
			value += 50
			break

	# misc part ########################
	misc_value = 0
	# TODO implement

	return 'city state', value + misc_value

def email_heuristic(token, typer):
	'''returns a certainty value for token being an email
	or zero if it definitely isn't an email'''
	# get the right classifier
	my_typer = typer.column_classifiers[EMAIL_POS]

	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()

	#check if it can't be an email
	if not my_typer.can_be(char_val_list):
		return 'email', 0
	
	# main part ###############
	value = 0

	# check column name
	if 'address' in typer.curr_col_name.lower():
		value += 3
	if 'email' in typer.curr_col_name.lower():
		value += 7

	#account for the form of the token
	if my_typer.has_form(token):
		value += 20

	# check examples
	for word in temp:
		if my_typer.is_a(word):
			value += 50
			break

	# misc part ####################3
	misc_value = 0
	if '@' in token:
		misc_value = 10

	return 'email', value + misc_value

def location_heuristic(token, typer):
	'''returns a certainty value for token being a location
	or zero if it definitely isn't a location'''
	# get the right classifier
	my_typer = typer.column_classifiers[LOCATION_POS]

	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	temp = token.split()
	lengths = [len(x) for x in temp]
	if len(lengths) == 0:
		return 'location', 0
	avg_len = float(sum(lengths)) / float(len(lengths))
	spaces = len(temp) - 1

	#check if it can't be a location
	if not my_typer.can_be(char_val_list):
		return 'location', 0

	# main part #####################
	value = 0

	# check column name
	if 'location' in typer.curr_col_name.lower():
		value += 10
	elif 'place' in typer.curr_col_name.lower():
		value += 10
	elif 'country' in typer.curr_col_name.lower():
		value += 10
	
	#account for the form of the token
	if my_typer.has_form(token):
		value += 20

	# looking at format of individual words
	for word in temp:
		if my_typer.is_a(word.lower()):
			value += 50
			break

	# misc part ###################333
	misc_value = 0
	# TODO implement properly
	# account for number of spaces
	value += NUM_LOCATION_SPACES - abs(spaces - NUM_LOCATION_SPACES)
	# account for location length
	value = LOCATION_LENGTH - abs(avg_len - LOCATION_LENGTH)

	return 'location', value

def description_heuristic(token, typer):
	'''returns a certainty value for token being a description
	or zero if it definitely isn't a description'''
	# get the right classifier
	my_typer = typer.column_classifiers[DESCRIPTION_POS]

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
	for word in temp:
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


heuristics = [full_name_heuristic, first_name_heuristic, last_name_heuristic,
				datestring_heuristic, full_address_heuristic, street_address_heuristic,
				city_state_heuristic, email_heuristic, location_heuristic,
				description_heuristic]
