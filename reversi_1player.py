# Reversi GUI

import random, sys, pygame, time, copy, reversi_engine, numpy
from textrect import render_textrect
from pygame.locals import *

FPS = 10 # frames per second to update the screen
WINDOW_X = 780 # window width
WINDOW_Y = 600 # window height
SQUARE_SIZE = 60 # size of each square in grid
BOARD_X = 8 # number of columns in grid
BOARD_Y = BOARD_X # number of rows in grid

XMARGIN = int((WINDOW_X-(BOARD_X*SQUARE_SIZE))/2)
YMARGIN = int((WINDOW_Y-(BOARD_Y*SQUARE_SIZE))/2)

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,155,0)
BLUE = (0,0,255)
RED = (255,0,0)
YELLOW = (255, 255, 0)
PINK = (255, 62, 150)
ORANGE = (255, 127, 0)
DARKRED = (139, 0, 0)
PURPLE = (142, 56, 142)

def main():
    
    global MAINCLOCK, DISPLAYSURF, RAVIE_FONT, WINDOW_BG, BRIT_FONT, CHOOSE_BG 
    global SNAP_FONT, START_BG, START_BG_RECT, OVER_BG, OVER_BG_RECT
    global BRIT_FONT_BIG, SAD, SAD_RECT, TROPHY, TROPHY_RECT, ABOUT_BG
    global ABOUT_RECT, ABOUT_CLOSE, ABOUT_CLOSE_RECT, RULES_RECT, RULES_SURF
    global YOUR_TURN, YOUR_TURN_RECT, OPP_TURN, OPP_TURN_RECT
    pygame.init()
    
    DISPLAYSURF = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
    pygame.display.set_caption('*** REVERSI ***')
    BRIT_FONT = pygame.font.Font('BRITANIC.ttf', 28)
    RAVIE_FONT = pygame.font.Font('RAVIE.ttf', 35)
    SNAP_FONT = pygame.font.Font('SNAP.ttf', 50)
    CLOSE_FONT = pygame.font.SysFont('tahoma', 16, True)
    BRIT_FONT_BIG = pygame.font.Font('BRITANIC.ttf', 85)

    START_BG = pygame.image.load('sky2.jpg')
    START_BG = pygame.transform.smoothscale(START_BG, (WINDOW_X, WINDOW_Y))
    START_BG_RECT = START_BG.get_rect()
    START_BG.blit(START_BG, START_BG_RECT)
    
    #background image for game board
    board_bg = pygame.image.load('sky.jpg')
    board_bg = pygame.transform.smoothscale(board_bg, (BOARD_X*SQUARE_SIZE, BOARD_Y*SQUARE_SIZE))
    board_bg_rect = board_bg.get_rect()
    board_bg_rect.topleft = (XMARGIN, YMARGIN)
 
    WINDOW_BG = pygame.image.load('aurora2.jpg')
    WINDOW_BG = pygame.transform.smoothscale(WINDOW_BG, (WINDOW_X, WINDOW_Y))
    WINDOW_BG.blit(board_bg, board_bg_rect)
    
    OVER_BG = pygame.image.load('sunset_faded.jpg')
    OVER_BG = pygame.transform.smoothscale(OVER_BG, (WINDOW_X, WINDOW_Y))
    OVER_BG_RECT = OVER_BG.get_rect()
    OVER_BG.blit(OVER_BG, OVER_BG_RECT)
    
    SAD = pygame.image.load('sad_lost_small.jpg')
    SAD_RECT = SAD.get_rect()
    SAD.blit(SAD, SAD_RECT)
    
    TROPHY = pygame.image.load('winner_small.jpg')
    TROPHY_RECT = TROPHY.get_rect()
    TROPHY.blit(TROPHY, TROPHY_RECT)    
    
    game_rules_txt = ""
    input_file = open("reversi_rules.txt", 'rU')
    for line in input_file:
        game_rules_txt += line
    
    RULES_FONT = pygame.font.SysFont('tahoma', 12, False)
    RULES_RECT = pygame.Rect((40, 40, 400, 450))
    RULES_RECT.center = (WINDOW_X/2, WINDOW_Y/2)
        
    RULES_SURF = render_textrect(game_rules_txt, RULES_FONT, RULES_RECT, BLACK, WHITE)
    RULES_SURF.set_alpha(200)
    
    ABOUT_CLOSE = CLOSE_FONT.render("Close", True, BLACK)
    ABOUT_CLOSE_RECT = ABOUT_CLOSE.get_rect()
    ABOUT_CLOSE_RECT.center = (WINDOW_X/2, 508)
    
    YOUR_TURN = BRIT_FONT.render("Your turn", True, WHITE)
    YOUR_TURN_RECT = YOUR_TURN.get_rect()
    YOUR_TURN_RECT.center= (WINDOW_X/2, WINDOW_Y - YMARGIN/2)
        
    OPP_TURN = BRIT_FONT.render("Opponent's turn", True, WHITE)
    OPP_TURN_RECT = OPP_TURN.get_rect()
    OPP_TURN_RECT.center= (WINDOW_X/2, WINDOW_Y - YMARGIN/2)
    
    #ABOUT_BG = pygame.image.load('aurora3.jpg')
    #ABOUT_BG = pygame.transform.smoothscale(ABOUT_BG, (WINDOW_X, WINDOW_Y))
    #ABOUT_RECT = ABOUT_BG.get_rect()
    #ABOUT_BG.blit(ABOUT_BG, ABOUT_RECT)
   # run game    
    while True:
        if reversi_run() == False:
            break

