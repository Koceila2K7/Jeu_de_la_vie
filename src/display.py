import sys
import time
import pygame
from Map import Map

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

DEFAULT_DEAD_CELL_COLOR = "#FFFFFF"
DEFAULT_ALIVE_CELL_COLOR = "#000000"


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(DEFAULT_DEAD_CELL_COLOR)
    a = Map("../assets/maps/example1.json")

    while True:
        drawGrid(a)
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
