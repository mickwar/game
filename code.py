import pygame
import random
import pygbutton


from units import *
from field import *
from menu import *

clock = pygame.time.Clock()


# Class for testing left click
class clickTest():
    def __init__(self, rect):
        self._rect = pygame.Rect(rect)
        self.mouseDown = False
        self.mouseOverRect = False
        self.lastMouseDownOverRect = False

    # Borrowed heavily from pygbutton's logic
    def handleEvent(self, event):
        if event.type not in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            return False

        if event.button != 1:
            return False

        #hasExited = False
        if not self.mouseOverRect and self._rect.collidepoint(event.pos):
            # if mouse has entered the rect:
            self.mouseOverRect = True
        elif self.mouseOverRect and not self._rect.collidepoint(event.pos):
            # if mouse has exited the rect:
            self.mouseOverRect = False
            #hasExited = True

        if self._rect.collidepoint(event.pos):
            # if mouse event happened over the rect:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseDown = True
                self.lastMouseDownOverRect = True
        else:
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                self.lastMouseDownOverRect = False

        # mouse up is handled whether or not it was over the rect
        isClicked = False
        if event.type == pygame.MOUSEBUTTONUP:
            if self.lastMouseDownOverRect:
                isClicked = True
            self.lastMouseDownOverRect = False

            if self.mouseDown:
                self.mouseDown = False

        return isClicked

    def draw(self, gameDisplay):
        pygame.draw.rect(gameDisplay, (0, 128, 0), self._rect)


# Creates a pop up menu for unit action selection
def menu_unit_main(gameDisplay, current_unit, x, y, w = 100, h = 110):
    # w and h are parameters, but as of now, they are treated as fixed constants
    # (meaning other relevant arguments are hard coded)

    COLOR_ENABLED = (200, 230, 216)
    COLOR_DISABLED = (64, 64, 64)

    # Create buttons and check whether unit has moved or acted
    if not current_unit.moved:
        b_move = pygbutton.PygButton(
            rect = (x + 5, y + 5, 90, 30),
            caption = "Move (M)",
            bgcolor = COLOR_ENABLED,
            fgcolor = (0,0,0),
            hotkeys = pygame.K_m)
    else:
        b_move = pygbutton.PygButton(
            rect = (x + 5, y + 5, 90, 30),
            caption = "Move (M)",
            bgcolor = COLOR_DISABLED,
            fgcolor = (0,0,0),
            hotkeys = [])

    if not current_unit.acted:
        # enabled
        b_attack = pygbutton.PygButton(
            rect = (x + 5, y + 5 + 30 + 5, 90, 30),
            caption = "Act (A)",
            bgcolor = COLOR_ENABLED,
            fgcolor = (0,0,0),
            hotkeys = pygame.K_a)
    else:
        # disabled
        b_attack = pygbutton.PygButton(
            rect = (x + 5, y + 5 + 30 + 5, 90, 30),
            caption = "Act (A)",
            bgcolor = COLOR_DISABLED,
            fgcolor = (0,0,0),
            hotkeys = [])

    # Can always wait
    b_wait = pygbutton.PygButton(
        rect = (x + 5, y + 5 + 30 + 5 + 30 + 5, 90, 30),
        caption = "Wait (W)",
        bgcolor = COLOR_ENABLED,
        fgcolor = (0,0,0),
        hotkeys = pygame.K_w)

    show = True
    while show:
        # Display the menu at given coordinates
        # Add buttons
        pygame.draw.rect(gameDisplay.screen, (128, 128, 0), (x, y, w, h))
        r = [0, 0, 0, 0]
        for event in pygame.event.get():
            if [e for e in ['left_click', 'hotkeyup'] if e in b_move.handleEvent(event)]:
                r[0] = 1
                show = False
            if [e for e in ['left_click', 'hotkeyup'] if e in b_attack.handleEvent(event)]:
                r[1] = 1
                show = False
            if [e for e in ['left_click', 'hotkeyup'] if e in b_wait.handleEvent(event)]:
                r[2] = 1
                show = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    r[3] = 1
                    show = False

        b_move.draw(gameDisplay.screen)
        b_attack.draw(gameDisplay.screen)
        b_wait.draw(gameDisplay.screen)
        pygame.display.update()

    if r[0] > 0 and r[1] > 0:
        r[1] = 0

    return r


# For waiting for user to select movement square
def do_move(gameDisplay, current_unit, Units):
    # Get possible movement paths
    current_unit.get_paths(Units, gameDisplay)

    c = []
    for p in current_unit.paths:
        c.append(clickTest(grid_to_pixel(p[0] + 5/GRID_TO_PIXEL, p[1] + 5/GRID_TO_PIXEL) + \
                  (GRID_TO_PIXEL-10, GRID_TO_PIXEL-10)))

    show = True
    back = False
    while show:
        for event in pygame.event.get():
            for i in c:
                if i.handleEvent(event):
                    show = False
                    pos = pixel_to_grid(*pygame.mouse.get_pos())
                    current_unit.move_exact(*pos, gameDisplay)
                    current_unit.moved = True
                    break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    show = False
                    back = True
                    break

        for i in c:
            i.draw(gameDisplay.screen)

        pygame.display.update()

    return current_unit, back


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


# During no selection
#def unit_select(gameDisplay, Units):
#
#    clickables = []
#    for u in Units:
#        clickables.append(clickTest(grid_to_pixel(u.x, u.y) + \
#                  (GRID_TO_PIXEL, GRID_TO_PIXEL)))
#
#    selected_unit = None
#    show = True
#    while show:
#        for event in pygame.event.get():
#            for i in clickables:
#                if i.handleEvent(event):
#                    show = False
#                    selected_unit = Units[clickables.index(i)]
#                    break
#
#        pygame.display.update()
#
#    return selected_unit

