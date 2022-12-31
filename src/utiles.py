NEIGHBORS_cord = set([(-1, -1), (-1, 0), (-1, 1),
                      (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)])


def cell_evolution(cell_state: int, neighbors_state: list[int]) -> int:
    """
    Cette fonction prend en entrée l'état de la cellule à l'instant N ainsi
    que l'etat de ses voisins.

    Et renvoi l'etat de la cellule à l'instant N+1

    >>> cell_evolution(0,[1,1,1])
    1
    >>> cell_evolution(1,[1,0,0])
    0
    """
    nbr_neighbors_alive = neighbors_state.count(1)

    return 1 if((cell_state == 0 and nbr_neighbors_alive == 3)
                or (cell_state == 1 and nbr_neighbors_alive in (2, 3))) \
        else 0


def get_cell_neighbors_from_matrix(matrix, x_cord, y_cord):
    """
    Cette méthode renvoie les voisins d'une cellule avec [x,y]
    >>> import numpy as np
    >>> a = np.zeros((6,6))
    >>> len(get_cell_neighbors_from_matrix(a,0,0))
    3
    >>> len(get_cell_neighbors_from_matrix(a,1,1))
    8
    """
    neighbors = []

    for coord in NEIGHBORS_cord:
        new_x = x_cord + coord[0]
        new_y = y_cord + coord[1]

        if matrix.shape[0] > new_x >= 0 and \
                matrix.shape[1] > new_y >= 0:
            neighbors.append(matrix[new_x, new_y])

    return neighbors
