class column:
    def __init__(self, rows, colName):
       self.colName = colName;
       self.rows = rows
       self.tentClass = ""
    def tentativeClassification(self, tc):
       self.tentClass = tc;

class table:
    def __init__(self, name):
        self.name = name;
        self.column_index = {}
        self.columns = [];
        
    def build column_index(self):
    	for i in range(len(self.coolumns))
    		self.column_index[self.columns[i].colName] = i 

    def addColumn(self, col):
        self.columns.append(col)
    def getColumns(self):
        return self.columns
