# helper functions

def dict_max(Adict):
	'''returns the key with the largest value in a dictionary'''
	max_val = float("-inf")
	max_key = ''
	for key in Adict.keys():
		if Adict[key] > max_val:
			max_val = Adict[key]
			max_key = key
	return max_key

def key_sum(Adict):
	'''returns the sum of the values of the keys in a dictionary'''
	total = 0
	vals = Adict.values()
	for num in vals:
		total += num
	return total

def make_form(inString):
	'''Turns the input string into a string that represents the general form of the string'''
	returnString = ''
	for char in inString:
		ord_char = ord(char)
		if ord_char <= 57 and ord_char >= 48:
			returnString += '0'
		elif ord_char <= 90 and ord_char >= 65:
			returnString += 'X'
		elif ord_char >= 97 and ord_char <= 122:
			returnString += 'x'
		else:
			returnString += char
	return returnString

def condense(inString):
	'''Turns the input form string into a standardized form string with word and number lengths removed'''
	condString = ''
	index = 0
	length = len(inString)
	while index < length:
		condString += inString[index]
		if inString[index] == 'x':
			while (index < length and inString[index] == 'x'):
				index += 1
			continue
		if inString[index] == '0':
			while (index < length and inString[index] == '0'):
				index += 1
			continue
		index += 1

	return condString

def normalize(val, maxVal):
	'''Normalizes the input value over a 0-1 scale'''
	return float(val)/float(maxVal)
	#TODO: Make it quadratic or logarithmic or something to make it work better