import re

def fingerprint_column(rows):
	clustered_dictionary = {}
	finger_indices = [] # column long list that will 1 to 1 match the column with just the fingerprints...
	#could instead have dictionary with names that have list of indices
	finger_dict = {}
	for x in range(len(rows)):
		finger = fingerprint_string(rows[x])
		finger_indices.append(finger)
		if finger in clustered_dictionary:
			clustered_dictionary[finger] += 1
			finger_dict[finger].append(x)
		else:
			clustered_dictionary[finger] = 1
			finger_dict[finger] = [x]
	return clustered_dictionary	



def fingerprint_string(text):
	text = text.strip() # removes trailing and leading spaces
	text = text.lower() # lowercased

	#sub_regex = re.compile(r'''[\x00-\x08\x0A-\a1F.!,.;:'"()]''')
	#text = sub_regex.sub('', text)

	text_tokens = text.split() #tokenify

	text_tokens = list(set(text_tokens)) # removes duplicates
	text_tokens.sort()

	fingerprint = ' '.join(text_tokens)	
	#can normalize to ascii if you want
	#ajdklf
	return fingerprint

