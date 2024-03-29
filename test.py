from main import *

X = None
Y = None
Z = None


def runT1():
    global X
    X = 1
    print("exection de t1 : ", X)


def runT2():
    global Y
    Y = 2
    print("execution de t2 :", Y)


def runTsomme():
    global X, Y, Z
    Z = X + Y
    print("execution de tsomme : ", Z)


t1 = Task()
t1.name = "T1"
t1.writes = ["X"]
t1.run = runT1


t2 = Task()
t2.name = "T2"
t2.writes = ["T2"]
t2.run = runT2

tsomme = Task()
tsomme.name = "somme"
tsomme.reads = ["X", "Y"]
tsomme.writes = ["Z"]
tsomme.run = runTsomme

t1.run()
t2.run()
tsomme.run()
