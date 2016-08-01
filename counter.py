# every time someone uploads a file to the server
# this class is called to count up what is 
# classified as what

import pickle, os
from secrets import path

class counter:
	def __init__(self):
		'''gets the current count of all predictions'''
		self.my_path = 'statistics.p'
		if not os.path.isfile(self.my_path):
			self.my_file = open(path+self.my_path, 'w+')
			pickle.dump( {} , self.my_file)
			self.my_file.close()
		self.my_file = open(self.my_path, 'r+')
		self.data = pickle.load(self.my_file)
		self.my_file.close()

	def __str__(self):
		'''prints out the statistics we have collected'''
		ret = 'Statistics collected so far:\n\n'
		for actual in self.data:
			ret += actual
			ret +=':\n'
			classifications = self.data[actual]
			for guess in classifications:
				ret += '  '
				ret += guess
				ret += ': '
				ret += str(classifications[guess])
				ret += '\n'
		ret += '\n'
		return ret

	def tally_and_save(self, new_data):
		'''takes in a table that has been fully classified 
		and add its data to the pickled file'''
		temp_data = self.data
		for tup in new_data:
			actual = tup[0]
			prediction = tup[1]
			if actual not in temp_data:
				temp_data[actual] = {prediction: 1}
			else:
				if prediction not in temp_data[actual]:
					temp_data[actual][prediction] = 1
				else:
					temp_data[actual][prediction] += 1
		pickle.dump(temp_data, open("statistics.p", "wb"))

	def get_results(self):
		'''returns just the dictionary of statistics, maybe
		we can use this somewhere'''
		return self.data