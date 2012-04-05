"""CIS192 Final Project; Othello_Reversi;
Paul Terwilliger, Jay Paik, Kirsten Lau"""
import re
import copy

"""(Paul) The game is complete and finished!  You guys should look over my 
code for bugs.  Also, try playing a few games.  I haven't been able to find
any bugs in the system.  I will probably start working on the engine now in
a new different file that I will upload to github.
Get cracking on the GUI and networking!!

--Note: type resign to exit the game.  
"""

class Reversi(object):
    """This is the Reversi class with the rules of the game"""
    
    def __init__(self):
        """Create board and other variables"""
        self.board = []
        self.move = '99'
        self.turn = 2
        self.flip = []
        self.skip = 0
        self.board_f = []
        self.end = 0
        self.remember_first = 1
        self.resign = 0
        
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
        self.move = '99'
        self.flip = []
        self.skip = 0
        self.end = 0
        self.resign = 0
        
    def check_end_game(self):
        """Checks to see if the game should end. To be run once every turn"""
        num = -1
        ber = 0
        available = []
        coo_aval = []
        for row in self.board:
            num += 1
            for square in row:
                if square == 0:
                    available.append((num, ber))
                ber += 1
            ber = 0
        if bool(available) == False:
            pass # pass
        else:
            coo_aval = ["".join([(str(num)), (str(ber))]) for (num, ber) in
                                                                  available]
        coo_left = []
        for coo in coo_aval:
            remain = self.flip_pebbles(coo)
            if bool(remain) == True:
                coo_left.append(coo)
        print coo_left, "<-- Legal moves"
        return coo_left
                

    def end_game(self):
        """Ends a reversi game. Should output who wins and ask for a rematch
        (with sides switched). If a rematch is decided upon, new_game should
        be run."""
        if self.resign != 1:
            score_white = 0
            score_black = 0
            for row in self.board:
                for square in row:
                    if square == 1:
                        score_white += 1
                    elif square == 2:
                        score_black += 1
            print "FINAL SCORE: white: {} points, and black: {} points".format(
                                                    score_white, score_black)
            if score_white == score_black:
                print "The game is a tie!"
            elif score_white > score_black:
                print "Player 1 White wins!"
            elif score_white < score_black:
                print "Player 2 Black wins!"
            play_again = raw_input("Would you like to play again? yes/no: ")
            if play_again == "yes":
                self.run_reversi()
                self.turn = ((self.remember_first % 2) + 1)
                self.remember_first = ((self.remember_first % 2) + 1)
            else:
                print "Game Over!"
        if self.resign == 1:
            print "Game Over! Player {} wins by resignation".format(
                                                (self.turn % 2) + 1)
        
    def print_board(self):
        """Prints the board: temporary function for developing code"""
        print "{})0  1  2  3  4  5  6  7 ".format(self.move)
        col_num = 0
        for row in self.board:
            print "{} {}".format(col_num, row)
            col_num += 1
        print "--------------------------"

    def flip_pebbles(self, coor_move):
        """Checks if any opponent pebbles are around the input pebble and
        flips the corresponding pebbles.  Returns a list of flipped
        pebbles.  If the move is illegal, the turn won't happen."""
        
        def legal(flip_list):
            """Input is a list of two-integer tuples which are coordinates,
            output is a list with the to-be-flipped pebbles remaining."""
            legl = 0
            counter = 0
            for (num, ber) in flip_list:
                if self.board[num][ber] == ((self.turn % 2) + 1):
                    counter += 1
                elif self.board[num][ber] == 0:
                    counter = 0
                    break
                elif self.board[num][ber] == self.turn:
                    legl = 1
                    break
            if legl == 0:
                counter = 0
            flip = flip_list[:counter]
            return flip

        # Defined variables:
        self.board_f = copy.deepcopy(self.board)
        coo_y = int(coor_move[0])
        coo_x = int(coor_move[1])
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
        if bool(re.match('[2-7][0-7]$', coor_move)) and (
                                self.board_f[coo_y - 1][coo_x] == turn_f):
            coors_y = [coor for coor in range(coo_y - 1, -1, -1)]
            coors_x = [coo_x for num in range(8)]
            north = zip(coors_y, coors_x)
            
        # Enemy north-east
        if bool(re.match('[2-7][0-5]$', coor_move)) and (
                            self.board_f[coo_y - 1][coo_x + 1] == turn_f):
            coors_y = [coor for coor in range(coo_y - 1, -1, -1)]
            coors_x = [coor for coor in range(coo_x + 1, 8)]
            neast = zip(coors_y, coors_x)
        
        # Enemy east
        if bool(re.match('[0-7][0-5]$', coor_move)) and (
                                self.board_f[coo_y][coo_x + 1] == turn_f):
            coors_y = [coo_y for num in range(8)]
            coors_x = [coor for coor in range(coo_x + 1, 8)]
            east = zip(coors_y, coors_x)
        
        # Enemy south-east        
        if bool(re.match('[0-5][0-5]$', coor_move)) and (
                            self.board_f[coo_y + 1][coo_x + 1] == turn_f):
            coors_y = [coor for coor in range(coo_y + 1, 8)]
            coors_x = [coor for coor in range(coo_x + 1, 8)]
            seast = zip(coors_y, coors_x)
            
        # Enemy south
        if bool(re.match('[0-5][0-7]$', coor_move)) and (
                                self.board_f[coo_y + 1][coo_x] == turn_f):
            coors_y = [coor for coor in range(coo_y + 1, 8)]
            coors_x = [coo_x for num in range(8)]
            south = zip(coors_y, coors_x)
        
        # Enemy south-west
        if bool(re.match('[0-5][2-7]$', coor_move)) and (
                            self.board_f[coo_y + 1][coo_x - 1] == turn_f):
            coors_y = [coor for coor in range(coo_y + 1, 8)]
            coors_x = [coor for coor in range(coo_x - 1, -1, -1)]
            swest = zip(coors_y, coors_x)
        
        #Enemy west
        if bool(re.match('[0-7][2-7]$', coor_move)) and (
                                self.board_f[coo_y][coo_x - 1] == turn_f):
            coors_y = [coo_y for num in range(8)]
            coors_x = [coor for coor in range(coo_x - 1, -1, -1)]
            west = zip(coors_y, coors_x)
        
        # Enemy north-west
        if bool(re.match('[2-7][2-7]$', coor_move)) and (
                            self.board_f[coo_y - 1][coo_x - 1] == turn_f):
            coors_y = [coor for coor in range(coo_y - 1, -1, -1)]
            coors_x = [coor for coor in range(coo_x - 1, -1, -1)]
            nwest = zip(coors_y, coors_x)
        
        self.flip = (legal(north) + legal(neast) + legal(east)
                   + legal(seast) + legal(south) + legal(swest)
                    + legal(west) + legal(nwest))
        
        # Flips over the pebbles chosen by flip
        lgal = 0
        for (num, ber) in self.flip:
            lgal += 1
            self.board_f[num][ber] = self.turn
        if 0 < lgal:
            self.board_f[int(coor_move[0])][int(coor_move[1])] = self.turn
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
        # The prompt for a move
        self.move = '99'
        self.print_board()
        while (bool(re.match(r'[0-7][0-7]$', self.move))) == False:
            self.move = raw_input("P{}, Where would you like to move? "
                     "Choose a two digit number 00-77: ".format(self.turn))
            match = (bool(re.match(r'[0-7][0-7]$', self.move)))
            if (len(self.move) == 2) and match and (self.board[int(
                                self.move[0])][int(self.move[1])] != 0):
                print "Invalid: Player {} has a piece there.".format(
                            self.board[int(self.move[0])][int(self.move[1])])
                self.move = '99'
            elif (len(self.move) == 2) and match and (self.board[int(
                                self.move[0])][int(self.move[1])] == 0):
                self.flip_pebbles(self.move)
                self.board = self.board_f[:]
                if bool(self.flip) == True: 
                    self.turn = ((self.turn % 2) + 1) # Changes turns
                else:
                    print "INVALID: no flipped tiles. Try again"
                    self.move = '99'
            elif self.move == "resign":
                self.resign = 1
                break
            else:
                print "Invalid entry, try again"
    
    def run_reversi(self):
        """This will run prompt_move() and new_game() and end_game() and 
        potentially every function. This function should be the one that 
        combines all of them until the game ends. This function
        should bring together all the rules into one, so the user can call
        just this one and this one only.  
        """
        self.new_game()
        while self.end == 0:
            # Makes the player pass if there are no available moves.
            end = self.check_end_game()
            if (bool(end) == False) and (self.resign != 1):
                #make the player pass
                print "No legal moves, Player {} passes!".format(self.turn)
                self.turn = ((self.turn % 2) + 1)
                self.skip += 1
                if self.skip == 4:
                    self.end = 1
            elif (self.resign != 1):
                self.prompt_move()
                self.skip = 0
            elif self.resign == 1:
                break
        self.end_game()


game = Reversi()        #temporary for developing code
game.run_reversi()      #temporary for developing code