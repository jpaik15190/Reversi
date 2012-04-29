"""Runs the client and connects to the provided host and port."""

# CIS-192: Python Programming
# Spring 2012
# Final Project: Reversi
# Kristen Lau, Jay Paik, Paul Terwilliger
#
# Required modules: pygame, numpy
# Included module: textrect

import pygame
import sys
import socket
from textrect import render_textrect
from PodSixNet.Connection import connection, ConnectionListener

WINDOW_X = 480 + 300 # window width
WINDOW_Y = 480 + 120 # window height
SQUARE_SIZE = 60 # size of each square in grid
BOARD_X = 8 # number of columns in grid
BOARD_Y = BOARD_X # number of rows in grid

XMARGIN = int((WINDOW_X-(BOARD_X*SQUARE_SIZE))/2)
YMARGIN = int((WINDOW_Y-(BOARD_Y*SQUARE_SIZE))/2)

WHITE_DISC = 1
BLACK_DISC = 2

DARK_OLIVE_GREEN = (85, 107, 47)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
NAVAJO_WHITE = (238, 207, 161)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0,155,0)
YELLOW = (255, 255, 0)
PINK = (255, 62, 150)
ORANGE = (255, 127, 0)
DARKRED = (139, 0, 0)
PURPLE = (142, 56, 142)

