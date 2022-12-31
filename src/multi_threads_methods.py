import threading
from utiles import cell_evolution, get_cell_neighbors_from_matrix


def thread_with_barrier(x_cord: int, y_cord: int, grille,
                        compute_matrix: list[list[int]],
                        voisin_condtion: threading.Condition,
                        barrier: threading.Barrier,
                        nb_tour: dict[str, int]):
    """
    Fonction qui sera exécuter par les threads
    args:
        x_cord et y_cord ce sont les coordonées de la cellule
        compute_matrix : matrices qui permet d'indiquer la fin de calcul
        grille : la Map (la grille de jeu)
        voisin_condition : la condition qui permet de synchroniser les
                        écritures avec les lectures des voisins
        barrier: la barrière qui permet de synchroniser tout les threads.
        nb_tour: ce qui permet d'arrêter les threads quand la variable arrive
                à zéro

    """
    while True:

        with voisin_condtion:
            # Calcul de la valeur N+1
            val = cell_evolution(grille.map[x_cord, y_cord],
                                 grille.get_cell_neighbors(x_cord, y_cord))

            # Déclarer que nous avons fini le calcul
            compute_matrix[x_cord, y_cord] = 1
            # Notifier les voisins de la fin de calcul
            voisin_condtion.notify_all()

            # Attendre que mes voisins finissent leurs calcul
            while get_cell_neighbors_from_matrix(compute_matrix, x_cord,
                                                 y_cord).count(0) != 0:
                voisin_condtion.wait()
            # Ecrire notre valeur
            grille.map[x_cord, y_cord] = val

        # Attendre les autres threads avant de recommencer
        barrier.wait()
        # Vérifier si on peut recommencer
        if nb_tour['nb'] == 0:
            return None


def thread_function_version_1(x_cord: int, y_cord: int, grille,
                              compute_matrix: list[list[int]],
                              voisin_condition: threading.Condition):
    """
    Fonction qui sera exécuter par les threads pour la version sans barrière
    de synchronisation.

    args:
        x_cord et y_cord ce sont les coordonées de la cellule
        grille : la Map (la grille de jeu)
        compute_matrix : matrices qui permet d'indiquer la fin de calcul
        voisin_condition : la condition qui permet de synchroniser les
                        écritures avec les lectures des voisins
    """

    with voisin_condition:
        # Calcul de la valeur n+1
        val = cell_evolution(
            grille.map[x_cord, y_cord],
            grille.get_cell_neighbors(x_cord, y_cord))

        # déclarer que nous avons fini le calcul
        compute_matrix[x_cord, y_cord] = 1
        voisin_condition.notify_all()

        # Attendre la fin des calculs des voisins
        while get_cell_neighbors_from_matrix(compute_matrix, x_cord, y_cord)\
                .count(0) != 0:
            voisin_condition.wait()
        # Ecrire la valeur calculer
        grille.map[x_cord, y_cord] = val
