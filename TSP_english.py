import itertools
import csv
import datetime
import os
__author__ = "Janik Klauenberg"
__version__ = 2.5
#Dieses Projekt wird auf Github demnaechst auf englisch verfuegbar sein, allerdings mit minimalen
min_py_ver = 2.65
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
        Comment: creates all possible paths for an instance
        Input: Name of the instance
        Output: Nothing, creates or changes local variable all_possible
        Special: Nothing special
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
        Comment: Searchen total distance for a path and returns it with the return constructor
        Input: Name of the Instance and path from which the distance is needed
        Output: Distance of the path with return constructor
        Special: Ther HAVE TO BE connections from every node to every other node, otherwise the program wont work
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
        Comment: Uses get_distances() to calculate the distances from all possible paths
        Input: name of the instance
        Output: NO direkt output, changes local variable all_possible
        Special: No return or similar, checks if problem already got solved
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
        Comment: Solves th Traveling Salesmen Problem by using the function get_all_distances
        Input: Name of the instance
        Output: Nothing directly, changes local variable all_possible
        Special: checks if problem was already solved
        """
        if not self.solved:
            self.get_all_distances()
            self.solved = True
        else:
            pass
    def get_solution(self):
        """
        Comment: Executes function get_all_distances after checking if problem was solved or not and return fastest solution for the problem
        Input: name of the instance
        Output: fastest solution for the TSP
        Special: Checks if problem was solved and if path is shorter than near infinity (means path is impossible)
        """
        self.solve_problem()
        if self.all_possible[0][0]>hash(float("inf")):
            return None
        else:
            return self.all_possible[0]
    def export_solution(self, filename=None):
        """
        Comment: Exports solutio and also all possible paths with their corresponding distance
        Input: Name of the instance, optional: filename, gets automaticaly generated with current date if not given
        Output: No direct output, only export of csv file
        Special: Optimized for both, python 2 and python 3
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
        writer = csv.writer(f)
        writer.writerow(first_row)
        for solutions in res:
            writer.writerow(solutions)
        f.close()


if __name__ == '__main__':
    """
    Comment: Standard main testing routine
    Input: Nothing, ist a main function
    Output: Only via Print
    Special: Nothing special, just a main function
    """
    distances ={
                0 : {1 : 15, 2 : 25, 3 : 25, 4 : 10},
                1 : {0 : 15, 2 : 6, 3 : 10, 4 : 4},
                2 : {0 : 25, 1 : 6, 3 : 7, 4 : 10},
                3 : {0 : 25, 1 : 10, 2 : 7, 4 : 5},
                4 : {0 : 10, 1 : 4, 2 : 10, 3 : 5}
    }

    test = SpeditionsProblem(distances, 0)
    print ("Bester Weg:")
    print (test.get_solution())
    print ("\nAlle Wege:")
    print (test.all_possible)
    print (test.export_solution())
