import sys, mysql.connector
execfile('column.py');

def getRows(columnName, fileName):
    query = "SELECT " + columnName + " FROM " + filename;
    cursor.execute(query);
    rows = cursor.fetchall();
    for j in range(len(rows)):
        rows[j] = str(''.join(rows[j]));
    return rows;

def getTable(tablename, u='root', p='123', h='localhost', d='world'):
    cnx = mysql.connector.connect(user=u, password=p, host=h, database=d);
    cursor = cnx.cursor();
    newTable = table(filename)
    for i in range(len(columns)):
        colName = columns[i];
        data = getRows(colName)
        newCol = column(data, colName);
        newTable.addColumn(newCol);
    cnx.commit()
    cursor.close()
    cnx.close()
    return newTable;
