output = open("zip.txt", "w")
names = []
with open("raw_zip.txt", "r") as f:
	for line in f:
		word = line.strip('\n').split()[0]
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