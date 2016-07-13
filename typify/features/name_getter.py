output = open("adjectives.txt", "w")
names = {}
with open("raw_adjectives.txt", "r") as f:
	for line in f:
		word = line.split()[1].lower()
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