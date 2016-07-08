output = open("URL_domain_extensions.txt", "w")
names = {}
with open("raw_URL_domain_extensions.txt", "r") as f:
	for line in f:
		word = line.split()[0].lower()
		if word not in names:
			names[word] = 1
ret = "["
for name in names.keys():
	ret += '\''
	ret += name
	ret += '\', '
ret = ret[:-2]
ret += "]"
output.write(ret)
output.close()