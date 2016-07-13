import sys, subprocess, json, operator, os
execfile('table.py')
execfile('typify/column_type.py')
execfile('numeric_classifier.py')
#execfile('typify/column_type.py')

table_name = subprocess.check_output([sys.executable, "extraction.py", sys.argv[1]])
table_name = table_name.replace("\n", "")
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
    result += '\n'



# call Keith and Pawel's script
c = column_typer(t);
cl = c.build_report();

#with open('output/' + table_name + '.txt', 'w') as outfile:
#    json.dump(cl, outfile);

with open("output/" + table_name + '_general.txt', "w") as text_file:
    text_file.write(cl);

with open("output/" + table_name + '_numeric.txt', "w") as text_file:
    text_file.write(result);


# loop to go through each column to build a JSON to save:
# for c in t.columns:
#
