import sys, mysql.connector
from secrets import password, port, user, host, database, path
execfile(path+'column.py');


def getRows(columnName, fileName, cursor):
    query = "SELECT " + columnName + " FROM " + fileName;
    cursor.execute(query);
    rows = cursor.fetchall();
    #print rows
    for j in range(len(rows)):
        try:
            rows[j] = str(''.join(rows[j]));
        except UnicodeEncodeError:
            rows[j] = str(''.join(rows[j][0].decode('utf-8')))
    return rows;

def getTable(tablename, u=user, p=password, h=host, d=database, port = port ):
    cnx = mysql.connector.connect(user=u, password=p, host=h, database=d, port=port);
    cursor = cnx.cursor();
    newTable = table(tablename);
    #print tablename
    query = "SHOW columns FROM " + tablename;
    cursor.execute(query)
    cols = cursor.fetchall();
    columns = []
    for i in range(len(cols)):
        columns.append(str(cols[i][0]))

    #print columns;
    for i in range(len(columns)):
        colName = columns[i];
        data = getRows(colName, tablename, cursor)
        #column_name = normalize_name(colName)
        # firstNum = "0"
        # for x in range(10): # not working.
        # 	colName.replace(chr(ord(firstNum) + x), "") # remove characters 0-9 in column name

        newCol = column(data, colName, tablename);
        newTable.addColumn(newCol);
    cnx.commit()
    cursor.close()
    cnx.close()
    return newTable;
