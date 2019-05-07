import pygame
import random
import pygbutton


from units import *
from field import *
from menu import *
from clickTest import *

clock = pygame.time.Clock()


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


