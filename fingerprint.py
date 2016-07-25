

def fingerprint_string(text):
	text = text.strip() # removes trailing and leading spaces
	text = text.lower() # lowercased

	text_tokens = text.split()
