output = open("new_spec_address_testing_data.txt", "w")
names = {}
with open("spec_address_testing_data.txt", "r") as f:
	for line in f:
		word = line.strip('\n')
		if word not in names:
			names[word] = 1
ret = "["
for name in names.keys():
	ret += 'r\"'
	ret += name
	ret += '\", '
ret = ret[:-2]
ret += "]"
output.write(ret)
output.close()