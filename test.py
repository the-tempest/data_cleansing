import os, sys, csv, json, mysql.connector

#execfile('column_type.py');
# db connector stuff
cnx = mysql.connector.connect(user='root', password='123', host='localhost', database='world')
cursor = cnx.cursor();
# sys.argv[1]
#"./uploaded/SalesJan2009.csv"
fn, file_extension = os.path.splitext(sys.argv[1]);
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
        data = map(lambda x: flatten_json(x), data)
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
        print query

        for item in data:
            cursor.execute(query, item)


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


for i in range (len(columns)):
    query = "SELECT " + columns[i] + " FROM " + filename;
    cursor.execute(query);
    rows = cursor.fetchall();
    for i in range(len(rows)):
        rows[i] = str(''.join(rows[i]));
    #coltyper = column_typer(rows);
    #coltyper.column_parser();

cnx.commit()
cursor.close()
cnx.close()
