import threading  # importer la Librairie pour la gestion des Threads


# classe de Tâche
class Task:
    # constructeur de la class Task avec parametre
    def __init__(self, name, reads, writes, run):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run

    # utilisation de Getter pour récuperer les attributs
    def getName(self):
        return self.name

    def getReads(self):
        return self.reads

    def getWrites(self):
        return self.writes


class TaskSystem:
    def __init__(self, task, parent):
        self.task = task
        self.parent = parent

    # renvoie la liste des taches qui s'excute avant la tache passer en parametre
    def getDependencies(self, task_name):
        return self.parent.get(task_name, [])
