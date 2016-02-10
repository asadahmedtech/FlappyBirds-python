import os
import pygame
import random
import sys


def load_image(img_file_name):
    file_name = os.path.join('.', 'FlappyBirds', 'assets', img_file_name)
    img = pygame.image.load(file_name)
    img.convert()
    return img


pygame.init()  # pygame.init()

# DISPLAY
display_x = 800
display_y = 600
screen = display_x, display_y  ##SCREEN

# GLOBAL INITIATION
gameExit = False
gameOver = False
move = 0
points = 0

# COLORS
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
light_red = (255, 0, 0)
yellow = (200, 200, 0)
light_yellow = (255, 255, 0)
green = (34, 177, 76)
light_green = (0, 255, 0)
blue = (0, 0, 255)

# CONSTANTS
high = 0

# FRAMES
FPS = 30  # FRAME-PER-SECOND
clock = pygame.time.Clock()

# FONTS
smallfont = pygame.font.SysFont("comicsansms", 25)  ##SMALL FONT
medfont = pygame.font.SysFont("comicsansms", 50)  ##MEDIUM FONT
largefont = pygame.font.SysFont("comicsansms", 70)  ##LARGE FONT
y_displace = 0

# IMAGES
bird = pygame.image.load('bird.png')
pipebottom = pygame.image.load('pipebottom.png')
pipe_bottom = pygame.transform.scale(pipebottom, (100, 600))
background = pygame.image.load('background.png')
bg = pygame.transform.scale(background, (display_x, display_y))
icon = pygame.image.load('flappy.ico')

# SETTING UP SCREEN
gameDisplay = pygame.display.set_mode(screen)  ##GAMEDISPLAY
pygame.display.set_caption('FLAPPY BIRDS')
pygame.display.set_icon(icon)

# points
add_points = 1
pipe_x_move = 10
y = 0


def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonx + (buttonwidth / 2)), buttony + (buttonheight / 2))
    gameDisplay.blit(textSurf, textRect)


# BUTTON
def button(text, x, y, width, height, inactive_color, active_color, action=None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()

            if action == "play":
                gameLoop()

            if action == "main":
                game_intro()

    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))

    text_to_button(text, black, x, y, width, height)


# PAUSE MENU
def pause():
    """
    :We are initiating the pause menu whenever KEY P is called during game this menu will be initiated:
    """
    paused = True
    global high
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Paused", black, -100, size="large")
        message_to_screen("HIGH SCORE :" + str(high), black, y_displace=-10, size="small")
        message_to_screen("Press C to countinue or Q to Quit", blue, 80, size="medium")
        pygame.display.update()
        clock.tick(5)


def scores(score):
    """
    :param score: The Score after every pair of pipe is passed
    :return: nothing :
    :screen-blit:
    """
    global high
    if score > high:
        high = score
    else:
        pass
    score = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(score, [0, 0])


def game_intro():
    """
    :return: None
    :For the ONE-TIME Menu:
    """
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Welcome to Flappy Birds", green, -100, "large")
        message_to_screen("The objective of the game is to pass the pipes", black, -30)
        message_to_screen("Press C to play, P to pause or Q to quit.", black, 50)

        button("play", 200, 500, 100, 50, green, light_green, action="play")
        button("quit", 400, 500, 100, 50, red, light_red, action="quit")

        pygame.display.update()
        clock.tick(15)


def text_objects(text, color, size):
    """
    :param text: The TEXT TO BE DISPLAYED
    :param color: COLOR OF THE TEXT
    :param size: SIZE OF THE TEXT
    :return: RETURNING THE TEXT IN A RECTANGULAR FORMAT
    :usage: TO CENTER THE TEXT
    """
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
    """
    :param msg: TEXT TO BE DISPLAYED
    :param color: COLOR OF TEXT
    :param y_displace: DISPLACEMENT OF THE TEXT FROM CENTER OF GAME-DISPLAY
    :param size: SIZE OF TEXT
    :return: NONE
    sreen-blit
    """
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_x / 2), (display_y / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


def bonus_round_aplha(scores):
    global points, FPS, add_points, pipe_x_move, y
    bonus_points = 0
    if scores == 0 or bonus_points > 0:
        FPS = 30
        add_points = 1
        pipe_x_move = 10
        y = 40
    elif scores % 5 == 0:
        message_to_screen("BONUS ROUND", black, 0, "medium")
        message_to_screen("", black, 0, "medium")
        while bonus_points <= 10:
            FPS = 40
            add_points = 2
            pipe_x_move = 10
            bonus_points += 1

def gameLoop():
    """
    THE MAIN LOOP OF THE GAME
    :return: NONE
    """
    ##LOCAL INITIATION
    gameExit = False
    gameOver = False
    gap = 300
    gap_min = 70  ##MIN-DIFFICULTY
    gap_max = 250  ##MAX-DIFFICULTY
    points = 0
    x_moving = display_x
    length_y = 300
    y_bottom = length_y + gap
    bird_x = display_x / 2
    bird_y1 = display_y / 2
    y = -5

    while not gameExit:
        gameDisplay.blit(bg, (0, 0))

        while gameOver:
            gameDisplay.fill(white)
            global high
            message_to_screen("Game over", red, y_displace=-80, size="large")
            message_to_screen("HIGH SCORE :" + str(high), black, y_displace=-10, size="small")

            button("PLAY", 200, 450, 100, 50, green, light_green, action="play")
            button("QUIT", 450, 450, 100, 50, red, light_red, action="quit")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        gameLoop()
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                gameOver = False
            if (event.type == pygame.KEYUP and (
                            event.key == pygame.K_UP or event.key == pygame.K_SPACE)) or event.type == pygame.MOUSEBUTTONDOWN:
                y = 40
                print "IN UP"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause()

        bird_y1 -= y
        pipe_top1 = pygame.transform.scale(pipe_bottom, (100, length_y))
        pipe_top = pygame.transform.rotate(pipe_top1, 180)

        ##pygame.draw.rect(gameDisplay , black , [bird_x,bird_y1,15,15])
        gameDisplay.blit(bird, (bird_x, bird_y1))
        gameDisplay.blit(pipe_bottom, (x_moving, length_y + gap))
        gameDisplay.blit(pipe_top, (x_moving, 0))
        ##pygame.draw.rect(gameDisplay , green , [x_moving ,0,100,length_y])
        ##pygame.draw.rect(gameDisplay , green , [x_moving ,y_bottom,100,display_y-length_y-gap])
        if x_moving <= 0:
            gap = random.randint(gap_min, gap_max)
            length_y = random.randint(100, display_y - gap - 100)
            y_bottom = length_y + gap
            x_moving = display_x

        if bird_y1 >= (display_y - 15):
            gameOver = True
        if bird_x == x_moving - 15 and bird_y1 <= length_y - 15:
            gameOver = True
        if bird_x == x_moving - 15 and bird_y1 >= length_y + gap:
            gameOver = True
        if ((x_moving - 15 < bird_x < x_moving + 100 - 15 and bird_y1 <= length_y - 15) or (
                                x_moving - 15 < bird_x < x_moving + 100 - 15 and bird_y1 >= length_y + gap - 15)):
            gameOver = True
        if x_moving + 100 == bird_x:
            points += add_points
        x_moving -= pipe_x_move

        bonus_round_aplha(points)
        print bird_y1

        scores(points)
        pygame.display.update()

        clock.tick(FPS)
        y = -5

    pygame.quit()
    sys.exit(0)

game_intro()
gameLoop()
