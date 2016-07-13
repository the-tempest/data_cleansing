import sys, subprocess, json, operator
execfile('table.py')
execfile('typify/column_type.py')
execfile('numeric_classifier.py')
#execfile('typify/column_type.py')

table_name = subprocess.check_output([sys.executable, "extraction.py", sys.argv[1]])
t = getTable(table_name);
#t.build_column_index();

numClass = numeric_classifier();
result = "";
for col in t.columns:
    diction = {}
    for item in col.rows:
        res = numClass.classify(item);
        if res in diction:
            diction[res] += 1;
        else:
            diction[res] = 1;
    result += col.colName + ': ' + max(diction.iteritems(), key=operator.itemgetter(1))[0];
    result += str(" \n ");



# call Keith and Pawel's script
#c = column_typer("temp");
#cl = c.build_report(t);

with open('output/' + table_name + '.txt', 'w') as outfile:
    json.dump(result, outfile);

# loop to go through each column to build a JSON to save:
# for c in t.columns:
#
