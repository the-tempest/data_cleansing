#writing something to a text file
f = open("eecs348.txt", "w")   #open this file for writing
        #if you're opening a file for writing, the file does not have
        #  to exist already
f.write("I love AI!!!") #write something
f.close()                   #close the file

#reading something from a file
f = open("eecs348.txt", "r")   #open this file for reading
        #if you're opening a file for reading, the file DOES have
        #  to exist already
t= f.read()
f.close()

print "t is: " + str(t)

#if you want to open a file and you're not sure if it exists already,
#  what might you do to avoid an error?
try:
    f = open("eecs348.txt", "r")
except IOError:
    print "I got an IO error!  eecs348.txt does not exist!"


########################################################

import pickle

def save(dObj, sFilename):
    '''Given an object and a file name, write the object to the file using pickle.'''
    f = open(sFilename, "w")
    p = pickle.Pickler(f)
    p.dump(dObj)
    f.close()

def load(sFilename):
    '''Given a file name, load and return the object stored in the file.'''
    f = open(sFilename, "r")
    u = pickle.Unpickler(f)
    dObj = u.load()
    f.close()
    return dObj

#pickle something - dump it to a file
x = dict()
x["wonderful"] = 25
x["movie"] = 23
x["the"] = 700
print "x is: " + str(x)
save(x, "x.dat")


#unpickle something - load it from a file
y = load("x.dat")
print "y is: " + str(y)