def reversi_run():    
    
    board = blank_board()
    board = init_board(board)
    player_colour, comp_colour = choose_colour() 
    pygame.display.flip()     
    draw_board(board)
    about_open = False
     
    
    print 'colour chosen = ', player_colour
                
    pygame.display.update()
    
    #player 1 defaults to human player, player 2 defaults to computer
    if player_colour == 1:
        turn = 'computer'
    else:
        turn = 'player'
        
    print turn  
    
    player_engine = reversi_engine.ReversiEngine(numpy.array(board), comp_colour) 
    
    while True:
        
        if turn == 'player':  
     
            if no_more_valid_moves(board, player_colour) and not no_more_valid_moves(board, comp_colour):
                print 'player has no valid moves'
                turn = 'computer'
                        
            else:                 
                game_move = None
                while game_move == None:
                    valid_moves = get_valid_moves(board, player_colour)
                    quit_check()
                    for event in pygame.event.get(): # event handling loop
                        if event.type == MOUSEBUTTONUP:
                            mouse_x, mouse_y = event.pos
                            if ABOUT_RECT.collidepoint((mouse_x, mouse_y)):
                                #pygame.display.flip()
                                #display_rules()
                                #break
                                about_open = True
                                print 'This is a game of Reversi.  Good luck!'
                                
                            elif NEWGAME_RECT.collidepoint((mouse_x, mouse_y)):   
                                print 'new game'
                                return True                         
                                break                          
                                pygame.display.update()                        
                                return True                            
                            elif EXIT_RECT.collidepoint((mouse_x, mouse_y)):
                                pygame.quit()
                                sys.exit()
                                return False
                            if about_open and ABOUT_CLOSE_RECT.collidepoint((mouse_x, mouse_y)):
                                about_open = False
                            game_move = get_index_from_coords(mouse_x, mouse_y)  
                            print game_move 
                                                       
                            if game_move in valid_moves:
                                flipx, flipy = game_move
                                to_flip = get_flipped_discs(board, player_colour, flipx, flipy)
                                #print flipx, flipy
                                #print to_flip
                                
                                for x,y in to_flip:
                                    board[x][y] = player_colour
                                    board[flipx][flipy]= player_colour
                                
                            else:
                                if game_move != None:
                                    game_move = None                                                                
                        
                        draw_board(board)
                        display_about(about_open) 
                        score = get_my_score(board, player_colour)
                        #print score
                        display_score(score)
                        display_whose_turn(board, turn, player_colour)
                        pygame.display.update()                   
    
                turn = 'computer'
                       
        elif turn == 'computer':            
            print 'computer plays'
            draw_board(board)
            display_whose_turn(board, turn, player_colour)            
            pygame.display.update()
                
            if no_more_valid_moves(board, comp_colour) and not no_more_valid_moves(board, player_colour):
                print 'computer has no valid moves'
                turn = 'player'   
            elif not no_more_valid_moves(board, comp_colour):                                
            
            #### Don't ask the AI to move when there's no legal moves ###
            # AI doing his stuff...
                print numpy.array(board)  
                np_board = numpy.array(board) # Turns the board into a numpy 2-d board
                selected_ai_move = player_engine.best(np_board) # Receives the output of the engine
                flipx, flipy = selected_ai_move 
                # flipx and flipy are the two coordinates selected by the engine
                
                to_flip = get_flipped_discs(board, comp_colour, flipx, flipy)
                for x,y in to_flip:
                    board[x][y] = comp_colour
                    board[flipx][flipy] = comp_colour
                
                #print board
                draw_board(board)
                turn = 'player'
                pygame.time.delay(1000)
                score = get_my_score(board, player_colour)
                #print score
                display_score(score)
                
                pygame.display.update()
                
         
        if no_more_valid_moves(board, comp_colour) and no_more_valid_moves(board, player_colour):
            # 'Game Over' screen  
            display_game_over(score)
            pygame.display.update()
            while True:
            # Process events until the user clicks on Yes or No.
                quit_check()
                for event in pygame.event.get(): # event handling loop
                    if event.type == MOUSEBUTTONUP:
                        mouse_x, mouse_y = event.pos
                        if YES_RECT.collidepoint( (mouse_x, mouse_y) ):
                            pygame.display.flip()
                            return True
                        elif NO_RECT.collidepoint( (mouse_x, mouse_y) ):
                            return False
        score = get_my_score(board, player_colour)
        #print score
        display_score(score)
        pygame.display.update()

