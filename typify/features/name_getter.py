output = open("street_names.txt", "w")
names = {}
with open("raw_street_names.txt", "r") as f:
	for line in f:
		word = line.split()[0].lower()
		if word not in names:
			names[word] = 1
ret = "["
for name in names.keys():
	ret += '\''
	ret += name
	ret += '\', '
ret += "]"
output.write(ret)
output.close()