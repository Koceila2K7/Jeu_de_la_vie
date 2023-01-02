"""
Authors : Koceila KIRECHE and Nabil KERDOUCHE
Desc : Define Map class and map funtions
"""

import threading
import time
import json
import numpy as np
from utiles import get_cell_neighbors_from_matrix
from multi_threads_methods import thread_function_version_1,\
    thread_with_barrier
# --- Default vars
DEFAULT_DEAD_CELL_COLOR = "#FFFFFF"
DEFAULT_ALIVE_CELL_COLOR = "#000000"
DEFAULT_ROW_NUMBER = 10
DEFAULT_COL_NUMBER = 10


def load_map_from_json_file(json_file_path: str):
    """
    Cette fonction permet de lire une map
    """
    file = open(json_file_path, encoding="utf8")

    with file:
        data = json.load(file)
    return {"map":  np.matrix(data["map"]),

            "dead_cell_color": data.get('dead_cell_color')
            if data.get('dead_cell_color') is not None
            else DEFAULT_DEAD_CELL_COLOR,

            "alive_cell_color": data.get('alive_cell_color')
            if data.get('alive_cell_color') is not None
            else DEFAULT_ALIVE_CELL_COLOR}


class Map:
    """
    Class qui représente une grid de jeu

    >>> a = Map()
    >>> a.map.shape
    (10, 10)
    """

    def __init__(self, json_file_path: str = None) -> None:

        if json_file_path is None:
            self.map = np.random.randint(
                0, 2, (DEFAULT_ROW_NUMBER, DEFAULT_COL_NUMBER)) \
                if(json_file_path is None) \
                else load_map_from_json_file(json_file_path)

            self.dead_cell_color = DEFAULT_DEAD_CELL_COLOR
            self.alive_cell_color = DEFAULT_ALIVE_CELL_COLOR
        else:
            result = load_map_from_json_file(json_file_path)
            self.map = result.get('map')
            self.dead_cell_color = result.get('dead_cell_color')
            self.alive_cell_color = result.get('alive_cell_color')

    def version_sans_barriere(self, verbose: int = 1) -> None:
        """
        Fonction qui permet d'avancer dans le jeu
        """
        thrads = []
        # création des threads
        compute_matrix = np.zeros(self.map.shape)
        condition = threading.Condition()

        for x_row in range(self.map.shape[0]):
            for y_col in range(self.map.shape[1]):
                thrads.append(threading.Thread(
                    target=thread_function_version_1,
                    args=(x_row, y_col, self, compute_matrix, condition)))
        if(verbose == 1):
            print(self.map)
        # lancement
        for thread in thrads:
            thread.start()

        for thread in thrads:
            thread.join()

    def get_cell_neighbors(self, x_cord: int, y_cord: int) -> list[int]:
        """
        Cette méthode renvoie les voisins d'une cellule avec [x,y]
        >>> a = Map(None)
        >>> len(a.get_cell_neighbors(0,0))
        3
        >>> len(a.get_cell_neighbors(1,1))
        8
        """
        return get_cell_neighbors_from_matrix(self.map, x_cord, y_cord)

    def version_avec_barriere(self, nb_tour_max: int, verbose: int = 1):
        nb_tour = {'nb': nb_tour_max}

        nb_threads = self.map.shape[0] * self.map.shape[1]

        compute_matrix = np.zeros(self.map.shape)

        def orchestrator():
            compute_matrix[:] = 0
            nb_tour["nb"] -= 1
            time.sleep(2)
            if verbose == 1:
                print(self.map)
                print("Dipslay to screen ")

        barrier = threading.Barrier(nb_threads, action=orchestrator)
        voisin_condtion = threading.Condition()
        threads = []
        for x_cord in range(self.map.shape[0]):
            for y_cord in range(self.map.shape[1]):
                threads.append(threading.Thread(target=thread_with_barrier,
                                                args=(
                                                    x_cord, y_cord, self,
                                                    compute_matrix,
                                                    voisin_condtion,
                                                    barrier,
                                                    nb_tour)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    a = Map("../assets/maps/example1.json")
    a.version_avec_barriere(5)

    a = Map("../assets/maps/example1.json")
    for i in range(5):
        a.version_sans_barriere()
