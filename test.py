import os, sys, csv, json, mysql.connector

# db connector stuff
cnx = mysql.connector.connect(user='root', password='123', host='localhost', database='kappa')
cursor = cnx.cursor();
# sys.argv[1]
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
        print query

        for data in reader:
            print query
            print data
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
            print query
            print data
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

def extract_csv(fn, file_extension)

cnx.commit()
cursor.close()
cnx.close()
