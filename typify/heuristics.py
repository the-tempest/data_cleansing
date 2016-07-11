# heuristics.py
# this file contains all the string heuristics
# that we use to predict what type a string token
# belongs to. They take in a token and a classifier,
# which is a helper class defined in classifier.py
# TODO these need to be merged with the numeric 
# heuristics somehow


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
EMAIL_POS          = 6
LOCATION_POS       = 7
DESCRIPTION_POS    = 8


def full_name_heuristic(token, typer):
	'''returns a  name heuristic value or negative infinity
	if it definitely isn't a name'''
	# get the right classifier
	my_typer = typer.column_classifiers[FULL_NAME_POS]

	# check if it can't be a name
	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not my_typer.can_be(char_val_list):
		return value

	# check column name
	if 'name' in typer.column_name.lower():
		value += 10

	# counting common features of names
	if my_typer.contains_a(token.lower()):
		value += 1

	# account for name length
	temp = token.split()
	lengths = [len(x) for x in temp]
	if len(lengths) == 0:
		return 0
	avg_len = float(sum(lengths)) / float(len(lengths))
	value += NAME_LENGTH - abs(avg_len - NAME_LENGTH)

	# looking at format of individual words
	for word in temp:
		# check for common names
		#TODO: Need to change because it will flag all single names as full names
		if my_typer.is_a(word.lower()):
			value += 50
		word_form = condense(make_form(word))
		if word_form == 'Xx':
			value += 2
		if word_form.strip('.') == 'X':
			value += 1
	
	# account for number of spaces
	spaces = len(temp) - 1
	value += NUM_SPACES - abs(spaces - NUM_NAME_SPACES)
	
	return value

def first_name_heuristic(token, typer):
	'''returns a  first name heuristic value or negative infinity
	if it definitely isn't a name'''
	# get the right classifier
	my_typer = typer.column_classifiers[FIRST_NAME_POS]


	#TODO edit to be more relevant to first names

	# check if it can't be a name
	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not my_typer.can_be(char_val_list):
		return value

	# check column name
	if 'first' in typer.column_name.lower():
		value += 10
	if 'name' in typer.column_name.lower():
		value += 10

	# counting common features of names
	if my_typer.contains_a(token.lower()):
		value += 1

	# account for name length
	temp = token.split()
	lengths = [len(x) for x in temp]
	if len(lengths) == 0:
		return 0
	if len(lengths) == 1:
		value += 10

	# check for common names
	#TODO: Need to change because it will flag all single names as full names
	if my_typer.is_a(token.lower()):
		return 100
	word_form = condense(make_form(token))
	if word_form == 'Xx':
		value += 2
	if word_form.strip('.') == 'X':
		value += 1

	return value

def last_name_heuristic(token, typer):
	'''returns a last name heuristic value or negative infinity
	if it definitely isn't a name'''
	# get the right classifier
	my_typer = typer.column_classifiers[LAST_NAME_POS]


	#TODO edit to be more relevant to last names

	# check if it can't be a name
	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
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
	if my_typer.contains_a(token.lower()):
		value += 1

	# account for name length
	temp = token.split()
	lengths = [len(x) for x in temp]
	if len(lengths) == 0:
		return 0
	if len(lengths) == 1:
		value += 10

	# check for common names
	#TODO: Need to change because it will flag all single names as full names
	if my_typer.is_a(token.lower()):
		return 100
	word_form = condense(make_form(token))
	if word_form == 'Xx':
		value += 2
	if word_form.strip('.') == 'X':
		value += 1

	return value

def datestring_heuristic(token, typer):
	'''returns a certainty value for token being a date string
	or zero if it definitely isn't a date string'''
	# get the right classifier
	my_typer = typer.column_classifiers[DATESTRING_POS]

	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not my_typer.can_be(char_val_list):
		return value

	# check column name
	if 'date' in typer.column_name.lower():
		value += 10

	# counting common features of date strings
	if my_typer.contains_a(token.lower()):
		value += 1

	# account for name length
	temp = token.split()
	if len(temp) == 3:
		value += 10
	
	# check if it's a mix of strings and numbers
	numStrings = 0
	numNums = 0
	for word in temp:
		word_form = condense(make_form(word))
		if '0' in word_form:
			numNums += 1
		elif 'X' in word_form or 'x' in word_form:
			numStrings += 1
	numPair = (numStrings, numNums)
	if numPair == (2,1) or numPair == (2,2) or numPair (1,1):
		value += 5

	# check forms
	form = condense(make_form(token))
	if my_typer.has_form(form):
		value += 10

	for word in temp:
		if my_typer.is_a(word):
			value += 20

	return value

