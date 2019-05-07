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
class menuUnitMain():

    def __init__(self, unit, w = 100, h = 135):
        # w and h are parameters, but as of now, they are treated as fixed constants
        # (meaning other relevant arguments are hard coded)
        self.COLOR_ENABLED = (200, 230, 216)
        self.COLOR_DISABLED = (64, 64, 64)
        self.x, self.y = grid_to_pixel(unit.x + 1, unit.y - 0.3)
        self.w = w
        self.h = h
        # Create buttons
        self.b_move = pygbutton.PygButton(
            rect = (0,0,90,30),
            caption = "Move (M)",
            bgcolor = self.COLOR_ENABLED,
            fgcolor = (0,0,0),
            hotkeys = pygame.K_m)
        self.b_attack = pygbutton.PygButton(
            rect = (0,0,90,30),
            caption = "Act (A)",
            bgcolor = self.COLOR_ENABLED,
            fgcolor = (0,0,0),
            hotkeys = pygame.K_a)
        self.b_wait = pygbutton.PygButton(
            rect = (0,0,90,30),
            caption = "Wait (W)",
            bgcolor = self.COLOR_ENABLED,
            fgcolor = (0,0,0),
            hotkeys = pygame.K_w)
        self.b_bpdec = pygbutton.PygButton(
            rect = (0,0,30,20),
            caption = "-",
            bgcolor = self.COLOR_ENABLED,
            fgcolor = (0,0,0),
            hotkeys = pygame.K_z)
        self.b_bpinc = pygbutton.PygButton(
            rect = (0,0,30,20),
            caption = "+",
            bgcolor = self.COLOR_ENABLED,
            fgcolor = (0,0,0),
            hotkeys = pygame.K_x)

        # Text on the menu
        self.t_bpsurf = pygame.font.SysFont("Arial", 12).render("BP", True, (0,0,0))
        self.t_bprect = self.t_bpsurf.get_rect()
        self.t_bprect.center = (self.x + (self.w/2), self.y + 120)

        self.update(unit)

    def handleEvent(self, event, unit):
        # Also checks logic for whether the unit in its current state
        # can perform the selected action
        if [e for e in ['left_click', 'hotkeyup'] if e in self.b_move.handleEvent(event)]:
            if not unit.moved:
                return 'move'

        if [e for e in ['left_click', 'hotkeyup'] if e in self.b_attack.handleEvent(event)]:
            if not unit.acted:
                return 'attack'

        if [e for e in ['left_click', 'hotkeyup'] if e in self.b_wait.handleEvent(event)]:
            return 'wait'

        if [e for e in ['left_click', 'hotkeyup'] if e in self.b_bpdec.handleEvent(event)]:
            if unit.boost_count > 0:
                return 'bpdec'

        if [e for e in ['left_click', 'hotkeyup'] if e in self.b_bpinc.handleEvent(event)]:
            if unit.stat_bp - unit.boost_count > 0 and unit.boost_count < 3:
                return 'bpinc'

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                return 'escape'

        return None

    def draw(self, gameDisplay):
        # Draw rects and buttons
        pygame.draw.rect(gameDisplay.screen, (128, 128, 0), (self.x, self.y, self.w, self.h))
        self.b_move.draw(gameDisplay.screen)
        self.b_attack.draw(gameDisplay.screen)
        self.b_wait.draw(gameDisplay.screen)

        self.b_bpdec.draw(gameDisplay.screen)
        self.b_bpinc.draw(gameDisplay.screen)

        gameDisplay.screen.blit(self.t_bpsurf, self.t_bprect)

    def update(self, unit):
        # There is something strange with changing the width and height
        # of the buttons, the Rect changes, but width/height are affected
        # in a strange way (change the values in _propSetRect())

        # Update position of menu
        self.x, self.y = grid_to_pixel(unit.x + 1, unit.y - 0.3)

        # move
        self.b_move._propSetRect(  pygame.Rect(self.x + 5,  self.y + 5,   90, 30))
        if not unit.moved:
            self.b_move._propSetBgColor(self.COLOR_ENABLED)
        else:
            self.b_move._propSetBgColor(self.COLOR_DISABLED)

        # act
        self.b_attack._propSetRect(pygame.Rect(self.x + 5,  self.y + 40,  90, 30))
        if not unit.acted:
            self.b_attack._propSetBgColor(self.COLOR_ENABLED)
        else:
            self.b_attack._propSetBgColor(self.COLOR_DISABLED)

        # wait
        self.b_wait._propSetRect(  pygame.Rect(self.x + 5,  self.y + 75,  90, 30))

        # boost decrease
        self.b_bpdec._propSetRect( pygame.Rect(self.x + 5,  self.y + 110, 30, 20))
        if unit.boost_count > 0:
            self.b_bpdec._propSetBgColor(self.COLOR_ENABLED)
        else:
            self.b_bpdec._propSetBgColor(self.COLOR_DISABLED)

        # boost increase
        self.b_bpinc._propSetRect( pygame.Rect(self.x + 65, self.y + 110, 30, 20))
        if unit.stat_bp - unit.boost_count > 0 and unit.boost_count < 3:
            self.b_bpinc._propSetBgColor(self.COLOR_ENABLED)
        else:
            self.b_bpinc._propSetBgColor(self.COLOR_DISABLED)

        self.t_bprect.center = (self.x + (self.w/2), self.y + 120)

        # Update the buttons
        self.b_move._update()
        self.b_attack._update()
        self.b_wait._update()
        self.b_bpdec._update()
        self.b_bpinc._update()



