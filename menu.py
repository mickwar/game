import pygame
import pygbutton

from field import *

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def quit_game():
    print("quitting")
    pygame.quit()
    quit()

def main_menu():
    w = 640
    h = 480
    b_WIDTH = 150
    b_HEIGHT = 50
    
    gameDisplay = pygame.display.set_mode((w, h))

    b_FONT = pygame.font.SysFont("Arial", 32)
    b_play = pygbutton.PygButton(
        rect = (w * 1/4 - b_WIDTH/2, h * 3/4 - b_HEIGHT/2, b_WIDTH, b_HEIGHT),
        caption = "Play",
        font = b_FONT,
        hotkeys = pygame.K_p)
    b_quit = pygbutton.PygButton(
        rect = (w * 3/4 - b_WIDTH/2, h * 3/4 - b_HEIGHT/2, b_WIDTH, b_HEIGHT),
        caption = "Quit",
        font = b_FONT,
        hotkeys = pygame.K_q)

    intro = True
    while intro:

        gameDisplay.fill((16, 16, 16))
        largeText = pygame.font.SysFont("Arial", 64)
        TextSurf, TextRect = text_objects("a game", largeText)
        TextRect.center = ((w/2), (h/4))
        gameDisplay.blit(TextSurf, TextRect)

        for event in pygame.event.get():
            if [e for e in ['left_click', 'hotkeyup'] if e in b_play.handleEvent(event)]:
                intro = False
            if [e for e in ['left_click', 'hotkeyup'] if e in b_quit.handleEvent(event)]:
                quit_game()
            if event.type == pygame.QUIT:
                quit_game()

        b_play.draw(gameDisplay)
        b_quit.draw(gameDisplay)

        pygame.display.update()


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

