#########################################
# Rush Hour                             #
#                                       #
# Created: June 2020                    #
# Author: James Wu                      #
#                                       #
# Images snipped from thinkfun website  #
#                                       #
#########################################
#                                       #
# Requirements:                         #
# Python 3.8.3, Pygame 1.9.6            #
#                                       #
#########################################

import pygame
import sys

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Initialisation
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rush Hour")
clock = pygame.time.Clock()

# Font constants
pygame.font.init()
COMIC_FONT_BIG = pygame.font.SysFont("Comic Sans MS", 60)
COMIC_FONT_MEDIUM = pygame.font.SysFont("Comic Sans MS", 40)
COMIC_FONT_SMALL = pygame.font.SysFont("Comic Sans MS", 20)

# Colour constants
PALE_RED = (255, 102, 102)
YELLOW = (240, 230, 140)
GREEN = (152, 251, 152)
BLUE = (32, 178, 178)
WHITE = (255, 255, 255)
BROWN = (160, 82, 45)
GREY = (175, 175, 175)
DARK_GREY = (145, 145, 145)
HONEYDEW = (240, 250, 240)

# images
home = pygame.image.load("home.png")
home = pygame.transform.scale(home, (40, 40))
lock = pygame.image.load("lock.png")
lock = pygame.transform.scale(lock, (60, 60))

hor2 = pygame.image.load("hor2.png")
hor3 = pygame.image.load("hor3.png")
ver2 = pygame.image.load("ver2.png")
ver3 = pygame.image.load("ver3.png")
red = pygame.image.load("red.png")
hor2 = pygame.transform.scale(hor2, (140, 70))
hor3 = pygame.transform.scale(hor3, (210, 70))
ver2 = pygame.transform.scale(ver2, (70, 140))
ver3 = pygame.transform.scale(ver3, (70, 210))
red = pygame.transform.scale(red, (140, 70))

