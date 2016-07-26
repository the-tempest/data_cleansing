import re

def fingerprint_column(rows):
	clustered_dictionary = {}
	for item in rows:
		finger = fingerprint_string(item)
		if finger in clustered_dictionary:
			clustered_dictionary += 1
		else:
			clustered_dictionary[item] = 1



def fingerprint_string(text):
	text = text.strip() # removes trailing and leading spaces
	text = text.lower() # lowercased

	sub_regex = re.compile(r'''[\x00-\x08\x0A-\a1F.!,.;:'"()]''')
	text = sub_regex.sub('', text)

	text_tokens = text.split() #tokenify

	text_tokens = list(set(text_tokens)) # removes duplicates
	text_tokens.sort()

	fingerprint = ' '.join(text_tokens)	
	#can normalize to ascii if you want
	return fingerprint