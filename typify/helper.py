# helper.py
# these functions are used extensively in the
# files in this directory, to aid in classifying
# various types of strings and translate them into
# condensed formats
import re


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
	ret = ''
	for char in inString:
		ord_char = ord(char)
		if ord_char <= 57 and ord_char >= 48:
			ret += '0' # it's a digit
		elif ord_char <= 90 and ord_char >= 65:
			ret += 'X' # it's uppercase
		elif ord_char >= 97 and ord_char <= 122:
			ret += 'x' # it's lowercase
		else:
			ret += char # it's punctuation
	return ret

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

def no_letters(inString):
	'''Returns true if there are no letters in an input string'''
	for char in inString:
		if ((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122)):
			return False
	return True


#NAMES
regex = re.compile(r'''^[-.a-zA-Z']*?,?\s(?:[-a-zA-Z']*\.?\s)*?[-a-zA-Z']*\.?$''')

#FIRST NAMES
regex = re.compile(r'''^[A-Z][a-z'-]*$''')

#LAST NAMES
regex = re.compile(r'''^[A-Z][a-zA-Z'-]*$''')

#DATESTRINGS
regex = re.compile(r'''^(?:[A-Z][a-zA-Z]*\.?,?\s)?(?:[0-3][0-9]\s)?[A-Z][a-zA-Z]*\.?,?\s(?:[0-3][0-9]\.?,?\s)?[0-9]*$''')

#FULL_ADDRESSES
regex = re.compile(r'''^\d*\s(?:[NSEW]\.\s?|[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?\s)?[a-zA-Z'-]*\s[a-zA-Z][a-z]*?\.?\s(?:(?:[a-zA-Z][a-z]*\.?|[Pp][Oo]\.?\s?[Bb][Oo][Xx])(?:\s\d*[a-zA-Z]?))?,?\s(?:[a-zA-Z'-]*\s)*?[a-zA-Z'-]*,?\s[a-zA-Z]*,?\s(?:\d{5}|\d{5}(?:\s|[.-])?\d{4})(?:,?\s[A-Za-z'-]*)*$''')

#STREET_ADDRESSES
regex = re.compile(r'''^\d*\s(?:[NSEW]\.\s?|[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?\s)?[a-zA-Z'-]*\s[a-zA-Z][a-z]*?\.?\s(?:(?:[a-zA-Z][a-z]*\.?|[Pp][Oo]\.?\s?[Bb][Oo][Xx])(?:\s\d*[a-zA-Z]?))?$''')

#CITY_STATE
regex = re.compile(r'''^(?:[a-zA-Z'-]*\s)*?[a-zA-Z'-]*,?\s[a-zA-Z]*$''')

#EMAIL
regex = re.compile(r'''^\S*?@\S*?(?:\.\S*?)+$''')

#LOCATION
regex = re.compile(r'''^(?:[A-Z][a-z'-]*\s)*?(?:[A-Z][a-z'-]*)$''')

#DESCRIPTION
regex = re.compile(r'''^(?:["'<-]?[A-Za-z'-]+[>"',;:-]?(?:\s|[.?!]\s*))+$''')
