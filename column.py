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
        self.columns = [];
    def addColumn(self, col):
        self.columns.append(col)
    def getColumns(self):
        return self.columns
