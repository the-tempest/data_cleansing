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
        self.num_queries = 0

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

    def start_transaction(self):

        self.t.transaction = True
        
        query = "START TRANSACTION;" + "\n" # execute the command
        self.t.query_list.append(query)
        self.t.cursor.execute(query)
        self.t.num_queries += 1

        savepoint_name = savepoint_generator() # this executes the command but also returns the name

        return 

    def savepoint_generator(self):
        '''returns the name of the savepoint but also executes ''' 
        letter = self.t.num_queries #make sure t normalize to 0 A = 65 
        letter = str(letter)

        letter += 'a'

        query = "SAVEPOINT " + letter + ";"
        self.t.cursor.execute(query)

        return letter


       
    def edit_cell(self,index, new_val):
        if self.t.transaction == False: # need to know if at beginning of transaction
            self.start_transaction()

        index = index+1 # auto increment starts at 1 but python users will index at 0 

        self.rows[index] = new_val # python easy change
        # need to edit sql database
        query = 'Update ' + self.t.name + ' \n' +  "Set " + self.colName + '=' + new_val + '\n' + "Where " + "TableIndex = " + index + ';'
        self.t.cursor.execute(query)
        self.t.query_list.append(query)
        selt.t.num_queries += 1

        return

    def revert_previous_changes_to_index(self,restore_index):
        ''' Will revert all changes and revert to a previous savepoint '''
        self.t.cursor.execute("ROLLBACK TO " + str(restore_index) + "a") # a is there to satisfy mysql syntax
        # not sure exactly what to do with the python object at this point


    def undo_single_change(self, command_index):
        ''' will undo a single change and attempt to re execute all the other commands ASSUME INDEX OF COMMAND IS INDEXED BY 0'''

        #savepoint_number = command_index - 1 # want to go to the savepoint just before

        self.t.cursor.execute("ROLLBACK TO " + str(command_index) + "a")

        for x in range(command_index + 1, len(self.t.query_list)):
            self.t.cursor.execute(self.t.query_list[x])
            #hopefully no dependencies. what to do with python object?

        return


