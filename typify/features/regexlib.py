import re

def regex_test(regex_strs, tokens):
	regex_dict = {}
	counter = 1
	for regex_str in regex_strs:
		regex_dict[regex_str] = counter
		counter += 1

	compiled_regexs = []
	for regex_str in regex_strs:
		compiled_regexs.append(re.compile(regex_str))

	return_list = []
	for token in tokens:
		found = False
		for regex in compiled_regexs:
			if regex.match(token) != None:
				print regex.pattern
				#return_list.append((token,regex_dict[regex.pattern]))
				found = True
				break
		if found == False:
			return_list.append(token)

	return return_list


#FULL_NAME_TESTER_STRINGS = ['John M. Smith', 'John m Smith', 'John M McSmith', 'John m MacSmith', 'Smith-Fisherman, John M.', 'Smith, John m', 'John Michael MacSmith', 'John Michael Steve Jeffery Smith', 'Smith, John Michael Jeffery', 'John M von Smith','von Smith, John m.', 'John Michael von Smith', 'von Smith, John Michael Steve', 'John Smith', 'J Smith', 'j. Smith', 'j. s. smith', 'JOHN M. S. SMITH', 'SMITH, JOHN M. S.', 'JOHN MICHAEL SMITH', 'SMITH-FISHERMAN, JOHN MICHAEL', 'JOHN SMITH', 'J SMITH', 'J. SMITH', 'john m. smith', 'john m t smith', 'smith, john m', 'john michael robert smith-macrobertson', 'smith, john robert', 'john smith', 'j smith', 'j. smith']

#FIRST_NAME_TESTER_STRINGS = ['John', 'John m', 'John m.', 'John m. s.', 'John M. S. T.', 'John Michael', 'john', 'john h w', 'john m.', 'john michael', 'JOHN', 'JOHN M', 'JOHN M.', 'JOHN MICHAEL']
#LAST_NAME_TESTER_STRINGS = ['Smith', 'von Smith', 'MacFisherman-McSmith', 'Von Smith-Robertson', 'smith', 'von smith', 'smith-smith', 'von smith-smith', 'SMITH', 'VON SMITH', 'SMITH-SMITH', 'VON SMITH-SMITH']

#DATESTRING_TESTER_STRINGS = ['Jul. 2016', 'Jul., 2016', 'July 2016', 'July, 2016', '27 Jul. 2016', '27 Jul., 2016', '27 July 2016', '27 July, 2016', 'Jul. 27 2016', 'Jul. 27, 2016', 'July 27 2016', 'July 27, 2016', 'Wed. 27 Jul. 2016', 'Wed., 27 Jul., 2016', 'Wed. Jul. 27 2016', 'Wed., Jul. 27, 2016', 'Wed. 27 July, 2016', 'Wed., 27 July 2016', 'Wed. July 27, 2016', 'Wed., July 27, 2016', 'Wednesday, 27 Jul. 2016', 'Wednesday 27 Jul., 2016', 'Wednesday Jul. 27 2016', 'Wednesday, Jul. 27 2016', 'Wednesday, 27 July, 2016', 'Wednesday 27 July 2016', 'Wednesday July 27, 2016', 'Wednesday, July 27 2016', 'JUL. 2016', 'JUL., 2016', 'JULY 2016', 'JULY, 2016', '27 JUL. 2016', '27 JUL., 2016', '27 JULY 2016', '27 JULY, 2016', 'JUL. 27 2016', 'JUL. 27, 2016', 'JULY 27 2016', 'JULY 27, 2016', 'WED. 27 JUL. 2016', 'WED., 27 JUL., 2016', 'WED. JUL. 27, 2016', 'WED. JUL. 27, 2016', 'WED. 27 JULY 2016', 'WED., 27 JULY, 2016', 'WED. JULY 27 2016', 'WED. JULY 27, 2016', 'WEDNESDAY 27 JUL. 2016', 'WEDNESDAY, 27 JUL., 2016', 'WEDNESDAY JUL. 27, 2016', 'WEDNESDAY, JUL. 27 2016', 'WEDNESDAY, 27 JULY, 2016', 'WEDNESDAY 27 JULY 2016', 'WEDNESDAY, JULY 27, 2016', 'WEDNESDAY, JULY 27 2016', 'jul. 2016', 'jul., 2016', 'july, 2016', 'july 2016', '27 jul. 2016', '27 jul 2016', '27 july 2016', '27 july, 2016', 'jul. 27 2016', 'jul. 27, 2016', 'july 27 2016', 'july 27, 2016', 'wed., 27 jul. 2016', 'wed. 27 jul., 2016', 'wed. jul. 27 2016', 'wed., jul. 27, 2016', 'wed. 27 july 2016', 'wed., 27 july, 2016', 'wed. july 27 2016', 'wed., july 27, 2016', 'wednesday, 27 jul. 2016', 'wednesday, 27 jul., 2016', 'wednesday, jul. 27, 2016', 'wednesday jul. 27 2016', 'wednesday, 27 july 2016', 'wednesday 27 july, 2016', 'wednesday 27 july 2016', 'wednesday, 27 july, 2016', 'wednesday july 27 2016', 'wednesday, july 27, 2016'] 

#fn_regex = r'''^[-.a-zA-Z']*?,?\s(?:[-a-zA-Z']*\.?\s)*?[-a-zA-Z']*\.?$'''
FULL_NAME_REGEXS = [r'''^[A-Z][a-z]+\s+(?:[A-Za-z]\.?\s+)+[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*(?:-[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*)?$''', #John (m/M)(.) Sm(i/I)(t/T)h(-Sm(i/I)(t/T)h)
	r'''^[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*(?:-[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*)?,\s+[A-Z][a-z]+\s+(?:[A-Za-z]\.?\s+)*[A-Za-z]\.?$''', #Sm(i/I)(t/T)h(-Sm(i/I)(t/T)h), John (m/M)(.) (...)
	r'''^[A-Z][a-z]+\s+(?:[A-Z][a-z]+\s+)+[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*(?:-[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*)?$''', #John Michael Sm(i/I)(t/T)h(-Sm(i/I)(t/T)h)
	r'''^[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*(?:-[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*)?,\s+[A-Z][a-z]+\s+(?:[A-Z][a-z]+\s+)*[A-Z][a-z]+$''',	#Sm(i/I)(t/T)h(-Sm(i/I)(t/T)h), John Michael (...)
	r'''^[A-Z][a-z]+\s+(?:[A-Za-z]\.?\s+)+[a-z]+\s+[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*(?:-[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*)?$''', #John (m/M)(.) von Sm(i/I)(t/T)h(-Sm(i/I)(t/T)h)
	r'''^[a-z]+\s+[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*(?:-[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*)?,\s+[A-Z][a-z]+\s+(?:[A-Za-z]\.?\s+)*[A-Za-z]\.?$''', #von Sm(i/I)(t/T)h(-Sm(i/I)(t/T)h), John (m/M)(.) (...)
	r'''^[A-Z][a-z]+\s+(?:[A-Z][a-z]+\s+)+[a-z]+\s+[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*(?:-[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*)?$''', #John Michael von Sm(i/I)(t/T)h(-Sm(i/I)(t/T)h)
	r'''^[a-z]+\s+[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*(?:-[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*)?,\s+[A-Z][a-z]+\s+(?:[A-Z][a-z]+\s+)*[A-Z][a-z]+$''',	#von Sm(i/I)(t/T)h(-Sm(i/I)(t/T)h), John Michael (...)
	r'''^[A-Z][a-z]+\s+[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*(?:-[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*)?$''', #John Sm(i/I)(t/T)h(-Sm(i/I)(t/T)h)
	r'''^(?:[A-Za-z]\.?\s+)+[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*(?:-[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*)?$''',	#(j/J)(.) (...) Sm(i/I)(t/T)h(-Sm(i/I)(t/T)h)
	r'''^[A-Z]{2,}\s+(?:[A-Z]\.?\s+)+[A-Z]{2,}(?:-[A-Z]{2,})?$''', #JOHN M(.) (...) SMITH(-SMITH)
	r'''^[A-Z]{2,}(?:-[A-Z]{2,})?,\s+[A-Z]{2,}\s+(?:[A-Z]\.?\s+)*[A-Z]\.?$''',	#SMITH(-SMITH), JOHN M(.) (...)
	r'''^[A-Z]{2,}\s+(?:[A-Z]{2,}\s+)+[A-Z]{2,}(?:-[A-Z]{2,})?$''',	#JOHN MICHAEL SMITH(-SMITH)
	r'''^[A-Z]{2,}(?:-[A-Z]{2,})?,\s+[A-Z]{2,}\s+(?:[A-Z]{2,}\s+)*[A-Z]{2,}$''',	#SMITH(-SMITH), JOHN MICHAEL (...)
	r'''^[A-Z]{2,}\s+[A-Z]{2,}(?:-[A-Z]{2,})?$''', #JOHN SMITH
	r'''^(?:[A-Z]\.?\s+)+[A-Z]{2,}(?:-[A-Z]{2,})?$''',	#J(.) (...) SMITH
	r'''^[a-z]{2,}\s+(?:[a-z]\.?\s+)+[a-z]{2,}(?:-[a-z]{2,})?$''',	#john m(.) (...) smith(-smith)
	r'''^[a-z]{2,}(?:-[a-z]{2,})?,\s+[a-z]{2,}\s+(?:[a-z]\.?\s+)*[a-z]\.?$''',	#smith(-smith), john m(.) (...)
	r'''^[a-z]{2,}\s+(?:[a-z]{2,}\s+)+[a-z]{2,}(?:-[a-z]{2,})?$''',	#john michael (...) smith(-smith)
	r'''^[a-z]{2,}(?:-[a-z]{2,})?,\s+[a-z]{2,}\s+(?:[a-z]{2,}\s+)*[a-z]{2,}$''',	#smith(-smith), john michael (...)
	r'''^[a-z]{2,}\s+[a-z]{2,}(?:-[a-z]{2,})?$''', #john smith
	r'''^(?:[a-z]\.?\s+)+[a-z]{2,}(?:-[a-z]{2,})?$''']	#j(.) (...) smith

