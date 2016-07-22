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

def no_letters(token):
	'''Returns true if there are no letters in an input string'''
	for char in token:
		if ((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122)):
			return False
	return True


def strings_to_regex(strLst):
	'''Makes a regular expression that matches the main form in the list'''
	numStrings = len(strLst)

	for string in strLst:
		for char in string:
			index = 0
			section_length = 0
			while string[index] != ' ':
				section_length += 1
				index += 1




fn_regex = r'''^[-.a-zA-Z']*?,?\s(?:[-a-zA-Z']*\.?\s)*?[-a-zA-Z']*\.?$'''
ds_regex = r'''^(?:[A-Z][a-zA-Z]*\.?,?\s)?(?:[0-3][0-9]\s)?[A-Z][a-zA-Z]*\.?,?\s(?:[0-3][0-9]\.?,?\s)?[0-9]*$'''
fa_regex = r'''^(?:[Oo][Nn][Ee]|[0-9-]*[a-zA-Z]?)\s+(?:[NSEW]\.?[NSEW]?\.?\s+|(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+)?(?:\d*(?:[SNRTsnrt][TDHtdh])?(?:\s+[a-zA-Z'-]*)?|(?:[a-zA-Z'-]*\s+)*?(?:[a-zA-Z'-]*))\.?(?:\s+\d*)?,?(?:\s+[NSEW]\.?[NESW]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])?)?(?:\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|\s+(?:[a-zA-Z][a-z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?(?:\s+(?:[#]\s*)?\w*(?:[-/: ]\w*)?))?,?\s(?:[a-zA-Z'-]*\s)*?[a-zA-Z'-]*,?\s[a-zA-Z]*,?\s(?:\d{5}|\d{5}(?:\s|[.-])?\d{4})(?:,?\s[A-Za-z'-]*)*$'''
sa_regex = r'''^(?:[Oo][Nn][Ee]|[0-9-]*[a-zA-Z]?)\s+(?:[NSEW]\.?[NSEW]?\.?\s+|(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+)?(?:\d*(?:[SNRTsnrt][TDHtdh])?(?:\s+[a-zA-Z'-]*)?|(?:[a-zA-Z'-]*\s+)*?(?:[a-zA-Z'-]*))\.?(?:\s+\d*)?,?(?:\s+[NSEW]\.?[NESW]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])?)?(?:\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|\s+(?:[a-zA-Z][a-z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?(?:\s+(?:[#]\s*)?\w*(?:[-/: ]\w*)?))?$'''
cs_regex = r'''^(?:[a-zA-Z'-]*\s)*?[a-zA-Z'-]*,?\s[a-zA-Z]*$'''
em_regex = r'''^\S*?@\S*?(?:\.\S*?)+$'''
lo_regex = r'''^(?:[A-Z][a-z'-]*\s)*?(?:[A-Z][a-z'-]*)$'''
de_regex = r'''^(?:["'<-]?[A-Za-z0-9'-]+[>"',;:-]?(?:\s|[.?!]\s+))+$'''
