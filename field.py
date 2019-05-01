import pygame
import random

GRID_TO_PIXEL = 50
GRID_OFFSET = 25
def grid_to_pixel(x, y):
    return (int((x-1)*GRID_TO_PIXEL + GRID_OFFSET), int((y-1)*GRID_TO_PIXEL + GRID_OFFSET))

def pixel_to_grid(x, y):
    return (int((x - GRID_OFFSET) / GRID_TO_PIXEL + 1), int((y - GRID_OFFSET) / GRID_TO_PIXEL + 1))

class Field():
    def __init__(self, x, y, n = 0):
        self.xrange = (1, x)
        self.yrange = (1, y)
        self.grid = []
        for i in range(1, x+1):
            for j in range(1, y+1):
                self.grid.append((i,j))
        while n > 0:
            n = n - 1
            self.grid.pop(random.randint(0, len(self.grid) - 1))
        self.screen = pygame.display.set_mode(grid_to_pixel(self.xrange[1]+1.5, self.yrange[1]+1.5))

