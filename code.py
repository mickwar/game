import pygame
import random

from units import *
from field import *
from menu import *

clock = pygame.time.Clock()


def test_func():
    print("this is a test")
    return True

# Function that always returns true
def func_true():
    return True

def popup_menu(gameDisplay, x, y, w, h):

    # Display the menu at given coordinates
    # Add buttons
    pygame.draw.rect(gameDisplay.screen, (128, 0, 128), (x, y, w, h))
    r = [False, False]
    r[0] = button(gameDisplay.screen, "M", x + 5, y + 5, 30, 30,
        (196,0,0), (255,0,0), "m", func_true)
    r[1] = button(gameDisplay.screen, "A", x + w/2 + 5, y + 5, 30, 30,
        (196,0,0), (255,0,0), "a", func_true)
    pygame.display.update()

    if r[0] and r[1]:
        r[1] = False

    return r


# Get unit next in turn order
def unit_order(Units):
    # Sort first so highest CT will go first
    sl = sorted(Units, key = lambda x: x.stat_ct, reverse = True)
    # Check if any unit's CT as reached 100
    for u in sl:
        if u.stat_ct >= 100:
            return u
    else:
        # Increase all units CT by SPEED, don't need to use sorted list
        for u in Units:
            u.stat_ct += u.base_speed

        # Repeat until a unit reaches 100
        return unit_order(Units)


def main():
    pygame.init()

    pygame.font.init()
    myfont = pygame.font.SysFont('Arial', 16)

    # load and set the logo
    logo = pygame.image.load("red_triangle.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")

    main_menu()
     
    # create a surface on screen that has the size of 240 x 180
    area = Field(10, 10, 0)
     
    # define a variable to control the main loop
    running = True

    Units = []
    for i in range(6):
        if i % 2 == 0:
            s = Unit(chr(range(ord('a'), ord('z'))[i]), "blue", Type1)
        if i % 2 == 1:
            s = Unit(chr(range(ord('a'), ord('z'))[i]), "red", Type2)
        tmp = area.grid[random.randint(0, len(area.grid)-1)]
        s.x = tmp[0]
        s.y = tmp[1]
        s.stat_ct += i
        Units.append(s)


    tmp_text = "nothing selected"
    textsurface = myfont.render(str(tmp_text), False, (128, 0, 0))
    focused = None
    status = 1
     
    # main loop
    while running:

        clock.tick(30)

        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                quit_game()

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        key = pygame.key.get_pressed()

        # Go back one level on ESCAPE key press
        if key[27] == 1 and status > 0:
            print("status down")
            status -= 1

        # Get next unit's turn
        if focused is None:
            focused = unit_order(Units)
            focused.get_paths(Units, area)
            status = 1

        # Moving
        if not pygame.mouse.get_pressed()[0]:
            wait_flag = False

        if pygame.mouse.get_pressed()[0] and not wait_flag and not focused:
            wait_flag = True
            pos = pixel_to_grid(*pygame.mouse.get_pos())
            for s in Units:
                if pos == (s.x, s.y):
                    tmp_text = str(s.name) + ", move: " + str(s.base_move)
                    focused = s
                    focused.get_paths(Units, area)
                    #paths = get_paths(focused, Units, area)

        if pygame.mouse.get_pressed()[0] and not wait_flag and focused:
            wait_flag = True
            pos = pixel_to_grid(*pygame.mouse.get_pos())
            try:
                focused.paths.index(pos)
                focused.move_exact(*pos, area)
                focused.stat_ct = max(0, focused.stat_ct - 50)
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
        #    for dx in range(-focused.base_move, focused.base_move + 1):
        #        for dy in range(-focused.base_move, focused.base_move + 1):
        #            tmp_pos = (focused.x - dx, focused.y - dy)
        #            # Make sure not moving over an existing unit
        #            for s in Units:
        #                if tmp_pos == (s.x, s.y):
        #                    break
        #            else:
        #                # Make sure within bounds and movement range
        #                if abs(dx) + abs(dy) <= focused.base_move and \
        #                    area.xrange[0] <= tmp_pos[0] and tmp_pos[0] <= area.xrange[1] and \
        #                    area.yrange[0] <= tmp_pos[1] and tmp_pos[1] <= area.yrange[1]:
        #                    pygame.draw.rect(area.screen, (0, 128, 0),
        #                        grid_to_pixel(focused.x - dx, focused.y - dy) + \
        #                        (GRID_TO_PIXEL-5, GRID_TO_PIXEL-5))

        # Show the possible move options
        # Path-like
        if focused and status == 2:
            #paths = get_paths(focused, Units, area)
            for p in focused.paths:
                pygame.draw.rect(area.screen, (0, 128, 0),
                    grid_to_pixel(p[0] + 5/GRID_TO_PIXEL, p[1] + 5/GRID_TO_PIXEL) + \
                    (GRID_TO_PIXEL-10, GRID_TO_PIXEL-10))



        # event handling, gets all event from the event queue
        #one.move(round(random.uniform(-1, 1)/1.99 * 1), round(random.uniform(-1, 1)/1.99 * 1), area)
        for s in Units:
            area.screen.blit(s.image, grid_to_pixel(s.x, s.y))

        if focused and status == 1:
            r = popup_menu(area, *(grid_to_pixel(focused.x + 1, focused.y - 0.3) + (80, 40)))
            if r[0]:
                status = 2
            if r[1]:
                status = 3
            print(r)

        #area.screen.blit(one.image, grid_to_pixel(one.x, one.y))
        area.screen.blit(textsurface,(8,4))
        textsurface = myfont.render(str(tmp_text), False, (128, 0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    main()