# Responsible for screen movement, changes the variable state
class Mouse:

    # finds out which level is selected based on button press
    def return_level():
        x, y = pygame.mouse.get_pos()
        if x >= 175 and x <= 245 and y >= 150 and y <= 220:
            return 1
        elif x >= 285 and x <= 355 and y >= 150 and y <= 220:
            return 2
        elif x >= 395 and x <= 465 and y >= 150 and y <= 220:
            return 3
        elif x >= 175 and x <= 245 and y >= 260 and y <= 330:
            return 4
        elif x >= 285 and x <= 355 and y >= 260 and y <= 330:
            return 5
        elif x >= 395 and x <= 465 and y >= 260 and y <= 330:
            return 6
        elif x >= 175 and x <= 245 and y >= 370 and y <= 440:
            return 7
        elif x >= 285 and x <= 355 and y >= 370 and y <= 440:
            return 8
        elif x >= 395 and x <= 465 and y >= 370 and y <= 440:
            return 9
        else:
            return 10

    # adds functions to the home screen
    def home_screen():
        global state
        x, y = pygame.mouse.get_pos()
        if x >= 140 and x <= 500 and y >= 220 and y <= 270:
            state = "MENU"
        elif x >= 140 and x <= 500 and y >= 340 and y <= 410:
            state = "HOW TO"

    # adds functions to the menu or level select screen
    def menu_screen():
        global state, playing_level, current_level
        f = open("current_level.txt", "r")
        current_level = int(f.read())
        f.close()

        x, y = pygame.mouse.get_pos()
        if x >= 20 and x <= 60 and y >= 20 and y <= 60:
            state = "HOME"
        elif Mouse.return_level() <= current_level:
            state = "IN GAME"
            playing_level = Mouse.return_level()
            Board.start()

    # adds functions to the in game screen
    def in_game_screen():
        global state
        x, y = pygame.mouse.get_pos()
        if x >= 20 and x <= 60 and y >= 20 and y <= 60:
            state = "HOME"
        elif x >= 30 and x <= 130 and y >= 160 and y <= 200:
            state = "MENU"
        elif x >= 30 and x <= 130 and y >= 240 and y <= 280:
            Board.start()
        elif x >= 170 and x <= 590 and y >= 30 and y <= 450:
            Mouse.select_piece()

    # adds functions to the how to screen
    def how_to_screen():
        global state
        x, y = pygame.mouse.get_pos()
        if x >= 20 and x <= 60 and y >= 20 and y <= 60:
            state = "HOME"
        elif x >= 150 and x <= 490 and y >= 340 and y <= 410:
            state = "MENU"
    
    # adds functions to the win screen
    def win_screen():
        global state, playing_level , current_level
        x, y = pygame.mouse.get_pos()
        if x >= 20 and x <= 60 and y >= 20 and y <= 60:
            state = "HOME"
        elif x >= 240 and x <= 400 and y >= 210 and y <= 270:
            playing_level += 1
            Board.start()
            state = "IN GAME"
            if playing_level >= current_level:
                f1 = open("current_level.txt", "w")
                f1.write(str(playing_level))
                f1.close()

        elif x >= 240 and x <= 400 and y >= 295 and y <= 355:
            state = "MENU"

    # identifies the piece and its information
    def select_piece():
        global piece, offset, select_x, select_y, select
        if Board.identify() != False:
            select = True
            piece, offset, select_x, select_y = Board.identify()

    # allows movement of the piece
    def move():
        global select_x, select_y, current_level, state
        if select == True:
            if Board.mouse_pos() != False:
                x, y = Board.mouse_pos()
                # sets rules for moving vehicles
                if piece == "v":
                    if y - select_y == 1:
                        if y-offset+1 < 6:
                            if squares[y-offset+1][select_x] == ".":
                                game_state[y-offset][select_x] = piece
                                game_state[select_y-offset][select_x] = '.'
                                select_y = y
                    elif y - select_y == -1:
                        if y-offset >= 0:
                            if squares[y-offset][select_x] == ".":
                                game_state[y-offset][select_x] = piece
                                game_state[select_y-offset][select_x] = '.'
                                select_y = y
                elif piece == "V":
                    if y - select_y == 1:
                        if y-offset+2 < 6:
                            if squares[y-offset+2][select_x] == ".":
                                game_state[y-offset][select_x] = piece
                                game_state[select_y-offset][select_x] = '.'
                                select_y = y
                    elif y - select_y == -1:
                        if y-offset >= 0:
                            if squares[y-offset][select_x] == ".":
                                game_state[y-offset][select_x] = piece
                                game_state[select_y-offset][select_x] = '.'
                                select_y = y
                elif piece == "h":
                    if x - select_x == 1:
                        if x-offset+1 < 6:
                            if squares[select_y][x-offset+1] == ".":
                                game_state[select_y][x-offset] = piece
                                game_state[select_y][select_x - offset] = '.'
                                select_x = x
                    elif x - select_x == -1:
                        if x-offset >= 0:
                            if squares[select_y][x-offset] == ".":
                                game_state[select_y][x-offset] = piece
                                game_state[select_y][select_x - offset] = '.'
                                select_x = x
                elif piece == "H":
                    if x - select_x == 1:
                        if x-offset+2 < 6:
                            if squares[select_y][x-offset+2] == ".":
                                game_state[select_y][x-offset] = piece
                                game_state[select_y][select_x - offset] = '.'
                                select_x = x
                    elif x - select_x == -1:
                        if x-offset >= 0:
                            if squares[select_y][x-offset] == ".":
                                game_state[select_y][x-offset] = piece
                                game_state[select_y][select_x - offset] = '.'
                                select_x = x
                elif piece == "r":
                    if x - select_x == 1:
                        if x-offset+1 < 6:
                            if squares[select_y][x-offset+1] == ".":
                                game_state[select_y][x-offset] = piece
                                game_state[select_y][select_x - offset] = '.'
                                select_x = x
                        elif x-offset+2 >= 6:
                            game_state[select_y][select_x] = "."
                            if current_level == playing_level:
                                f1 = open("current_level.txt", "w")
                                f1.write(str(current_level + 1))
                                f1.close()
                            state = "WIN"
                            screen.blit(red, (520, 170))
                    elif x - select_x == -1:
                        if x-offset >= 0:
                            if squares[select_y][x-offset] == ".":
                                game_state[select_y][x-offset] = piece
                                game_state[select_y][select_x - offset] = '.'
                                select_x = x

    # generalises all screens so the game loop only needs to call one function
    def general():
        if state == "HOME":
            Mouse.home_screen()
        elif state == "MENU":
            Mouse.menu_screen()
        elif state == "IN GAME":
            Mouse.in_game_screen()
        elif state == "HOW TO":
            Mouse.how_to_screen()
        elif state == "WIN":
            Mouse.win_screen()

