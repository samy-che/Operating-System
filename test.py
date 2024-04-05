from maxpar import *

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
t4 = Task("T4", ["somme"], ["T4"], runT1)
t5 = Task("T5", ["Z"], ["T5"], runT2)


s1 = TaskSystem([t1, t2, tSomme, t4, t5], {"T1": [], "T2": [
                "T1"], "somme": ["T1", "T2"], "T4": ["T1", "somme"], "T5": ["T1", "T4"]})
t1.run()
t2.run()
tSomme.run()
s1.runSeq()
s1.run()
s1.draw()
