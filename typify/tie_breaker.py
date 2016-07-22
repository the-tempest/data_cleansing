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
col2_POS     = 6
EMAIL_POS          = 7
LOCATION_POS       = 8
DESCRIPTION_POS    = 9



def __init__(self, guesses, prediction_1, prediction_2, typer):
	first = guesses[1]
	return differ(first, typer, prediction_1, prediction_2)
		
	
	
#possibly this type_switch thing will be unecessary
def get_index(self, feature): # need to build this up
	''' gets the index corresponding to the feature. This will be used in to access the correct 
classifier in the list of classfiers'''
	switcher = {"full name" : 0,
					"first name" : 1,
					"last name" : 2,
					"datestring": 3,
					"full address": 4, 
					"street address": 5,
					"city, state": 6,
					"email": 7,
					"location": 8,
					"description": 9}
					

	return switcher.get(feature)
	
def get_key(self, feature): # need to build this up
	''' gets the words that might actually show up in the column name'''
	switcher = {"full name" : 0,
					"first name" : 'name',
					"last name" : ('first', 'name'),
					"datestring": 'date',
					"full address": 'address', 
					"street address": ('street', 'address'),
					"city, state": ('city', 'state'),
					"email": ('address', 'email'),
					"location": ('location', 'place', 'country'),
					"description": ('description')}
					

	return switcher.get(feature)

def differ(token, typer, prediction_1, prediction_2):
	'''this is not really a heuristic of the same form as the others; it functions
	as a tie breaker'''
	
	index1 = self.get_index(prediction_1)
	index2 = self.get_index(prediction_2)
	
	y = self.get_key(prediction_1)
	x = self.get_key(prediction_2)
	
	char_val_list = []
	for char in token:
		char_val_list.append(ord(char))
	split_token = token.split()
	len_split_token = len(split_token)
	
	col1 = 0
	col2 = 0
	# get the right classifier
	my_typer = typer.column_classifiers[index1]
	# main part #####################

	# check column name		
	if ( not isinstance(y,tuple)): # same problem as in generate dict below
		if y in typer.curr_col_name.lower():
			col1 = 1
	else:
		if y[0] in typer.curr_col_name.lower():
			col1 = 1
		if y[1] in typer.curr_col_name.lower():
			col1 = 1
	
	
	
	# looking at format of individual words
	for word in split_token:
		if my_typer.is_a(word.lower()):
			nvalue += 50
			break
	
	my_typer = typer.column_classifiers[index2]
	# main part #####################

	# check column name
	if ( not isinstance(y,tuple)): # same problem as in generate dict below
		if x in typer.curr_col_name.lower():
			col2 = 1
	else:
		if x[0] in typer.curr_col_name.lower():
			col2 = 1
		if x[1] in typer.curr_col_name.lower():
			col2 = 1
	# looking at format of individual words
	for word in split_token:
		if my_typer.is_a(word.lower()):
			cvalue += 50
			break
	
	if col1 ==1 and col2 ==1:
		#strange
		return 'unclear'
	elif col2==0 and col1 ==0:
		return 'unclear'
	elif col2 ==1 and col1 ==0:
		return prediction_2
	elif col2 ==0 and col1 ==1:
		return prediction_1


	