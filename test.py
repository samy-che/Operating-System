from main import *

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

#test de git 