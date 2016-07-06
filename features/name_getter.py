output = open("first_names.txt", "w")
names = []
with open("raw_first_names.txt", "r") as f:
	for line in f:
		word = line.split()[0].lower()
		names.append(word)
ret = "["
for name in names:
	ret += '\''
	ret += name
	ret += '\', '
ret += "]"
output.write(ret)
output.close()