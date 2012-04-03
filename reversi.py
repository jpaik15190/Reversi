"""CIS192 Final Project; Othello_Reversi;
Paul Terwilliger, Jay Paik, Kristen Lau"""
import re

class Reversi(object):
    """This is the Reversi class with the rules of the game"""
    
    def __init__(self):
        """Create board and other variables"""
        self.board = []
        self.move = '99'
        self.turn = 0
        self.angles = []
        self.coors = {}
        self.end_pebbles = {}
        
    def new_game(self):
        """Starts a new game of Reversi"""
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0,],
                      [0, 0, 0, 0, 0, 0, 0, 0,],
                      [0, 0, 0, 0, 0, 0, 0, 0,],
                      [0, 0, 0, 1, 2, 0, 0, 0,],
                      [0, 0, 0, 2, 1, 0, 0, 0,],
                      [0, 0, 0, 0, 0, 0, 0, 0,],
                      [0, 0, 0, 0, 0, 0, 0, 0,],
                      [0, 0, 0, 0, 0, 0, 0, 0,]]
        self.turn = 1
        self.print_board()
        
    def print_board(self):
        """Prints the board: temporary function for developing code"""
        print "{})0  1  2  3  4  5  6  7 ".format(self.move)
        col_num = 0
        for row in self.board:
            print "{} {}".format(col_num, row)
            col_num += 1
        print "--------------------------"

    def check_pebbles(self):
        """Checks if any opponent pebbles are around the input pebble
        Stores the coordinates of opposing pebbles in self.coors"""

        # Defined variables:
        coo_y = int(self.move[0])
        coo_x = int(self.move[1])
        turn_f = ((self.turn % 2) + 1)

        # Enemy at 12:00
        if bool(re.match('[2-7][0-7]$', self.move)) and (
                                    self.board[coo_y - 1][coo_x] == turn_f):
            coors_y = [coo for coo in range(coo_y - 1, -1, -1)]
            coors_x = [coo_x for num in range(8)]
            self.coors[0] = zip(coors_y, coors_x)
            self.end_pebbles[0] = [self.board[self.coors[0][num][0]][
                        self.coors[0][num][1]] for num in range(len(self.coors[
                                                                          0]))]
        if bool(re.match('[2-7][0-5]$', self.move)): #enemy 1:30,  [1]
            if self.board[coo_y - 1][coo_x + 1] == turn_f:
                coors_y = [coo for coo in range(coo_y - 1, -1, -1)]
                coors_x = [coor for coor in range(coo_x + 1, 8)]
                self.coors[1] = zip(coors_y, coors_x)
                self.end_pebbles[1] = [self.board[self.coors[1][num][0]][self.coors[1][num][1]] for
                                       num in range(len(self.coors[1]))]
                print self.end_pebbles, self.coors
        if bool(re.match('[0-7][0-5]$', self.move)): #enemy 3:00,  [2]
            if self.board[coo_y][coo_x + 1] == turn_f:
                coors_y = [coo_y for num in range(8)]
                coors_x = [coor for coor in range(coo_x + 1, 8)]
                self.coors[2] = zip(coors_y, coors_x)
                self.end_pebbles[2] = [self.board[self.coors[2][num][0]][self.coors[2][num][1]] for
                                       num in range(len(self.coors[2]))]
                print self.end_pebbles, self.coors
        if bool(re.match('[0-5][0-5]$', self.move)): #enemy 4:30,  [3]
            if self.board[coo_y + 1][coo_x + 1] == turn_f:
                pass
        if bool(re.match('[0-5][0-7]$', self.move)): #enemy 6:00,  [4]
            if self.board[coo_y + 1][coo_x] == (
                                                    (self.turn % 2) + 1): self.angles.append(4)
        if bool(re.match('[0-5][2-7]$', self.move)): #enemy 7:30,  [5]
            if self.board[coo_y + 1][coo_x - 1] == (
                                                    (self.turn % 2) + 1): self.angles.append(5)
        if bool(re.match('[0-7][2-7]$', self.move)): #enemy 9:00,  [6]
            if self.board[coo_y][coo_x - 1] == (
                                                    (self.turn % 2) + 1): self.angles.append(6)
        if bool(re.match('[2-7][2-7]$', self.move)): #enemy 10:30, [7]
            if self.board[coo_y - 1][coo_x - 1] == (
                                                    (self.turn % 2) + 1): self.angles.append(7)
        
    def prompt_move(self):
        """Receives a move from the user and runs it"""
        self.move = '99'
        while bool(re.match('[0-7][0-7]$', self.move)) == False:
            self.move = raw_input("Where would you like to move? "
                                  "Choose a two digit number 00-77: ")
            self.check_pebbles()
            self.end_pebbles = {}
            self.coors ={}
            if (bool(re.match('[0-7][0-7]$', self.move)) and (self.board[int(self.move[0])][
                                                                    int(self.move[1])] == 0)):
                self.board[int(self.move[0])][int(self.move[1])], self.turn = self.turn, (
                                    (self.turn % 2) + 1) #append move to board and change turns
                self.print_board()
            elif bool(re.match('[0-7][0-7]$', self.move)) == True:
                print "Invalid move, Player {} already has a piece there.".format(
                                        self.board[int(self.move[0])][int(self.move[1])])
                self.move = '99'
            else:
                print "Invalid entry."


game = Reversi()
game.new_game()
for x in range(1):
    game.prompt_move()
print 'Good move.'