def full_address_heuristic(token, typer):
	'''returns a certainty value for token being an address
	or zero if it definitely isn't an address'''
	# get the right classifier
	my_typer = typer.column_classifiers[FULL_ADDRESS_POS]


	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not my_typer.can_be(char_val_list):
		return value

	# check column name
	if 'add' in typer.column_name.lower():
		value += 5
		if 'address' in typer.column_name.lower():
			value += 5

	# counting common features of address strings
	if my_typer.contains_a(token.lower()):
		value += 1
	
	# check if it's a mix of strings and numbers
	numStrings = 0
	numNums = 0
	for word in temp:
		word_form = condense(make_form(word))
		if '0' in word_form:
			numNums += 1
		elif 'X' in word_form or 'x' in word_form:
			numStrings += 1
	if numStrings and numNums:
		value += 10
	    
	form = condense(make_form(token))
	if my_typer.has_form(form):
		value += 10

	for word in temp:
		if my_typer.is_a(word):
			value += 20

	return value

def street_address(token, typer):
	'''returns a certainty value for token being an address
	or zero if it definitely isn't an address'''
	# get the right classifier
	my_typer = typer.column_classifiers[STREET_ADDRESS_POS]

	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not my_typer.can_be(char_val_list):
		return value

	# check column name
	if 'add' in typer.column_name.lower():
		value += 5
		if 'address' in typer.column_name.lower():
			value += 5

	# counting common features of address strings
	if my_typer.contains_a(token.lower()):
		value += 1
	
	# check if it's a mix of strings and numbers
	numStrings = 0
	numNums = 0
	for word in temp:
		word_form = condense(make_form(word))
		if '0' in word_form:
			numNums += 1
		elif 'X' in word_form or 'x' in word_form:
			numStrings += 1
	if numStrings and numNums:
		value += 10
	    
	form = condense(make_form(token))
	if my_typer.has_form(form):
		value += 10

	for word in temp:
		if my_typer.is_a(word):
			value += 20

	return value

def email_heuristic(token, typer):
	'''returns a certainty value for token being an email
	or zero if it definitely isn't an email'''
	# get the right classifier
	my_typer = typer.column_classifiers[EMAIL_POS]

	# check if it can't be an email
	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not my_typer.can_be(char_val_list):
		return value
	if '@' not in token:
		return value
	else:
		value += 50

	# check column name
	if 'address' in typer.column_name.lower():
		value += 5
	if 'email' in typer.column_name.lower():
		value += 10

	# counting common features of emails
	if my_typer.contains_a(token.lower()):
		value += 1

	regex = re.compile('[Xx0\W]*@[Xx0\W]*.x')
	if regex.search(token):
		value += 20
	
	return value

def location_heuristic(token, typer):
	'''returns a certainty value for token being a location
	or zero if it definitely isn't a location'''
	# get the right classifier
	my_typer = typer.column_classifiers[LOCATION_POS]

	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not my_typer.can_be(char_val_list):
		return value

	# check column name
	#TODO fix this part of the heuristic to accurately reflect locations
	if 'location' in typer.column_name.lower():
		value += 10
	elif 'place' in typer.column_name.lower():
		value += 10
	elif 'country' in typer.column_name.lower():
		value += 10

	# counting common features of locations
	if my_typer.contains_a(token.lower()):
		value += 1

	# account for location length
	temp = token.split()
	lengths = [len(x) for x in temp]
	if len(lengths) == 0:
		return 0
	avg_len = float(sum(lengths)) / float(len(lengths))
	value += LOCATION_LENGTH - abs(avg_len - LOCATION_LENGTH)

	# looking at format of individual words
	for word in temp:
		# check for common names
		#TODO: Need to change because it will flag all single names as full names
		if my_typer.is_a(word.lower()):
			value += 50
		word_form = condense(make_form(word))
		if word_form == 'Xx':
			value += 2
	
	# account for number of spaces
	spaces = len(temp) - 1
	value += NUM_LOCATION_SPACES - abs(spaces - NUM_LOCATION_SPACES)
	
	return value

def description_heuristic(token, typer):
	'''returns a certainty value for token being a description
	or zero if it definitely isn't a description'''
	# get the right classifier
	my_typer = typer.column_classifiers[DESCRIPTION_POS]

	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not my_typer.can_be(char_val_list):
		return value

	# check column name
	if 'description' in typer.column_name.lower():
		value += 10
	if 'note' in typer.column_name.lower():
		value += 10

	# counting common features of descriptions
	if my_typer.contains_a(token.lower()):
		value += 1

	# account for description length
	# using number of spaces
	# maxes out at 100
	# since that's where it normalizes
	split_token = token.split()
	len_split_token = len(split_token)
	if len_split_token == 0:
		value = 0
	if len_split_token >= 100:
		value = 100
	else:
		value += len_split_token

	return value