import pygame

clock = pygame.time.Clock()

# Process text
def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

# Returns False or the result of running action()
# Should this be a class?
def button(gameDisplay, msg, x, y, w, h, ic, ac, hotkey = None, action = None):
    # Get mouse position and click status
    mouse = pygame.mouse.get_pos()      # (x, y)
    click = pygame.mouse.get_pressed()  # (LeftClick, MiddleButton, RightClick)
    key = pygame.key.get_pressed()

    # Check if mouse is within the rectangle
    r = False
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        # Check if clicked
        if click[0] == 1 and action != None:
            r = action() 
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    # Or execute on hotkey
    if hotkey is not None and type(hotkey) is str:
        if key[ord(hotkey)] == 1:
            r = action()

    # Place text in center
    smallText = pygame.font.SysFont("Arial", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

    return r
    

# The main menu
def main_menu(display_width = 640, display_height = 480):

    gameDisplay = pygame.display.set_mode((display_width, display_height))

    intro = True
    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                quit_game()

        gameDisplay.fill((16, 16, 16))
        largeText = pygame.font.SysFont("Arial", 32)
        TextSurf, TextRect = text_objects("game", largeText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        # play_game() returns True, so we want to exit main menu
        intro = not button(gameDisplay, "Play", 150, 350, 100, 50, (196,0,0), (255,0,0), "p", play_game)
        button(gameDisplay, "Quit", 350, 350, 100, 50, (196,0,0), (255,0,0), "q", quit_game)

        pygame.display.update()
        clock.tick(30)



# Button actions
def play_game():
    print("play")
    return True

def quit_game():
    print("quitting")
    pygame.quit()
    quit()
