import pygame
from pygame.locals import *

class clickTest():
    def __init__(self, rect):
        self._rect = pygame.Rect(rect)
        self.mouseDown = False
        self.mouseOverRect = False
        self.lastMouseDownOverRect = False

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

    def draw(self, gameDisplay, COLOR = (0, 128, 0)):
        pygame.draw.rect(gameDisplay, COLOR, self._rect)
