import mysql.connector, os
class column_typer: 	
	def __init__(self, column_list):
		self.column_list = column_list


	def column_parser(self):
		for item in self.column_list:
			for character in item:
				if (ord(character) <= 57 or ord(character) >= 48):
					