# For waiting for user to select movement square
class doMove():

    def __init__(self, unit, Units, gameDisplay):
        unit.get_paths(Units, gameDisplay)
        self.paths = unit.paths
        self.clickables = []
        for p in self.paths:
            self.clickables.append(clickTest(
                grid_to_pixel(p[0] + 5/GRID_TO_PIXEL, p[1] + 5/GRID_TO_PIXEL) + \
                (GRID_TO_PIXEL-10, GRID_TO_PIXEL-10)))

    def handleEvent(self, event, unit, gameDisplay):
        for c in self.clickables:
            if c.handleEvent(event):
                pos = pixel_to_grid(*pygame.mouse.get_pos())
                unit.move_exact(*pos, gameDisplay)
                unit.moved = True
                break

        return unit

    def draw(self, gameDisplay):
        for c in self.clickables:
            c.draw(gameDisplay.screen)



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
    obj_menuUnitMain = None
    obj_doMove = None
     
    # main loop
    while running:

        clock.tick(30)

        # Get next unit's turn
        if current_unit is None:
            current_unit = unit_order(Units)
            current_unit.get_paths(Units, area)
            current_unit.moved = False
            current_unit.acted = False
            #current_unit.boosted = False
            current_unit.boost_count = 0
            selected_unit = current_unit
            status = 1

        # Check the status to determine which classes need to be instantiated
        if status == 0 and obj_unitSelect is None:
            obj_unitSelect = unitSelect(Units)

        if status == 1 and obj_doMove is None:
            obj_doMove = doMove(current_unit, Units, area)

        if status == 1 and obj_menuUnitMain is None:
            obj_menuUnitMain = menuUnitMain(current_unit)

        if obj_menuUnitMain:
            obj_menuUnitMain.update(current_unit)

        # Pass events to the appropriate class based on the status
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                quit_game()

            if status == 0 and obj_unitSelect is not None:
                selected_unit = obj_unitSelect.handleEvent(event, Units)
                if selected_unit is current_unit:
                    obj_unitSelect = None
                    status = 1

            if status == 2 and current_unit:
                current_unit = obj_doMove.handleEvent(event, current_unit, area)
                if current_unit.moved:
                    obj_doMove = None
                    status = 1

            # Go back in menus
            # 0 - Nothing selected
            # 1 - Action menu for current unit
            # 2 - Move
            # 3 - Act
            # 4 - Wait
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if status == 0:
                        selected_unit = None

                    if status == 1:
                        selected_unit = None
                        status = 0

                    if (status == 2 or status == 3):
                        status = 1


            if current_unit and status == 1:
                # Valid inputs are tested in .handleEvent
                r = obj_menuUnitMain.handleEvent(event, current_unit)
                if r == 'move':
                    status = 2
                elif r == 'attack':
                    status = 3
                elif r == 'wait':
                    status = 4
                elif r == 'bpdec':
                    current_unit.boost_count -= 1
                elif r == 'bpinc':
                    current_unit.boost_count += 1
                elif r == 'escape':
                    status = 0

                if r:
                    obj_menuUnitMain.update(current_unit)



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

        # Draw the move possibilities
        if obj_doMove and status == 2:
            obj_doMove.draw(area)

        # Draw the action menu
        if obj_menuUnitMain and status == 1:
            obj_menuUnitMain.draw(area)

        pygame.display.update()

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

                if current_unit.boost_count == 0:
                    current_unit.stat_bp = min(current_unit.base_bp_max, current_unit.stat_bp + 1)

                # Reset
                status = 1
                current_unit.moved = False
                current_unit.acted = False
                #current_unit.boosted = False
                current_unit.stat_bp -= current_unit.boost_count
                current_unit.boost_count = 0
                current_unit = None
                obj_doMove = None
                obj_menuUnitMain = None


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


