# Reversi GUI

import random, sys, pygame, time, copy
from pygame.locals import *

FPS = 10 # frames per second to update the screen
WINDOW_X = 1000 # window width
WINDOW_Y = 800 # window height
SQUARE_SIZE = 80 # size of each square in grid
BOARD_X = 8 # number of columns in grid
BOARD_Y = BOARD_X # number of rows in grid
WHITE_DISK = 'WHITE_TILE' # an arbitrary but unique value
BLACK_DISK = 'BLACK_TILE' # an arbitrary but unique value
EMPTY_SPACE = 'EMPTY_SPACE' # an arbitrary but unique value
HINT_DISK = 'HINT_DISK' # an arbitrary but unique value
ANIMATIONSPEED = 25 # integer from 1 to 100, higher is faster animation
XMARGIN = int((WINDOW_X-(BOARD_X*SQUARE_SIZE))/2)
YMARGIN = int((WINDOW_Y-(BOARD_Y*SQUARE_SIZE))/2)

WHITE_COLOUR = (255,255,255)
BLACK_COLOUR = (0,0,0)
GREEN_COLOUR = (0,155,0)
BLUE_COLOUR = (0,0,255)
RED_COLOUR = (255,0,0)

def main():
    
    global MAINCLOCK, DISPLAYSURF, RAVIE_FONT, WINDOW_BG, BRIT_FONT

    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
    pygame.display.set_caption('*** REVERSI ***')
    BRIT_FONT = pygame.font.Font('BRITANIC.ttf', 40)
    RAVIE_FONT = pygame.font.Font('RAVIE.ttf', 50)

    #background image for game board
    board_bg = pygame.image.load('sky.jpg')
    board_bg = pygame.transform.smoothscale(board_bg, (BOARD_X*SQUARE_SIZE, BOARD_Y*SQUARE_SIZE))
    board_bg_rect = board_bg.get_rect()
    board_bg_rect.topleft = (XMARGIN, YMARGIN)
 
    WINDOW_BG = pygame.image.load('matrix1.jpg')
    WINDOW_BG = pygame.transform.smoothscale(WINDOW_BG, (WINDOW_X, WINDOW_Y))
    WINDOW_BG.blit(board_bg, board_bg_rect)

    # Run game    
    while True:
        if runGame() == False:
            break

def runGame():

    # set board to initial conditions
    main_board = get_board()
    init_board(main_board)
    draw_board(main_board)    # draw starting board

    # Make the Surface and Rect objects for the buttons
    newgame_surf = BRIT_FONT.render('New Game', True, WHITE_COLOUR)
    newgame_rect = newgame_surf.get_rect()
    newgame_rect.topright = (WINDOW_X - 8, 10)
    
    about_surf = BRIT_FONT.render('About', True, WHITE_COLOUR)
    about_rect = about_surf.get_rect()
    about_rect.topright = (WINDOW_X - 8, 45)
    
    title_surf = RAVIE_FONT.render('REVERSI', True, RED_COLOUR)
    title_rect= title_surf.get_rect()
    title_rect.topleft = (300, 30)

    # Draw the "New Game" and "Hints" buttons.
    DISPLAYSURF.blit(newgame_surf, newgame_rect)
    DISPLAYSURF.blit(about_surf, about_rect)
    DISPLAYSURF.blit(title_surf, title_rect)

    pygame.display.update()
    
    quit_check()

def get_pixel(x,y):
    return XMARGIN + x*SQUARE_SIZE + int(SQUARE_SIZE/2), YMARGIN + y*SQUARE_SIZE + int(SQUARE_SIZE/2)

def draw_board(board):
    # render board background
    DISPLAYSURF.blit(WINDOW_BG, WINDOW_BG.get_rect())

    # horizontal lines
    for x in range(BOARD_X+1):
        x1 = (x*SQUARE_SIZE) + XMARGIN
        y1 = YMARGIN
        x2 = (x*SQUARE_SIZE) + XMARGIN
        y2 = YMARGIN + (BOARD_Y*SQUARE_SIZE)
        pygame.draw.line(DISPLAYSURF, BLACK_COLOUR, (x1, y1), (x2, y2))
    
    # vertical lines
    for y in range(BOARD_X+1):
        x1 = XMARGIN
        y1 = (y*SQUARE_SIZE) + YMARGIN
        x2 = XMARGIN + (BOARD_X*SQUARE_SIZE)
        y2 = (y*SQUARE_SIZE) + YMARGIN
        pygame.draw.line(DISPLAYSURF, BLACK_COLOUR, (x1, y1), (x2, y2))

    # draw circles
    for x in range(BOARD_X):
        for y in range(BOARD_Y):
            x_center, y_center = get_pixel(x, y)
            if board[x][y] == WHITE_DISK or board[x][y] == BLACK_DISK:
                if board[x][y] == WHITE_DISK:
                    tileColor = WHITE_COLOUR
                else:
                    tileColor = BLACK_COLOUR
                
                pygame.draw.circle(DISPLAYSURF, tileColor, (x_center, y_center), int(SQUARE_SIZE/2)-4)
            

def get_click(mouse_x, mouse_y):
    # Return a tuple of two integers of the board space coordinates where
    # the mouse was clicked. (Or returns None not in any space.)
    for x in range(BOARD_X):
        for y in range(BOARD_Y):
            if mouse_x > (x*SQUARE_SIZE + XMARGIN):
                if mouse_x < ((x+1)*SQUARE_SIZE + XMARGIN):
                    if mouse_y > (y*SQUARE_SIZE + YMARGIN):
                        if mouse_y < ((y+1)*SQUARE_SIZE + YMARGIN):
                            return (x, y)
    return None

def init_board(board):
    ### initializes game board ###
    
    for x in range(BOARD_X):
        for y in range(BOARD_Y):
            board[x][y] = EMPTY_SPACE

    # places the starting pieces    
    board[3][3] = WHITE_DISK
    board[3][4] = BLACK_DISK
    board[4][3] = BLACK_DISK
    board[4][4] = WHITE_DISK

def get_board():
    # Creates a brand new, empty board data structure.
    board = []
    for i in range(BOARD_X):
        board.append([EMPTY_SPACE]*BOARD_Y)
        
    return board

def quit_check():
    for event in pygame.event.get((QUIT, KEYUP)): # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    main()
