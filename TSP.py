import itertools
import csv
import datetime
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
    def __init__(self, dists, startpunkt):
        """
        Kommentar: Klasse die zur loesung des Traveling Salesmen Problem gedacht ist
        Input: Name der Instanz, Distanzen in form eines Dictionarys und ein Startpunkt welcher im Dictionary enthalten sein MUSS
        Output: Keins, da Init
        Besonders: Ruft methode get_alle_pfade auf, Es muss von jedem Punkt eine angabe zur Distanz zu jedem anderen Punkt geben
        """
        self.distanzen = dists
        self.start = startpunkt
        self.geloest = False
        self.get_alle_pfade()

    def get_alle_pfade(self):
        """
        Kommentar: Erzeugt alle moeglichen Pfade fuer die Instanz
        Input: Name der Instanz
        Output: Keins, erzeugt oder aendert lokale Variable alle_moeglichen
        Besonders: Keine Besonderheiten
        """
        main_pfad = []
        for i in self.distanzen:
            main_pfad.append(i)
        main_pfad.remove(self.start)
        alle = list(itertools.permutations(main_pfad))
        for j in range(len(alle)):
            alle[j] = [list(alle[j])]
            alle[j][0].insert(0, self.start)
            alle[j][0].append(self.start)
        self.alle_moeglichen = alle
    def get_distanz(self, pfad):
        """
        Kommentar: Sucht fuer einen Pfad die gesamtdistanz und gibt diese mittels return konstruktor zurueck
        Input: Name der Instanz, Pfad von welchem die Distanz benoetigt wird
        Output: Distanz eines Pfades mittels Return konstruktor
        Besonders: Es muessen Verbindungen von ALLEN knoten untereinander existieren
        """
        res = 0
        for i in range(len(pfad)-1):
            try:
                res += self.distanzen[pfad[i]][pfad[i+1]]
            except KeyError:
                res += hash(float("inf"))
        return res
    def get_all_distanzen(self):
        """
        Kommentar: Nutzt get_distanz() um die distanz von allen moeglichen Wegen zu ermitteln
        Input: Name der Instanz
        Output: Kein direktes, aendert lokale variable alle_moeglichen
        Besonders: Kein direktes Return oder so, prueft ob problem bereits geloest wurde
        """
        if self.geloest:
            return
        temp = self.alle_moeglichen
        for i in range(len(temp)):
            dist = self.get_distanz(temp[i][0])
            temp[i].insert(0, dist)
        temp.sort()
        self.alle_moeglichen = temp
    def solve_problem(self):
        """
        Kommentar: loest das Problem indem es die Methode get_all_distanzen aufruft
        Input: Name der Instanz
        Output: Kein direktes, lokale variable alle_moeglichen wird veraendert
        Besonders: prueft ob problem bereits geloest wurde
        """
        if not self.geloest:
            self.get_all_distanzen()
            self.geloest = True
        else:
            pass
    def get_loesung(self):
        """
        Kommentar: Fuehrt Methode get_all_distanzen aus und gibt schnellsten weg aus
        Input: Name der Instanz
        Output: Kein direktes
        Besonders: prueft ob problem bereits geloest wurde
        """
        self.solve_problem()
        return self.alle_moeglichen[0]
    def export_loesung(self, filename=None):
        """
        Kommentar: Exportiert die Loesung sowie alle anderen moeglichen Pfade mit gewicht
        Input: name der Instanz, optional: Name der Datei
        Output: Kein direktes Output
        Besonders: Optimiert fuer python 3 und python 3
        """
        res = []
        if not self.geloest:
            self.solve_problem
        if not filename:
            filename = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + "--SpeditionsProblem")
        for i in range(len(self.alle_moeglichen)):
            res.append([self.alle_moeglichen[i][0]])
            for k in self.alle_moeglichen[i][1]:
                res[i].append(k)
        filename = filename + ".csv"
        first_row = ["Distanz", "Pfad"]
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
    print (erster.get_loesung())
    print ("\nAlle Wege:")
    print (erster.alle_moeglichen)
    print (erster.export_loesung())