#NAME_REGEX = r'''^[A-Z][a-z'-]*$'''
FIRST_NAME_REGEXS = [r'''^[A-Z][a-z]+$''',	#John
	r'''^[A-Z][a-z]+\s+(?:[a-z]\s+)*[a-z]$''',	#John m
	r'''^[A-Z][a-z]+\s+(?:[a-z]\.\s+)*[a-z]\.$''',	#John m.
	r'''^[A-Z][a-z]+\s+(?:[A-Z]\s+)*[A-Z]$''',	#John M
	r'''^[A-Z][a-z]+\s+(?:[A-Z]\.\s+)*[A-Z]\.$''',	#John M.
	r'''^[A-Z][a-z]+\s+(?:[A-Z][a-z]+\s+)*[A-Z][a-z]+$''',	#John Michael
	r'''^[a-z]{2,}$''',	#john
	r'''^[a-z]{2,}\s+(?:[a-z]\s+)*[a-z]$''',	#john m
	r'''^[a-z]{2,}\s+(?:[a-z]\.\s+)*[a-z]\.$''',	#john m.
	r'''^[a-z]{2,}\s+(?:[a-z]{2,}\s*)+$''',	#john michael
	r'''^[A-Z]{2,}$''',	#JOHN
	r'''^[A-Z]{2,}\s+(?:[A-Z]\s+)*[A-Z]$''',	#JOHN M
	r'''^[A-Z]{2,}\s+(?:[A-Z]\.\s+)*[A-Z]\.$''',	#JOHN M.
	r'''^[A-Z]{2,}\s+(?:[A-Z]{2,}\s*)+$''']	#JOHN MICHAEL
LAST_NAME_REGEXS = [r'''^[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*$''',	#Sm(i/I)(t/T)h
	r'''^[A-Za-z][a-z]+\s+[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*$''',	#(v/V)on Sm(i/I)(t/T)h
	r'''^[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*-[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*$''',	#Sm(i/I)(t/T)h-Sm(i/I)(t/T)h
	r'''^[A-Za-z][a-z]+\s+[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*-[A-Z][a-z][A-Za-z]?[A-Za-z]?[a-z]*$''',	#(v/V)on Sm(i/I)(t/T)h-Sm(i/I)(t/T)h
	r'''^[a-z]{2,}$''',	#smith
	r'''^[a-z]{2,}\s+[a-z]{2,}$''',	#von smith
	r'''^[a-z]{2,}-[a-z]{2,}$''',	#smith-smith
	r'''^[a-z]{2,}\s+[a-z]{2,}-[a-z]{2,}$''',	#von smith-smith
	r'''^[A-Z]{2,}$''',	#SMITH
	r'''^[A-Z]{2,}\s+[A-Z]{2,}$''',	#VON SMITH
	r'''^[A-Z]{2,}-[A-Z]{2,}$''',	#SMITH-SMITH
	r'''^[A-Z]{2,}\s+[A-Z]+-[A-Z]{2,}$''']	#VON SMITH-SMITH

