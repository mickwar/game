import pygame
import random

from units import *

GRID_TO_PIXEL = 50
GRID_OFFSET = 25
def grid_to_pixel(x, y):
    return (int((x-1)*GRID_TO_PIXEL + GRID_OFFSET), int((y-1)*GRID_TO_PIXEL + GRID_OFFSET))

def pixel_to_grid(x, y):
    return (int((x - GRID_OFFSET) / GRID_TO_PIXEL + 1), int((y - GRID_OFFSET) / GRID_TO_PIXEL + 1))

class Area():
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


def main():
    pygame.init()

    pygame.font.init()
    myfont = pygame.font.SysFont('Arial', 16)

    # load and set the logo
    logo = pygame.image.load("red_triangle.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")
     
    # create a surface on screen that has the size of 240 x 180
    area = Area(10, 10, 20)
     
    # define a variable to control the main loop
    running = True

    sprites = []
    for i in range(6):
        if i % 2 == 0:
            s = Unit(chr(range(ord('a'), ord('z'))[i]), "blue", Type1, Type2)
        if i % 2 == 1:
            s = Unit(chr(range(ord('a'), ord('z'))[i]), "red", Type2, Type2)
        tmp = area.grid[random.randint(0, len(area.grid)-1)]
        s.x = tmp[0]
        s.y = tmp[1]
        sprites.append(s)


    tmp_text = "nothing selected"
    textsurface = myfont.render(str(tmp_text), False, (128, 0, 0))
    focused = None
     
    # main loop
    while running:

        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        # Moving
        if not pygame.mouse.get_pressed()[0]:
            wait_flag = False

        if pygame.mouse.get_pressed()[0] and not wait_flag and not focused:
            wait_flag = True
            pos = pixel_to_grid(*pygame.mouse.get_pos())
            for s in sprites:
                if pos == (s.x, s.y):
                    tmp_text = str(s.name) + ", move: " + str(s.stat_move)
                    focused = s
                    focused.get_paths(sprites, area)
                    #paths = get_paths(focused, sprites, area)

        if pygame.mouse.get_pressed()[0] and not wait_flag and focused:
            wait_flag = True
            pos = pixel_to_grid(*pygame.mouse.get_pos())
            try:
                focused.paths.index(pos)
                focused.move_exact(*pos, area)
                focused = None
                tmp_text = "nothing selected"
            except:
                focused = None
                tmp_text = "cannot move there"

        if pygame.mouse.get_pressed()[2] and not wait_flag and focused:
            wait_flag = True
            focused = None
            tmp_text = "nothing selected"



        area.screen.fill((16, 16, 16))
        for g in area.grid:
            pygame.draw.rect(area.screen, (48, 48, 48),
                grid_to_pixel(g[0], g[1]) + \
                grid_to_pixel(1.5, 1.5))

        # Show the possible move options
        # Teleportation-like
        #if focused:
        #    for dx in range(-focused.stat_move, focused.stat_move + 1):
        #        for dy in range(-focused.stat_move, focused.stat_move + 1):
        #            tmp_pos = (focused.x - dx, focused.y - dy)
        #            # Make sure not moving over an existing unit
        #            for s in sprites:
        #                if tmp_pos == (s.x, s.y):
        #                    break
        #            else:
        #                # Make sure within bounds and movement range
        #                if abs(dx) + abs(dy) <= focused.stat_move and \
        #                    area.xrange[0] <= tmp_pos[0] and tmp_pos[0] <= area.xrange[1] and \
        #                    area.yrange[0] <= tmp_pos[1] and tmp_pos[1] <= area.yrange[1]:
        #                    pygame.draw.rect(area.screen, (0, 128, 0),
        #                        grid_to_pixel(focused.x - dx, focused.y - dy) + \
        #                        (GRID_TO_PIXEL-5, GRID_TO_PIXEL-5))

        # Show the possible move options
        # Path-like
        if focused:
            #paths = get_paths(focused, sprites, area)
            for p in focused.paths:
                pygame.draw.rect(area.screen, (0, 128, 0),
                    grid_to_pixel(p[0] + 5/GRID_TO_PIXEL, p[1] + 5/GRID_TO_PIXEL) + \
                    (GRID_TO_PIXEL-10, GRID_TO_PIXEL-10))


        # event handling, gets all event from the event queue
        #one.move(round(random.uniform(-1, 1)/1.99 * 1), round(random.uniform(-1, 1)/1.99 * 1), area)
        for s in sprites:
            area.screen.blit(s.image, grid_to_pixel(s.x, s.y))

        #area.screen.blit(one.image, grid_to_pixel(one.x, one.y))
        area.screen.blit(textsurface,(8,4))
        textsurface = myfont.render(str(tmp_text), False, (128, 0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    main()


