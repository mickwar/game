import pygame
import random

#GRID_TO_PIXEL = 50
#def grid_to_pixel(x, y):
#    return (int((x-1)*GRID_TO_PIXEL), int((y-1)*GRID_TO_PIXEL))
#
#def pixel_to_grid(x, y):
#    return (int(x / GRID_TO_PIXEL + 1), int(y / GRID_TO_PIXEL + 1))

#class Field(pygame.Surface):
# 4:3
#RES = (640, 480)
#RES = (800, 600)
#RES = (1024, 768)

# 16:9
RES = (1280, 720)


class Field():
    def __init__(self, x, y, n = 0, map_width = RES[0], map_height = RES[1], side_height = 200):
        self.zoom = [50, 56, 63, 72, 81, 92, 104, 117, 132, 150]
        self.zoom_ind = 0
        self.GRID_TO_PIXEL = self.zoom[self.zoom_ind]
        self.pixel_offset = (0, 0)
        self.scroll_flag = False
        self.map_w = map_width
        self.map_h = map_height - side_height
        self.side_h = side_height
        self.xrange = (1, x)
        self.yrange = (1, y)
        self.grid = []
        self.tree = pygame.image.load("assets/tree.png")
        self.trees = []
        for i in range(1, x+1):
            for j in range(1, y+1):
                self.grid.append((i,j))
        while n > 0:
            n = n - 1
            h = self.grid.pop(random.randint(0, len(self.grid) - 1))
            self.trees.append(h)
        #self.screen = pygame.display.set_mode(grid_to_pixel(self.xrange[1]+6.5, self.yrange[1]+2.0))
        self.screen = pygame.display.set_mode((self.map_w, self.map_h + self.side_h))

    def handleEvent(self, event):
        # Scroll around the map
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.scroll_flag = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.scroll_flag = False

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 4:
                self.zoom_ind = min(len(self.zoom)-1, self.zoom_ind + 1)
                self.GRID_TO_PIXEL = self.zoom[self.zoom_ind]
            if event.button == 5:
                self.zoom_ind = max(0, self.zoom_ind - 1)
                self.GRID_TO_PIXEL = self.zoom[self.zoom_ind]

        if event.type == pygame.MOUSEMOTION:
            if self.scroll_flag:
                self.pixel_offset = list(map(sum, zip(self.pixel_offset, event.rel)))
                self.pixel_offset[0] = max(self.map_w - self.GRID_TO_PIXEL*self.xrange[1] - 100, self.pixel_offset[0])
                self.pixel_offset[0] = min(100, self.pixel_offset[0])
                self.pixel_offset[1] = max(self.map_h - self.GRID_TO_PIXEL*self.yrange[1] - 100, self.pixel_offset[1])
                self.pixel_offset[1] = min(100, self.pixel_offset[1])
                self.pixel_offset = tuple(self.pixel_offset)


    # Convert from a grid point to a pixel
    # px = (gx - 1) * GTP + PO[0]
    # py = (gy - 1) * GTP + PO[1]

    # Convert from a pixel to a grid point
    # gx = (px - PO[0]) / GTP + 1
    # gy = (py - PO[1]) / GTP + 1

    def grid_to_pixel(self, gx, gy, offset = True):
        if offset:
            return (int((gx-1)*self.GRID_TO_PIXEL + self.pixel_offset[0]),
                    int((gy-1)*self.GRID_TO_PIXEL + self.pixel_offset[1]))
        else:
            return (int((gx-1)*self.GRID_TO_PIXEL),
                    int((gy-1)*self.GRID_TO_PIXEL))

    def pixel_to_grid(self, px, py):
        return (int((px - self.pixel_offset[0]) / self.GRID_TO_PIXEL + 1),
                int((py - self.pixel_offset[1]) / self.GRID_TO_PIXEL + 1))

    def draw(self):
        # Draw the map
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (24, 96, 24),
            (self.pixel_offset[0], self.pixel_offset[1], self.GRID_TO_PIXEL*self.xrange[1], self.GRID_TO_PIXEL*self.yrange[1]))


        for g in self.grid:
            pygame.draw.rect(self.screen, (48, 128, 48),
                self.grid_to_pixel(g[0], g[1]) + (self.GRID_TO_PIXEL, self.GRID_TO_PIXEL))
                #self.grid_to_pixel(g[0] + self.pixel_offset[0] / self.GRID_TO_PIXEL, g[1] + self.pixel_offset[1] / self.GRID_TO_PIXEL) + \
                #self.grid_to_pixel(2.0, 2.0))
            #pygame.draw.rect(self.screen, (48, 48, 48),
            #    grid_to_pixel(g[0], g[1]) + \
            #    grid_to_pixel(1.5, 1.5))

        for t in self.trees:
            self.screen.blit(self.tree, self.grid_to_pixel(t[0], t[1]))
            #self.screen.blit(self.tree, self.grid_to_pixel(t[0] + self.pixel_offset[0] / self.GRID_TO_PIXEL, t[1] + self.pixel_offset[1] / self.GRID_TO_PIXEL))
            #self.screen.blit(tree, grid_to_pixel(*t))

