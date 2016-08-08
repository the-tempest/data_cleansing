# class to represent a column in the table
import mysql.connector
from secrets import password, port, database, user, host, path



    


# class to represent a table
class table:
    def __init__(self, name):
        self.name = name; # the name of the table
        self.column_index = {} # dictionary mapping column names to indices
        self.columns = []; # the list containing the columns of the table
        self.build_column_index()

        self.transaction = False # are we editing and in a transaction?

        self.query_list = []

        cnx = mysql.connector.connect(user=user,password=password, host=host, database=database, port=port)
        self.cursor = cnx.cursor()

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

    


class column(table):
    def __init__(self, rows, colName, table):
        self.colName = colName; # name of the column
        self.rows = rows # the actual data inside the column (in the form of list)
        self.tentClass = None # tentative Classification
        self.dictionary = {}  #dictionary of predictions and counts associated

        self.guesses = {} # dictionary of index of token and guess for that token
        
        self.table = table
        # cnx = mysql.connector.connect(user=user,password=password, host=host, database=database, port=port)
        # self.cursor = cnx.cursor()


    def tentativeClassification(self, tc):
        ''' the argument tc is the tentative classification for the column '''
        self.tentClass = tc

    def addDict(self, dyct):
        self.dictionary = dyct
    
    def addGuesses(self, g):
        self.guesses = g

    def edit_cell(self,index, new_val):
        if self.t.transaction == False: # need to know if at beginning of transaction
            self.t.transaction = True
            
            query = "START TRANSACTION;" + "\n" # execute the command
            self.t.query_list.append(query)
            self.t.cursor.execute(query)

        index = index+1 # auto increment starts at 1 but python users will index at 0 

        self.rows[index] = new_val # python easy change
        # need to edit sql database
        query = 'Update ' + self.t.name + ' \n' +  "Set " + self.colName + '=' + new_val + '\n' + "Where " + "TableIndex = " + index + ';'
        self.t.cursor.execute(query)
        return