def display_whose_turn(board, turn, player_colour):
    if turn == 'player' and get_valid_moves(board, player_colour):
        DISPLAYSURF.blit(YOUR_TURN, YOUR_TURN_RECT)
        print "your turn"
    else:
        DISPLAYSURF.blit(OPP_TURN, OPP_TURN_RECT)
        print "their turn"
               
def display_game_over(score):
    
    global YES_RECT, NO_RECT
        
    DISPLAYSURF.blit(OVER_BG, OVER_BG_RECT)
    
    if (score[0] > score [1]):
        #player wins
        TROPHY_RECT.center=(int(WINDOW_X/2), 250)
        DISPLAYSURF.blit(TROPHY, TROPHY_RECT)
        
    else:
        # player loses        
        SAD_RECT.center=(int(WINDOW_X/2), 250)
        DISPLAYSURF.blit(SAD, SAD_RECT)
   
    text_surf = BRIT_FONT_BIG.render("GAME OVER!", True, PURPLE)
    text_rect = text_surf.get_rect()
    text_rect.center = (int(WINDOW_X/2), 50)
    
    score_surf = BRIT_FONT.render(" %s -- %s  " % (str(score[0]), str(score[1])), True, BLACK)
    score_rect = score_surf.get_rect()
    score_rect.center = (int(WINDOW_X/2), 400)

    text2_surf = BRIT_FONT.render('What do you want to do?', True, BLACK)
    text2_rect = text2_surf.get_rect()
    text2_rect.center = (int(WINDOW_X/2), 450)

    yes_surf = BRIT_FONT.render('Play again!', True, RED)
    YES_RECT = yes_surf.get_rect()
    YES_RECT.center = (int(WINDOW_X/2) - 100, 500)

    # Make "No" button.
    no_surf = BRIT_FONT.render('Exit', True, BLUE)
    NO_RECT = no_surf.get_rect()
    NO_RECT.center = (int(WINDOW_X/2) + 100, 500)
    
    DISPLAYSURF.blit(text_surf, text_rect)
    DISPLAYSURF.blit(text2_surf, text2_rect)
    DISPLAYSURF.blit(yes_surf, YES_RECT)
    DISPLAYSURF.blit(no_surf, NO_RECT)  
    DISPLAYSURF.blit(score_surf, score_rect)
    