class Client(ConnectionListener):
    """A class representing the client."""

    def __init__(self, host, port):
        """Initialize the client at the given host/port."""

        global MAINCLOCK, DISPLAYSURF, RAVIE_FONT, WINDOW_BG, BRIT_FONT, \
               CHOOSE_BG, SNAP_FONT, START_BG, START_BG_RECT, OVER_BG, \
               OVER_BG_RECT, YOUR_TURN, YOUR_TURN_RECT, OPP_TURN, \
               OPP_TURN_RECT, BRIT_FONT_BIG, SAD, SAD_RECT, TROPHY, \
               TROPHY_RECT, ABOUT_BG, ABOUT_RECT, ABOUT_CLOSE, \
               ABOUT_CLOSE_RECT, TIE, TIE_RECT

        pygame.init() # Initialize pygame

        # Connect to the server
        self.Connect((host, port))
        self.host_addr = str(host)

        # Set screen display surface
        self.screen = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
        pygame.display.set_caption('*** REVERSI ***')

        # Initialize game variables
        self.num = None
        self.turn = False
        self.ready = False
        self.start = False
        self.gameover = False
        self.about = False
        self.board = self.set_board()

        # Initialize the fonts
        self.font = pygame.font.SysFont('arial', 20, False)
        self.close_font = pygame.font.SysFont('arial', 16, True)
        self.font2 = pygame.font.SysFont('arial', 40, False)
        self.font3 = pygame.font.SysFont('arial', 30, False)
        self.rules_font = pygame.font.SysFont('arial', 12, False)
        BRIT_FONT = pygame.font.SysFont('arial black', 26)
        RAVIE_FONT = pygame.font.SysFont('arial black', 35)
        SNAP_FONT = pygame.font.SysFont('arial black', 50)
        BRIT_FONT_BIG = pygame.font.SysFont('arial black', 85)

        # About window
        game_rules_txt = ""
        input_file = open("reversi_rules.txt", 'rU')
        for line in input_file:
            game_rules_txt += line
        self.rules_rect = pygame.Rect((40, 40, 400, 450))
        self.rules_rect.center = (WINDOW_X/2, WINDOW_Y/2)
        self.rules_surf = render_textrect(game_rules_txt, self.rules_font,
                                          self.rules_rect, BLACK, WHITE)
        self.rules_surf.set_alpha(200)
        ABOUT_CLOSE = self.close_font.render("Close", True, BLACK)
        ABOUT_CLOSE_RECT = ABOUT_CLOSE.get_rect()
        ABOUT_CLOSE_RECT.center = (WINDOW_X/2, 508)
        
        # Turn display
        YOUR_TURN = self.font.render("Your turn", True, WHITE)
        YOUR_TURN_RECT = YOUR_TURN.get_rect()
        YOUR_TURN_RECT.center= (WINDOW_X/2, WINDOW_Y - YMARGIN/2)
        OPP_TURN = self.font.render("The opponent is thinking...", True, WHITE)
        OPP_TURN_RECT = OPP_TURN.get_rect()
        OPP_TURN_RECT.center= (WINDOW_X/2, WINDOW_Y - YMARGIN/2)
        
        # Starting background
        START_BG = pygame.image.load('sky2.jpg')
        START_BG = pygame.transform.smoothscale(START_BG, (WINDOW_X, WINDOW_Y))
        START_BG_RECT = START_BG.get_rect()
        
        # Game grid background
        board_bg = pygame.image.load('sky.jpg')
        board_bg = pygame.transform.smoothscale(board_bg,
                                                (BOARD_X*SQUARE_SIZE,
                                                 BOARD_Y*SQUARE_SIZE))
        board_bg_rect = board_bg.get_rect()
        board_bg_rect.topleft = (XMARGIN, YMARGIN)
        
        # Game window background
        WINDOW_BG = pygame.image.load('aurora2.jpg')
        WINDOW_BG = pygame.transform.smoothscale(WINDOW_BG,
                                                 (WINDOW_X, WINDOW_Y))
        WINDOW_BG.blit(board_bg, board_bg_rect)
        
        # Game over background
        OVER_BG = pygame.image.load('sunset_faded.jpg')
        OVER_BG = pygame.transform.smoothscale(OVER_BG, (WINDOW_X, WINDOW_Y))
        OVER_BG_RECT = OVER_BG.get_rect()
        
        # Game over image: loss
        SAD = pygame.image.load('sad_lost_small.jpg')
        SAD_RECT = SAD.get_rect()
        SAD_RECT.center=(int(WINDOW_X/2), 250)

        # Game over image: win
        TROPHY = pygame.image.load('winner_small.jpg')
        TROPHY_RECT = TROPHY.get_rect()
        TROPHY_RECT.center=(int(WINDOW_X/2), 250)

        # Game over image: tie
        TIE = pygame.image.load('tie_small.jpg')  
        TIE_RECT = TIE.get_rect()
        TIE_RECT.center=(int(WINDOW_X/2), 250)

        # Game over button: play again        
        self.play_again = BRIT_FONT.render('Play Again!', True, RED)
        self.play_again_rect = self.play_again.get_rect()
        self.play_again_rect.center = (int(WINDOW_X/2) - 100, 500)

        # Game over button: exit
        self.quit_game = BRIT_FONT.render('Exit', True, BLUE)
        self.quit_game_rect = self.quit_game.get_rect()
        self.quit_game_rect.center = (int(WINDOW_X/2) + 100, 500)

    
    def set_board(self):
        """Set the initial game board."""
        board = [[0 for x in range(8)] for y in range(8)]
        board[3][3] = 1
        board[3][4] = 2
        board[4][3] = 2
        board[4][4] = 1
        return board

    # NETWORK METHODS
    # These execute when data is received from the server.
    # For data['action'], respective methods are executed.
    def Network_move(self, data):
        """Make the move for the given player and flip pieces."""
        x, y = data['pos']
        if data['player'] != self.num:
            self.turn = True
        else:
            self.turn = False
        for x_to_flip, y_to_flip in data['flip']:
            self.board[x_to_flip][y_to_flip] = data['player']
        self.board[x][y] = data['player']
        
    def Network_reset(self, data):
        """Reset the game variables to start a new game."""
        print data['message']
        self.board = self.set_board()
        self.turn = False
        self.ready = False
        self.start = False
        self.gameover = False
        if self.num == 2:
           self.turn = True
        
    def Network_quit(self, data):
        """Quit the game."""
        print data['message']
        connection.Close()
        sys.exit(0)
        
    def Network_number(self, data):
        """Assign player number/color. Host is always 1/white."""
        self.num = data['num']
        if self.num == 2:
           self.turn = True
    
    def Network_turn(self, data):
        """Regulate turns."""
        if data['player'] == self.num:
            self.turn = False
        else:
            self.turn = True
    
    def Network_ready(self, data):
        """Make player ready."""
        self.ready = not self.ready
        
    def Network_start(self, data):
        """Start the game."""
        self.ready = False
        self.start = True
        
    def get_coordinates(self, x, y):
        """Return the coordinates of the center of the given tile."""
        x_coord = 150 + 30 + (x * 60) + 1 
        y_coord = 60 + 30 + (y * 60) + 1
        return (x_coord, y_coord)
    
    def get_score(self, board):
        """Get the scores given the board."""
        black_score = 0
        white_score = 0
        for row in board:
            for tile in row:
                if tile == 1:
                    white_score += 1
                elif tile == 2:
                    black_score += 1
        return (white_score, black_score)
    
    def get_my_score(self, board):
        """Return my score first, then the opponent's score."""
        white_score, black_score = self.get_score(board)
        if self.num == 1:
            return (white_score, black_score)
        elif self.num == 2:
            return (black_score, white_score)
        return None
    
    def get_opponent(self):
        """Get the opponent's number."""
        if self.num == 1:
            return 2
        elif self.num == 2:
            return 1
        return None
    
    def get_index_from_coords(self, x, y):
        """Get the tile indices from the given mouse coordinates."""
        for index_x in range(8):
            for index_y in range(8):
                if (x > index_x * 60 + 150 and
                    x < (index_x + 1) * 60 + 150 and
                    y > index_y * 60 + 60 and
                    y < (index_y + 1) * 60 + 60):
                    return (index_x, index_y)
        return None
    
    def get_flipped_discs(self, board, player, x_init, y_init):
        """Return a list of discs to be flipped given the move."""
        if board[x_init][y_init] != 0:
            return False
        
        my_disc = player
        board[x_init][y_init] = my_disc
        if my_disc == 1:
            opp_disc = 2
        else:
            opp_disc = 1
        
        to_flip = []
        for x_offset, y_offset in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], \
                                   [-1, -1], [-1, 0], [-1, 1]]:
            x, y = x_init, y_init
            x += x_offset
            y += y_offset
            if self.is_on_board(x, y) and board[x][y] == opp_disc:
                x += x_offset
                y += y_offset
                if not self.is_on_board(x, y):
                    continue
                while board[x][y] == opp_disc:
                    x += x_offset
                    y += y_offset
                    if not self.is_on_board(x, y):
                        break
                if not self.is_on_board(x, y):
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
                  
    def is_on_board(self, x, y):
        """Check if the move is within the board."""
        if x in range(8) and y in range(8):
            return True
        else:
            return False
        
    def get_valid_moves(self, board, player):
        """Return a set of valid moves for the given player."""
        valid_moves = []
        for x in range(8):
            for y in range(8):
                if self.get_flipped_discs(board, player, x, y):
                    valid_moves.append((x, y))
        return valid_moves
    
    def no_more_valid_moves(self):
        """Check if there are no more valid moves for both players."""
        if (not self.get_valid_moves(self.board, self.num) and
            not self.get_valid_moves(self.board, self.get_opponent())):
            return True
        return False
    
    #def num_to_color_string(self, num):
        #if num == 1:
        #    return "WHITE"
        #elif num == 2:
        #    return "BLACK"
        #return None
    
    def display_buttons(self, screen):
        """Display the labels and buttons on the game screen."""
        
        global NEWGAME_RECT, ABOUT_RECT, TITLE_RECT, PLAYER1_RECT, \
               PLAYER2_RECT, EXIT_RECT

        # About button
        about_surf = BRIT_FONT.render('About', True, WHITE)
        ABOUT_RECT = about_surf.get_rect()
        ABOUT_RECT.topright = (WINDOW_X - 20, 30)

        # Exit button
        exit_surf = BRIT_FONT.render('EXIT', True, WHITE)
        EXIT_RECT = exit_surf.get_rect()
        EXIT_RECT.topright = (WINDOW_X - 20, WINDOW_Y - 50)

        # Game title label
        title_surf = RAVIE_FONT.render('REVERSI', True, YELLOW)
        TITLE_RECT= title_surf.get_rect()
        TITLE_RECT.center= (WINDOW_X/2, 30)

        # Player 1 label
        player1_surf = BRIT_FONT.render('You', True, ORANGE)
        PLAYER1_RECT = player1_surf.get_rect()
        PLAYER1_RECT.topleft = (XMARGIN/2 - BRIT_FONT.size('You')[0]/2, 200)

        # Player 2 label
        player2_surf = BRIT_FONT.render('Opponent', True, ORANGE)
        PLAYER2_RECT = player2_surf.get_rect()
        PLAYER2_RECT.topleft = (WINDOW_X - XMARGIN/2 -
                                BRIT_FONT.size('Opponent')[0]/2, 200)

        # Player 1 color label
        colour1_surf = BRIT_FONT.render(PLAYER1_COLOUR, True, COLOUR1, COLOUR2)
        colour1_rect = colour1_surf.get_rect()
        colour1_rect.topleft = (XMARGIN/2 -
                                BRIT_FONT.size(PLAYER1_COLOUR)[0]/2, 240)

        # Player 2 color label
        colour2_surf = BRIT_FONT.render(PLAYER2_COLOUR, True, COLOUR2, COLOUR1)
        colour2_rect = colour2_surf.get_rect()
        colour2_rect.topleft = (WINDOW_X - XMARGIN/2 -
                                BRIT_FONT.size(PLAYER2_COLOUR)[0]/2, 240)

        # Display the labels and buttons on the screen
        screen.blit(about_surf, ABOUT_RECT)
        screen.blit(title_surf, TITLE_RECT)
        screen.blit(player1_surf, PLAYER1_RECT)
        screen.blit(player2_surf, PLAYER2_RECT)
        screen.blit(exit_surf, EXIT_RECT)
        screen.blit(colour1_surf, colour1_rect)
        screen.blit(colour2_surf, colour2_rect)
    
    def display_score(self, screen):
        """Show the current score on the screen."""
        my_score, opp_score = self.get_my_score(self.board)

        # My score label
        my_score_surf = SNAP_FONT.render(str(my_score), True, RED)
        my_score_rect = my_score_surf.get_rect()
        my_score_rect.center = (XMARGIN/2, 300)

        # Opponent's score label
        opp_score_surf = SNAP_FONT.render(str(opp_score), True, RED)
        opp_score_rect = opp_score_surf.get_rect()
        opp_score_rect.center = (WINDOW_X-XMARGIN/2, 300)

        # Display it on the screen
        screen.blit(my_score_surf, my_score_rect)
        screen.blit(opp_score_surf, opp_score_rect)

    def display_whose_turn(self, screen):
        """Display whose turn it is."""
        if self.turn and self.get_valid_moves(self.board, self.num):
            screen.blit(YOUR_TURN, YOUR_TURN_RECT)
        else:
            screen.blit(OPP_TURN, OPP_TURN_RECT)
    
    def display_about(self, screen):
        """Display the about window."""
        if self.about:
            screen.blit(self.rules_surf, self.rules_rect)
            screen.blit(ABOUT_CLOSE, ABOUT_CLOSE_RECT)
    
    def display_game_over(self, screen):
        """Display the game over screen."""
        my_score, opp_score = self.get_my_score(self.board)
        
        screen.blit(OVER_BG, OVER_BG_RECT)
        
        # Decide win, lose, or draw
        if my_score > opp_score:
            screen.blit(TROPHY, TROPHY_RECT)
        elif my_score < opp_score:
            screen.blit(SAD, SAD_RECT)
        elif my_score == opp_score:
            screen.blit(TIE, TIE_RECT)

        # Game over text
        text_surf = BRIT_FONT_BIG.render("GAME OVER!", True, PURPLE)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(WINDOW_X/2), 50)

        # Score text
        score_surf = BRIT_FONT.render(" %s -- %s  " %
                                      (str(my_score), str(opp_score)),
                                      True, BLACK)
        score_rect = score_surf.get_rect()
        score_rect.center = (int(WINDOW_X/2), 400)

        #Query text
        text2_surf = BRIT_FONT.render('What do you want to do?', True, BLACK)
        text2_rect = text2_surf.get_rect()
        text2_rect.center = (int(WINDOW_X/2), 450)

        # Display the elements
        screen.blit(text_surf, text_rect)
        screen.blit(text2_surf, text2_rect)
        screen.blit(score_surf, score_rect)
        screen.blit(self.play_again, self.play_again_rect)
        screen.blit(self.quit_game, self.quit_game_rect)  

        # Set game over trigger
        self.gameover = True
        
    def draw_board(self, screen):
        """Draw the board and the pieces."""
        screen.blit(WINDOW_BG, WINDOW_BG.get_rect())

        # Draw the gridlines of the board (8x8)
        for x in range(9):
            start_x = (x * 60) + 150
            start_y = 60
            end_x = (x * 60) + 150
            end_y = 60 + (8 * 60)
            pygame.draw.line(screen, BLACK, (start_x, start_y), (end_x, end_y))
        for y in range(9):
            start_x = 150
            start_y = (y * 60) + 60
            end_x = 150 + (8 * 60)
            end_y = (y * 60) + 60
            pygame.draw.line(screen, BLACK, (start_x, start_y), (end_x, end_y))

        # Draw the white and black discs
        for x in range(8):
            for y in range(8):
                if (self.board[x][y] == WHITE_DISC or
                    self.board[x][y] == BLACK_DISC):
                    coords = self.get_coordinates(x, y)
                    if self.board[x][y] == WHITE_DISC:
                        disc_color = WHITE
                    else:
                        disc_color = BLACK
                    pygame.draw.circle(screen, disc_color, coords, 27)

    def choose_colour(self):
        """Set the color of the player."""
        global PLAYER1_COLOUR, PLAYER2_COLOUR, COLOUR1, COLOUR2
        
        if self.num == 1:
            PLAYER1_COLOUR = "WHITE"
            PLAYER2_COLOUR = "BLACK"
            COLOUR1 = WHITE
            COLOUR2 = BLACK
        elif self.num == 2:
            PLAYER1_COLOUR = "BLACK"
            PLAYER2_COLOUR = "WHITE"
            COLOUR1 = BLACK
            COLOUR2 = WHITE
    
    def Loop(self):
        """Start the main game loop."""
        
        while True:
            
            # Pump to communicate with server
            connection.Pump()
            self.Pump()

            # If host does not exist, exit
            if not self.start and not connection.isConnected:
                print "The host does not exist."
                connection.Close()
                sys.exit(0)
                
            
            if self.start:
                # Manage turns, forfeit turn if no moves available
                if (self.turn and
                    not self.get_valid_moves(self.board, self.num) and
                    self.get_valid_moves(self.board, self.get_opponent())):
                    connection.Send({'action': 'turn', 'player': self.num})
                
            # Manage pygame events
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    connection.Close()
                    sys.exit(0)
                    
                elif self.start:
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and self.turn:
                        cx, cy = event.pos
                        tile = self.get_index_from_coords(cx, cy)
                        valid_moves = self.get_valid_moves(self.board,
                                                           self.num)
                        if tile in valid_moves:
                            tx, ty = tile
                            to_flip = self.get_flipped_discs(self.board,
                                                             self.num, tx, ty)
                            connection.Send({'action': 'move',
                                             'player': self.num,
                                             'pos': tile,
                                             'flip': to_flip})

                    if (event.type == pygame.MOUSEBUTTONDOWN and
                        not self.gameover):
                        cx, cy = event.pos
                        if EXIT_RECT.collidepoint((cx, cy)):
                            pygame.quit()
                            connection.Close()
                            sys.exit()
                        elif ABOUT_RECT.collidepoint((cx, cy)):
                            self.about = True
                        if (self.about and
                            ABOUT_CLOSE_RECT.collidepoint((cx, cy))):
                            self.about = False
                    
                if self.gameover:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        cx, cy = event.pos
                        if self.quit_game_rect.collidepoint((cx, cy)):
                            connection.Close()
                            sys.exit(0)
                        elif self.play_again_rect.collidepoint((cx, cy)):
                            connection.Send({'action': 'reset',
                                             'message': "Let's play again!"})

            if self.start:
                # Draw and update board
                if not connection.isConnected:
                    print "The host has left the game."
                    connection.Close()
                    sys.exit(0)
                self.draw_board(self.screen)
                self.display_buttons(self.screen)
                self.display_score(self.screen)
                
                if not self.no_more_valid_moves():
                    self.display_whose_turn(self.screen)
                    
                self.display_about(self.screen)
                
                if self.no_more_valid_moves():

                    if not self.gameover:
                        pygame.display.flip()
                        pygame.time.delay(1500)
                    self.display_game_over(self.screen)
                    
                pygame.display.flip()

            if self.ready:
                # Show ready screen, start the game
                self.screen.blit(START_BG, START_BG_RECT)
                self.screen.blit(self.font.render('Ready?', True, BLACK),
                                 (390-self.font.size('Ready?')[0]/2, 300))
                self.choose_colour()
                pygame.display.flip()
                
            elif not self.start:
                # Show starting screen, wait for player
                self.screen.blit(START_BG, START_BG_RECT)
                self.screen.blit(self.font.render\
                                 ('Waiting for opponent...', True, BLACK),
                                 (390-self.font.\
                                  size('Waiting for opponent...')[0]/2, 280))
                self.screen.blit(self.font.render(self.host_addr, True, WHITE),
                                 (390-self.font.size\
                                  (self.host_addr)[0]/2, 320))
                pygame.display.flip()
 
            pygame.time.wait(25)


def new_client(address, port):
    """Start a new client."""
    client = Client(address, port)
    client.Loop()
