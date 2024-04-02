import threading  # importer la Librairie pour la gestion des Threads


# classe de Tâche
class Task:
    # constructeur de la class Task avec parametre
    def __init__(self, name, reads, writes, run):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run


class TaskSystem:
    def __init__(self, task, parent):
        self.task = task
        self.parent = parent
        self.valid()

    # renvoie la liste de dependence pour une tache selon le système de parallélisme maximal
    def getDependencies(self, nomTache):

        # si la tache n'a aucune dependance cas exeptionel
        if self.parent["nomTache"] == []:
            return self.parent["nomTache"]
        else:
            # pour chaque dependance de notre tache :
            for element in self.parent["nomTache"]:
                # pour la dependence on verifie si parmis ces dependance y'en a une qui appartient a la liste de dependence de nomTache
                for dependance in self.parent["element"]:
                    if dependance in self.parent["nomTache"]:
                        # supprimer la dependance qui sert a rien de la liste
                        self.parent["nomTache"].remove(dependance)

        return self.parent["nomTache"]

    def valid(self):
        # vérifie que les noms des tâches sont uniques
        task_names = [task.name for task in self.task]
        if len(task_names) != len(set(task_names)):
            raise ValueError("Les noms des tâches ne sont pas unique")

        for i in range(len(task_names)):
            # vérifie que les noms des tâches ne sont pas vide
            if task_names[i] == "":
                raise ValueError(
                    "La tâche à l'indice {} dans le système de tâches n'a pas de nom".format(i))

            # vérifie que toutes les tâches du système de tâches font partie du dictionnaire.
            temp = False
            for key in self.parent.keys():
                if task_names[i] == key:
                    temp = True
            if temp == False:
                raise ValueError(
                    "La tâche à l'indice {} dans le système des tâches ne fait pas partie du dictionnaire.".format(i))

        for key in self.parent.keys():
            # vérifie la cohérence entre les noms des tâches dans la liste des tâches et ceux dans le graphe de précédence
            if key not in task_names:
                raise ValueError(
                    f"Le nom de tâche {key} dans le dictionnaire de précédence n'est pas dans la liste des tâches")

             # vérifie que la clé "tâche" ne doit pas être précéder par elle-même.
            if key in self.parent[key]:
                raise ValueError(
                    "Erreur : La clé est présente dans sa propre valeur.")

            # vérifie si des tâches ne sont pas mutuellement dépandante
            for key2 in self.parent.keys():
                if key in self.parent[key2] and key2 in self.parent[key]:
                    raise ValueError("les tâches sont mutuellement dependante")

        # verifie si la dépendance est dans la liste des tâches
        for dependencies in self.parent.values():
            for dep in dependencies:
                if dep not in task_names:
                    raise ValueError(
                        f"La dépendance {dep} n'est pas dans la liste des tâches")
