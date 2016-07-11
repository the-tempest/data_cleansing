import sys, subprocess
execfile('table.py')
#execfile('typify/column_type.py')

table_name = subprocess.check_output([sys.executable, "extraction.py", sys.argv[1]])
t = table(table_name);
print table_name;

# call Keith and Pawel's script
# c = column_typer(t);
# c.column_typify();

# loop to go through each column to build a JSON to save:
# for c in t.columns:
#
