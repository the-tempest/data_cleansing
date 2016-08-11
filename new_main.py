import sys, subprocess, json, operator, os
import extraction
from secrets import path
execfile(path+'table.py')
execfile(path+'main_classifier.py')
execfile(path+'counter.py')
execfile(path+'errors.py')

ct = counter()

def execute(filename):
    filename = filename.replace("\n", "")
    filename = filename.replace(" ", "_")
    table_name = extraction.extract(filename);
    t = getTable(table_name);

    # call column classifier script
    x = main_classifier();
    x.new_tabe(t)
    cl = x.report
    
    # collect statistics
    ct.tally_and_save(x.results)

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
