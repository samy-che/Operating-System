class Task:
    def __init__(self):
        self.name = ""
        self.reads = []
        self.writes = []
        self.run = None

    def getName(self):
        return self.name

    def getReads(self):
        return self.reads

    def getWrites(self):
        return self.writes


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
