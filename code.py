import pygame
import random

#class Character(pygame.sprite.Sprite):
class Character():
    def __init__(self, ClassType, name):
        self.x = 1
        self.y = 1
        self.name = name
        self.image = pygame.image.load("blue_triangle.png")
        self.stat_atk = 10 + ClassType.s1
        self.stat_hp = 50 + ClassType.s2
        self.stat_move = 3 + ClassType.s3
        self.stat_speed = 7 + ClassType.s4

    def move_delta(self, dx, dy, Area):
        self.x = min(max(Area.xrange[0], self.x + dx), Area.xrange[1])
        self.y = min(max(Area.yrange[0], self.y + dy), Area.yrange[1])

    def move_exact(self, dx, dy, Area):
        if abs(self.x - dx) + abs(self.y - dy) <= self.stat_move and \
            Area.xrange[0] <= dx and dx <= Area.xrange[1] and \
            Area.yrange[0] <= dy and dy <= Area.yrange[1]:
            self.x = dx
            self.y = dy


class Type1():
    s1 = 2
    s2 = -3
    s3 = 0
    s4 = 1

class Type2():
    s1 = -1
    s2 = 5
    s3 = 1
    s4 = 0

GRID_TO_PIXEL = 50
GRID_OFFSET = 25
def grid_to_pixel(x, y):
    return (int((x-1)*GRID_TO_PIXEL + GRID_OFFSET), int((y-1)*GRID_TO_PIXEL + GRID_OFFSET))

def pixel_to_grid(x, y):
    return (int((x - GRID_OFFSET) / GRID_TO_PIXEL + 1), int((y - GRID_OFFSET) / GRID_TO_PIXEL + 1))

class Area():
    def __init__(self, x, y):
        self.xrange = (1, x)
        self.yrange = (1, y)
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
    area = Area(10, 10)
     
    # define a variable to control the main loop
    running = True

    one = Character(Type1, "one")
    one.x = 2
    one.y = 1

    two = Character(Type2, "two")
    two.x = 6
    two.y = 5

    sprites = [one, two]

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

        if pygame.mouse.get_pressed()[0] and not wait_flag and focused:
            wait_flag = True
            pos = pixel_to_grid(*pygame.mouse.get_pos())
            for s in sprites:
                if pos == (s.x, s.y):
                    focused = None
                    tmp_text = "cannot move there"
            if focused:
                focused.move_exact(*pos, area)
                focused = None
                tmp_text = "nothing selected"

        if pygame.mouse.get_pressed()[2] and not wait_flag and focused:
            wait_flag = True
            focused = None
            tmp_text = "nothing selected"



        area.screen.fill((16, 16, 16))
        pygame.draw.rect(area.screen, (48, 48, 48),
            grid_to_pixel(area.xrange[0], area.yrange[0]) + \
            grid_to_pixel(area.xrange[1]+0.5, area.yrange[1]+0.5))

        # Show the possible move options
        if focused:
            for dx in range(-focused.stat_move, focused.stat_move + 1):
                for dy in range(-focused.stat_move, focused.stat_move + 1):
                    tmp_pos = (focused.x - dx, focused.y - dy)
                    # Make sure not moving over an existing unit
                    for s in sprites:
                        if tmp_pos == (s.x, s.y):
                            break
                    else:
                        # Make sure within bounds and movement range
                        if abs(dx) + abs(dy) <= focused.stat_move and \
                            area.xrange[0] <= tmp_pos[0] and tmp_pos[0] <= area.xrange[1] and \
                            area.yrange[0] <= tmp_pos[1] and tmp_pos[1] <= area.yrange[1]:
                            pygame.draw.rect(area.screen, (0, 128, 0),
                                grid_to_pixel(focused.x - dx, focused.y - dy) + \
                                (GRID_TO_PIXEL-5, GRID_TO_PIXEL-5))

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


