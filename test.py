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


t1 = Task("T1", [], ["X"], runT1)
t2 = Task("T2", ["X"], ["Y"], runT2)
tSomme = Task("somme", ["X", "Y"], ["Z"], runTsomme)

t1.run()
t2.run()
tSomme.run()
