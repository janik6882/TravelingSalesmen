import itertools
import csv
import datetime
import os
__author__ = "Janik Klauenberg"
__version__ = 2.5
#Dieses Projekt wird auf Github demnaechst auf englisch verfuegbar sein, allerdings mit minimalen
min_py_ver = 2.6
#__github__ = "https://github.com/janik6882/TravelingSalesmen" Currently Private
import sys
x = sys.version_info
py_ver = float(str(x[0]) + "." + str(x[1]))
if min_py_ver>py_ver:
    sys.exit()

class SpeditionsProblem():
    def __init__(self, dists, startingpoint):
        """
        Comment: Class for solving the Traveling Salesmen Problem
        Input: Name of instance, Distanz as a Dictionary and a startingpoint which must be in the Dictionary
        Output: Nothing, just a standard Init
        Special: Uses method get_alle_pathe, there HAS TO BE a connection from every node to every other node
        """
        self.distances = dists
        self.start = startingpoint
        self.solved = False
        self.get_all_paths()

    def get_all_paths(self):
        """
        Kommentar: Erzeugt alle moeglichen pathe fuer die Instanz
        Input: Name der Instanz
        Output: Keins, erzeugt oder aendert lokale Variable alle_moeglichen
        Besonders: Keine Besonderheiten
        """
        main_path = []
        for i in self.distances:
            main_path.append(i)
        main_path.remove(self.start)
        all = list(itertools.permutations(main_path))
        for j in range(len(all)):
            all[j] = [list(all[j])]
            all[j][0].insert(0, self.start)
            all[j][0].append(self.start)
        self.all_possible = all
    def get_distances(self, path):
        """
        Kommentar: Sucht fuer einen path die gesamtdistanz und gibt diese mittels return konstruktor zurueck
        Input: Name der Instanz, path von welchem die Distanz benoetigt wird
        Output: Distanz eines pathes mittels Return konstruktor
        Besonders: Es muessen Verbindungen von ALLEN knoten untereinander existieren
        """
        res = 0
        for i in range(len(path)-1):
            try:
                res += self.distances[path[i]][path[i+1]]
            except KeyError:
                res += hash(float("inf"))
        return res
    def get_all_distances(self):
        """
        Kommentar: Nutzt get_distanz() um die distanz von allen moeglichen Wegen zu ermitteln
        Input: Name der Instanz
        Output: Kein direktes, aendert lokale variable alle_moeglichen
        Besonders: Kein direktes Return oder so, prueft ob problem bereits geloest wurde
        """
        if self.solved:
            return
        temp = self.all_possible
        for i in range(len(temp)):
            dist = self.get_distances(temp[i][0])
            temp[i].insert(0, dist)
        temp.sort()
        self.all_possible = temp
    def solve_problem(self):
        """
        Kommentar: loest das Problem indem es die Methode get_all_distances aufruft
        Input: Name der Instanz
        Output: Kein direktes, lokale variable alle_moeglichen wird veraendert
        Besonders: prueft ob problem bereits geloest wurde
        """
        if not self.solved:
            self.get_all_distances()
            self.solved = True
        else:
            pass
    def get_solution(self):
        """
        Kommentar: Fuehrt Methode get_all_distances aus und gibt schnellsten weg aus
        Input: Name der Instanz
        Output: Kein direktes
        Besonders: prueft ob problem bereits geloest wurde
        """
        self.solve_problem()
        return self.all_possible[0]
    def export_loesung(self, filename=None):
        """
        Kommentar: Exportiert die Loesung sowie alle anderen moeglichen pathe mit gewicht
        Input: name der Instanz, optional: Name der Datei
        Output: Kein direktes Output
        Besonders: Optimiert fuer python 3 und python 3
        """
        res = []
        if not self.solved:
            self.solve_problem
        if not filename:
            filename = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + "--SpeditionsProblem")
        for i in range(len(self.all_possible)):
            res.append([self.all_possible[i][0]])
            for k in self.all_possible[i][1]:
                res[i].append(k)
        filename = filename + ".csv"
        filename = os.path.join("csv", filename)
        first_row = ["Distanz", "path"]
        print (res)
        global x
        if x[0]==3:
            f = open(filename, "w", newline="")
        elif x[0]==2:
            f = open(filename, "wb")
        #with open(filename, "wb") as f:
        writer = csv.writer(f)
        writer.writerow(first_row)
        for loesung in res:
            writer.writerow(loesung)
        f.close()


if __name__ == '__main__':
    """
    Kommentar: Main Programm, erstellt Instanz "erster" und uebergibt einen ungerichteten Graphen
    Input: Keins, da Main
    Output: Ausgabe des ergebnisses mittels Print
    Besonders: nichts Besonders, da Main funktion
    """
    distanzen ={
                0 : {1 : 15, 2 : 25, 3 : 25, 4 : 10},
                1 : {0 : 15, 2 : 6, 3 : 10, 4 : 4},
                2 : {0 : 25, 1 : 6, 3 : 7, 4 : 10},
                3 : {0 : 25, 1 : 10, 2 : 7, 4 : 5},
                4 : {0 : 10, 1 : 4, 2 : 10, 3 : 5}
    }

    erster = SpeditionsProblem(distanzen, 0)
    print ("Bester Weg:")
    print (erster.get_solution())
    print ("\nAlle Wege:")
    print (erster.all_possible)
    #print (erster.export_loesung())
