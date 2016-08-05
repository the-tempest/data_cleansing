output = open("url_examples.txt", "w")
names = []
with open("url_example_list.txt", "r") as f:
	for line in f:
		word = line.strip('\n')
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