def display_score(score):
    
    score1 = str(score[0])
    score2 = str(score[1])
   
    score1_surf = SNAP_FONT.render(score1, True, RED)
    score1_rect = score1_surf.get_rect()
    score1_rect.center = (60, 300)
    
    score2_surf = SNAP_FONT.render(score2, True, RED)
    score2_rect = score2_surf.get_rect()
    score2_rect.center = (WINDOW_X-60, 300)
    
    DISPLAYSURF.blit(score1_surf, score1_rect)
    DISPLAYSURF.blit(score2_surf, score2_rect)

def display_about(about_open):
    if about_open:
        DISPLAYSURF.blit(RULES_SURF, RULES_RECT)
        DISPLAYSURF.blit(ABOUT_CLOSE, ABOUT_CLOSE_RECT)           

def display_buttons(): 
    
    global NEWGAME_RECT, ABOUT_RECT, TITLE_RECT, PLAYER1_RECT, PLAYER2_RECT, EXIT_RECT
 
    # make objects for buttons
    newgame_surf = BRIT_FONT.render('New Game', True, WHITE)
    NEWGAME_RECT = newgame_surf.get_rect()
    NEWGAME_RECT.topright = (WINDOW_X - 8, 10)
    
    about_surf = BRIT_FONT.render('About', True, WHITE)
    ABOUT_RECT = about_surf.get_rect()
    ABOUT_RECT.topright = (WINDOW_X - 20, 50)
    
    title_surf = RAVIE_FONT.render('REVERSI', True, YELLOW)
    TITLE_RECT= title_surf.get_rect()
    TITLE_RECT.center= (WINDOW_X/2, 40)
       
    player1_surf = BRIT_FONT.render('You', True, ORANGE)
    PLAYER1_RECT = player1_surf.get_rect()
    #PLAYER1_RECT.topleft = (15, 200)
    PLAYER1_RECT.topleft = (XMARGIN/2-BRIT_FONT.size('You')[0]/2, 200)
       
    player2_surf = BRIT_FONT.render('Opponent', True, ORANGE)
    PLAYER2_RECT = player2_surf.get_rect()
    #PLAYER2_RECT.topright = (WINDOW_X-15, 200)
    PLAYER2_RECT.topleft = (WINDOW_X-XMARGIN/2-BRIT_FONT.size('Opponent')[0]/2, 200)
       
    colour1_surf = BRIT_FONT.render(PLAYER1_COLOUR, True, COLOUR1, COLOUR2)
    colour1_rect = colour1_surf.get_rect()
    #colour1_rect.topleft = (25, 240)
    colour1_rect.topleft = (XMARGIN/2-BRIT_FONT.size(PLAYER1_COLOUR)[0]/2, 240)
       
    colour2_surf = BRIT_FONT.render(PLAYER2_COLOUR, True, COLOUR2, COLOUR1)
    colour2_rect = colour2_surf.get_rect()
    #colour2_rect.topright = (WINDOW_X-25, 240)
    colour2_rect.topleft = (WINDOW_X-XMARGIN/2-BRIT_FONT.size(PLAYER2_COLOUR)[0]/2, 240)
       
    exit_surf = BRIT_FONT.render('EXIT', True, WHITE)
    EXIT_RECT = exit_surf.get_rect()
    EXIT_RECT.topright = WINDOW_X-20, WINDOW_Y-50
    
    # put buttons on board
    DISPLAYSURF.blit(newgame_surf, NEWGAME_RECT)
    DISPLAYSURF.blit(about_surf, ABOUT_RECT)
    DISPLAYSURF.blit(title_surf, TITLE_RECT)
    DISPLAYSURF.blit(player1_surf, PLAYER1_RECT)
    DISPLAYSURF.blit(player2_surf, PLAYER2_RECT)
    DISPLAYSURF.blit(exit_surf, EXIT_RECT)
    DISPLAYSURF.blit(colour1_surf, colour1_rect)
    DISPLAYSURF.blit(colour2_surf, colour2_rect)

