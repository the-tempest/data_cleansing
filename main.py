import sys, subprocess, json, operator, os
import extraction
from secrets import path
execfile(path+'table.py')
execfile(path+'new_classifier/main_classifier.py')
execfile(path+'evaluation/counter.py')
execfile(path+'error_detection/errors.py')

ct = counter()

def execute(filename):
    filename = filename.replace("\n", "")
    filename = filename.replace(" ", "_")
    table_name = extraction.extract(filename);
    t = getTable(table_name);

    # call column classifier script
    x = main_classifier();
    x.new_table(t)
    cl = x.report
    
    # collect statistics
    ct.tally_and_save(x.results)

    dirToSave = path+"output";
    fn = table_name + ".txt"
    pathToSave = os.path.join(dirToSave, fn);
    print pathToSave
    print 'this'
    with open(pathToSave, "w") as text_file:
        text_file.write(cl);