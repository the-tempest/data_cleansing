import re

def fingerprint_column(rows):
	''' '''
	clustered_dictionary = {} # number in each cluster
	finger_dict = {} #index of each thing that has the same cluster
	for x in range(len(rows)):
		finger = fingerprint_string(rows[x])
		if finger in clustered_dictionary:
			clustered_dictionary[finger] += 1
			finger_dict[finger].append(x)
		else:
			clustered_dictionary[finger] = 1
			finger_dict[finger] = [x]
	return clustered_dictionary, finger_dict	



def fingerprint_string(text):
	''' fingerprints a string using a fingerprinting technique on 1-gram could implement n-gram'''

	text = text.strip() # removes trailing and leading spaces
	text = text.lower() # lowercased

	sub_regex = re.compile(r'''[\x00-\x08\x0A-\x1F.!,.;:'"()]''')
	text = sub_regex.sub('', text)

	text_tokens = text.split() #tokenify

	text_tokens = list(set(text_tokens)) # removes duplicates
	text_tokens.sort()

	fingerprint = ' '.join(text_tokens)	
	#can normalize to ascii if you want
	#ajdklf
	return fingerprint