def get_pixel(x,y):
    
    return XMARGIN + x*SQUARE_SIZE + int(SQUARE_SIZE/2), YMARGIN + y*SQUARE_SIZE + int(SQUARE_SIZE/2)

def init_board(board):
    ### initializes game board ###
    
    for x in range(BOARD_X):
        for y in range(BOARD_Y):
            board[x][y] = 0

    # places the starting pieces    
    board[3][3] = 1
    board[3][4] = 2
    board[4][3] = 2
    board[4][4] = 1
    
    return board

def blank_board():
    # returns a blank board
    board = [[0 for x in range(8)] for y in range(8)]        
        
    return board

def draw_board(board):
       
    # render board background
    DISPLAYSURF.blit(WINDOW_BG, WINDOW_BG.get_rect())

    # horizontal lines
    for x in range(BOARD_X+1):
        x1 = (x*SQUARE_SIZE) + XMARGIN
        y1 = YMARGIN
        x2 = (x*SQUARE_SIZE) + XMARGIN
        y2 = YMARGIN + (BOARD_Y*SQUARE_SIZE)
        pygame.draw.line(DISPLAYSURF, BLACK, (x1, y1), (x2, y2))
    
    # vertical lines
    for y in range(BOARD_X+1):
        x1 = XMARGIN
        y1 = (y*SQUARE_SIZE) + YMARGIN
        x2 = XMARGIN + (BOARD_X*SQUARE_SIZE)
        y2 = (y*SQUARE_SIZE) + YMARGIN
        pygame.draw.line(DISPLAYSURF, BLACK, (x1, y1), (x2, y2))

    # draw circles
    for x in range(BOARD_X):
        for y in range(BOARD_Y):
            x_center, y_center = get_pixel(x, y)
            if board[x][y] == 1 or board[x][y] == 2:
                if board[x][y] == 1:
                    tile_colour= WHITE
                else:
                    tile_colour = BLACK
                
                pygame.draw.circle(DISPLAYSURF, tile_colour, (x_center, y_center), int(SQUARE_SIZE/2)-4)
                
    display_buttons()  
               
def choose_colour():  
    
    global PLAYER1_COLOUR, PLAYER2_COLOUR, COLOUR1, COLOUR2

    title_surf = RAVIE_FONT.render('REVERSI', True, RED)
    title_rect= title_surf.get_rect()
    title_rect.center= (WINDOW_X/2, 40)

    prompt_surf = BRIT_FONT_BIG.render('Choose your colour:', True, BLUE)
    prompt_rect = prompt_surf.get_rect()
    prompt_rect.center = (round(WINDOW_X/2), round(WINDOW_Y/2)-100)

    white_surf= BRIT_FONT.render('White', True, WHITE, BLACK)
    white_rect = white_surf.get_rect()
    white_rect.center = (round(WINDOW_X/2)-100, round(WINDOW_Y/2)+40)

    black_surf = BRIT_FONT.render('Black', True, BLACK, WHITE)
    black_rect= black_surf.get_rect()
    black_rect.center = (int(WINDOW_X/2)+100, int(WINDOW_Y/2)+40)

    while True:
        # Keep looping until the player has clicked on a color.
        quit_check()
        
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                if white_rect.collidepoint((mouse_x, mouse_y)):
                    PLAYER1_COLOUR = "WHITE"
                    PLAYER2_COLOUR = "BLACK"
                    COLOUR1 = WHITE
                    COLOUR2 = BLACK
                    print 'white'
                    return [1,2]
                elif black_rect.collidepoint((mouse_x, mouse_y)):
                    PLAYER1_COLOUR = "BLACK"
                    PLAYER2_COLOUR = "WHITE"
                    COLOUR1 = BLACK
                    COLOUR2 = WHITE
                    print 'black'
                    return [2,1]
        
        DISPLAYSURF.blit(START_BG, START_BG_RECT)
        DISPLAYSURF.blit(title_surf, title_rect)
        DISPLAYSURF.blit(prompt_surf, prompt_rect)
        DISPLAYSURF.blit(white_surf, white_rect)
        DISPLAYSURF.blit(black_surf, black_rect)
        pygame.display.update()

