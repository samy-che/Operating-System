import threading  # importer la Librairie pour la gestion des Threads
import networkx
import matplotlib.pyplot as plt


# classe de Tâche
class Task:
    # constructeur de la class Task avec parametre
    def __init__(self, name, reads, writes, run):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run

    # fonction qui prend deux taches qui renvoie false si il y a une intérférence entre les taches
    def bernstein(t1, t2):
        for i in t1.writes:
            for j in t2.writes:
                if (i == j):
                    print("interferance domaine d'écriture entre",
                          t1.name, t2.name)
                    return False
        for i in t1.reads:
            for j in t2.writes:
                if (i == j):
                    print("inteferance entre le domaine de lecture de",
                          t1.name, "et le domaine d'ecriture de", t2.name)
                    return False
        for i in t1.writes:
            for j in t2.reads:
                if (i == j):
                    print("inteferance entre le domaine d'ecriture de",
                          t1.name, "et le domaine de lecture de", t2.name)
                    return False

        return True

    # Fonction de suppression d'interférence
    def SupprInter(nomt1, nomt2):
        if not bernstein(nomt1, nomt2):  # vérifie s'il y a une interferance
            for i in dico[nomt1.name]:  # parcours les précédences de la tache 1
                if (i == nomt2.name):  # Est ce que t2 est deja dans les precedences de t1 ?
                    print(nomt2.name, " précéde ", nomt1.name)
                    return False
            if (dico[nomt2.name] == []):  # si t2 n'a pas de precedences
                # ajout de t1 dans les precedences de t2
                dico[nomt2.name].append(nomt1.name)
                return False
            for i in dico[nomt2.name]:  # parcours les précédences de la tache 2
                if (i == nomt1.name):  # Est ce que t1 est deja dans les precedences de t2 ?
                    print(nomt1.name, " précéde ", nomt2.name)
                    return False
                else:
                    # ajout de t1 dans les précédence de t2
                    dico[nomt2.name].append(nomt1.name)
                    print("ajout de "+nomt1.name +
                          " dans les précédences "+nomt2.name)

        else:
            print("Aucune interferance entre les deux taches " +
                  nomt1.name + " et " + nomt2.name)
            return True

    # Paralléliser les taches qui n'ont pas d'interférences
    def ParaTache(nomt1, nomt2):
        if bernstein(nomt1, nomt2):  # s'il n'y a pas d'interférance
            for i in dico[nomt2.name]:
                if (i == nomt1.name):
                    # suppression de t1 dans les précédences de t2
                    dico[nomt2.name].remove(nomt1.name)
                    print("Supression de ", nomt1.name,
                          " dans les précédences de ", nomt2.name)
                else:
                    print(nomt1.name, "n'est pas dans les précédences de", nomt2.name)
                    break


class TaskSystem:
    def __init__(self, task, dico):
        self.task = task
        self.dico = dico
        self.valid()
        self.graph = self.draw()

    def valid(self):
        # vérifie que les noms des tâches sont uniques
        task_names = [task.name for task in self.task]
        if len(task_names) != len(set(task_names)):
            raise ValueError("Les noms des tâches ne sont pas unique")

        for i in range(len(task_names)):
            # vérifie que les noms des tâches ne sont pas vide
            if task_names[i] == "":
                raise ValueError(
                    "La tâche à l'indicoe {} dans le système de tâches n'a pas de nom".format(i))

            # vérifie que toutes les tâches du système de tâches font partie du dicotionnaire.
            temp = False
            for key in self.dico.keys():
                if task_names[i] == key:
                    temp = True
            if temp == False:
                raise ValueError(
                    "La tâche à l'indicoe {} dans le système des tâches ne fait pas partie du dicotionnaire.".format(i))

        for key in self.dico.keys():
            # vérifie la cohérence entre les noms des tâches dans la liste des tâches et ceux dans le graphe de précédence
            if key not in task_names:
                raise ValueError(
                    f"Le nom de tâche {key} dans le dicotionnaire de précédence n'est pas dans la liste des tâches")

             # vérifie que la clé "tâche" ne doit pas être précéder par elle-même.
            if key in self.dico[key]:
                raise ValueError(
                    "Erreur : La clé est présente dans sa propre valeur.")

            # vérifie si des tâches ne sont pas mutuellement dépandante
            for key2 in self.dico.keys():
                if key in self.dico[key2] and key2 in self.dico[key]:
                    raise ValueError("les tâches sont mutuellement dependante")

        # verifie si la dépendance est dans la liste des tâches
        for dependencies in self.dico.values():
            for dep in dependencies:
                if dep not in task_names:
                    raise ValueError(
                        f"La dépendance {dep} n'est pas dans la liste des tâches")

    # renvoie la liste de dependence pour une tache selon le système de parallélisme maximal,

    def getDependencies(self, task):

        # si la tache n'a aucune dependance cas exeptionel
        if self.dico[task.name] == []:
            return self.dico[task.name]
        else:
            # pour chaque dependance de notre tache :
            for element in self.dico[task.name]:
                # pour la dependence on verifie si parmis ces dependance y'en a une qui appartient a la liste de dependence de nomTache
                for dependance in self.dico[element]:
                    if dependance in self.dico[task.name]:
                        # supprimer la dependance qui sert a rien de la liste
                        self.dico[task.name].remove(dependance)

        return self.dico[task.name]

    # exécute les tâches de façon séquentielle en respectant l’ordre imposé par la relation de précédence
    def runSeq(self):
        # effectue un tri topologique sur le graphe pour obtenir l'ordre d'exécution des tâches
        task_ord = list(networkx.topological_sort(self.graph))
        # parcour les tâches dans l'ordre obtenu
        for task_name in task_ord:
            # trouve l'instance de la tâche correspondante à partir de son nom et l'exécute
            task = next(t for t in self.task if t.name == task_name)
            task.run()

     # affiche graphiquement le grahe de précédence en utilisant la bilbiothèque "networkx"
    def draw(self):
        # crée un graphe dirigé vide
        graph = networkx.DiGraph()

        for task in self.task:
            # ajoute un noeud au graphe pour chaque tâche en utilisant son nom
            graph.add_node(task.name)
            # parcourir les dépendances de la tâche actuelle
            for dep in self.getDependencies(task):
                # ajoute un arc dirigé entre chaque dépendance et la tâche actuelle
                graph.add_edge(dep, task.name)

        # affiche le graphe dans une fenêtre
        pos = networkx.spring_layout(graph)
        networkx.draw(graph, pos, with_labels=True, node_size=2000,
                      node_color="lightblue", font_size=10, font_weight="bold")
        plt.show()
        return graph
