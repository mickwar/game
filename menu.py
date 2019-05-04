import pygame
import pygbutton

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

