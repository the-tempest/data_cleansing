# class to represent a column in the table
class column:
    def __init__(self, rows, colName):
       self.colName = colName; # name of the column
       self.rows = rows # the actual data inside the column (in the form of list)
       self.tentClass = "" # tentative Classification
       self.dictionary = {}  #dictionary of predictions and fractions associated 
    def tentativeClassification(self, tc):
       ''' the argument tc is the tentative classification for the column '''
       self.tentClass = tc; #spacing here could be off
    def addDict(self, dict):
	   	self.dictionary = dict
    	 

# class to represent a table
class table:
    def __init__(self, name):
        self.name = name; # the name of the table
        self.column_index = {} # dictionary mapping column names to indices
        self.columns = []; # the list containing the columns of the table

    def build_column_index(self):
        ''' build the column index dictionary '''
    	for i in range(len(self.columns)):
    		self.column_index[self.columns[i].colName] = i

    def addColumn(self, col):
        ''' add a column object to the table '''
        self.columns.append(col)
    def getColumns(self):
        ''' returns a list of column objects for the table '''
        return self.columns
