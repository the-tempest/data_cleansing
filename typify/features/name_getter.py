output = open("states.txt", "w")
names = []
with open("raw_states.txt", "r") as f:
	for line in f:
		word = line.split()[0].lower()
		if word not in names:
			names.append(word)
ret = "["
for name in names:
	ret += '\"'
	ret += name
	ret += '\", '
ret = ret[:-2]
ret += "]"
output.write(ret)
output.close()