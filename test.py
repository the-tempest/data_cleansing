import sys

toWrite = sys.argv[1]; # argument is the filename
f = open("./uploaded/test.txt","w") #opens file with name of "test.txt"
f.write(toWrite)
f.close()
