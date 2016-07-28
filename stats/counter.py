# every time someone uploads a file to the server
# this class is called to count up what is 
# classified as what

import pickle, os

class counter:
	def __init__(self):
		'''gets the current count of all predictions'''
		self.my_path = 'stats/statistics.p'
		if not os.path.isfile(self.my_path):
			self.my_file = open(self.my_path, 'w+')
			pickle.dump( {} , self.my_file)
			self.my_file.close()
		self.my_file = open(self.my_path, 'r+')
		self.data = pickle.load(self.my_file)
		self.my_file.close()

	def tally_and_save(self, new_data):
		'''takes in a table that has been fully classified 
		and add its data to the pickled file'''
		temp_data = self.data
		print 'before'
		print temp_data
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
		pickle.dump(temp_data, open("stats/statistics.p", "wb"))
		print 'after'
		print temp_data

	def display_results(self):
		'''prints out the statistics we have collected'''
		print 'implement me'



	def get_results(self):
		'''returns just the dictionary of statistics, maybe
		we can use this somewhere'''
		return self.data





# # Save a dictionary into a pickle file.
# import pickle
#  
# favorite_color = { "lion": "yellow", "kitty": "red" }
#  
# pickle.dump( favorite_color, open( "save.p", "wb" ) )

# # Load the dictionary back from the pickle file.
# import pickle
#  
# favorite_color = pickle.load( open( "save.p", "rb" ) )
# favorite_color is now { "lion": "yellow", "kitty": "red" }
