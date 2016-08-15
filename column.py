# class to represent a column in the table
import mysql.connector
from secrets import password, port, database, user, host, path
import table

# class to represent a table
class table:
    def __init__(self, name):
        self.name = name; # the name of the table
        self.column_index = {} # dictionary mapping column names to indices
        self.columns = []; # the list containing the columns of the table
        self.build_column_index()


        self.query_list = []
        self.num_queries = 0

        self.cnx = mysql.connector.connect(user=user,password=password, host=host, database=database, port=port)
        self.cursor = self.cnx.cursor()

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


    def startTransaction(self):

        #self.transaction = True
        
        query = "START TRANSACTION;" # execute the command
        self.query_list.append(query)
        #self.cursor.execute(query)
        self.cnx.start_transaction()

        self.num_queries += 1

        savepoint_name = self.savepoint_generator() # this executes the command but also returns the name

        return 

    def savepoint_generator(self):
        '''returns the name of the savepoint but also executes ''' 
        letter = self.num_queries #make sure t normalize to 0 A = 65 
        letter = str(letter)

        letter += 'a'

        query = "SAVEPOINT " + letter + ";"
        self.cursor.execute(query)

        #self.print_fetchall()
        return letter


    def revert_previous_changes_to_index(self,restore_index):
        ''' Will revert all changes and revert to a previous savepoint '''
        self.cursor.execute("ROLLBACK TO " + str(restore_index) + "a") # a is there to satisfy mysql syntax
        # not sure exactly what to do with the python object at this point
        #self.print_fetchall()


        return

    def print_fetchall(self):
        i = self.cursor.fetchall()
        print i
        return

    def reset_connection(self):
        self.cnx.cmd_reset_connection()
        self.cursor = self.cnx.cursor()
        return

    def undo_single_change(self, command_index):
        ''' will undo a single change and attempt to re execute all the other commands ASSUME INDEX OF COMMAND IS INDEXED BY 0'''

        self.cursor.execute("ROLLBACK TO " + str(command_index) + "a")

        for x in range(command_index + 1, len(self.query_list)):
            if self.query_list[x] == "START TRANSACTION;":
                self.cnx.start_transaction()
            else:
                self.cursor.execute(self.query_list[x])
            #hopefully no dependencies. what to do with python object?

        return

    def end_transaction(self):
        ''' A function to permanently save all the changes you've made. 
            Will flush the query_list so you cannot undo small changes ''' 


        self.cnx.commit()

        #self.print_fetchall()

        self.num_queries = 0 # reset num_queries

        self.query_list = [] # remove all queries from list, means you can't go back but maybe allow you to go all the way back at this point
        new_table = getTable(self.name, user, password,host, database)

        self.columns = new_table.columns; # the list containing the columns of the table
        self.build_column_index()



    
class column(table):
    def __init__(self, rows, colName, table):
        self.colName = colName; # name of the column
        self.rows = rows # the actual data inside the column (in the form of list)
        self.tentClass = None # tentative Classification
        self.dictionary = {}  #dictionary of predictions and counts associated

        self.guesses = {} # dictionary of index of token and guess for that token
        
        self.t = table
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
        ''' index is python 0 indexed value that user wants to update. new_value is a string that is getting put into table. string becuase table is all strings'''

        if self.t.cnx.in_transaction == False: # need to know if at beginning of transaction
            self.t.startTransaction()

        self.rows[index] = new_val # python easy change
        index = index+1 # auto increment starts at 1 but python users will index at 0 

        
        new_val = "'" + new_val + "'"

        # need to edit sql database
        query = 'Update ' + self.t.name + ' \n' +  "Set " + self.colName + '=' + str(new_val) + '\n' + "Where " + "TableIndex = " + str(index) + ';'
        # need to index+1 because auto_increment starts at 1 not 0. 
        #print query
        self.t.cursor.execute(query)

        #self.print_fetchall()

        self.t.query_list.append(query)
        self.t.num_queries += 1

        self.t.savepoint_generator()



        return

