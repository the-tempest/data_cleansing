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

def full_name_heuristic(token, typer):
	'''returns a  name heuristic value or negative infinity
	if it definitely isn't a name'''
	# check if it can't be a name
	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not typer.column_classifiers[0].can_be(char_val_list):
		return value

	# check column name
	if 'name' in typer.column_name.lower():
		value += 10

	# counting common features of names
	if typer.column_classifiers[0].contains_a(token.lower()):
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
		if typer.column_classifiers[0].is_a(word.lower()):
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
	#TODO edit to be more relevant to first names

	# check if it can't be a name
	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not typer.column_classifiers[1].can_be(char_val_list):
		return value

	# check column name
	if 'first' in typer.column_name.lower():
		value += 10
	if 'name' in typer.column_name.lower():
		value += 10

	# counting common features of names
	if typer.column_classifiers[1].contains_a(token.lower()):
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
	if typer.column_classifiers[1].is_a(token.lower()):
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
	#TODO edit to be more relevant to last names

	# check if it can't be a name
	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not typer.column_classifiers[2].can_be(char_val_list):
		return value

	# check column name
	if 'last' in typer.column_name.lower():
		value += 10
	if 'sur' in typer.column_name.lower():
		value += 10
	if 'name' in typer.column_name.lower():
		value += 10

	# counting common features of names
	if typer.column_classifiers[2].contains_a(token.lower()):
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
	if typer.column_classifiers[2].is_a(token.lower()):
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
	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not typer.column_classifiers[3].can_be(char_val_list):
		return value

	# check column name
	if 'date' in typer.column_name.lower():
		value += 10

	# counting common features of date strings
	if typer.column_classifiers[3].contains_a(token.lower()):
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
	if typer.column_classifiers[3].has_form(form):
		value += 10

	for word in temp:
		if typer.column_classifiers[3].is_a(word):
			value += 20

	return value

def address_heuristic(token, typer):
	'''returns a certainty value for token being an address
	or zero if it definitely isn't an address'''
	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not typer.column_classifiers[4].can_be(char_val_list):
		return value

	# check column name
	if 'add' in typer.column_name.lower():
		value += 5
		if 'address' in typer.column_name.lower():
			value += 5

	# counting common features of address strings
	if typer.column_classifiers[4].contains_a(token.lower()):
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
	if typer.column_classifiers[4].has_form(form):
		value += 10

	for word in temp:
		if typer.column_classifiers[4].is_a(word):
			value += 20

	return value

def email_heuristic(token, typer):
	'''returns a certainty value for token being an email
	or zero if it definitely isn't an email'''
	# check if it can't be a name
	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not self.column_classifiers[5].can_be(char_val_list):
		return value
	if '@' not in token:
		return value
	else:
		value += 50

	# check column name
	if 'address' in self.column_name.lower():
		value += 5
	if 'email' in self.column_name.lower():
		value += 10

	# counting common features of emails
	if self.column_classifiers[5].contains_a(token.lower()):
		value += 1

	regex = re.compile('[Xx0\W]*@[Xx0\W]*.x')
	if regex.search(token):
		value += 20
	
	return value

def location_heuristic(token, typer):
	'''returns a certainty value for token being a location
	or zero if it definitely isn't a location'''
	value = 0
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	if not typer.column_classifiers[6].can_be(char_val_list):
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
	if typer.column_classifiers[6].contains_a(token.lower()):
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
		if typer.column_classifiers[6].is_a(word.lower()):
			value += 50
		word_form = condense(make_form(word))
		if word_form == 'Xx':
			value += 2

	
	# account for number of spaces
	spaces = len(temp) - 1
	value += NUM_LOCATION_SPACES - abs(spaces - NUM_LOCATION_SPACES)
	
	return value

def descriptions(token, typer):
