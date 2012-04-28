import pygame
import sys
import socket

from PodSixNet.Connection import connection, ConnectionListener




WHITE_DISC = 1
BLACK_DISC = 2

#COLORS
DARK_OLIVE_GREEN = (85, 107, 47)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
NAVAJO_WHITE = (238, 207, 161)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Client(ConnectionListener):
    def __init__(self, host, port):
        
        pygame.init()
        
        self.Connect((host, port))
        
        self.screen = pygame.display.set_mode((480+300, 480+120))
        #self.screen = screen
        
        self.num = None
        
        self.turn = False
        
        self.ready = False
        
        self.start = False
        
        self.font = pygame.font.SysFont('tahoma', 20, False)
        
        self.points = [0, 0]
        
        self.movement = [0, 0]
        
        self.board = [[0 for x in range(8)] for y in range(8)]
        
        #default
        #-------
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1
        
        #testing
        #-------
        #self.board[1] = [1 for x in range(8)]
        #self.board[2] = [2 for x in range(8)]
        #self.board[3] = [2 for x in range(8)]
        #self.board[4] = [2 for x in range(8)]
        #self.board[5] = [2 for x in range(8)]
        #self.board[6] = [1 for x in range(8)]
        #self.board[6][7] = 0
    
    def Network_move(self, data):
        #self.movement[data['player']] = data['pos']
        x, y = data['pos']
        if data['player'] != self.num:
            self.turn = True
        else:
            self.turn = False
        #if self.board[x][y] != 0:
            #print "Invalid move: there's already a disc there."
        #else:
            #self.board[x][y] = data['player']
        for x_to_flip, y_to_flip in data['flip']:
            self.board[x_to_flip][y_to_flip] = data['player']
        self.board[x][y] = data['player']
        
    def Network_number(self, data):
        self.num = data['num']
        if self.num == 2:
           self.turn = True
    
    def Network_turn(self, data):
        if data['player'] == self.num:
            self.turn = False
        else:
            self.turn = True
    
    def Network_ready(self, data):
        self.ready = not self.ready
    
    #def Network_points(self, data):
        #self.points[0] = data[0]
        #self.points[1] = data[1]
        
    def Network_start(self, data):
        self.ready = False
        self.start = True
        
    def get_coordinates(self, x, y):
        x_coord = 150 + 30 + (x * 60) + 1 
        y_coord = 60 + 30 + (y * 60) + 1
        return (x_coord, y_coord)
    
    def get_score(self, board):
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
        white_score, black_score = self.get_score(board)
        if self.num == 1:
            return (white_score, black_score)
        elif self.num == 2:
            return (black_score, white_score)
        return None
    
    def get_opponent(self):
        if self.num == 1:
            return 2
        elif self.num == 2:
            return 1
        return None
    
    def get_index_from_coords(self, x, y):
        for index_x in range(8):
            for index_y in range(8):
                if (x > index_x * 60 + 150 and
                    x < (index_x + 1) * 60 + 150 and
                    y > index_y * 60 + 60 and
                    y < (index_y + 1) * 60 + 60):
                    return (index_x, index_y)
        return None
    
    def get_flipped_discs(self, board, player, x_init, y_init):
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
        if x in range(8) and y in range(8):
            return True
        else:
            return False
    
    
    def get_valid_moves(self, board, player):
        valid_moves = []
        for x in range(8):
            for y in range(8):
                if self.get_flipped_discs(board, player, x, y):
                    valid_moves.append((x, y))
        #print "for" + str(player) + " " + str(valid_moves)
        return valid_moves
    
    def no_more_valid_moves(self):
        if not self.get_valid_moves(self.board, self.num) and not self.get_valid_moves(self.board, self.get_opponent()):
            #print "for " + str(self.num) + " " + str(self.get_valid_moves(self.board, self.num))
            #print "for " + str(self.get_opponent()) + " " + str(self.get_valid_moves(self.board, self.get_opponent()))
            return True
        return False
    
    #def num_to_color_string(self, num):
        #if num == 1:
        #    return "WHITE"
        #elif num == 2:
        #    return "BLACK"
        #return None
    
    def draw_board(self, screen):
    
    	board_rect = pygame.Rect(150, 60, 480, 480)
    	screen.fill(DARK_OLIVE_GREEN, board_rect)
    	if self.num == 1:
    	    screen.blit(self.font.render("WHITE", True, WHITE), (45,20))
        elif self.num == 2:
    	    screen.blit(self.font.render("BLACK", True, BLACK), (45,20))    
    	
    	if self.turn and self.get_valid_moves(self.board, self.num):
    	    screen.blit(self.font.render(">", True, BLUE), (20,20))
    	    
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
            
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == WHITE_DISC or self.board[x][y] == BLACK_DISC:
                    coords = self.get_coordinates(x, y)
                    if self.board[x][y] == WHITE_DISC:
                        disc_color = WHITE
                    else:
                        disc_color = BLACK
                    pygame.draw.circle(screen, disc_color, coords, 27)
        
        white_score, black_score = self.get_score(self.board)
        screen.blit(self.font.render("BLACK: " + str(black_score), True, BLACK), (650,20))
        screen.blit(self.font.render("WHITE: " + str(white_score), True, BLACK), (650,50))
        
    
    def Loop(self):
        while True:
            connection.Pump()
            self.Pump()
            
            if self.start:
                if self.turn and not self.get_valid_moves(self.board, self.num) and self.get_valid_moves(self.board, self.get_opponent()):
                    connection.Send({'action': 'turn', 'player': self.num})
                
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif self.start:
                    if event.type == pygame.MOUSEBUTTONDOWN and self.turn:
                        print event.pos
                        print self.num
                        cx, cy = event.pos
                        tile = self.get_index_from_coords(cx, cy)
                        valid_moves = self.get_valid_moves(self.board, self.num)
                        
                        if tile in valid_moves:
                            tx, ty = tile
                            to_flip = self.get_flipped_discs(self.board, self.num, tx, ty)
                            connection.Send({'action': 'move', 'player': self.num, 'pos': tile, 'flip': to_flip})                            
                        
                    #take care of other menu item clicks here

            if self.start:
                self.screen.fill(NAVAJO_WHITE)
                self.draw_board(self.screen)
                if self.no_more_valid_moves():
                    
                    my_score, opp_score = self.get_my_score(self.board)
                    
                    self.screen.blit(self.font.render('Game Over', True, BLUE), (390-self.font.size('Game Over')[0]/2, 270))
                    
                    if my_score > opp_score:
                        self.screen.blit(self.font.render('YOU WIN!', True, RED), (390-self.font.size('YOU WIN!')[0]/2, 300))
                    elif my_score < opp_score:
                        self.screen.blit(self.font.render('YOU LOSE!', True, RED), (390-self.font.size('YOU LOSE!')[0]/2, 300))
                    elif my_score == opp_score:
                        self.screen.blit(self.font.render('DRAW!', True, RED), (390-self.font.size('DRAW!')[0]/2, 300))
                    
            	pygame.display.flip()
            

            if self.ready:
                self.screen.fill(NAVAJO_WHITE)
                self.screen.blit(self.font.render('Ready', True, BLACK), (390-self.font.size('Ready')[0]/2, 300))
                pygame.display.flip()
                self.screen.fill(NAVAJO_WHITE)
            elif not self.start:
                self.screen.fill(NAVAJO_WHITE)
                self.screen.blit(self.font.render('Waiting for players...', True, BLACK), (390-self.font.size('Waiting for players...')[0]/2, 300))
                pygame.display.flip()
                
                
            pygame.time.wait(25)

#print 'Enter the server IP address'
#print 'Empty for localhost'
# ask the server IP address
# server = raw_input('Server IP: ')
# control if server is empty
#if server == '':
#	server = 'localhost'

# init the listener
#client = Client(server, 31500)
#client = Client('localhost', 31500)
# start the mainloop
#client.Loop()

def new_client(address, port):
    #address = 'localhost'
    client = Client(address, port)
    client.Loop()

#new_client('localhost', 31500)