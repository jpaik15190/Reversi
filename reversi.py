"""CIS192 Final Project; Othello_Reversi;
Paul Terwilliger, Jay Paik, Kirsten Lau"""
import re

"""The code in prompt_move() is still ugly and can use some cleaning up. 
I'll probably do some things to make it run faster and look cleaner.  

A few things that the rules still do not do: 
a)tell you when the game is over
b)end the game
c)force a player to pass if they cannot move
d)allow a player to resign
e)run forever until a person wins, loses, or resigns.  
--Note: this game will not allow the player to voluntarily "pass"

Ending the game happens when:
a)both players cannot move
b)the board is full (same as "both players cannot move", trivial case)
c)one player resigns

Ending the game entails:
a)telling you who wins
b)asking for a rematch with sides switched Ex: black moves first if white
    moved first last game and vice-versa
c)resetting the board using the new_game() function



"""

class Reversi(object):
    """This is the Reversi class with the rules of the game"""
    
    def __init__(self):
        """Create board and other variables"""
        self.board = []
        self.move = '99'
        self.turn = 2
        self.flip = []
        
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
        self.turn = ((self.turn % 2) + 1)
        self.print_board()
        
    def print_board(self):
        """Prints the board: temporary function for developing code"""
        print "{})0  1  2  3  4  5  6  7 ".format(self.move)
        col_num = 0
        for row in self.board:
            print "{} {}".format(col_num, row)
            col_num += 1
        print "--------------------------"

    def flip_pebbles(self):
        """Checks if any opponent pebbles are around the input pebble and
        stores the coordinates of all opposing flippable pebbles in flip"""
        
        def legal_move(flip_list):
            """Input is a list of two-integer tuples which are coordinates,
            output is a list with the to-be-flipped pebbles remaining."""
            legal = 0
            counter = 0
            for (num, ber) in flip_list:
                if self.board[num][ber] == ((self.turn % 2) + 1):
                    counter += 1
                elif self.board[num][ber] == 0:
                    counter = 0
                    break
                elif self.board[num][ber] == self.turn:
                    legal = 1
                    break
            if legal == 0:
                counter = 0
            flip = flip_list[:counter]
            #flip = ["".join([str(num), str(ber)]) for (num, ber) in flip_]
            return flip

        # Defined variables:
        coo_y = int(self.move[0])
        coo_x = int(self.move[1])
        turn_f = ((self.turn % 2) + 1)
        self.flip = []
        north = []
        neast = []
        east = []
        seast = []
        south = []
        swest = []
        west = []
        nwest = []

        # Enemy north
        if bool(re.match('[2-7][0-7]$', self.move)) and (
                                self.board[coo_y - 1][coo_x] == turn_f):
            coors_y = [coor for coor in range(coo_y - 1, -1, -1)]
            coors_x = [coo_x for num in range(8)]
            north = zip(coors_y, coors_x)
            
        # Enemy north-east
        if bool(re.match('[2-7][0-5]$', self.move)) and (
                            self.board[coo_y - 1][coo_x + 1] == turn_f):
            coors_y = [coor for coor in range(coo_y - 1, -1, -1)]
            coors_x = [coor for coor in range(coo_x + 1, 8)]
            neast = zip(coors_y, coors_x)
        
        # Enemy east
        if bool(re.match('[0-7][0-5]$', self.move)) and (
                                self.board[coo_y][coo_x + 1] == turn_f):
            coors_y = [coo_y for num in range(8)]
            coors_x = [coor for coor in range(coo_x + 1, 8)]
            east = zip(coors_y, coors_x)
        
        # Enemy south-east        
        if bool(re.match('[0-5][0-5]$', self.move)) and (
                            self.board[coo_y + 1][coo_x + 1] == turn_f):
            coors_y = [coor for coor in range(coo_y + 1, 8)]
            coors_x = [coor for coor in range(coo_x + 1, 8)]
            seast = zip(coors_y, coors_x)
            
        # Enemy south
        if bool(re.match('[0-5][0-7]$', self.move)) and (
                                self.board[coo_y + 1][coo_x] == turn_f):
            coors_y = [coor for coor in range(coo_y + 1, 8)]
            coors_x = [coo_x for num in range(8)]
            south = zip(coors_y, coors_x)
        
        # Enemy south-west
        if bool(re.match('[0-5][2-7]$', self.move)) and (
                            self.board[coo_y + 1][coo_x - 1] == turn_f):
            coors_y = [coor for coor in range(coo_y + 1, 8)]
            coors_x = [coor for coor in range(coo_x - 1, -1, -1)]
            swest = zip(coors_y, coors_x)
        
        #Enemy west
        if bool(re.match('[0-7][2-7]$', self.move)) and (
                                self.board[coo_y][coo_x - 1] == turn_f):
            coors_y = [coo_y for num in range(8)]
            coors_x = [coor for coor in range(coo_x - 1, -1, -1)]
            west = zip(coors_y, coors_x)
        
        # Enemy north-west
        if bool(re.match('[2-7][2-7]$', self.move)) and (
                            self.board[coo_y - 1][coo_x - 1] == turn_f):
            coors_y = [coor for coor in range(coo_y - 1, -1, -1)]
            coors_x = [coor for coor in range(coo_x - 1, -1, -1)]
            west = zip(coors_y, coors_x)
        
        self.flip = (legal_move(north) + legal_move(neast) + legal_move(east)
                   + legal_move(seast) + legal_move(south) + legal_move(swest)
                    + legal_move(west) + legal_move(nwest))
        
        # Flips over the pebbles chosen by flip
        for (num, ber) in self.flip:
            self.board[num][ber] = self.turn
        
        return self.flip
        
    def prompt_move(self):
        """Receives a move from the user and runs it. Entries are a two-digit
        string with the y-coordinate first, then the x-coordinate. Both
        coordinates must be from 0 to 7 inclusive. Ex: valid entries are
        "00", "77", "45", "12", "70". Ex: invalid entries are: "90", "38", 
        "81", "031", "1", "a5"
        
        
        99)0  1  2  3  4  5  6  7 
        0 [0, 0, 0, 0, 0, 0, 0, 0]
        1 [0, 0, 0, 0, 0, 0, 0, 0]
        2 [0, 0, 0, 0, 0, 0, 0, 0]
        3 [0, 0, 0, 1, 2, 0, 0, 0]
        4 [0, 0, 0, 2, 1, 0, 0, 0]
        5 [0, 0, 0, 0, 0, 0, 0, 0]
        6 [0, 0, 0, 0, 0, 0, 0, 0]
        7 [0, 0, 0, 0, 0, 0, 0, 0]
        --------------------------
        
        --Note: 1 is white, 2 is black, 0 is an empty square
        """
        
        self.move = '99'
        while bool(re.match('[0-7][0-7]$', self.move)) == False:
            self.move = raw_input("Where would you like to move? "
                                  "Choose a two digit number 00-77: ")
            if (bool(re.match(r'[0-7][0-7]$', self.move)) == True) and (len(
                                                    self.move) == 2):
                self.flip_pebbles()
            
            # Append move to board and change turns
            if (bool(re.match(r'[0-7][0-7]$', self.move)) and (self.board[
                                int(self.move[0])][int(self.move[1])
                                ] == 0)) and (bool(self.flip) == True):
                self.board[int(self.move[0])][int(self.move[1])] = self.turn
                self.print_board()
            elif (bool(re.match(r'[0-7][0-7]$', self.move)) == True) and (
                                            bool(self.flip_pebbles())):
                print "Invalid: Player {} has a piece there.".format(
                        self.board[int(self.move[0])][int(self.move[1])])
                self.move = '99'
            else:
                print "Invalid entry, try again"


game = Reversi()        #temporary for developing code
game.new_game()         #temporary for developing code
for x in range(10):     #temporary for developing code
    game.prompt_move()  #temporary for developing code
print 'Good move.'      #temporary for developing code