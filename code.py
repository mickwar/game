import pygame
import random

#class Character(pygame.sprite.Sprite):
class Character():
    def __init__(self, ClassType):
        self.x = 1
        self.y = 1
        self.image = pygame.image.load("blue_triangle.png")
        self.stat_atk = 10 + ClassType.s1
        self.stat_hp = 50 + ClassType.s2
        self.stat_move = 3 + ClassType.s3
        self.stat_speed = 7 + ClassType.s4
    def move(self, dx, dy, Area):
        self.x = min(max(Area.xrange[0], self.x + dx), Area.xrange[1])
        self.y = min(max(Area.yrange[0], self.y + dy), Area.yrange[1])


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

class Area():
    def __init__(self, x, y):
        self.xrange = (1, x)
        self.yrange = (1, y)
        self.screen = pygame.display.set_mode(grid_to_pixel(self.xrange[1]+1.5, self.yrange[1]+1.5))


def main():
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("red_triangle.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")
     
    # create a surface on screen that has the size of 240 x 180
    area = Area(10, 10)
     
    # define a variable to control the main loop
    running = True

    blue = Character(Type1)
    area.screen.blit(blue.image, (blue.x, blue.y))
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        blue.move(round(random.uniform(-1, 1)/1.99 * 1), round(random.uniform(-1, 1)/1.99 * 1), area)
        area.screen.fill((16,16,16))
        pygame.draw.rect(area.screen, (48, 48, 48),
            grid_to_pixel(area.xrange[0], area.yrange[0]) + \
            grid_to_pixel(area.xrange[1]+0.5, area.yrange[1]+0.5))
        area.screen.blit(blue.image, grid_to_pixel(blue.x, blue.y))
        pygame.display.flip()
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False


if __name__ == "__main__":
    main()


