import pygame
from pygame.locals import *

class clickTest():
    def __init__(self, gameDisplay, x, y, offset = False):
        self._rect = pygame.Rect(gameDisplay.grid_to_pixel(x, y, offset) + \
            (gameDisplay.GRID_TO_PIXEL, gameDisplay.GRID_TO_PIXEL))
        self._rect_orig = self._rect.copy()
        self.mouseDown = False
        self.mouseOverRect = False
        self.lastMouseDownOverRect = False
    #def __init__(self, rect):
    #    self._rect = pygame.Rect(rect)
    #    self._rect_orig = self._rect.copy()
    #    self.mouseDown = False
    #    self.mouseOverRect = False
    #    self.lastMouseDownOverRect = False

    # Borrowed heavily from pygbutton's logic
    def handleEvent(self, event):
        if event.type not in (MOUSEBUTTONDOWN, MOUSEBUTTONUP):
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
            if event.type == MOUSEBUTTONDOWN:
                self.mouseDown = True
                self.lastMouseDownOverRect = True
        else:
            if event.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP):
                self.lastMouseDownOverRect = False

        # mouse up is handled whether or not it was over the rect
        isClicked = False
        if event.type == MOUSEBUTTONUP:
            if self.lastMouseDownOverRect:
                isClicked = True
            self.lastMouseDownOverRect = False

            if self.mouseDown:
                self.mouseDown = False

        return isClicked

    def update(self, gameDisplay):
        self._rect = self._rect_orig.move(gameDisplay.pixel_offset[0], gameDisplay.pixel_offset[1])

    def draw(self, gameDisplay, COLOR = (0, 128, 0)):
        self.update(gameDisplay)
        pygame.draw.rect(gameDisplay.screen, COLOR, self._rect)
