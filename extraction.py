import os, sys, csv, json, mysql.connector
execfile('column.py');
def main(arg):
    def flatten_json(raw):
        val = {}
        for i in raw.keys():
            if isinstance(raw[i], dict):
                get = flatten_json(raw[i])
                for j in get.keys():
                    val[i + "_" + j] = get[j]
            else:
                val[i] = raw[i]
        return val


    # db connector stuff
    cnx = mysql.connector.connect(user='root', password='spence23', host='localhost', database='world')
    cursor = cnx.cursor();
    # sys.argv[1]
    #"./uploaded/SalesJan2009.csv"
    fn, file_extension = os.path.splitext(arg);
    filename = os.path.basename(fn);
    if (file_extension == '.csv'):
        with open (fn+file_extension, 'rU') as f:
            reader = csv.reader(f)
            columns = next(reader)
            columnsToInitialize = []
            for col in columns:
                columnsToInitialize.append(col+ ' TEXT');

            # creating new database
            query = 'drop table if exists ' + filename;
            cursor.execute(query)

            # new table and headers
            query = 'create table ' + filename + '({0})'
            query = query.format(', '.join(columnsToInitialize))
            cursor.execute(query)

            s = []
            query = 'insert into '+ filename +' ({0}) values ({1})'
            for i in range(len(columns)):
                s.append('%s')
            query = query.format(','.join(columns), ','.join(s))

            for data in reader:
                cursor.execute(query, data)

    elif (file_extension == '.json'):
        with open(fn+file_extension, 'rU') as f:
            # load and flatten the json file
            raw_data = json.load(f)
            data = map(lambda x: flatten_json(x), raw_data)
            columns = map(lambda x: x.keys(), data)
            columns = reduce(lambda x,y: x+y, columns)
            columns = list(set(columns))

            columnsToInitialize = []
            for col in columns:
                columnsToInitialize.append(col+ ' TEXT');


            # creating new database
            query = 'drop table if exists ' + filename;
            cursor.execute(query)

            # new table and headers
            query = 'create table ' + filename + '({0})'
            query = query.format(', '.join(columnsToInitialize))
            cursor.execute(query)

            s = []
            query = 'insert into '+ filename +' ({0}) values ({1})'
            for i in range(len(columns)):
                s.append('%s')
            query = query.format(','.join(columns), ','.join(s))

            for item in data:
                new_item = []
                for key in item:
                    new_item.append(str(item[key]))
                cursor.execute(query, new_item);

    else:
        sys.exit();

    #columnTypePairs = {};



    #def classify(col):
        ''' takes a column object and runs Keith's script on it '''
        '''coltyper = column_typer(col)
        t = coltyper.column_typify() #type
        columnTypePairs[columns[i]] = t'''





    '''rows = None;
    nextCol = getRows(columns[0]);

    for i in range (len(columns)-1):
        prevCol = rows;
        rows = nextCol;
        nextCol = getRows(columns[i+1]);
        colName = columns[i];
        col = column(rows, colName, prevCol, nextCol);
        #classify(col);

    col = column(nextCol, columns[i+1], rows, None);
    #classify(col);


    # for testing
    #columnTypePairs = {"city" : "location", "Name": "name"} ;

    ##with open('output/' + filename + '.txt', 'w') as outfile:
    #    json.dump(columnTypePairs, outfile);

    '''

    cnx.commit()
    cursor.close()
    cnx.close()
    return filename;

if __name__ == "__main__":
    x = main(sys.argv[1])
    print x;