# During no selection
class unitSelect():

    def __init__(self, Units):
        self.selected = None
        self.clickables = []
        for u in Units:
            self.clickables.append(clickTest(grid_to_pixel(u.x, u.y) + \
                      (GRID_TO_PIXEL, GRID_TO_PIXEL)))

    def handleEvent(self, event, Units):
        for c in self.clickables:
            if c.handleEvent(event):
                self.selected = Units[self.clickables.index(c)]
                break

        return self.selected


# A temporary initialization function for spawning units
def unit_create(area):
    Units = []
    for i in range(6):
        if i % 2 == 0:
            s = Unit(i % 2, chr(range(ord('a'), ord('z'))[i]), "blue", Type1)
        if i % 2 == 1:
            s = Unit(i % 2, chr(range(ord('a'), ord('z'))[i]), "red", Type2)
        tmp = area.grid[random.randint(0, len(area.grid)-1)]
        s.x = tmp[0]
        s.y = tmp[1]
        s.stat_ct += i
        Units.append(s)

    return Units


def game_loop():

    # create a surface on screen that has the size of 240 x 180
    area = Field(10, 10, 30)

    # initialize some units
    Units = unit_create(area)

    selected_unit = None
    current_unit = None
    status = 1

    key = []

    # define a variable to control the main loop
    running = True

    obj_unitSelect = None
     
    # main loop
    while running:

        clock.tick(30)
        if status == 0 and obj_unitSelect is None:
            obj_unitSelect = unitSelect(Units)

        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                quit_game()

            # Go back in menus
            # 0 - Nothing selected
            # 1 - Action menu for current unit
            # 2 - Move
            # 3 - Act
            # 4 - Wait
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if status == 1:
                        selected_unit = None
                        status = 0

                    if (status == 2 or status == 3):
                        status = 1

                    if status == 0:
                        selected_unit = None

            if status == 0 and obj_unitSelect is not None:
                selected_unit = obj_unitSelect.handleEvent(event, Units)
                if selected_unit is current_unit:
                    obj_unitSelect = None
                    status = 1


        # Go back one level on ESCAPE key press
        #if key[27] == 1 and status == 1:
        #    status = 0

        #if key[27] == 1 and (status == 2 or status == 3):
        #    status = 1

        # Get next unit's turn
        if current_unit is None:
            current_unit = unit_order(Units)
            current_unit.get_paths(Units, area)
            current_unit.moved = False
            current_unit.acted = False
            current_unit.boosted = False
            selected_unit = current_unit
            status = 1

        # Allow unit selection
        #if status == 0:
        #    selected_unit = unit_select(area.screen, Units)
        #    if selected_unit is current_unit:
        #        status = 1


        # Draw the map
        area.screen.fill((16, 16, 16))
        for g in area.grid:
            pygame.draw.rect(area.screen, (48, 48, 48),
                grid_to_pixel(g[0], g[1]) + \
                grid_to_pixel(1.5, 1.5))


        # Show unit stats
        if selected_unit:
            show_stats(area.screen, selected_unit)


        # Draw the units
        for u in Units:

            if u is current_unit:
                # Highlight current unit
                pygame.draw.rect(area.screen, (230, 230, 0),
                    grid_to_pixel(u.x + 5/GRID_TO_PIXEL, u.y + 5/GRID_TO_PIXEL) + \
                    (GRID_TO_PIXEL-10, GRID_TO_PIXEL-10))

            elif u is selected_unit:
                # Highlight selected unit
                pygame.draw.rect(area.screen, (0, 230, 230),
                    grid_to_pixel(u.x + 5/GRID_TO_PIXEL, u.y + 5/GRID_TO_PIXEL) + \
                    (GRID_TO_PIXEL-10, GRID_TO_PIXEL-10))

            # Draw each unit
            area.screen.blit(u.image, grid_to_pixel(u.x, u.y))


        pygame.display.update()

        if current_unit and status == 2:
            current_unit, tmp = do_move(area, current_unit, Units)
            if tmp:
                status = 1
                tmp = False

        if current_unit and status == 1:
            r = menu_unit_main(area, current_unit, *(grid_to_pixel(current_unit.x + 1, current_unit.y - 0.3)))
            if r[0]:
                # Move
                status = 2
            if r[1]:
                # Act
                status = 3
            if r[2]:
                # Wait
                status = 4
            if r[3]:
                selected_unit = None
                status = 0
                # Go up menu

        if current_unit:
            if current_unit.moved and status == 2:
                status = 1

        # Finishing a turn
        if current_unit:
            if status == 4:
                # Wait without moving or attacking: -50 CT
                if not current_unit.moved and not current_unit.acted:
                    current_unit.stat_ct = max(0, current_unit.stat_ct - 50)
                # Move only or attack only: -75 CT
                if current_unit.moved ^ current_unit.acted:
                    current_unit.stat_ct = max(0, current_unit.stat_ct - 75)
                # Move and attack: -100 CT
                if current_unit.moved and current_unit.acted:
                    current_unit.stat_ct = max(0, current_unit.stat_ct - 100)

                if not current_unit.boosted:
                    current_unit.stat_bp = min(current_unit.base_bp_max, current_unit.stat_bp + 1)

                # Reset
                status = 1
                current_unit.moved = False
                current_unit.acted = False
                current_unit.boosted = False
                current_unit = None


        #area.screen.blit(one.image, grid_to_pixel(one.x, one.y))
        #pygame.display.update()




def main():
    pygame.init()

    pygame.font.init()
    #myfont = pygame.font.SysFont('Arial', 16)

    # load and set the logo
    logo = pygame.image.load("red_triangle.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")

    main_menu()
    game_loop()


if __name__ == "__main__":
    main()


