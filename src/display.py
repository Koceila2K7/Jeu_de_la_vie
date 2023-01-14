
import threading
import sys
import time
import pygame
from Map import Map


def path_constructor(file_name: str) -> str:
    return '../assets/maps/'+file_name+'.json'


def start_pygame_screnn(path, mode, nbr_tour):

    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)
    WINDOW_HEIGHT = 320
    WINDOW_WIDTH = 320

    DEFAULT_DEAD_CELL_COLOR = "#FFFFFF"
    DEFAULT_ALIVE_CELL_COLOR = "#000000"

    def main():
        global SCREEN, CLOCK
        pygame.init()
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        CLOCK = pygame.time.Clock()
        SCREEN.fill(DEFAULT_DEAD_CELL_COLOR)
        a = Map(path)
        INFINITE = mode != 0

        if INFINITE:
            a.version_avec_barriere(nbr_tour, 0, draw_grid_mode_infinite)
        else:
            for i in range(nbr_tour):
                drawGrid(a)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.update()

    def draw_grid_mode_infinite(matrix: list[list[int]]):
        blockSize = 20  # Set the size of the grid block
        for countx, x in enumerate(range(0, WINDOW_WIDTH, blockSize)):
            for county, y in enumerate(range(0, WINDOW_HEIGHT, blockSize)):
                rect = pygame.Rect(x, y, blockSize, blockSize)

                pygame.draw.rect(
                    SCREEN, DEFAULT_ALIVE_CELL_COLOR
                    if matrix[countx, county] == 1
                    else DEFAULT_DEAD_CELL_COLOR, rect)
                pygame.draw.rect(
                    SCREEN,
                    (0, 0, 0), rect, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

    def drawGrid(map: Map):
        blockSize = 20  # Set the size of the grid block

        for countx, x in enumerate(range(0, WINDOW_WIDTH, blockSize)):
            for county, y in enumerate(range(0, WINDOW_HEIGHT, blockSize)):
                rect = pygame.Rect(x, y, blockSize, blockSize)

                pygame.draw.rect(
                    SCREEN, DEFAULT_ALIVE_CELL_COLOR
                    if map.map[countx, county] == 1
                    else DEFAULT_DEAD_CELL_COLOR, rect)
                pygame.draw.rect(
                    SCREEN,
                    (0, 0, 0), rect, 1)

        map.version_sans_barriere(verbose=0)

    main()


# threading.Thread(target=start_pygame_screnn,).start()

if __name__ == "__main__":
    if(len(sys.argv) == 1):
        exit(1)
    file_name = sys.argv[1]
    # If 0 mode step by step else Infinite

    mode_d_execution = sys.argv[2] if (len(sys.argv) > 2) else 0
    nbr_tour = 10
    try:
        nbr_tour = int(sys.argv[3]) if (len(sys.argv) > 3) else 50
    except:
        pass
    print(path_constructor(file_name), mode_d_execution)
    start_pygame_screnn(path_constructor(file_name),
                        mode_d_execution, nbr_tour)