#ds_regex = r'''^(?:[A-Z][a-zA-Z]*\.?,?\s)?(?:[0-3][0-9]\s)?[A-Z][a-zA-Z]*\.?,?\s(?:[0-3][0-9]\.?,?\s)?[0-9]*$'''
DATESTRING_REGEXS = [r'''^[A-Z][a-z]*\.,?\s+\d{1,4}$''',	#Jul.(,) 2016
	r'''^[A-Z][a-z]*,?\s+\d{1,4}$''',	#July(,) 2016 
	r'''^[0-3][0-9]\s+[A-Z][a-z]*\.,?\s+\d{1,4}$''',	#27 Jul.(,) 2016
	r'''^[0-3][0-9]\s+[A-Z][a-z]*,?\s+\d{1,4}$''',	#27 July(,) 2016
	r'''^[A-Z][a-z]*\.\s+[0-3][0-9],?\s+\d{1,4}$''',	#Jul. 27(,) 2016
	r'''^[A-Z][a-z]*\s+[0-3][0-9],?\s+\d{1,4}$''',	#July 27(,) 2016
	r'''^[A-Z][a-z]*\.,?\s+[0-3][0-9]\s+[A-Z][a-z]*\.,?\s+\d{1,4}$''',	#Wed.(,) 27 Jul.(,) 2016
	r'''^[A-Z][a-z]*\.,?\s+[A-Z][a-z]*\.\s+[0-3][0-9],?\s+\d{1,4}$''',	#Wed.(,) Jul. 27(,) 2016
	r'''^[A-Z][a-z]*\.,?\s+[0-3][0-9]\s+[A-Z][a-z]*,?\s+\d{1,4}$''',	#Wed.(,) 27 July(,) 2016
	r'''^[A-Z][a-z]*\.,?\s+[A-Z][a-z]*\s+[0-3][0-9],?\s+\d{1,4}$''',	#Wed.(,) July 27(,) 2016
	r'''^[A-Z][a-z]*,?\s+[0-3][0-9]\s+[A-Z][a-z]*\.,?\s+\d{1,4}$''',	#Wednesday(,) 27 Jul.(,) 2016
	r'''^[A-Z][a-z]*,?\s+[A-Z][a-z]*\.\s+[0-3][0-9],?\s+\d{1,4}$''',	#Wednesday(,) Jul. 27(,) 2016
	r'''^[A-Z][a-z]*,?\s+[0-3][0-9]\s+[A-Z][a-z]*,?\s+\d{1,4}$''',	#Wednesday(,) 27 July(,) 2016
	r'''^[A-Z][a-z]*,?\s+[A-Z][a-z]*\s+[0-3][0-9],?\s+\d{1,4}$''',	#Wednesday(,) July 27(,) 2016
	r'''^[A-Z]+\.,?\s+\d{1,4}$''',	#JUL.(,) 2016
	r'''^[A-Z]+,?\s+\d{1,4}$''',	#JULY(,) 2016
	r'''^[0-3][0-9]\s+[A-Z]+\.,?\s+\d{1,4}$''',	#27 JUL.(,) 2016
	r'''^[0-3][0-9]\s+[A-Z]+,?\s+\d{1,4}$''',	#27 JULY(,) 2016
	r'''^[A-Z]+\.\s+[0-3][0-9],?\s+\d{1,4}$''',	#JUL. 27(,) 2016
	r'''^[A-Z]+\s+[0-3][0-9],?\s+\d{1,4}$''',	#JULY 27(,) 2016
	r'''^[A-Z]+\.,?\s+[0-3][0-9]\s+[A-Z]+\.,?\s+\d{1,4}$''',	#WED.(,) 27 JUL.(,) 2016
	r'''^[A-Z]+\.,?\s+[A-Z]+\.\s+[0-3][0-9],?\s+\d{1,4}$''',	#WED.(,) JUL. 27(,) 2016
	r'''^[A-Z]+\.,?\s+[0-3][0-9]\s+[A-Z]+,?\s+\d{1,4}$''',	#WED.(,) 27 JULY(,) 2016
	r'''^[A-Z]+\.,?\s+[A-Z]+\s+[0-3][0-9],?\s+\d{1,4}$''',	#WED.(,) JULY 27(,) 2016
	r'''^[A-Z]+,?\s+[0-3][0-9]\s+[A-Z]+\.,?\s+\d{1,4}$''',	#WEDNESDAY(,) 27 JUL.(,) 2016
	r'''^[A-Z]+,?\s+[A-Z]+\.\s+[0-3][0-9],?\s+\d{1,4}$''',	#WEDNESDAY(,) JUL. 27(,) 2016
	r'''^[A-Z]+,?\s+[0-3][0-9]\s+[A-Z]+,?\s+\d{1,4}$''',	#WEDNESDAY(,) 27 JULY(,) 2016
	r'''^[A-Z]+,?\s+[A-Z]+\s+[0-3][0-9],?\s+\d{1,4}$''',	#WEDNESDAY(,) JULY 27(,) 2016
	r'''^[a-z]+\.,?\s+\d{1,4}$''',	#jul.(,) 2016
	r'''^[a-z]+,?\s+\d{1,4}$''',	#july(,) 2016
	r'''^[0-3][0-9]\s+[a-z]+\.,?\s+\d{1,4}$''',	#27 jul.(,) 2016
	r'''^[0-3][0-9]\s+[a-z]+,?\s+\d{1,4}$''',	#27 july(,) 2016
	r'''^[a-z]+\.\s+[0-3][0-9],?\s+\d{1,4}$''',	#jul. 27(,) 2016
	r'''^[a-z]+\s+[0-3][0-9],?\s+\d{1,4}$''',	#july 27(,) 2016
	r'''^[a-z]+\.,?\s+[0-3][0-9]\s+[a-z]+\.,?\s+\d{1,4}$''',	#wed.(,) 27 jul.(,) 2016
	r'''^[a-z]+\.,?\s+[a-z]+\.\s+[0-3][0-9],?\s+\d{1,4}$''',	#wed.(,) jul. 27(,) 2016
	r'''^[a-z]+\.,?\s+[0-3][0-9]\s+[a-z]+,?\s+\d{1,4}$''',	#wed.(,) 27 july(,) 2016
	r'''^[a-z]+\.,?\s+[a-z]+\s+[0-3][0-9],?\s+\d{1,4}$''',	#wed.(,) july 27(,) 2016
	r'''^[a-z]+,?\s+[0-3][0-9]\s+[a-z]+\.,?\s+\d{1,4}$''',	#wednesday(,) 27 jul.(,) 2016
	r'''^[a-z]+,?\s+[a-z]+\.\s+[0-3][0-9],?\s+\d{1,4}$''',	#wednesday(,) jul. 27(,) 2016
	r'''^[a-z]+,?\s+[0-3][0-9]\s+[a-z]+,?\s+\d{1,4}$''',	#wednesday(,) 27 july(,) 2016
	r'''^[a-z]+,?\s+[a-z]+\s+[0-3][0-9],?\s+\d{1,4}$''']	#wednesday(,) july 27(,) 2016

#fa_regex = r'''^(?:[Oo][Nn][Ee]|[0-9-]*[a-zA-Z]?)\s+(?:[NSEW]\.?[NSEW]?\.?\s+|(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+)?(?:\d*(?:[SNRTsnrt][TDHtdh])?(?:\s+[a-zA-Z'-]*)?|(?:[a-zA-Z'-]*\s+)*?(?:[a-zA-Z'-]*))\.?(?:\s+\d*)?,?(?:\s+[NSEW]\.?[NESW]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])?)?(?:\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|\s+(?:[a-zA-Z][a-z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?(?:\s+(?:[#]\s*)?\w*(?:[-/: ]\w*)?))?,?\s(?:[a-zA-Z'-]*\s)*?[a-zA-Z'-]*,?\s[a-zA-Z]*,?\s(?:\d{5}|\d{5}(?:\s|[.-])?\d{4})(?:,?\s[A-Za-z'-]*)*$'''
FULL_ADDRESS_REGEXS = [r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*),?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})?$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*),?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})?$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*),?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})?$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?))(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*),?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})?$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?))(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:St\.?\s+|Dr\.?\s+)?[A-Z][a-z]+\s+(?:[Aa]nd\s+)?)*[A-Z][a-z]+$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:St\.?\s+|Dr\.?\s+)?[A-Z][a-z]+\s+(?:[Aa]nd\s+)?)*[A-Z][a-z]+$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:St\.?\s+|Dr\.?\s+)?[A-Z][a-z]+\s+(?:[Aa]nd\s+)?)*[A-Z][a-z]+$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:St\.?\s+|Dr\.?\s+)?[A-Z][a-z]+\s+(?:[Aa]nd\s+)?)*[A-Z][a-z]+$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:St\.?\s+|Dr\.?\s+)?[A-Z][a-z]+\s+(?:[Aa]nd\s+)?)*[A-Z][a-z]+$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?))(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:St\.?\s+|Dr\.?\s+)?[A-Z][a-z]+\s+(?:[Aa]nd\s+)?)*[A-Z][a-z]+$''',
	#begin lower case
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*),?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})?$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)*(?:[a-z]+(?:'s|-[a-z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*),?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})?$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)*(?:[a-z]+(?:'s|-[a-z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*),?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})?$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)*(?:[a-z]+(?:'s|-[a-z]+)?))(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*),?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})?$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)*(?:[a-z]+(?:'s|-[a-z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)*(?:[a-z]+(?:'s|-[a-z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{2,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)*(?:[a-z]+(?:'s|-[a-z]+)?))(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:st\.?\s+|dr\.?\s+)?[a-z]+\s+(?:and\s+)?)*[a-z]+$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:st\.?\s+|dr\.?\s+)?[a-z]+\s+(?:and\s+)?)*[a-z]+$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:st\.?\s+|dr\.?\s+)?[a-z]+\s+(?:and\s+)?)*[a-z]+$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)*(?:[a-z]+(?:'s|-[a-z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:st\.?\s+|dr\.?\s+)?[a-z]+\s+(?:and\s+)?)*[a-z]+$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)*(?:[a-z]+(?:'s|-[a-z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:st\.?\s+|dr\.?\s+)?[a-z]+\s+(?:and\s+)?)*[a-z]+$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)*(?:[a-z]+(?:'s|-[a-z]+)?))(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:st\.?\s+)?(?:[a-z]*(?:'s)?\s+)*?[a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[a-z]{3,}\s+)*[a-z]{3,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:st\.?\s+|dr\.?\s+)?[a-z]+\s+(?:and\s+)?)*[a-z]+$''',
	#begin upper case
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*),?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})?$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)*(?:[A-Z]+(?:'S|-[A-Z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*),?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})?$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)*(?:[A-Z]+(?:'S|-[A-Z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*),?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})?$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)*(?:[A-Z]+(?:'S|-[A-Z]+)?))(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*),?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})?$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)*(?:[A-Z]+(?:'S|-[A-Z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)*(?:[A-Z]+(?:'S|-[A-Z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{2,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)*(?:[A-Z]+(?:'S|-[A-Z]+)?))(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})\s+\d{5}(?:[ -]?\d{4})?$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:ST\.?\s+|DR\.?\s+)?[A-Z]+\s+(?:AND\s+)?)*[A-Z]+$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:ST\.?\s+|DR\.?\s+)?[A-Z]+\s+(?:AND\s+)?)*[A-Z]+$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:ST\.?\s+|DR\.?\s+)?[A-Z]+\s+(?:AND\s+)?)*[A-Z]+$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)*(?:[A-Z]+(?:'S|-[A-Z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:ST\.?\s+|DR\.?\s+)?[A-Z]+\s+(?:AND\s+)?)*[A-Z]+$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)*(?:[A-Z]+(?:'S|-[A-Z]+)?))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:ST\.?\s+|DR\.?\s+)?[A-Z]+\s+(?:AND\s+)?)*[A-Z]+$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)*(?:[A-Z]+(?:'S|-[A-Z]+)?))(?:\s+[NSEWnsew]\.?[NSEWnsew]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]))(?:,?\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)?,?\s+(?:ST\.?\s+)?(?:[A-Z]*(?:'S)?\s+)*?[A-Z]*(?:'S)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z]{3,}\s+)*[A-Z]{3,})\s+\d{5}(?:[ -]?\d{4})?,?\s+(?:(?:ST\.?\s+|DR\.?\s+)?[A-Z]+\s+(?:AND\s+)?)*[A-Z]+$''']

