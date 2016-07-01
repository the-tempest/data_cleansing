import os, sys, csv, mysql.connector

# db connector stuff
cnx = mysql.connector.connect(user='root', password='123', host='localhost', database='world')
cursor = cnx.cursor();
# sys.argv[1]
fn, file_extension = os.path.splitext(sys.argv[1]);
filename = os.path.basename(fn);
if (file_extension == '.csv'):
    with open (fn+file_extension, 'rU') as f:
        reader = csv.reader(f)
        columns = next(reader)
        columnsToInitialize = [];
        for col in columns:
            columnsToInitialize.append(col+ ' TEXT');

        # creating new database
        query = 'drop table if exists ' + filename;
        cursor.execute(query);

        # new table and headers
        query = 'create table ' + filename + '({0})'
        query = query.format(', '.join(columnsToInitialize));
        cursor.execute(query);

        s = []
        query = 'insert into '+ filename +' ({0}) values ({1})';
        for i in range(len(columns)):
            s.append('%s');
        query = query.format(','.join(columns), ','.join(s))
        print query;

        for data in reader:
            print query
            print data
            cursor.execute(query, data)

#elif (file_extension == '.json'):

cnx.commit()
cursor.close()
cnx.close()
