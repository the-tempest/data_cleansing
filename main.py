import sys, subprocess, json, operator, os
import extraction
from secrets import path
execfile(path+'table.py')
execfile(path+'typify/column_type.py')
execfile(path+'numeric_classifier.py')
execfile(path+'counter.py')
execfile(path+'error_detection/errors.py')

ct = counter()

def execute(filename):
    filename = filename.replace("\n", "")
    filename = filename.replace(" ", "_")
    table_name = extraction.extract(filename);
    t = getTable(table_name);

    '''numClass = numeric_classifier();
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
        '''


    # call Keith and Pawel's script
    c = column_typer(t);
    cl = c.build_report();
    
    # collect statistics
    results = c.table_typify(t)
    ct.tally_and_save(results)

    #with open('output/' + table_name + '.txt', 'w') as outfile:
    #    json.dump(cl, outfile);

    # errors commented to avoid gettin an email from the server
    # detective = error_detector(t)
    # possible_errors_dictionary = detective.find_table_errors(errors_to_check_list)


    dirToSave = path+"output";
    fn = table_name + ".txt"
    pathToSave = os.path.join(dirToSave, fn);
    print pathToSave
    print 'this'
    with open(pathToSave, "w") as text_file:
        text_file.write(cl);

    #with open("output/" + table_name + '_numeric.txt', "w") as text_file:
    #    text_file.write(result);


    # loop to go through each column to build a JSON to save:
    # for c in t.columns:
    #