#sa_regex = r'''^(?:[Oo][Nn][Ee]|[0-9-]*[a-zA-Z]?)\s+(?:[NSEW]\.?[NSEW]?\.?\s+|(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+)?(?:\d*(?:[SNRTsnrt][TDHtdh])?(?:\s+[a-zA-Z'-]*)?|(?:[a-zA-Z'-]*\s+)*?(?:[a-zA-Z'-]*))\.?(?:\s+\d*)?,?(?:\s+[NSEW]\.?[NESW]?\.?|\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])?)?(?:\s+\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|\s+(?:[a-zA-Z][a-z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?(?:\s+(?:[#]\s*)?\w*(?:[-/: ]\w*)?))?$'''
STREET_ADDRESS_REGEXS = [r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?$''',	#(One/123) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore)) (Road/Rd(.))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?))$''',	#(One/123) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?))$''',	#(One/123) ((n/N)(.)((w/W)(.))) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?))$''',	#(One/123) (North/East...Southwest) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?$''',	#(One/123) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore))((n/N)(.)((w/W)(.)))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])$''',	#(One/123) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore)) (North/East...Southwest)
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?$''',	#(One/123) ((n/N)(.)((w/W)(.))) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore)) (Road/Rd(.))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?$''',	#(One/123) (North/East...Southwest) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore)) (Road/Rd(.))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?\s+[NSEWnsew]\.?[NSEWnsew]?\.?$''',	#(One/123) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore)) (Road/Rd(.)) ((n/N)(.)((w/W)(.)))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])$''',	#(One/123) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore)) (Road/Rd(.)) (North/East...Southwest)
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?,?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',	#(One/123) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore)) (Road/Rd(.))(,) (3(rd) Flr(.)/(Apt(.)\PO(.) Box) (# ) 23A(-F)(...))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?)),?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',	#(One/123) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore))(,) (3(rd) Flr(.)/(Apt(.)\PO(.) Box) (# ) 23A(-F)(...))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?)),?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',	#(One/123) ((n/N)(.)((w/W)(.))) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore))(,) (3(rd) Flr(.)/(Apt(.)\PO(.) Box) (# ) 23A(-F)(...))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?)),?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',	#(One/123) (North/East...Southwest) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore))(,) (3(rd) Flr(.)/(Apt(.)\PO(.) Box) (# ) 23A(-F)(...))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?,?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',	#(One/123) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore))((n/N)(.)((w/W)(.)))(,) (3(rd) Flr(.)/(Apt(.)\PO(.) Box) (# ) 23A(-F)(...))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]),?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',	#(One/123) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore)) (North/East...Southwest)(,) (3(rd) Flr(.)/(Apt(.)\PO(.) Box) (# ) 23A(-F)(...))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?,?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',	#(One/123) ((n/N)(.)((w/W)(.))) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore)) (Road/Rd(.))(,) (3(rd) Flr(.)/(Apt(.)\PO(.) Box) (# ) 23A(-F)(...))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?,?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',	#(One/123) (North/East...Southwest) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore)) (Road/Rd(.))(,) (3(rd) Flr(.)/(Apt(.)\PO(.) Box) (# ) 23A(-F)(...))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?\s+[NSEWnsew]\.?[NSEWnsew]?\.?,?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',	#(One/123) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore)) (Road/Rd(.)) ((n/N)(.)((w/W)(.)))(,) (3(rd) Flr(.)/(Apt(.)\PO(.) Box) (# ) 23A(-F)(...))
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)+?)[A-Z][a-z]+\.?\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]),?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',	#(One/123) (2nd/((St(.)/Dr(.))) Ardmore('s/-Ardmore)) (Road/Rd(.))(,) (North/East...Southwest) (3(rd) Flr(.)/(Apt(.)\PO(.) Box) (# ) 23A(-F)(...))
	#same as above but lower case
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)*(?:[a-z]+(?:'s|-[a-z]+)?))$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)*(?:[a-z]+(?:'s|-[a-z]+)?))$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)*(?:[a-z]+(?:'s|-[a-z]+)?))$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?\s+[NSEWnsew]\.?[NSEWnsew]?\.?$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?,?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)*(?:[a-z]+(?:'s|-[a-z]+)?)),?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)*(?:[a-z]+(?:'s|-[a-z]+)?)),?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)*(?:[a-z]+(?:'s|-[a-z]+)?)),?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?,?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]),?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?,?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?,?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?\s+[NSEWnsew]\.?[NSEWnsew]?\.?,?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:one|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:st\.?\s+|dr\.?\s+)?(?:[a-z]+(?:'s|-[a-z]+)?\s+)+?)[a-z]+\.?\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]),?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	#same as above but all upper-case
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)*(?:[A-Z]+(?:'S|-[A-Z]+)?))$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:St\.?\s+|Dr\.?\s+)?(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?\s+)*(?:[A-Z][a-z]+(?:'s|-[A-Z][a-z]+)?))$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)*(?:[A-Z]+(?:'S|-[A-Z]+)?))$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?$''',
	r'''^(?:One|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?\s+[NSEWnsew]\.?[NSEWnsew]?\.?$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'s|-[A-Z]+)?\s+)+?)[A-Z]+\.?,?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)*(?:[A-Z]+(?:'S|-[A-Z]+)?)),?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)*(?:[A-Z]+(?:'S|-[A-Z]+)?)),?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+(?:\d*(?:[SNRTsnrt][TDHtdh])|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)*(?:[A-Z]+(?:'S|-[A-Z]+)?)),?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?,?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]),?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+[NSEWnsew]\.?[NSEWnsew]?\.?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?,?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt])\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?,?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?\s+[NSEWnsew]\.?[NSEWnsew]?\.?,?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''',
	r'''^(?:ONE|[0-9-]*[a-zA-Z]?)\s+(?:\d*(?:[SNRTsnrt][TDHtdh])\s+|(?:ST\.?\s+|DR\.?\s+)?(?:[A-Z]+(?:'S|-[A-Z]+)?\s+)+?)[A-Z]+\.?\s+(?:[NSEWnsew][OAEoae][RUSrus][Tt][Hh]?|[NSns][Oo][RUru][Tt][Hh][EWew][EAea][Ss][Tt]),?\s+(?:\d*(?:[SNRTsnrt][TDHtdh])?\s+[a-zA-Z]*\.?|(?:[a-zA-Z]*\.?|[Pp][Oo]\.?\s+?[Bb][Oo][Xx])?\s+(?:#\s*)?\w*(?:[-/: ]\w*)*)$''']
#cs_regex = r'''^(?:[a-zA-Z'-]*\s)*?[a-zA-Z'-]*,?\s[a-zA-Z]*$'''

#CITYSTATE_TESTER_STRINGS = ['Chicago, IL', 'St. Chicago, Il', "St Chicago's, il", 'Chicago, Illinois', 'CHICAGO, IL', 'ST. CHICAGO, ILLINOIS', 'chicago, il', "chicago's park, illinois", 'St Chicago IL', 'St Chicago Il', 'Chicago il', "Arbor's Peak Illiois", 'CHICAGO HEIGHTS IL', 'CHICAGO STATION ILLINOIS', 'st. chicago il', 'chicago illinois']

CITYSTATE_REGEXS = [r'''^(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,\s+[A-Z][A-Z]$''', #(St(.) )Chicago('s) (...), IL
	r'''^(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,\s+[A-Z][a-z]$''',	#(St(.) )Chicago('s) (...), Il
	r'''^(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,\s+[a-z][a-z]$''',	#(St(.) )Chicago('s) (...), il
	r'''^(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,\s+(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,}$''',	#(St(.) )Chicago('s) (...), Illinois (...)
	r'''^(?:ST\.?\s+)?(?:[A-Z]+(?:'S)?\s+)*?[A-Z]+(?:'S)?,\s+[A-Z][A-Z]$''',	#(ST. )CHICAGO('S) (...), IL
	r'''^(?:ST\.?\s+)?(?:[A-Z]+(?:'S)?\s+)*?[A-Z]+(?:'S)?,\s+(?:[A-Z]{3,}\s+)*[A-Z]{3,}$''',	#(ST. )CHICAGO('S) (...), ILLINOIS (...)
	r'''^(?:st\.?\s+)?(?:[a-z]+(?:'s)?\s+)*?[a-z]+(?:'s)?,\s+[a-z][a-z]$''',	#(st. )chicago('s) (...), il
	r'''^(?:st\.?\s+)?(?:[a-z]+(?:'s)?\s+)*?[a-z]+(?:'s)?,\s+(?:[a-z]{3,}\s+)*[a-z]{3,}$''',	#(st. )chicago('s) (...), illinois (...)
	r'''^(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?\s+[A-Z][A-Z]$''', #(St(.) )Chicago('s) (...) IL
	r'''^(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?\s+[A-Z][a-z]$''',	#(St(.) )Chicago('s) (...) Il
	r'''^(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?\s+[a-z][a-z]$''',	#(St(.) )Chicago('s) (...) il
	r'''^(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?\s+(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,}$''',	#(St(.) )Chicago('s) (...) Illinois (...)
	r'''^(?:ST\.?\s+)?(?:[A-Z]+(?:'S)?\s+)*?[A-Z]+(?:'S)?\s+[A-Z][A-Z]$''',	#(ST. )CHICAGO('S) (...) IL
	r'''^(?:ST\.?\s+)?(?:[A-Z]+(?:'S)?\s+)*?[A-Z]+(?:'S)?\s+(?:[A-Z]{3,}\s+)*[A-Z]{3,}$''',	#(ST. )CHICAGO('S) (...) ILLINOIS (...)
	r'''^(?:st\.?\s+)?(?:[a-z]+(?:'s)?\s+)*?[a-z]+(?:'s)?\s+[a-z][a-z]$''',	#(st. )chicago('s) (...) il
	r'''^(?:st\.?\s+)?(?:[a-z]+(?:'s)?\s+)*?[a-z]+(?:'s)?\s+(?:[a-z]{3,}\s+)*[a-z]{3,}$''']	#(st. )chicago('s) (...) illinois (...)

#em_regex = r'''^\S*?@\S*?(?:\.\S*?)+$'''
EMAIL_REGEXS = [r'''^[a-zA-Z0-9!#$%&'*+-/=?^_`{|}~.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+$''',	#j.smith24@gmail.com
	r'''^[a-zA-Z0-9!#$%&'*+-/=?^_`{|}~.]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+$''']	#j.smith24@kr.string.mymail.(...).com

#lo_regex = r'''^(?:[A-Z][a-z'-]*\s)*?(?:[A-Z][a-z'-]*)$'''
LOCATION_REGEXS = [r'''^(?:[A-Z][a-z'-]*\s)*?(?:[A-Z][a-z'-]*)$''',	#Golden Gate Bridge
	r'''^(?:[a-z'-]*\s)*?(?:[a-z'-]*)$''',	#golden gate bridge
	r'''^(?:[A-Z'-]*\s)*?(?:[A-Z'-]*)$''']	#GOLDEN GATE BRIDGE

#de_regex = r'''^(?:["'<-]?[A-Za-z0-9'-]+[>"',;:-]?(?:\s|[.?!]\s+))+$'''
DESCRIPTION_REGEXS = [r'''^(?:["'<-]?[A-Za-z0-9'-]+[>"',;:-]?(?:\s|[.?!]\s+))+$''']	#This is a "description" example.
	
#url_regex = r'''^[A-Za-z][a-zA-Z0-9+.-]*:(?:[/][/])?(?:[a-zA-Z0-9!$&'()*+,;=%+-]+?(?:[:][a-zA-Z0-9!$&'()*+,;=%+-]+?)@?)?(?:(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+)?|\[(?:[a-eA-E0-9]*[:])+[a-eA-E0-9]*(?:(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+))?|(?:[0-9a-zA-Z-]\.)+[0-9a-zA-Z-]+))(?:[:]\d+)?[/]?(?:[a-zA-Z0-9!$&'()*+,;=%+-:@]+[/])*[a-zA-Z0-9!$&'()*+,;=%+-:@]+(?:\.[a-zA-Z]+)?(?:\?[a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?(?:[#][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?$'''
URL_REGEXS = [r'''^(?:[/][/])(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+)?(?:[:]\d+)?$''',	#//1.2.3.4(/8)(:8000) - actually just an ip address but included for completeness - can be removed later for efficiency or whatever
	r'''^(?:[/][/])?\[?(?:[a-eA-E0-9]*[:])+[a-eA-E0-9]*(?:(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+))?](?:[:]\d+)?$''',	#(//)[1:2:3:4:5:6(1.2.3.4/:7:8)](:8000)
	r'''^(?:[/][/])?(?:[0-9a-zA-Z-]+\.)+[0-9a-zA-Z-]+$''',	#(//)www.example.com(:8000)
	r'''^(?:[/][/])?(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+)?(?:[:]\d+)?[/]?(?:[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/])*[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/]?(?:[?][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?(?:[#][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?$''',	#(//)1.2.3.4(/8)(:8000)/path/name(?query)(#fragment)
	r'''^(?:[/][/])?\[?(?:[a-eA-E0-9]*[:])+[a-eA-E0-9]*(?:(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+))?](?:[:]\d+)?[/]?(?:[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/])*[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/]?(?:[?][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?(?:[#][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?$''',	#(//)[1:2:3:4:5:6(1.2.3.4/:7:8)](:8000)/path/name(?query)(#fragment)
	r'''^(?:[/][/])?(?:[0-9a-zA-Z-]+\.)+[0-9a-zA-Z-]+(?:[:]\d+)?[/]?(?:[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/])*[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/]?(?:[?][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?(?:[#][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?$''',	#(//)www.example.com(:8000)/path/name(?query)(#fragment)
	r'''^(?:[/][/])?(?:[a-zA-Z0-9!$&'()*+,;=%+-]+?(?:[:][a-zA-Z0-9!$&'()*+,;=%+-]+?)?@)(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+)?(?:[:]\d+)?$''',	#(//)user(:password)@1.2.3.4(/8)(:8000)
	r'''^(?:[/][/])?(?:[a-zA-Z0-9!$&'()*+,;=%+-]+?(?:[:][a-zA-Z0-9!$&'()*+,;=%+-]+?)?@)\[?(?:[a-eA-E0-9]*[:])+[a-eA-E0-9]*(?:(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+))?](?:[:]\d+)?$''',	#(//)user(:password)@[1:2:3:4:5:6(1.2.3.4/:7:8)](:8000)
	r'''^(?:[/][/])?(?:[a-zA-Z0-9!$&'()*+,;=%+-]+?(?:[:][a-zA-Z0-9!$&'()*+,;=%+-]+?)?@)(?:[0-9a-zA-Z-]+\.)+[0-9a-zA-Z-]+$''',	#(//)user(:password)@www.example.com(:8000)
	r'''^(?:[/][/])?(?:[a-zA-Z0-9!$&'()*+,;=%+-]+?(?:[:][a-zA-Z0-9!$&'()*+,;=%+-]+?)?@)(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+)?(?:[:]\d+)?[/]?(?:[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/])*[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/]?(?:[?][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?(?:[#][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?$''',	#(//)user(:password)@1.2.3.4(/8)(:8000)/path/name(?query)(#fragment)
	r'''^(?:[/][/])?(?:[a-zA-Z0-9!$&'()*+,;=%+-]+?(?:[:][a-zA-Z0-9!$&'()*+,;=%+-]+?)?@)\[?(?:[a-eA-E0-9]*[:])+[a-eA-E0-9]*(?:(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+))?](?:[:]\d+)?[/]?(?:[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/])*[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/]?(?:[?][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?(?:[#][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?$''',	#(//)user(:password)@[1:2:3:4:5:6(1.2.3.4/:7:8)](:8000)/path/name(?query)(#fragment)
	r'''^(?:[/][/])?(?:[a-zA-Z0-9!$&'()*+,;=%+-]+?(?:[:][a-zA-Z0-9!$&'()*+,;=%+-]+?)?@)(?:[0-9a-zA-Z-]+\.)+[0-9a-zA-Z-]+(?:[:]\d+)?[/]?(?:[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/])*[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/]?(?:[?][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?(?:[#][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?$''',	#(//)user(:password)@www.example.com(:8000)/path/name(?query)(#fragment)
	#the following regexs are the same as above with a scheme: included at the beginning
	r'''^[A-Za-z][a-zA-Z0-9+.-]*:(?:[/][/])?(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+)?(?:[:]\d+)?$''',
	r'''^[A-Za-z][a-zA-Z0-9+.-]*:(?:[/][/])?\[?(?:[a-eA-E0-9]*[:])+[a-eA-E0-9]*(?:(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+))?](?:[:]\d+)?$''',
	r'''^[A-Za-z][a-zA-Z0-9+.-]*:(?:[/][/])?(?:[0-9a-zA-Z-]+\.)+[0-9a-zA-Z-]+$''',
	r'''^[A-Za-z][a-zA-Z0-9+.-]*:(?:[/][/])?(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+)?(?:[:]\d+)?[/]?(?:[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/])*[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/]?(?:[?][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?(?:[#][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?$''',
	r'''^[A-Za-z][a-zA-Z0-9+.-]*:(?:[/][/])?\[?(?:[a-eA-E0-9]*[:])+[a-eA-E0-9]*(?:(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+))?](?:[:]\d+)?[/]?(?:[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/])*[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/]?(?:[?][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?(?:[#][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?$''',
	r'''^[A-Za-z][a-zA-Z0-9+.-]*:(?:[/][/])?(?:[0-9a-zA-Z-]+\.)+[0-9a-zA-Z-]+(?:[:]\d+)?[/]?(?:[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/])*[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/]?(?:[?][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?(?:[#][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?$''',
	r'''^[A-Za-z][a-zA-Z0-9+.-]*:(?:[/][/])?(?:[a-zA-Z0-9!$&'()*+,;=%+-]+?(?:[:][a-zA-Z0-9!$&'()*+,;=%+-]+?)?@)(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+)?(?:[:]\d+)?$''',
	r'''^[A-Za-z][a-zA-Z0-9+.-]*:(?:[/][/])?(?:[a-zA-Z0-9!$&'()*+,;=%+-]+?(?:[:][a-zA-Z0-9!$&'()*+,;=%+-]+?)?@)\[?(?:[a-eA-E0-9]*[:])+[a-eA-E0-9]*(?:(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+))?](?:[:]\d+)?$''',
	r'''^[A-Za-z][a-zA-Z0-9+.-]*:(?:[/][/])?(?:[a-zA-Z0-9!$&'()*+,;=%+-]+?(?:[:][a-zA-Z0-9!$&'()*+,;=%+-]+?)?@)(?:[0-9a-zA-Z-]+\.)+[0-9a-zA-Z-]+$''',
	r'''^[A-Za-z][a-zA-Z0-9+.-]*:(?:[/][/])?(?:[a-zA-Z0-9!$&'()*+,;=%+-]+?(?:[:][a-zA-Z0-9!$&'()*+,;=%+-]+?)?@)(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+)?(?:[:]\d+)?[/]?(?:[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/])*[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/]?(?:[?][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?(?:[#][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?$''',
	r'''^[A-Za-z][a-zA-Z0-9+.-]*:(?:[/][/])?(?:[a-zA-Z0-9!$&'()*+,;=%+-]+?(?:[:][a-zA-Z0-9!$&'()*+,;=%+-]+?)?@)\[?(?:[a-eA-E0-9]*[:])+[a-eA-E0-9]*(?:(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+))?](?:[:]\d+)?[/]?(?:[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/])*[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/]?(?:[?][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?(?:[#][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?$''',
	r'''^[A-Za-z][a-zA-Z0-9+.-]*:(?:[/][/])?(?:[a-zA-Z0-9!$&'()*+,;=%+-]+?(?:[:][a-zA-Z0-9!$&'()*+,;=%+-]+?)?@)(?:[0-9a-zA-Z-]+\.)+[0-9a-zA-Z-]+(?:[:]\d+)?[/]?(?:[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/])*[a-zA-Z0-9!$&'()*+.,;=%+:~@_-]+[/]?(?:[?][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?(?:[#][a-zA-Z0-9!$&'()*+,;=%+-:@?]*)?$''']

#r'''(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*?[A-Z][a-z]*(?:'s)?,?\s+(?:[A-Za-z][A-Za-z]|(?:[A-Z][a-z]{2,}\s+)*[A-Z][a-z]{2,})\s+'''
CITY_REGEXS = [r'''^(?:St\.?\s+)?(?:[A-Z][a-z]*(?:'s)?\s+)*[A-Z][a-z]*(?:'s)?''',	#(St. )Chicago's Place
	r'''^(?:ST\.?\s+)?(?:[A-Z]+(?:'S)?\s+)*[A-Z]+(?:'S)?''',	#(ST. )CHICAGO'S PLACE
	r'''^(?:st\.?\s+)?(?:[a-z]+(?:'s)?\s+)*[a-z]+(?:'s)?''']	#(st. )chicago's place
STATE_REGEXS = [r'''^[A-Z][a-z]{2,}$''',	#California
	r'''^(?:[A-Z][a-z]{2,}\s+)+[A-Z][a-z]{2,}$''',	#Rhode Island (...)
	r'''^[A-Z]{3,}$''',	#CALIFORNIA
	r'''^(?:[A-Z]{3,}\s+)+[A-Z]{3,}$''',	#RHODE ISLAND (...)
	r'''^[a-z]{3,}$''',	#california
	r'''^(?:[a-z]{3,}\s+)+[a-z]{3,}$''',	#rhode island (...)
	r'''^[A-Z][A-Z]$''',	#IL
	r'''^[A-Z][a-z]$''',	#Il
	r'''^[a-z][a-z]$''']	#il



#list of types for new regular expressions - date, longitude, latitude, number, zip, phone number, ip, year, ISBN

#dt_regex = r'''^\d{1,2}[./, -]\d{1,2}[./, -]'?\d{1,4}$'''
DATE_REGEXS = [r'''^[01]?\d[.][0123]?\d[.]\d{1,4}$''',	#8.3.2016
	r'''^[01]?\d[/][0123]?\d[/]\d{1,4}$''',	#8/3/2016
	r'''^[01]?\d[,][0123]?\d[,]\d{1,4}$''',	#8,3,2016
	r'''^[01]?\d[ ][0123]?\d[ ]\d{1,4}$''',	#8 3 2016
	r'''^[01]?\d[-][0123]?\d[-]\d{1,4}$''',	#8-3-2016
	r'''^[01]?\d[.][0123]?\d[.]'\d{2}$''',	#8.3.'16
	r'''^[01]?\d[/][0123]?\d[/]'\d{2}$''',	#8/3/'16
	r'''^[01]?\d[,][0123]?\d[,]'\d{2}$''',	#8,3,'16
	r'''^[01]?\d[ ][0123]?\d[ ]'\d{2}$''',	#8 3 '16
	r'''^[01]?\d[-][0123]?\d[-]'\d{2}$''',	#8-3-'16
	r'''^[0123]?\d[.][01]?\d[.]\d{1,4}$''',	#3.8.2016
	r'''^[0123]?\d[/][01]?\d[/]\d{1,4}$''',	#3/8/2016
	r'''^[0123]?\d[,][01]?\d[,]\d{1,4}$''',	#3,8,2016
	r'''^[0123]?\d[ ][01]?\d[ ]\d{1,4}$''',	#3 8 2016
	r'''^[0123]?\d[-][01]?\d[-]\d{1,4}$''',	#3-8-2016
	r'''^[0123]?\d[.][01]?\d[.]'\d{2}$''',	#3.8.'16
	r'''^[0123]?\d[/][01]?\d[/]'\d{2}$''',	#3/8/'16
	r'''^[0123]?\d[,][01]?\d[,]'\d{2}$''',	#3,8,'16
	r'''^[0123]?\d[ ][01]?\d[ ]'\d{2}$''',	#3 8 '16
	r'''^[0123]?\d[-][01]?\d[-]'\d{2}$''',	#3-8-'16
	r'''^\d{1,4}[.][0123]?\d[.][01]?\d$''',	#2016.3.8
	r'''^\d{1,4}[/][0123]?\d[/][01]?\d$''',	#2016/3/8
	r'''^\d{1,4}[,][0123]?\d[,][01]?\d$''',	#2016,3,8
	r'''^\d{1,4}[ ][0123]?\d[ ][01]?\d$''',	#2016 3 8
	r'''^\d{1,4}[-][0123]?\d[-][01]?\d$''',	#2016-3-8
	r'''^'\d{2}[.][0123]?\d[.][01]?\d$''',	#'16.3.8
	r'''^'\d{2}[/][0123]?\d[/][01]?\d$''',	#'16/3/8
	r'''^'\d{2}[,][0123]?\d[,][01]?\d$''',	#'16,3,8
	r'''^'\d{2}[ ][0123]?\d[ ][01]?\d$''',	#'16 3 8
	r'''^'\d{2}[-][0123]?\d[-][01]?\d$''',	#'16-3-8
	r'''^\d{1,4}[.][01]?\d[.][0123]?\d$''',	#2016.8.3
	r'''^\d{1,4}[/][01]?\d[/][0123]?\d$''',	#2016/8/3
	r'''^\d{1,4}[,][01]?\d[,][0123]?\d$''',	#2016,8,3
	r'''^\d{1,4}[ ][01]?\d[ ][0123]?\d$''',	#2016 8 3
	r'''^\d{1,4}[-][01]?\d[-][0123]?\d$''',	#2016-8-3
	r'''^'\d{2}[.][01]?\d[.][0123]?\d$''',	#'16.8.3
	r'''^'\d{2}[/][01]?\d[/][0123]?\d$''',	#'16/8/3
	r'''^'\d{2}[,][01]?\d[,][0123]?\d$''',	#'16,8,3
	r'''^'\d{2}[ ][01]?\d[ ][0123]?\d$''',	#'16 8 3
	r'''^'\d{2}[-][01]?\d[-][0123]?\d$''',	#'16-8-3
	r'''^[01]?\d[.][0123]?\d$''',	#8.3
	r'''^[01]?\d[/][0123]?\d$''',	#8/3
	r'''^[01]?\d[,][0123]?\d$''',	#8,3
	r'''^[01]?\d[ ][0123]?\d$''',	#8 3
	r'''^[01]?\d[-][0123]?\d$''',	#8-3
	r'''^[0123]?\d[.][01]?\d$''',	#3.8
	r'''^[0123]?\d[/][01]?\d$''',	#3/8
	r'''^[0123]?\d[,][01]?\d$''',	#3,8
	r'''^[0123]?\d[ ][01]?\d$''',	#3 8
	r'''^[0123]?\d[-][01]?\d$''']	#3-8
	

#long_regex = r'''^[-]?\d{1,3}\.\d{1,20}$'''
LONGITUDE_REGEXS = [r'''^-1\d{1,2}\.\d*$''',	#-123.19502
	r'''^-\d{1,2}\.\d*$''',	#-23.19502
	r'''^1\d{1,2}\.\d*$''',	#123.19502
	r'''^\d{1,2}\.\d*$''']	#23.19502

#lat_regex = r'''^[-]?\d{1,2}\.\d{1,20}$'''
LATITUDE_REGEXS = [r'''^-1\d{1,2}\.\d*$''',	#-123.19502
	r'''^-\d{1,2}\.\d*$''',	#-23.19502
	r'''^1\d{1,2}\.\d*$''',	#123.19502
	r'''^\d{1,2}\.\d*$''']	#23.19502

#num_regex = r'''^\d*(?:\.\d*)$'''
NUMBER_REGEXS = [r'''^\d+$''',	#123
	r'''^\d+\.\d*$''',	#123.4
	r'''^-\d+$''',	#-123
	r'''^-\d+\.\d*$''',	#-123.4
	r'''^\d{1,3},(?:\d{3},)*\d{3}$''',	#1,234,567
	r'''^\d{1,3},(?:\d{3},)*\d{3}\.\d+$''',	#1,234,567.8
	r'''^-\d{1,3},(?:\d{3},)*\d{3}$''',	#-1,234,567
	r'''^-\d{1,3},(?:\d{3},)*\d{3}\.\d+$''',	#-1,234,567.8
	r'''^\d+,\d*$''',	#123,4
	r'''^-\d+,\d*$''',	#-123,4
	r'''^\d{1,3}\.(?:\d{3}\.)*\d{3}$''',	#1.234.567
	r'''^\d{1,3}\.(?:\d{3}\.)*\d{3},\d+$''',	#1.234.567,8
	r'''^-\d{1,3}\.(?:\d{3}\.)*\d{3}$''',	#-1.234.567
	r'''^-\d{1,3}\.(?:\d{3}\.)*\d{3},\d+$''']	#-1.234.567,8

#zip_regex = r'''^\d{5}(?:[ -]?\d{4})?$'''
ZIP_REGEXS = [r'''^\d{5}$''', #12345
	r'''^\d{5}\s\d{4}$''',	#12345 6789
	r'''^\d{5}-\d{4}$''',	#12345-6789
	r'''^\d{5}\d{4}$''']	#123456789

#ph_regex = r'''^(?:[+]?\d+[ -]?)?\(?\d{3}[). -]?\d{3}[). -]?\d{4}$'''
PHONE_REGEXS = [r'''^\d{3}\d{4}$''',	#1234567
	r'''^\d{3}\d{3}\d{4}$''',	#1234567890
	r'''^\d{3}\s\d{3}\d{4}$''',	#123 4567890
	r'''^\(\d{3}\)\d{3}\d{4}$''',	#(123)4567890
	r'''^\(\d{3}\)\s\d{3}\d{4}$''',	#(123) 4567890
	r'''^[+]?\d{1,2}?\d{3}\d{3}\d{4}$''',	#11234567890
	r'''^[+]?\d+\s\d{3}\d{3}\d{4}$''',	#1 1234567890
	r'''^[+]?\d{1,2}?\d{3}\s\d{3}\d{4}$''',	#1123 4567890
	r'''^[+]?\d+\s\d{3}\s\d{3}\d{4}$''',	#1 123 4567890
	r'''^[+]?\d{1,2}?\(\d{3}\)\d{3}\d{4}$''',	#1(123)4567890
	r'''^[+]?\d+\s\(\d{3}\)\d{3}\d{4}$''',	#1 (123)4567890
	r'''^[+]?\d{1,2}?\(\d{3}\)\s\d{3}\d{4}$''',	#1(123) 4567890
	r'''^[+]?\d+\s\(\d{3}\)\s\d{3}\d{4}$''',	#1 (123) 4567890
	r'''^\d{3}\s\d{4}$''',	#123 4567
	r'''^\d{3}\s\d{3}\s\d{4}$''',	#123 456 7890
	r'''^\(\d{3}\)\d{3}\s\d{4}$''',	#(123)456 7890
	r'''^\(\d{3}\)\s\d{3}\s\d{4}$''',	#(123) 456 7890
	r'''^[+]?\d{1,2}?\d{3}\s\d{3}\s\d{4}$''',	#1123 456 7890
	r'''^[+]?\d+\s\d{3}\s\d{3}\s\d{4}$''',	#1 123 456 7890
	r'''^[+]?\d{1,2}?\(\d{3}\)\d{3}\s\d{4}$''',	#1(123)456 7890
	r'''^[+]?\d+\s\(\d{3}\)\d{3}\s\d{4}$''',	#1 (123)456 7890
	r'''^[+]?\d{1,2}?\(\d{3}\)\s\d{3}\s\d{4}$''',	#1(123) 456 7890
	r'''^[+]?\d+\s\(\d{3}\)\s\d{3}\s\d{4}$''',	#1 (123) 456 7890
	r'''^\d{3}\.\d{4}$''',	#123.4567
	r'''^\d{3}\.\d{3}\.\d{4}$''',	#123.456.7890
	r'''^\d{3}\s\d{3}\.\d{4}$''',	#123 456.7890
	r'''^\(\d{3}\)\d{3}\.\d{4}$''',	#(123)456.7890
	r'''^\(\d{3}\)\s\d{3}\.\d{4}$''',	#(123) 456.7890
	r'''^\(\d{3}\)\.\d{3}\.\d{4}$''',	#(123).456.7890
	r'''^[+]?\d{1,2}?\d{3}\.\d{3}\.\d{4}$''',	#1123.456.7890
	r'''^[+]?\d+\s\d{3}\.\d{3}\.\d{4}$''',	#1 123.456.7890
	r'''^[+]?\d+\.\d{3}\.\d{3}\.\d{4}$''',	#1.123.456.7890
	r'''^[+]?\d{1,2}?\d{3}\s\d{3}\.\d{4}$''',	#1123 456.7890
	r'''^[+]?\d+\s\d{3}\s\d{3}\.\d{4}$''',	#1 123 456.7890
	r'''^[+]?\d+\.\d{3}\s\d{3}\.\d{4}$''',	#1.123 456.7890
	r'''^[+]?\d{1,2}?\(\d{3}\)\d{3}\.\d{4}$''',	#1(123)456.7890
	r'''^[+]?\d+\s\(\d{3}\)\d{3}\.\d{4}$''',	#1 (123)456.7890
	r'''^[+]?\d+\.\(\d{3}\)\d{3}\.\d{4}$''',	#1.(123)456.7890
	r'''^[+]?\d{1,2}?\(\d{3}\)\s\d{3}\.\d{4}$''',	#1(123) 456.7890
	r'''^[+]?\d+\s\(\d{3}\)\s\d{3}\.\d{4}$''',	#1 (123) 456.7890
	r'''^[+]?\d+\.\(\d{3}\)\s\d{3}\.\d{4}$''',	#1.(123) 456.7890
	r'''^[+]?\d{1,2}?\(\d{3}\)\.\d{3}\.\d{4}$''',	#1(123).456.7890
	r'''^[+]?\d+\s\(\d{3}\)\.\d{3}\.\d{4}$''',	#1 (123).456.7890
	r'''^[+]?\d+\.\(\d{3}\)\.\d{3}\.\d{4}$''',	#1.(123).456.7890
	r'''^\d{3}-\d{4}$''',	#123-4567
	r'''^\d{3}-\d{3}-\d{4}$''',	#123-456-7890
	r'''^\d{3}\s\d{3}-\d{4}$''',	#123 456-7890
	r'''^\(\d{3}\)\d{3}-\d{4}$''',	#(123)456-7890
	r'''^\(\d{3}\)\s\d{3}-\d{4}$''',	#(123) 456-7890
	r'''^\(\d{3}\)-\d{3}-\d{4}$''',	#(123)-456-7890
	r'''^[+]?\d{1,2}?\d{3}-\d{3}-\d{4}$''',	#1123-456-7890
	r'''^[+]?\d+\s\d{3}-\d{3}-\d{4}$''',	#1 123-456-7890
	r'''^[+]?\d+-\d{3}-\d{3}-\d{4}$''',	#1-123-456-7890
	r'''^[+]?\d{1,2}?\d{3}\s\d{3}-\d{4}$''',	#1123 456-7890
	r'''^[+]?\d+\s\d{3}\s\d{3}-\d{4}$''',	#1 123 456-7890
	r'''^[+]?\d+-\d{3}\s\d{3}-\d{4}$''',	#1-123 456-7890
	r'''^[+]?\d{1,2}?\(\d{3}\)\d{3}-\d{4}$''',	#1(123)456-7890
	r'''^[+]?\d+\s\(\d{3}\)\d{3}-\d{4}$''',	#1 (123)456-7890
	r'''^[+]?\d+-\(\d{3}\)\d{3}-\d{4}$''',	#1-(123)456-7890
	r'''^[+]?\d{1,2}?\(\d{3}\)\s\d{3}-\d{4}$''',	#1(123) 456-7890
	r'''^[+]?\d+\s\(\d{3}\)\s\d{3}-\d{4}$''',	#1 (123) 456-7890
	r'''^[+]?\d+-\(\d{3}\)\s\d{3}-\d{4}$''',	#1-(123) 456-7890
	r'''^[+]?\d{1,2}?\(\d{3}\)-\d{3}-\d{4}$''',	#1(123)-456-7890
	r'''^[+]?\d+\s\(\d{3}\)-\d{3}-\d{4}$''',	#1 (123)-456-7890
	r'''^[+]?\d+-\(\d{3}\)-\d{3}-\d{4}$''']	#1-(123)-456-7890

#ip_regex = r'''^(?:\d{1,3}\.){3}\d{1,3}(?:[/]\d+)?(?:[:]\d+)?$'''
IP_REGEXS = [r'''^(?:\d{1,3}\.){3}\d{1,3}$''',	#123.45.67
	r'''^(?:\d{1,3}\.){3}\d{1,3}[/]\d+$''',	#123.45.67/8
	r'''^(?:\d{1,3}\.){3}\d{1,3}[:]\d+$''',	#123.45.67:8000
	r'''^(?:\d{1,3}\.){3}\d{1,3}[/]\d+[:]\d+$''']	#123.45.67/8:5000

#yr_regex = r'''^(?:\d{1,4}|'\d{2})$'''
YEAR_REGEXS = [r'''^\d{1,4}$''', #798
	r'''^'\d{2}$''']	#'98

#isbn_regex = r'''^(?:\d{3}[ -])?\d{1,5}[ -]\d{1,7}[ -]\d{1,6}[ -]\d$'''
ISBN_REGEXS = [r'''^\d{1,5}-\d{1,7}-\d{1,6}-\d$''',	#1234-567-89-0
	r'''^\d{1,5}\s\d{1,7}\s\d{1,6}\s\d$''',	#1234 567 89 0
	r'''^\d{3}-\d{1,5}-\d{1,7}-\d{1,6}-\d$''',	#978-1234-567-89-0
	r'''^\d{3}\s\d{1,5}\s\d{1,7}\s\d{1,6}\s\d$''']	#978 1234 567 89 0