# Responsible for displaying screens based on the state
class Screen:

    # Sets the layout of the home screen
    def home_screen():
        screen.fill(BLUE)
        title = COMIC_FONT_BIG.render("Rush Hour", False, BROWN)
        screen.blit(title, (180, 80))
        pygame.draw.rect(screen, GREEN, (140, 220, 360, 70))
        pygame.draw.rect(screen, GREEN, (140, 340, 360, 70))

        start = COMIC_FONT_MEDIUM.render("START", False, BROWN)
        how_to = COMIC_FONT_MEDIUM.render("How to play", False, BROWN)

        screen.blit(start, (255, 230))
        screen.blit(how_to, (220, 345))
    
    # Sets the layout of the menu or level select screen
    def menu_screen():
        screen.fill(GREEN)
        level_select = COMIC_FONT_MEDIUM.render("Level Select", False, BROWN)
        screen.blit(level_select, (210, 60))

        f = open("current_level.txt", "r")
        current_level = int(f.read())
        f.close()

        for i in range(9):
            pygame.draw.rect(screen, PALE_RED, (175 + (i%3 * 110), 150 + (i//3) * 110, 70, 70))
            screen.blit(lock, (180 + (i%3 * 110), 155 + (i//3) * 110))
        
        for j in range(current_level):
            pygame.draw.rect(screen, YELLOW, (175 + (j%3 * 110), 150 + (j//3) * 110, 70, 70))

        for k in range(current_level):
            level_number = COMIC_FONT_MEDIUM.render(str(k + 1), False, BROWN)
            screen.blit(level_number, (200 + (k%3 * 110), 155 + (k//3) * 110))
        
        # home button
        screen.blit(home, (20, 20))

    # Sets the layout of the in game screen
    def in_game_screen():
        screen.fill(YELLOW)
        # home button
        screen.blit(home, (20, 20))
        # game board
        Board.draw_on_screen()
        # back button
        pygame.draw.rect(screen, HONEYDEW, (30, 160, 100, 40))
        back_text = COMIC_FONT_SMALL.render("Back", False, BROWN)
        screen.blit(back_text, (40, 160))
        # restart button
        pygame.draw.rect(screen, HONEYDEW, (30, 240, 100, 40))
        restart_text = COMIC_FONT_SMALL.render("Restart", False, BROWN)
        screen.blit(restart_text, (40, 240))

        level_text = COMIC_FONT_MEDIUM.render("Level " + str(playing_level), False, BROWN)
        screen.blit(level_text, (20, 70))

    # Sets the layout of the how to play screen
    def how_to_screen():
        screen.fill(PALE_RED)
        title = COMIC_FONT_MEDIUM.render("HOW TO PLAY", False, BROWN)
        line1 = COMIC_FONT_SMALL.render("Slide the blocking cars and trucks in their lanes - up and down,", False, WHITE)
        line2 = COMIC_FONT_SMALL.render("left and right - until the path is clear for the red car to", False, WHITE)
        line3 = COMIC_FONT_SMALL.render("escape. Vehicles can only slide forwards & backwards.", False, WHITE)
        screen.blit(title, (180, 40))
        screen.blit(line1, (35, 120))
        screen.blit(line2, (60, 180))
        screen.blit(line3, (75, 240))

        # home button
        screen.blit(home, (20, 20))
        # start button
        pygame.draw.rect(screen, GREEN, (150, 340, 340, 70))
        start = COMIC_FONT_MEDIUM.render("Start", False, BLUE)
        screen.blit(start, (265, 344))

    # Sets the layout of the level complete screen
    def win_screen():
        pygame.draw.rect(screen, BLUE, (95, 95, 450, 290))
        pygame.draw.rect(screen, HONEYDEW, (100, 100, 440, 280))
        # next level button
        pygame.draw.rect(screen, GREEN, (240, 210, 160, 60))
        # levels button
        pygame.draw.rect(screen, GREEN, (240, 295, 160, 60))

        level_complete = COMIC_FONT_MEDIUM.render("Level Complete!", False, BROWN)
        screen.blit(level_complete, (185, 120))
        next_level = COMIC_FONT_SMALL.render("Next Level", False, BLUE)
        screen.blit(next_level, (270, 225))
        levels = COMIC_FONT_SMALL.render("Levels", False, BLUE)
        screen.blit(levels, (290, 310))

    # Generalises all screens so the main game loop only needs to call one function
    def display_screen():
        if state == "HOME":
            Screen.home_screen()
        elif state == "MENU":
            Screen.menu_screen()
        elif state == "IN GAME":
            Screen.in_game_screen()
        elif state == "HOW TO":
            Screen.how_to_screen()
        elif state == "WIN":
            Screen.win_screen()

# Responsible for the whole game
class Board:

    # Starts, restarts and generates levels
    def start():
        global game_state
        if playing_level == 1:    
            level1 = []
            one = open("level1.txt", "r")
            for l in one:
                line = list(l.strip())
                level1.append(line)
            game_state = level1

        elif playing_level == 2:
            level2 = []
            two = open("level2.txt", "r")
            for l in two:
                line = list(l.strip())
                level2.append(line)
            game_state = level2

        elif playing_level == 3:
            level3 = []
            three = open("level3.txt", "r")
            for l in three:
                line = list(l.strip())
                level3.append(line)
            game_state = level3

        elif playing_level == 4:
            level4 = []
            four = open("level4.txt", "r")
            for l in four:
                line = list(l.strip())
                level4.append(line)
            game_state = level4

        elif playing_level == 5:
            level5 = []
            five = open("level5.txt", "r")
            for l in five:
                line = list(l.strip())
                level5.append(line)
            game_state = level5

        elif playing_level == 6:
            level6 = []
            six = open("level6.txt", "r")
            for l in six:
                line = list(l.strip())
                level6.append(line)
            game_state = level6

        elif playing_level == 7:
            level7 = []
            seven = open("level7.txt", "r")
            for l in seven:
                line = list(l.strip())
                level7.append(line)
            game_state = level7

        elif playing_level == 8:
            level8 = []
            eight = open("level8.txt", "r")
            for l in eight:
                line = list(l.strip())
                level8.append(line)
            game_state = level8

        elif playing_level == 9:
            level9 = []
            nine = open("level9.txt", "r")
            for l in nine:
                line = list(l.strip())
                level9.append(line)
            game_state = level9

    # for seeing which squares are occupied with parts of which vehicle
    def occupied_squares():
        global squares
        squares = [
            ['.','.','.','.','.','.'],
            ['.','.','.','.','.','.'],
            ['.','.','.','.','.','.'],
            ['.','.','.','.','.','.'],
            ['.','.','.','.','.','.'],
            ['.','.','.','.','.','.']
        ]
        for y in range(6):
            for x in range(6):
                if game_state[y][x] == "v":
                    squares[y][x] = "v"
                    squares[y+1][x] = "v"
                elif game_state[y][x] == "V":
                    squares[y][x] = "V"
                    squares[y+1][x] = "V"
                    squares[y+2][x] = "V"
                elif game_state[y][x] == "h":
                    squares[y][x] = "h"
                    squares[y][x+1] = "h"
                elif game_state[y][x] == "H":
                    squares[y][x] = "H"
                    squares[y][x+1] = "H"
                    squares[y][x+2] = "H"
                elif game_state[y][x] == "r":
                    squares[y][x] = "r"
                    squares[y][x+1] = "r"
        return squares

    # returns an x y coordinate on the board
    def mouse_pos():
        x, y = pygame.mouse.get_pos()
        if x >= 170 and x <= 590 and y >= 30 and y <= 450:
            x -= 170
            y -= 30
            return x//70, y//70
        else:
            return False

    # function on locating piece selected and position
    def identify():
        x, y = Board.mouse_pos()
        if squares[y][x] == "v":
            if game_state[y][x] == "v":
                return "v", 0, x, y
            else:
                return "v", 1, x, y

        elif squares[y][x] == "V":
            if game_state[y][x] == "V":
                return "V", 0, x, y
            elif game_state[y-1][x] == "V":
                return "V", 1, x, y
            else:
                return "V", 2, x, y
        elif squares[y][x] == "h":
            if game_state[y][x] == "h":
                return "h", 0, x, y
            else:
                return "h", 1, x, y
        elif squares[y][x] == "H":
            if game_state[y][x] == "H":
                return "H", 0, x, y
            elif game_state[y][x-1] == "H":
                return "H", 1, x, y
            else:
                return "H", 2, x, y
        elif squares[y][x] == "r":
            if game_state[y][x] == "r":
                return "r", 0, x, y
            else:
                return "r", 1, x, y
        else:
            return False

    # Draws the board on a part of the IN GAME screen
    def draw_on_screen():
        # Structure
        pygame.draw.rect(screen, BROWN, (165, 25, 430, 430))
        pygame.draw.rect(screen, GREY, (170, 30, 420, 420))
        for i in range(36):
            pygame.draw.rect(screen, DARK_GREY, (190 + (i%6)*70, 50 + (i//6)*70, 30, 30))
        pygame.draw.line(screen, YELLOW, (592, 167), (592, 237), 5)
        # Cars
        Board.occupied_squares()
        for y in range(6):
            for x in range(6):
                if game_state[y][x] == "v":
                    screen.blit(ver2, (170 + x*70, 30 + y*70))
                elif game_state[y][x] == "V":
                    screen.blit(ver3, (170 + x*70, 30 + y*70))
                elif game_state[y][x] == "h":
                    screen.blit(hor2, (170 + x*70, 30 + y*70))
                elif game_state[y][x] == "H":
                    screen.blit(hor3, (170 + x*70, 30 + y*70))
                elif game_state[y][x] == "r":
                    screen.blit(red, (170 + x*70, 30 + y*70))


# Assigning game variables
state = "HOME"

f = open("current_level.txt", "r")
current_level = int(f.read())
f.close()

playing_level = 1

select = False

game_state = []
squares = []

piece = 0
offset = 0
select_x = 0
select_y = 0

# Main game loop
while True:
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            Mouse.general()
        if event.type == pygame.MOUSEBUTTONUP:
            select = False
    Mouse.move()
    Screen.display_screen()
    pygame.display.update()