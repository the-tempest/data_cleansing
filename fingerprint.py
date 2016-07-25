import re

def fingerprint_string(text):
	text = text.strip() # removes trailing and leading spaces
	text = text.lower() # lowercased

	sub_regex = re.compile(r'''[\x00-\x08\x0A-\a1F.!,.;:'"()]''')
	text = sub_regex.sub('', text)

	text_tokens = text.split()
