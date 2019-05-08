import pygame
import random
import pygbutton


from units import *
from field import *
from menu import *
from clickTest import *

clock = pygame.time.Clock()


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
    area = Field(10, 10, 20)

    tree = pygame.image.load("assets/tree.png")

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
    obj_doAttack = None
     
    # main loop
    while running:

        clock.tick(30)

        # Get next unit's turn and make sure certain variables are reset
        if current_unit is None:
            current_unit = unit_order(Units)
            current_unit.get_paths(Units, area)
            current_unit.moved = False
            current_unit.acted = False
            current_unit.boosted = False
            current_unit.boost_count = 0
            selected_unit = current_unit
            status = 1

        # Check the status to determine which classes need to be instantiated
        if status == 0 and obj_unitSelect is None:
            obj_unitSelect = unitSelect(Units)

        if status == 1 and obj_doMove is None:
            obj_doMove = doMove(current_unit, Units, area)

        if obj_doMove.boost_count != current_unit.boost_count:
            current_unit.get_paths(Units, area)
            obj_doMove = doMove(current_unit, Units, area)

        if status == 1 and obj_menuUnitMain is None:
            obj_menuUnitMain = menuUnitMain(current_unit)


        if status == 3 and obj_doAttack is None:
            obj_doAttack = doAttack(current_unit)

        if obj_doAttack:
            if obj_doAttack.boost_count != current_unit.boost_count:
                obj_doAttack = doAttack(current_unit)

        if status != 3 and obj_doAttack:
            obj_doAttack = None


        #if obj_menuUnitMain:
        #    obj_menuUnitMain.update(current_unit)

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

            if status == 1 and current_unit is not None:
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

            if status == 2 and current_unit is not None:
                current_unit = obj_doMove.handleEvent(event, current_unit, area)
                if current_unit.moved:
                    obj_doMove = None
                    status = 1
                    # Check if boosted
                    if current_unit.boost_count > 0 and not current_unit.boosted:
                        current_unit.boosted = True

            if status == 3 and current_unit is not None and obj_doAttack:
                attacked_unit = obj_doAttack.handleEvent(event, current_unit, Units)
                if attacked_unit == 'nothing':
                    # Nothing was attacked
                    status = 1
                    obj_doAttack = None
                    attacked_unit = None
                elif attacked_unit:
                    # A unit was attacked
                    status = 1
                    obj_doAttack = None
                    attacked_unit = func_attack(current_unit, attacked_unit)
                    # Check if boosted
                    if current_unit.boost_count > 0 and not current_unit.boosted:
                        current_unit.boosted = True
                        for i in range(current_unit.boost_count):
                            attacked_unit = func_attack(current_unit, attacked_unit)
                    attacked_unit = None


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


        # Remove a dead unit
        for u in Units:
            if u.stat_hp <= 0:
                Units.remove(u)


        # Draw the map
        area.screen.fill((16, 16, 16))
        pygame.draw.rect(area.screen, (24, 96, 24),
            (GRID_OFFSET, GRID_OFFSET, 500, 500))


        for g in area.grid:
            pygame.draw.rect(area.screen, (48, 128, 48),
                grid_to_pixel(g[0], g[1]) + \
                grid_to_pixel(1.5, 1.5))
            #pygame.draw.rect(area.screen, (48, 48, 48),
            #    grid_to_pixel(g[0], g[1]) + \
            #    grid_to_pixel(1.5, 1.5))

        for t in area.trees:
            area.screen.blit(tree, grid_to_pixel(*t))


        # Show unit stats
        if selected_unit:
            show_stats(area.screen, selected_unit)

        # Draw the attack possibilities
        if status == 3 and obj_doAttack:
            obj_doAttack.draw(area)

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

        # Draw the action menu
        if status == 1 and obj_menuUnitMain:
            obj_menuUnitMain.update(current_unit)
            obj_menuUnitMain.draw(area)

        # Draw the move possibilities
        if status == 2 and obj_doMove:
            obj_doMove.draw(area)


        # Update the display
        pygame.display.update()


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

                # Boosting on a wait
                if current_unit.boost_count > 0 and not current_unit.boosted:
                    current_unit.stat_ct += current_unit.boost_count * current_unit.base_speed
                    current_unit.boosted = True

                # Increase boost if unit didn't boost
                if not current_unit.boosted:
                    current_unit.stat_bp = min(current_unit.base_bp_max, current_unit.stat_bp + 1)

                # Reset
                status = 1
                current_unit.moved = False
                current_unit.acted = False
                current_unit.boosted = False
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


