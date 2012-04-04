"""CIS192 Final Project; Othello_Reversi;
Paul Terwilliger, Jay Paik, Kristen Lau"""
import string
import re

class Chess(object):
    """The chess class with the rules and chessboard
    >>> chess = Chess()"""

    def __init__(self):
        """Creates board and other variables"""
        self.board = []
        self.turn = 0
        self.self_pieces = [1, 2, 3, 4, 5, 6]
        self.opps_pieces = [-1, -2, -3, -4, -5, -6]

    def new_game(self):
        """Starts a new game of Chess.  Black pieces are negative numbers, and
        white pieces are positive numbers
        >>> chess.new_game()"""
        self.board = [[-4, -2, -3, -5, -6, -3, -2, -4,],
                      [-1, -1, -1, -1, -1, -1, -1, -1,],
                      [ 0,  0,  0,  0,  0,  0,  0,  0,],
                      [ 0,  0,  0,  0,  0,  0,  0,  0,],
                      [ 0,  0,  0,  0,  0,  0,  0,  0,],
                      [ 0,  0,  0,  0,  0,  0,  0,  0,],
                      [ 1,  1,  1,  1,  1,  1,  1,  1,],
                      [ 4,  2,  3,  5,  6,  3,  2,  4,]]
        self.turn = 1
        
    def change_turns(self):
        """Function for changing turns"""
        self.turn = ((self.turn % 2) + 1)
        self.self_pieces = [(-num) for num in self.self_pieces]
        self.opps_pieces = [(-num) for num in self.opps_pieces]
        
    def coors_to_nums(self, string):
        """Turns chess coordinates ([a-h][1-8]) into numerical coordinates
        ([0-7][0-7]) for the chess program to process
        
        >>> chess.coors_to_nums('a1')
        '70'
        >>> chess.coors_to_nums('d5')
        '33'
        >>> chess.coors_to_nums('f4')
        '45'
        """
        # Change the type of error!!!
        coors_dict = {'a': '0', 'b': '1', 'c': '2', 'd': '3', 'e': '4', 'f':
                      '5', 'g': '6', 'h': '7'}
        output_string = []
        if bool(re.match('[a-h][1-8]$', string)) == False:
            raise TypeError("ERROR: Improper coordinates ({})".format(string))
        else:
            output_string.append(str(8 - int(string[1])))
            output_string.append(coors_dict[string[0]])
            return ''.join(output_string)
        
    def nums_to_coors(self, string):
        """Turns numerical coordinates ([0-7][0-7]) into chess coordinates 
        ([a-h][1-8])
        """
        # Change the type of error!!!
        coors_dict = {'0': 'a', '1': 'b', '2': 'c', '3': 'd', '4': 'e', '5':
                      'f', '6': 'g', '7': 'h'}
        output_string = []
        if bool(re.match('[0-7][0-7]$', string)) == False:
            raise TypeError("ERROR: Improper coordinates ({})".format(string))
        else:
            output_string.append(coors_dict[string[1]])
            output_string.append(str(8 - int(string[0])))
            return ''.join(output_string)
        
    def print_board(self):
        """Prints the board: temporary function for developing code"""
        print "    0     1     2     3     4     5     6     7 "
        col_num = 0
        fake_board = [[0, 0, 0, 0, 0, 0, 0, 0,],
                      [0, 0, 0, 0, 0, 0, 0, 0,],
                      [0, 0, 0, 0, 0, 0, 0, 0,],
                      [0, 0, 0, 0, 0, 0, 0, 0,],
                      [0, 0, 0, 0, 0, 0, 0, 0,],
                      [0, 0, 0, 0, 0, 0, 0, 0,],
                      [0, 0, 0, 0, 0, 0, 0, 0,],
                      [0, 0, 0, 0, 0, 0, 0, 0,]]
        piece_count = 0
        for row in self.board:
            for piece in row:
                piece2 = str(piece)
                if len(str(piece)) < 2:
                    piece2 = " " + str(piece)
                fake_board[col_num][piece_count] = piece2
                piece_count += 1
            col_num += 1
            piece_count = 0
        col_num = 0
        for row in fake_board:
            print "{} {}".format(col_num, row)
            col_num += 1
        print "--------------------------"
        
    def move_rook(self, co_yx):
        """Input is chess coordinates of a rook [a-h][1-8], output is chess
        coordinates of all legal squares the rook can move"""
        co_yx = self.coors_to_nums(co_yx)
        
        # Creating the list of up coordinates
        coors_y = [str(coor) for coor in range(int(co_yx[0]) - 1, -1, -1)]
        coors_x = [co_yx[1] for coor in range(8)]
        coors_yx_up = zip(coors_y, coors_x)
        for coors in coors_yx_up:
            if self.board[int(coors[0])][int(coors[1])] in self.opps_pieces:
                coors_yx_up = coors_yx_up[:coors_yx_up.index(coors) + 1]
                break
            elif self.board[int(coors[0])][int(coors[1])] in self.self_pieces:
                coors_yx_up = coors_yx_up[:coors_yx_up.index(coors)]
                break
        
        # Creating the list of down coordinates
        coors_y = [str(coor) for coor in range(int(co_yx[0]) + 1, 8)]
        coors_x = [co_yx[1] for coor in range(8)]
        coors_yx_dow = zip(coors_y, coors_x)
        for coors in coors_yx_dow:
            if self.board[int(coors[0])][int(coors[1])] in self.opps_pieces:
                coors_yx_dow = coors_yx_dow[:coors_yx_dow.index(coors) + 1]
                break
            elif self.board[int(coors[0])][int(coors[1])] in self.self_pieces:
                coors_yx_dow = coors_yx_dow[:coors_yx_dow.index(coors)]
                break
        
        # Creating the list of right coordinates
        coors_y = [co_yx[0] for coor in range(8)]
        coors_x = [str(coor) for coor in range(int(co_yx[0]), 8)]
        coors_yx_rig = zip(coors_y, coors_x)
        for coors in coors_yx_rig:
            if self.board[int(coors[0])][int(coors[1])] in self.opps_pieces:
                coors_yx_rig = coors_yx_rig[:coors_yx_rig.index(coors) + 1]
                break
            elif self.board[int(coors[0])][int(coors[1])] in self.self_pieces:
                coors_yx_rig = coors_yx_rig[:coors_yx_rig.index(coors)]
                break
        
        # Creating the list of left coordinates
        coors_y = [co_yx[0] for coor in range(8)]
        coors_x = [str(coor) for coor in range(int(co_yx[0]) - 2, -1, -1)]
        coors_yx_lef = zip(coors_y, coors_x)
        for coors in coors_yx_lef:
            if self.board[int(coors[0])][int(coors[1])] in self.opps_pieces:
                coors_yx_lef = coors_yx_lef[:coors_yx_lef.index(coors) + 1]
                break
            elif self.board[int(coors[0])][int(coors[1])] in self.self_pieces:
                coors_yx_lef = coors_yx_lef[:coors_yx_lef.index(coors)]
                break
        
        # Turning numerical coordinates into chess coordinates for output
        coors_yx_ = coors_yx_up + coors_yx_dow + coors_yx_rig + coors_yx_lef
        coors_yx = [self.nums_to_coors(''.join(co)) for co in coors_yx_]
        return coors_yx
    
    def move_knight(self, co_yx):
        """Input is chess coordinates of a knight [a-h][1-8], output is chess
        coordinates of all legal squares the knight can move"""
        co_yx = self.coors_to_nums(co_yx)
        coors_xy = []
        
        coors_y = [str(int(co_yx[0]) + 2), str(int(co_yx[0]) + 2), #+2y, +-1x
                   str(int(co_yx[0]) + 1), str(int(co_yx[0]) + 1), #+1y, +-2x
                   str(int(co_yx[0]) - 1), str(int(co_yx[0]) - 1), #-1y, +-2x
                   str(int(co_yx[0]) - 2), str(int(co_yx[0]) - 2)] #-2y, +-1x
        coors_x = [str(int(co_yx[1]) + 1), str(int(co_yx[1]) - 1), #+2y, +-1x
                   str(int(co_yx[1]) + 2), str(int(co_yx[1]) - 2), #+1y, +-2x
                   str(int(co_yx[1]) + 2), str(int(co_yx[1]) - 2), #-1y, +-2x
                   str(int(co_yx[1]) + 1), str(int(co_yx[1]) - 1)] #-2y, +-1x
        coors_xy = zip(coors_y, coors_x)
        coors_temp = ["".join(coor) for coor in coors_xy]
        coors_xy = []
        for coor in coors_temp:
            if (bool(re.match('[0-7][0-7]$', coor)) == True) and (
                                                    len(coor) == 2):
                coors_xy.append(coor)
        print coors_xy
        
    def prompt_move(self):
        """Receives chess coordinates from the user"""
        chosen = '99'
        test_counter = 0
        while (bool(re.match("[0-7][0-7]$", chosen)) == False) or (
                                                test_counter != 1):
            test_counter = 1
            chosen = raw_input("Which piece would you like to move?"
                                  " Choose coordinates [a-h][1-8]: ")
            chosen = self.coors_to_nums(chosen)
            if (self.board[int(chosen[0])][int(chosen[1])
                    ] in self.opps_pieces) or (self.board[int(chosen[0])
                    ][int(chosen[1])] not in self.self_pieces):
                print "That's not one of your pieces"
                test_counter = 0
        return chosen
    
    def make_move(self):
        """The body of making a move: will prompt for a piece then a square to
        move the piece to"""  
        chosen = prompt_move()
        pass
        
         # Figures out what kind of piece is there
        
chess = Chess()
chess.new_game()
chess.print_board()
#chess.prompt_move()
print chess.move_rook('a1')
print chess.move_knight('a8')

if __name__ == "__main__":
    import doctest
    doctest.testmod()