def display_rules():
    
    #pygame.display.flip()
    
    DISPLAYSURF.blit(START_BG, START_BG_RECT)
    
    title_surf = RAVIE_FONT.render('REVERSI\nHello', True, BLACK)
    title_rect= title_surf.get_rect()
    title_rect.center= (WINDOW_X/2, 40)
    
    back_surf = BRIT_FONT.render('Go Back', True, WHITE)
    back_rect = back_surf.get_rect()
    back_rect.topleft = WINDOW_X-150, WINDOW_Y-50
    
    DISPLAYSURF.blit(title_surf, title_rect)
    DISPLAYSURF.blit(back_surf, back_rect)    
    pygame.display.update() 
    quit_check()    
    
    for event in pygame.event.get(): # event handling loop
        if event.type == MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            if back_rect.collidepoint((mouse_x, mouse_y)):
                #pygame.display.flip()
                print 'Go back'   

def get_score(board):
    black_score = 0
    white_score = 0
    for row in board:
        for tile in row:
            if tile == 1:
                white_score += 1
            elif tile == 2:
                black_score += 1
    return (white_score, black_score)
    
def get_my_score(board, player_colour):
    white_score, black_score = get_score(board)
    if player_colour == 1:
        return (white_score, black_score)
    elif player_colour == 2:
        return (black_score, white_score)

def get_index_from_coords(x, y):
    for index_x in range(8):
        for index_y in range(8):
            if (x > index_x * SQUARE_SIZE + XMARGIN and
                x < (index_x + 1) * SQUARE_SIZE + XMARGIN and
                y > index_y * SQUARE_SIZE + YMARGIN and
                y < (index_y + 1) * SQUARE_SIZE + YMARGIN):
                return (index_x, index_y)
    return None

def get_flipped_discs(board, player, x_init, y_init):
    if board[x_init][y_init] != 0:
        return False
    
    my_disc = player
    board[x_init][y_init] = my_disc
    if my_disc == 1:
        opp_disc = 2
    else:
        opp_disc = 1
    
    to_flip = []
    
    for x_offset, y_offset in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = x_init, y_init
        x += x_offset
        y += y_offset
        if is_on_board(x, y) and board[x][y] == opp_disc:
            x += x_offset
            y += y_offset
            if not is_on_board(x, y):
                continue
            while board[x][y] == opp_disc:
                x += x_offset
                y += y_offset
                if not is_on_board(x, y):
                    break
            if not is_on_board(x, y):
                continue
            if board[x][y] == my_disc:
                while True:
                    x -= x_offset
                    y -= y_offset
                    if x == x_init and y == y_init:
                        break
                    to_flip.append((x, y))
    board[x_init][y_init] = 0
    if len(to_flip) == 0:
        return False
    else:
        return to_flip                
        
def is_on_board(x, y):
    if x in range(8) and y in range(8):
        return True
    else:
        return False

def get_valid_moves(board, player):
    valid_moves = []
    for x in range(8):
        for y in range(8):
            if get_flipped_discs(board, player, x, y):
                valid_moves.append((x, y))
    #print "for" + str(player) + " " + str(valid_moves)
    return valid_moves

def get_opponent(player):
    if player == 1:
        return 2
    elif player== 2:
        return 1
    return None

def no_more_valid_moves(board, player):
    if not get_valid_moves(board, player) and not get_valid_moves(board, get_opponent(player)):
        #print "for " + str(self.num) + " " + str(self.get_valid_moves(self.board, self.num))
        #print "for " + str(self.get_opponent()) + " " + str(self.get_valid_moves(self.board, self.get_opponent()))
        return True
    return False

def quit_check():    
    # checks if exit conditions have been met
    
    for event in pygame.event.get((QUIT, KEYUP)): 
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        
if __name__ == '__main__':
    
    main()
